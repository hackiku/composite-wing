# cad/presets.py

aircraft_presets = {
        "330-LT": {
        "specs": {
            "name": "Extra 330 LT",
            "manufacturer": "Extra Aircraft",
            "mass": 950.00,
            "load_factor": 10,
            "wingspan": 7.50,
            "3_view": "cad/imgs/placeholder.png",
            "crop_params": [0, 0, 200, 100],
        },
        "wing": {
            "span_wet": 3.75, # 7.50 / 2 [m]
            "fwd_spar": 0.30,
            "aft_spar": 0.20,
            "tip": 1.20,
            "root": 1.80,
            "sweep_angle": 5.0,
            "dihedral_angle": 1.5,
            "airfoil_root": "NACA-0018",
            "airfoil_tip": "NACA-0012",
        },
        "materials": {
            "fiber": 4,
            "matrix": 6,
            "Vf": 0.58,
            "Vvoid": 0.25
        },
        "model": {
            "project": "Extra 330 LT",
            "box": "d7774b5d778de27ba31db2e5",
            "wing": "a6c4f6c9d83beca3762a25ea",
            # "cutouts": "86ba0a1ee3dec8669f4c7d4e",
        }
    },
    "P-51": { 
        "specs": { 
            "name": "P-51 Mustang",
            "manufacturer": "North American Aviation",
            "mass": 5489.00,
            "load_factor": 10,
            "wingspan": 11.286,
            "3_view": "cad/imgs/P-51_3-view.png",
            "crop_params": [0, 1103, 1693, 1100],
        },        
        "wing": {
            "span_wet": 5.643, # 11.286 / 2 [m]
            "fwd_spar": 0.3,
            "aft_spar": 0.2,
            "tip": 1.297,
            "root": 2.752,
            "sweep_angle": 10.388,
            "dihedral_angle": 5,
            "airfoil_root": "NACA-2418",
            "airfoil_tip": "NACA-2212",
        },
        "materials": {
            "fiber": 3,
            "matrix": 7,
            "Vf": 0.60,
            "Vvoid": 0.30
        },
        "model": {
            "project": "composite_wing",
            "box": "0f38721b826a5669e2acf9d0",
            "wing": "b879915fba35863ee60116c6",
            "cutouts": "593c35c15b6c45dc507e4af4",
        }
    },
    "Glider": {
        "specs": {
            "name": "Cool Motor Glider",
            "manufacturer": "Glider Inc.",
            "mass": 8.500,
            "load_factor": 6,
            "wingspan": 15.000,
            "3_view": "cad/imgs/placeholder.png",
            "crop_params": [0, 0, 200, 100],
        },
        "wing": {
            "span_wet": 7.500, # 15.000 / 2 [m]
            "fwd_spar": 0.25,
            "aft_spar": 0.15,
            "tip": 0.800,
            "root": 1.800,
            "sweep_angle": 5.0,
            "dihedral_angle": 3,
            "airfoil_root": "NACA-0012",
            "airfoil_tip": "NACA-0010",
        },
        "materials": {
            "fiber": 5,
            "matrix": 2,
            "Vf": 0.55,
            "Vvoid": 0.25
        },
        "model": {
            "project": "glider_project",
            "box": "1a2b3c4d5e6f7g8h9i0j",
            "wing": "1k2l3m4n5o6p7q8r9s0t",
            "cutouts": "9z8y7x6w5v4u3t2s1r0p",
        }
    },
}

onshape_projects = {
    "composite_wing": {
        "did": "f6ac5c0b25ce21ecd85991db",
        "wv": "w",
        "wvid": "2f1903d2edb515536def7421",
    },
    "Extra 330 LT": {
        "did": "3b6bce5824912adfda10b52d",
        "wv": "w",
        "wvid": "91730fd668a615d074229f54",
    },
    "Torsion box": {
        "did": "f6ac5c0b25ce21ecd85991db",
        "wv": "w",
        "wvid": "2f1903d2edb515536def7421",
    },
    "Full wing (old)": {
        "did": "f6ac5c0b25ce21ecd85991db",
        "wv": "w",
        "wvid": "2f1903d2edb515536def7421",
    },
    "Parametric Wing": {
        "did": "308d36ae2431fbf4b9b96a48",
        "wv": "w",
        "wvid": "4dfbfac17da94e7168ec10cd",
    },
}
