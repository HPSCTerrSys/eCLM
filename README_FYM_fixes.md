# eCLM_FYM — correctness fixes before production runs

Branch: `eCLM_FYM_fixes` (branched from `eCLM_FYM`)
All changes are marked in the source with `tboas-fix`.

Verified: RELEASE and DEBUG builds complete and link (GCC 13, OpenMPI, netCDF 4.9.2,
PnetCDF 1.12.3).

---

## 1. CropType restart state (`src/clm5/biogeochem/CropType.F90`)

The 12 patch variables added for winter-cereal cold hardening and perennial crop
age were never written to the restart file. They initialise to `spval` (~1e36)
and `huge(1)`, so any restart during hardening or during a perennial's growing
season fed garbage into

    rateh = Hparam*(10-tcrown)*(lt50-lt50max)          (CNPhenologyMod:~3324)
    fsurv = 2**(-(|tcrown|/|lt50|)**4)
    idpp  = dayspyr*(kyr-yrop) + jday - idop           (CNPhenologyMod:~1802, ~3675)

`yrop` is an integer, so `kyr - huge(1)` overflowed.

`yrop`, `lt50`, `wdd`, `rateh`, `rated`, `rates`, `rater`, `fsurv`, `accfsurv`,
`countfsurv`, `ck` and `tcrown` are now restarted. Reading a pre-fix restart file
is handled: `yrop` falls back to the current year and the hardening state falls
back to the values `CropPhenology` assigns at planting (`lt50=-5`, `fsurv=1`,
`accfsurv=1`, `countfsurv=1`, rates `=0`). Both fallbacks log on `masterproc`.

**This is the fix that matters most for spinup**, because a long spinup is by
definition a restart chain.

## 2. Manure nitrogen was counted twice

`manunitro(ivt(p))` was applied in full as immediately-available mineral N
*and* used again, multiplied by `manure_CN_ratio`, to size a pulse of organic
carbon that carried no nitrogen at all.

Now, when `use_cfert = .true.`:

* `manure_nh4_frac` (new, default **0.25**) of the manure N goes to the mineral
  pool on the existing fertiliser schedule — the ammoniacal fraction.
* the remaining `(1 - manure_nh4_frac)` enters the litter pools as organic N
  together with the manure C, at exactly `manure_CN_ratio`, and is mineralised
  by the decomposition cascade. This is the DNDC/DayCent convention.
* the manure C is sized from the **organic** N only, so no nitrogen is used twice.
* the `manure_freq_years` / `manure_apply_month` gate now applies to the mineral
  part as well. Previously the gate only governed the carbon, so manure N was
  applied every year even in years when no manure carbon was.

With `use_cfert = .false.` the behaviour is unchanged: `manunitro` is treated
purely as mineral fertiliser N, exactly as in stock CLM5.

Typical `manure_nh4_frac`: ~0.25 solid farmyard manure, ~0.5–0.6 cattle/pig slurry.

New patch flux `fertN_patch` (history field `Norg_FERT`, gN/m²/s, inactive by
default) mirrors the existing `fertC_patch` / `Corg_FERT`, and is restarted.

## 3. Mass-conservation checks restored

`CNBalanceCheckMod` had its abort thresholds hardcoded to `100` gC and gN
m⁻² per timestep — roughly a season of NPP, i.e. the check was off. They are
back at the CLM5 default `1e-7`, now via `cn_balance_tol_c` / `cn_balance_tol_n`
so a tolerance can be widened *deliberately and visibly* while debugging. Any
value above `1e-6` prints a "do not use for production" warning at startup.

The underlying imbalance is also fixed. `covercrop_switch_ivt` set
`xsmrpool_patch(p) = 0`, and `xsmrpool` is inside `totc_patch` — so that
statement destroyed carbon (or created it, when the pool held a respiration
debt) with no matching flux. It now moves into `xsmrpool_loss_patch`, which is
also inside `totc_patch`, and `CNCStateUpdate1Mod` releases it through
`xsmrpool_to_atm` — a flux the C balance already counts as an output. A branch
was added there so the pool still drains when `dribble_crophrv_xsmrpool_2atm`
is off, which is the default.

The manure C and N balance terms are now aggregated over active patches only,
matching how `CNCSoilFert` actually applies them.

## 4. Out-of-bounds write on the PFT table (`pftconMod.F90`)

`set_is_pft_known_to_model` marked literal indices `27, 28, 55, 56, 59, 60, 65,
66, 78, 79`. `mxpft = 78` and the array is allocated `(0:mxpft)`, so **index 79
was out of bounds** — trapped in DEBUG, silent heap corruption in RELEASE. And
per `expected_pftnames`, `covercrop_1`/`covercrop_2` are at 77/78, not 78/79, so
the cover-crop pair was off by one and `covercrop_1` was never marked.

The list is now resolved by name (`nwbarley`, `nirrig_wbarley`, `npotatoes`,
`nirrig_potatoes`, `nrapeseed`, `nirrig_rapeseed`, `nsugarbeet`,
`nirrig_sugarbeet`, `ncovercrop_1`, `ncovercrop_2`) using the same idiom already
used for `apple` and `covercrop_1`, so it survives a change of parameter file.
Each resolved index is range-checked against `[npcropmin, mxpft]` and echoed to
the log with the PFT name found there.

> Please confirm this name list is what was intended. It was reverse-engineered
> from the literal indices against `expected_pftnames`.

## 5. Uninitialised landunit index (`CNVegCarbonStateType.F90`)

In the AD-spinup reseed block, `lun%itype(l)` was read one statement *before*
`l = patch%landunit(i)` was assigned, so it used the previous loop iteration's
value. `l = patch%landunit(i)` now comes first. Confirmed with gfortran: the
pre-fix file emits `'l' may be used uninitialized` at that line; the fixed file
does not.

`deadstemc_soy` / `deadstemc_storage_soy` / `deadstemn_soy` are also now included
in the x10 / ÷10 AAD-spinup rescaling applied to `deadstemc` / `deadstemn`, since
they are compared against those pools.

## 6. Per-patch debug writes

15 `write(iulog,*)` statements in `dynHarvestMod`, `dynCovercropFileMod`,
`CNPhenologyMod` and `CNBalanceCheckMod` fired once per patch, from every MPI
rank, with no `masterproc` guard — on rotation dates that is O(10⁵) lines per
rank at 1 km, and the `coldtolerance` and `cbalance warning` traces fired every
timestep.

They are now behind `debug_covercrop`, a `logical, parameter` in `clm_varctl`
(default `.false.`), so the compiler removes them entirely. Set it to `.true.`
and rebuild for single-point debugging.

---

## New namelist variables (`&cfert_inparm`)

| Variable | Type | Default | Meaning |
|---|---|---|---|
| `manure_nh4_frac` | real | 0.25 | Ammoniacal fraction of applied manure N. The rest becomes organic N in litter. Range-checked to [0,1]. |
| `cn_balance_tol_c` | real | 1e-7 | C mass-conservation abort threshold, gC/m²/timestep. |
| `cn_balance_tol_n` | real | 1e-7 | N mass-conservation abort threshold, gN/m²/timestep. |

The Python namelist generator does not need to know about these; the Fortran
defaults apply when they are absent from `lnd_in`.

## Also worth setting, unchanged by this branch

`use_grainproduct = .true.`. It defaults to `.false.`, and when false
`grainc_to_food` is routed into `litfall` (`CNVegCarbonFluxType:~4367`) — the
harvested grain never leaves the domain and is eventually respired back, which
biases cropland NEE/NBP.

## 7. Calendar-date manure application

`manure_apply_month > 0` never worked: the gate sat inside the leaf-emergence
onset block, which fires on a single timestep once per season, so a fixed
calendar date essentially never coincided with it and the manure was silently
never applied. Only `manure_apply_month = 0` was functional.

The date-driven case is now handled at the top of the crop patch loop, where it
is reached every timestep, and the onset path is restricted to
`manure_apply_month == 0` so the two cannot both fire. Only the organic C and N
are date-driven; the ammoniacal fraction stays on the standard fertiliser
schedule, metered from onset over `ndays_on`, since that is plant-available N.
The `manure_freq_years` gate now applies to the ammoniacal N on both paths.

Because the new block sits before the perennial branch, fruit-tree patches also
receive manure for the first time -- `FruitTreePhenology` writes no `fertC` /
`fertN` of its own, so with `manure_apply_month = 0` perennials still get none.

## Not addressed here

* The single-timestep manure C pulse (`fertC = manureC / dtrad`) is kept, as
  requested. It is numerically violent; if the balance check trips at a manure
  application date, spreading it over `ndays_on` is the first thing to try.
* In `CNNStateUpdate1Mod`, the perennial-woody branch skips
  `livestemn_to_litter` while `CNPhenologyMod` may still route that flux into
  the litter pools. If the N balance trips on fruit-tree patches, look there.
