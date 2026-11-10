# eCLM_FYM vs. master: functional review of `src/clm5`

** AI GENERATED **

- Branch: `eCLM_FYM_fixes_merged_with_master` at `e79767641a`
- Compared with: `master` at `e113460a91`
- Date: 2026-09-29

The line numbers below refer to the branch at `e79767641a`.

Whitespace, blank-line and file-mode artefacts were already cleaned up
before this review. See the commits "remove whitespace" and "src: mode
changes of several files".

## Summary

**With all FYM switches off (`use_cfert`, `use_covercropping`,
`use_fruittree`), the branch does not behave like master.** 

The new features themselves are mostly switched properly, but several
crop changes apply to every crop run, and a few look like bugs.

## A. Changes to default crop runs that have no switch

All of these are in `src/clm5/biogeochem/CNPhenologyMod.F90` unless noted.

1. **Winter cereals use a different model.** For winter wheat, and for
   winter barley and rapeseed when active:
   - `vernalization_2` (Lu et al. 2017) replaces master's
     `vernalization` (:2751). The old routine is now dead code.
   - a new `coldtolerance` routine runs in phase 2 and moves leaf C
     and N to litter as frost damage (:2791)
   - seeding adds `frootc_xfer = 0.1` (:2431, :2485)
   - on 1 January, a living winter crop now gets `cropplant = .true.`
     where master sets `.false.` (:2350)
   - new rule: after day 170, a winter wheat patch that isn't growing
     is reset to "not planted" (:2357)
2. **Maize and sugarcane maturity changed.** At normal planting,
   `gddmaturity = hybgdd` replaces master's climate-adjusted `max(950,
   min(gdd820*0.85, hybgdd))` formula (:2540). This affects every
   maize patch.
3. **Probable bug: soybean matures immediately.** The soybean
   `gddmaturity` rule at normal planting is commented out (:2533). The
   value then stays at the 0 it was reset to while unplanted, so `hui
   >= gddmaturity` is true right away. Temperate soybean exists in
   default CLM5 runs. A single-point run with soybean would confirm
   it.
4. **Tropical soybean lost its special handling.** It is still an
   active PFT, but no longer gets the soybean maturity rule or the
   stem-allocation exception in both `NutrientCompetition*Mod`
   (e.g. `NutrientCompetitionFlexibleCNMod.F90:1838`).
5. **Six more crop types become active PFTs.** `pftconMod.F90:1413`
   marks barley, winter barley, winter rye, potatoes, rapeseed and
   sugar beet (plus irrigated versions) as "known to model". In master
   these areas are merged into the standard CLM5 crops. With real
   surface data, the patch structure changes, and in turn items 1 and
   2 apply to these crops. Sugar beet and potato also get `gddmaturity
   = hybgdd` (:2547, :2603).
6. **The N balance check is 10,000x stricter.** In master the run
   aborts when `|col_errnb| > 1e-3`. In the branch the threshold is
   `cn_balance_tol_n`, default `1e-7`
   (`CNBalanceCheckMod.F90:379`). The comment in `clm_varctl.F90` says
   the defaults are "the stock CLM5 values", but that's only true for
   C. Runs that pass on master could abort here.

## B. Changes that are properly switched off by default

- **Manure (`use_cfert`)** is clean. With it off, `fert` is computed
  exactly as in master, and `CNCSoilFert` returns early.
- **Cover crops (`use_covercropping`)**: `dynCovercropFileMod`,
  `covercropping_update` and the rotation dates are all behind the
  switch. With it off, `ncovercrop_1/2 = 0`, which never matches a
  crop patch.
- **Fruit trees (`use_fruittree`)**: with it off, `perennial = 0` for
  every PFT. That disables all the `perennial(ivt)==1` branches in
  about 10 modules (allocation, state updates, pruning, orchard
  rotation, respiration, FUN, gap mortality) and `FruitTreePhenology`
  itself.
- **Tree allometry**: `taper` and `nstem` fall back to master's
  hard-coded values (200 or 10 for shrubs, and 0.1) when they're
  missing from the parameter file.

## C. Bugs to verify

- **`CNVegCarbonStateType.F90:1473`** (Restart, reseeding block): the
  loop runs over `i` but tests `patch%itype(p)`, where `p` is a
  leftover value from an earlier loop. Also, non-woody PFTs no longer
  get `deadstemc = 0`. This only matters with `reseed_dead_plants =
  .true.`.
- **`CNRotationToColumn`** (`CNPhenologyMod.F90`): its final loop adds
  `pwood_harvestc` for *all* active patches. `CNLitterToColumn` has
  already added it for pruned fruit trees, so pruning wood harvest
  appears to be counted twice when fruit trees are on. It adds 0 in
  default runs.

## D. Cosmetic changes with no effect on results

- **Deleted comments.**
  - `CNNDynamicsMod.F90`: apart from the new `CNCSoilFert`, the whole
    diff consists of master's comments being deleted. It could be
    rebuilt as master plus that one routine, which removes about 250
    lines from the diff.
  - `clm_varctl.F90`: the argument comments of `clm_varctl_set` were
    deleted as well.
- **`controlMod.F90`**:
  - `covercrop_paramfile` and `transient_landuse_file` are each
    declared twice in `clm_inparm` (:228-231).
  - The comment "this broadcast was lost" (:620) describes a bug that
    existed only on the FYM branch. Master already broadcasts
    `use_grainproduct`, so the comment can go.
- **`TemperatureType.F90`**: a `T24` accumulator is defined but never
  used.
- **`PatchType.F90`**: comments were renamed from citrus to apple and
  from tropical soybean to cover crop. These are only true when the
  switches are on.
- **Commented-out code**: examples are the old `vernalization` and
  `coldtolerance` calls in `CNPhenologyMod.F90` (2735-2765), the
  `fun_cn_flex_c` writes in `CNFUNMod.F90` (1233-1253),
  `CNVegCarbonStateType.F90` (958-965) and `CNVegStateType.F90`
  (531-544).

## Recommendation

If this is heading toward master, the rule should be that **all
switches off means identical to master**:

- **Put behind a switch:** A1, A2, A5 and the sugar beet/potato
  part. They could be tied to the FYM crop-calendar setup or get their
  own switch.
- **Restore master's behaviour:** A3 and A4, and change the
  `cn_balance_tol_n` default to `1e-3` (A6).
- **Start with A3 and A6:** they're small, clear-cut fixes, and A3
  probably also affects FYM results that have soybean patches.
