# materials.py
fibers = {
    "E-Glass": {
        "E1f": 73, "E2f": 73, "G12f": 30, "G23f": 30, "v12f": 0.23, "F1ft": 3450,
        "alpha1": 5.0, "alpha2": 5.0
    },
    "S-Glass": {
        "E1f": 86, "E2f": 86, "G12f": 35, "G23f": 35, "v12f": 0.23, "F1ft": 4500,
        "alpha1": 5.6, "alpha2": 5.6
    },
    "AS-4 Carbon": {
        "E1f": 235, "E2f": 15, "G12f": 27, "G23f": 7, "v12f": 0.20, "F1ft": 3700,
        "alpha1": -0.5, "alpha2": 15
    },
    "T-300 Carbon": {
        "E1f": 230, "E2f": 15, "G12f": 27, "G23f": 7, "v12f": 0.20, "F1ft": 3100,
        "alpha1": -0.7, "alpha2": 12
    },
    "IM7 Carbon": {
        "E1f": 290, "E2f": 21, "G12f": 14, "G23f": None, "v12f": 0.20, "F1ft": 5170,
        "alpha1": -0.2, "alpha2": 10
    },
    "Boron": {
        "E1f": 395, "E2f": 395, "G12f": 165, "G23f": None, "v12f": 0.13, "F1ft": 3450,
        "alpha1": 16, "alpha2": 16
    },
    "Kevlar 49 Aramid": {
        "E1f": 131, "E2f": 7, "G12f": 21, "G23f": None, "v12f": 0.33, "F1ft": 3800,
        "alpha1": -2, "alpha2": 60
    },
    "Silicon Carbide (Nicalon)": {
        "E1f": 172, "E2f": 172, "G12f": 73, "G23f": None, "v12f": 0.20, "F1ft": 2070,
        "alpha1": 3.2, "alpha2": 3.2
    }
}

matrices = {
    "Epoxy_3501_6": {
        "density": 1.27, "Em": 4.3, "Gm": 1.60, "vm": 0.35,
        "FmT": 69, "FmC": 200, "FmS": 100, "alpha_m": 45,
        "Tg": 200, "Tmax": 150, "epsilon_mT": 2.5
    },
    "Epoxy_977_3": {
        "density": 1.28, "Em": 3.7, "Gm": 1.37, "vm": 0.35,
        "FmT": 90, "FmC": 175, "FmS": 52, "alpha_m": None,
        "Tg": 200, "Tmax": 177, "epsilon_mT": None
    },
    "Epoxy_HY6010_HT917_DY7070": {
        "density": 1.17, "Em": 3.4, "Gm": 1.26, "vm": 0.36,
        "FmT": 80, "FmC": 104, "FmS": 40, "alpha_m": 62,
        "Tg": 152, "Tmax": None, "epsilon_mT": None
    },
    "Polyester": {
        "density": 1.2, "Em": 3.35, "Gm": 1.35, "vm": 0.35,
        "FmT": 70, "FmC": 220, "FmS": 45, "alpha_m": 90,
        "Tg": 131, "Tmax": None, "epsilon_mT": 3.5
    },
    "Vinylester": {
        "density": 1.15, "Em": 3.5, "Gm": 1.30, "vm": 0.35,
        "FmT": 77.5, "FmC": 127, "FmS": 53, "alpha_m": 156,
        "Tg": 100, "Tmax": None, "epsilon_mT": 3.0
    },
    "Polyimide": {
        "density": 1.65, "Em": 4.5, "Gm": 4.20, "vm": 0.35,
        "FmT": 95, "FmC": 135, "FmS": 86.5, "alpha_m": 45,
        "Tg": 300, "Tmax": 325, "epsilon_mT": 2.5
    },
    "PEEK": {
        "density": 1.32, "Em": 3.7, "Gm": 4.65, "vm": 0.35,
        "FmT": 108, "FmC": 143, "FmS": 58, "alpha_m": 90,
        "Tg": 143, "Tmax": 250, "epsilon_mT": 2.5
    },
    "BSL914C": {
        "density": 0.00, "Em": 4.0, "Gm": 1.481, "vm": 0.35,
        "FmT": 75, "FmC": 150, "FmS": 70, "alpha_m": None,
        "Tg": None, "Tmax": None, "epsilon_mT": None
    },   
}
