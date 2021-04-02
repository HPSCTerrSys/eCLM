from pathlib import Path

def build_seq_maps_rc(seq_maps_file: str = "seq_maps.rc"):
    # Seems like this could be transformed into a
    # loop, but I don't see a clear pattern how.
    seq_maps = {
        "atm2ice_fmapname" : "idmap",
        "atm2ice_fmaptype" : "X",
        "atm2ice_smapname" : "idmap",
        "atm2ice_smaptype" : "X",
        "atm2ice_vmapname" : "idmap",
        "atm2ice_vmaptype" : "X",
        "atm2lnd_fmapname" : "idmap",
        "atm2lnd_fmaptype" : "X",
        "atm2lnd_smapname" : "idmap",
        "atm2lnd_smaptype" : "X",
        "atm2ocn_fmapname" : "idmap",
        "atm2ocn_fmaptype" : "X",
        "atm2ocn_smapname" : "idmap",
        "atm2ocn_smaptype" : "X",
        "atm2ocn_vmapname" : "idmap",
        "atm2ocn_vmaptype" : "X",
        "atm2wav_smapname" : "idmap",
        "atm2wav_smaptype" : "Y",
        "glc2ice_rmapname" : "idmap_ignore",
        "glc2ice_rmaptype" : "Y",
        "glc2lnd_fmapname" : "idmap",
        "glc2lnd_fmaptype" : "Y",
        "glc2lnd_smapname" : "idmap",
        "glc2lnd_smaptype" : "Y",
        "glc2ocn_ice_rmapname" : "idmap_ignore",
        "glc2ocn_ice_rmaptype" : "Y",
        "glc2ocn_liq_rmapname" : "idmap_ignore",
        "glc2ocn_liq_rmaptype" : "Y",
        "ice2atm_fmapname" : "idmap",
        "ice2atm_fmaptype" : "Y",
        "ice2atm_smapname" : "idmap",
        "ice2atm_smaptype" : "Y",
        "ice2wav_smapname" : "idmap",
        "ice2wav_smaptype" : "Y",
        "lnd2atm_fmapname" : "idmap",
        "lnd2atm_fmaptype" : "Y",
        "lnd2atm_smapname" : "idmap",
        "lnd2atm_smaptype" : "Y",
        "lnd2glc_fmapname" : "idmap",
        "lnd2glc_fmaptype" : "X",
        "lnd2glc_smapname" : "idmap",
        "lnd2glc_smaptype" : "X",
        "lnd2rof_fmapname" : "idmap",
        "lnd2rof_fmaptype" : "X",
        "ocn2atm_fmapname" : "idmap",
        "ocn2atm_fmaptype" : "Y",
        "ocn2atm_smapname" : "idmap",
        "ocn2atm_smaptype" : "Y",
        "ocn2wav_smapname" : "idmap",
        "ocn2wav_smaptype" : "Y",
        "rof2lnd_fmapname" : "idmap",
        "rof2lnd_fmaptype" : "Y",
        "rof2ocn_fmapname" : "idmap_ignore",
        "rof2ocn_fmaptype" : "Y",
        "rof2ocn_ice_rmapname" : "idmap",
        "rof2ocn_ice_rmaptype" : "Y",
        "rof2ocn_liq_rmapname" : "idmap",
        "rof2ocn_liq_rmaptype" : "Y",
        "wav2ocn_smapname" : "idmap",
        "wav2ocn_smaptype" : "X"
    }

    if seq_maps_file and Path(seq_maps_file).name.strip() != "":   
        with open(seq_maps_file, "w") as f:
            for k, v in seq_maps.items():
                f.write(f'{k} : "{v}"\n')
        return True, Path(seq_maps_file)
    else:
        return True, ""