# cad/presets.py

aircraft_presets = {
    "P-51 Mustang": {
        "specs": {
            "mass": 11.286,
            "load_factor": 10,
            "wingspan": 11.286,
            "3_view": "data/North_American_P-51B_Mustang_3-view_line_drawing.png",
            "crop_params": [100, 200, 200, 200],
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
        "box": {
            "project": "composite_wing",
            "stl": "cad/stl/BOX.stl",
            "step": "cad/step/BOX.stl",
        },
        "wings": {
            "project": "composite_wing",
            "box": "cad/stl/todo.stl",
            "wing": "cad/stl/todp.stl",
            "aircraft": ""
        },
        "step": {
            "box": "femap/p51_box.step"
        }       
    },
}


onshape_projects = { # files? projects?
    "composite_wing": {
        "did": "f6ac5c0b25ce21ecd85991db",
        "wv": "w",
        "wvid": "2f1903d2edb515536def7421",
        "eid": {
            "BOX": "0f38721b826a5669e2acf9d0",
            "FULL_WING": "5f4c32c21a91aecefb2f3c0e",
            "WING-p51-2spline": "535ea5121f0dc13c398cec23"
            },
        "default_url": "https://cad.onshape.com/documents/f6ac5c0b25ce21ecd85991db/w/2f1903d2edb515536def7421/e/0f38721b826a5669e2acf9d0"
    },
    "Torsion box": {
        "did": "f6ac5c0b25ce21ecd85991db",
        "wv": "w",
        "wvid": "2f1903d2edb515536def7421",
        "eid": {
            "BOX": "1746a09d07c6f27e71172a7f"
        },
        "url": "https://cad.onshape.com/documents/cae4cba9e2f625664baf1122/w/ba81e6382142c773cd7b78ba/e/640a7618098c9be6fe97b244?renderMode=0&uiState=6654e4567ce53e2d5ac81735"
    },
    "Full wing (old)": {
        "did": "f6ac5c0b25ce21ecd85991db",
        "wv": "w",
        "wvid": "2f1903d2edb515536def7421",
        "eid": {
            "BOX": "b879915fba35863ee60116c6"
        },
        "url": ""
    },
    "Parametric Wing": {
        "did": "308d36ae2431fbf4b9b96a48",
        "wv": "w",
        "wvid": "4dfbfac17da94e7168ec10cd",
        "eid": {
            "BOX": "1c23a328748cc03fde2f37f5"
        },
        "url": "https://cad.onshape.com/documents/308d36ae2431fbf4b9b96a48/w/4dfbfac17da94e7168ec10cd/e/1c23a328748cc03fde2f37f5"
    },
}
