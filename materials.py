# materials.py

fibers = {
    "AS-4": {
        "type": "Carbon",
        "E1f": 225,             # [GPa]
        "E2f": 15,              # [GPa]
        "G12f": 15,             # [GPa]
        "G23f": 7,              # [GPa]
        "ni12f": 0.2,           # [/]
        "ni21f": 0.2,           # [/]
        "F1ft": 3350,           # [MPa]
        "F1fc": 2500,           # [MPa]
        "epsilon1ft": 1.488,    # [%]
        "epsilon1fc": 1.111,    # [%]
        "alpha1f": -0.5e-6,     # [1/°C]
        "alpha2f": 15e-6,       # [1/°C]
    },
    "T-300": {
        "type": "Carbon",
        "E1f": 230,             # [GPa]
        "E2f": 15,              # [GPa]
        "G12f": 15,             # [GPa]
        "G23f": 7,              # [GPa]
        "ni12f": 0.2,           # [/]
        "ni21f": 0.2,           # [/]
        "F1ft": 2500,           # [MPa]
        "F1fc": 2000,           # [MPa]
        "epsilon1ft": 1.086,    # [%]
        "epsilon1fc": 0.869,    # [%]
        "alpha1f": -0.7e-6,     # [1/°C]
        "alpha2f": 12e-6,       # [1/°C]
    },
    "21xK43 Gevetex": {
        "type": "E-Glass",
        "E1f": 80,              # [GPa]
        "E2f": 80,              # [GPa]
        "G12f": 33.33,          # [GPa]
        "G23f": 33.33,           # [GPa]
        "ni12f": 0.2,           # [/]
        "ni21f": 0.2,           # [/]
        "F1ft": 2150,           # [MPa]
        "F1fc": 1450,           # [MPa]
        "epsilon1ft": 2.687,    # [%]
        "epsilon1fc": 1.813,    # [%]
        "alpha1f": 4.9e-6,      # [1/°C]
        "alpha2f": 4.9e-6,      # [1/°C]
    },
    "Silenka 1200tex": {
        "type": "E-Glass",
        "E1f": 74,              # [GPa]
        "E2f": 74,              # [GPa]
        "G12f": 30.8,           # [GPa]
        "G23f": 30.8,           # [GPa]
        "ni12f": 0.2,           # [/]
        "ni21f": 0.2,           # [/]
        "F1ft": 2150,           # [MPa]
        "F1fc": 1450,           # [MPa]
        "epsilon1ft": 2.905,    # [%]
        "epsilon1fc": 1.959,    # [%]
        "alpha1f": 4.9e-6,      # [1/°C]
        "alpha2f": 4.9e-6,      # [1/°C]
    },
    "E-Glass": {                # what the fuck
        "type": "E-Glass",
        "E1f": 73,              # [GPa]
        "E2f": 73,              # [GPa]
        "G12f": 30,             # [GPa]
        "G23f": 30,             # [GPa]
        "ni12f": 0.23,          # [/]
        "ni21f": 0.23,          # [/]
        "F1ft": 3450,           # [MPa]
        "alpha1f": 5.0e-6,      # [1/°C]
        "alpha2f": 5.0e-6,      # [1/°C]
    },
    "S-Glass": {                # what the fuck
        "type": "Glass",
        "E1f": 86,              # [GPa]
        "E2f": 86,              # [GPa]
        "G12f": 35,             # [GPa]
        "G23f": 35,             # [GPa]
        "ni12f": 0.23,          # [/]
        "ni21f": 0.23,          # [/]
        "F1ft": 4500,           # [MPa]
        "alpha1f": 5.6e-6,      # [1/°C]
        "alpha2f": 5.6e-6,      # [1/°C]
    },
    "IM7": {
        "type": "Carbon",
        "E1f": 290,             # [GPa]
        "E2f": 21,              # [GPa]
        "G12f": 14,             # [GPa]
        "G23f": None,           # [GPa]
        "ni12f": 0.20,          # [/]
        "ni21f": 0.20,          # [/]
        "F1ft": 5170,           # [MPa]
        "F1fc": None,           # [MPa]
        "epsilon1ft": None,     # [%]
        "epsilon1fc": None,     # [%]
        "alpha1f": -0.2e-6,     # [1/°C]
        "alpha2f": 10e-6,       # [1/°C]
    },
    "Boron": {
        "type": "Boron",
        "E1f": 395,             # [GPa]
        "E2f": 395,             # [GPa]
        "G12f": 165,            # [GPa]
        "G23f": None,           # [GPa]
        "ni12f": 0.13,          # [/]
        "ni21f": 0.13,          # [/]
        "F1ft": 3450,           # [MPa]
        "F1fc": None,           # [MPa]
        "epsilon1ft": None,     # [%]
        "epsilon1fc": None,     # [%]
        "alpha1f": 16e-6,       # [1/°C]
        "alpha2f": 16e-6,       # [1/°C]
    },
    "Kevlar 49": {
        "type": "Aramid",
        "E1f": 131,             # [GPa]
        "E2f": 7,               # [GPa]
        "G12f": 21,             # [GPa]
        "G23f": None,           # [GPa]
        "ni12f": 0.33,          # [/]
        "ni21f": 0.33,          # [/]
        "F1ft": 3800,           # [MPa]
        "F1fc": None,           # [MPa]
        "epsilon1ft": None,     # [%]
        "epsilon1fc": None,     # [%]
        "alpha1f": -2e-6,       # [1/°C]
        "alpha2f": 60e-6,       # [1/°C]
    },
    "Nicalon": {
        "type": "Silicon Carbide",
        "E1f": 172,             # [GPa]
        "E2f": 172,             # [GPa]
        "G12f": 73,             # [GPa]
        "G23f": None,           # [GPa]
        "ni12f": 0.20,          # [/]
        "ni21f": 0.20,          # [/]
        "F1ft": 2070,           # [MPa]
        "F1fc": None,           # [MPa]
        "epsilon1ft": None,     # [%]
        "epsilon1fc": None,     # [%]
        "alpha1f": 3.2e-6,      # [1/°C]
        "alpha2f": 3.2e-6,      # [1/°C]
    }
}


# materials.py

matrices = {
    "3501-6": {
        "type": "Epoxy",
        "rho": 1.27,            # [g/cm³]
        "Em": 4.2,              # [GPa]
        "Gm": 1.57,             # [GPa]
        "nim": 0.34,            # [/]
        "FmT": 69,              # [MPa]
        "FmC": 250,             # [MPa]
        "FmS": 50,              # [MPa]
        "alpha_m": 45e-6,       # [1/°C]
        "Tg": 200,              # [°C]
        "Tmax": 150,            # [°C]
        "epsilon_mT": 1.7,      # [%]
    },
    "BSL914C": {
        "type": "Epoxy",
        "rho": 0.00,            # [g/cm³] - should be corrected
        "Em": 4.0,              # [GPa]
        "Gm": 1.481,            # [GPa]
        "nim": 0.35,            # [/]
        "FmT": 75,              # [MPa]
        "FmC": 150,             # [MPa]
        "FmS": 70,              # [MPa]
        "alpha_m": 55e-6,       # [1/°C]
        "Tg": None,             # [°C]
        "Tmax": None,           # [°C]
        "epsilon_mT": 4,        # [%]
    },
    "LY556-HT907-DY063": {
        "type": "Epoxy",
        "rho": 1.17,            # [g/cm³]
        "Em": 3.4,              # [GPa]
        "Gm": 1.26,             # [GPa]
        "nim": 0.36,            # [/]
        "FmT": 80,              # [MPa]
        "FmC": 120,             # [MPa]
        "FmS": 52,              # [MPa]
        "alpha_m": 58e-6,       # [1/°C]
        "Tg": 152,              # [°C]
        "Tmax": None,           # [°C]
        "epsilon_mT": 5,        # [%]
    },
    "MY750-HY917-DY063": {
        "type": "Epoxy",
        "rho": 1.15,            # [g/cm³]
        "Em": 3.5,              # [GPa]
        "Gm": 1.30,             # [GPa]
        "nim": 0.35,            # [/]
        "FmT": 77.5,            # [MPa]
        "FmC": 127,             # [MPa]
        "FmS": 53,              # [MPa]
        "alpha_m": 58e-6,       # [1/°C]
        "Tg": 100,              # [°C]
        "Tmax": None,           # [°C]
        "epsilon_mT": 5,        # [%]
    },
    "977-3": {
        "type": "Epoxy",
        "rho": 1.28,            # [g/cm³]
        "Em": 3.7,              # [GPa]
        "Gm": 1.37,             # [GPa]
        "nim": 0.35,            # [/]
        "FmT": 90,              # [MPa]
        "FmC": 175,             # [MPa]
        "FmS": 52,              # [MPa]
        "alpha_m": None,        # [1/°C]
        "Tg": 200,              # [°C]
        "Tmax": 177,            # [°C]
        "epsilon_mT": None,     # [%]
    },
    "HY6010-HT917-DY7070": {
        "type": "Epoxy",
        "rho": 1.17,            # [g/cm³]
        "Em": 3.4,              # [GPa]
        "Gm": 1.26,             # [GPa]
        "nim": 0.36,            # [/]
        "FmT": 80,              # [MPa]
        "FmC": 104,             # [MPa]
        "FmS": 40,              # [MPa]
        "alpha_m": 62e-6,       # [1/°C]
        "Tg": 152,              # [°C]
        "Tmax": None,           # [°C]
        "epsilon_mT": None,     # [%]
    },
    "Polyester": {
        "type": "Polyester",
        "rho": 1.2,             # [g/cm³]
        "Em": 3.35,             # [GPa]
        "Gm": 1.35,             # [GPa]
        "nim": 0.35,            # [/]
        "FmT": 70,              # [MPa]
        "FmC": 220,             # [MPa]
        "FmS": 45,              # [MPa]
        "alpha_m": 90e-6,       # [1/°C]
        "Tg": 131,              # [°C]
        "Tmax": None,           # [°C]
        "epsilon_mT": 3.5,      # [%]
    },
    "Vinylester": {
        "type": "Vinylester",
        "rho": 1.15,            # [g/cm³]
        "Em": 3.5,              # [GPa]
        "Gm": 1.30,             # [GPa]
        "nim": 0.35,            # [/]
        "FmT": 77.5,            # [MPa]
        "FmC": 127,             # [MPa]
        "FmS": 53,              # [MPa]
        "alpha_m": 156e-6,      # [1/°C]
        "Tg": 100,              # [°C]
        "Tmax": None,           # [°C]
        "epsilon_mT": 3.0,      # [%]
    },
    "Polyimide": {
        "type": "Polyimide",
        "rho": 1.65,            # [g/cm³]
        "Em": 4.5,              # [GPa]
        "Gm": 4.20,             # [GPa]
        "nim": 0.35,            # [/]
        "FmT": 95,              # [MPa]
        "FmC": 135,             # [MPa]
        "FmS": 86.5,            # [MPa]
        "alpha_m": 45e-6,       # [1/°C]
        "Tg": 300,              # [°C]
        "Tmax": 325,            # [°C]
        "epsilon_mT": 2.5,      # [%]
    },
    "PEEK": {
        "type": "PEEK",
        "rho": 1.32,            # [g/cm³]
        "Em": 3.7,              # [GPa]
        "Gm": 4.65,             # [GPa]
        "nim": 0.35,            # [/]
        "FmT": 108,             # [MPa]
        "FmC": 143,             # [MPa]
        "FmS": 58,              # [MPa]
        "alpha_m": 90e-6,       # [1/°C]
        "Tg": 143,              # [°C]
        "Tmax": 250,            # [°C]
        "epsilon_mT": 2.5,      # [%]
    }
}
