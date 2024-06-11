# cad/aircraft_presets.py


aircraft_presets = {
    "P-51 Mustang": {
        "specs": {
            "mass": 5489.00,
            "load_factor": 10,
            "3_view": "data/North_American_P-51B_Mustang_3-view_line_drawing.png",
            "crop_params": [100, 200, 200, 200],
        },        
        "onshape" : {
            "wingspan": 5.641, # 11.286 / 2 [m]
            "tip": 1.297,
            "root": 2.752,
            "sweep_angle": 10.388,
        },
        "stl": {
            "box": "cad/stl/TODO.stl",
            "wing": "cad/stl/TODO.stl",
            "aircraft": ""
        },
        "step": {
            "box": "femap/p51_box.step"
        }       
    },
    "J-22 Orao": {
        "specs": {
            "hnjo": 12.00,
        },
        "hnjo": 12.00,
        "mass": 11300.00,
        "wingspan": 9.262,
        "tip": 1.297,
        "root": 2.752,
        "sweep_angle": 12.0,
        "3_view": "",
        "crop_params": [400, 200, 200, 200],
        "load_factor": 10
    }
},
