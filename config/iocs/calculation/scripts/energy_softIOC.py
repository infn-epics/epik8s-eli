"""
Soft IOC: beam energy calculation for the ELI dipole.

Physics (from energy.m):
  k1      = mean(Int_Bz / I)           [Tm/A]  — dipole calibration
  p       = 300 * k1 * I_dip / angle_rad       [MeV/c]
  E_kin   = sqrt(p^2 + m_e^2) - m_e           [MeV]
"""

from softioc import softioc, builder
import numpy as np
import json
import argparse
import cothread
from cothread.catools import caget

# ---------------------------------------------------------------------------
# Dipole calibration data (Int_Bz [Tm] vs I [A])
# ---------------------------------------------------------------------------
INT_BZ = np.array([
    0.0200, 0.0382, 0.0568, 0.0755, 0.0943,
    0.1130, 0.1316, 0.1499, 0.1678, 0.1852,
    0.1921, 0.1989, 0.2057, 0.2122, 0.2185,
    0.2246, 0.2304, 0.2255, 0.2203, 0.2148,
    0.2091, 0.2029, 0.1962, 0.1893, 0.1714,
    0.1531, 0.1346, 0.1159, 0.0971, 0.0783,
    0.0594, 0.0405, 0.0215,
])

I_CAL = np.array([
    12, 24, 36, 48, 60, 72, 84, 96, 108, 120,
    125, 130, 135, 140, 145, 150, 155, 150, 145, 140,
    135, 130, 125, 120, 108, 96, 84, 72, 60, 48,
    36, 24, 12,
])

ELECTRON_MASS_MEV = 0.511  # MeV/c^2
K1 = float(np.mean(INT_BZ / I_CAL))  # calibration constant [Tm/A]


def compute_energy(i_dip: float, bending_angle_deg: float):
    """Return (momentum [MeV/c], kinetic_energy [MeV])."""
    angle_rad = bending_angle_deg * np.pi / 180.0
    p = 300.0 * K1 * i_dip / angle_rad  # MeV/c
    e_kin = np.sqrt(p**2 + ELECTRON_MASS_MEV**2) - ELECTRON_MASS_MEV
    return float(p), float(e_kin)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--conf", required=True, default="energy.json")
args = parser.parse_args()

with open(args.conf, "r") as f:
    config = json.load(f)

prefix = config.get("prefix_energy", "ELI:ENERGY")
dipole_current_pv = config.get("dipole_current_pv", "")  # external PV or ""
default_i_dip = float(config.get("default_i_dip", 65.0))
default_angle = float(config.get("bending_angle_deg", 24.0))
loop_period = float(config.get("loop_period_s", 1.0))

# ---------------------------------------------------------------------------
# PV creation
# ---------------------------------------------------------------------------
builder.SetDeviceName(prefix)

# Inputs / setpoints
i_dip_sp = builder.aOut(
    "LEL:MAG:DPSU01:DIP01:CURRENT_SP",
    initial_value=default_i_dip,
    EGU="A",
    PREC=2,
    DESC="Dipole current setpoint",
)

# Read-only outputs
k1_pv = builder.aIn(
    "K1",
    initial_value=K1,
    EGU="Tm/A",
    PREC=6,
    DESC="Dipole calibration constant",
)
p_pv = builder.aIn(
    "P",
    initial_value=0.0,
    EGU="MeV/c",
    PREC=4,
    DESC="Beam momentum",
)
e_kin_pv = builder.aIn(
    "E_KIN",
    initial_value=0.0,
    EGU="MeV",
    PREC=4,
    DESC="Beam kinetic energy",
)
i_dip_rb = builder.aIn(
    "LEL:MAG:DPSU01:DIP01:CURRENT_RB",
    initial_value=default_i_dip,
    EGU="A",
    PREC=2,
    DESC="Dipole current used in calculation",
)

builder.LoadDatabase()
softioc.iocInit()


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main():
    k1_pv.set(K1)

    while True:
        # Resolve dipole current
        if dipole_current_pv:
            try:
                i_dip = float(caget(dipole_current_pv, timeout=0.5))
            except Exception:
                i_dip = i_dip_sp.get()
        else:
            i_dip = i_dip_sp.get()

        p, e_kin = compute_energy(i_dip, default_angle)

        # i_dip_rb.set(i_dip)
        p_pv.set(p)
        e_kin_pv.set(e_kin)

        cothread.Sleep(loop_period)


cothread.Spawn(main)
softioc.interactive_ioc(globals())
