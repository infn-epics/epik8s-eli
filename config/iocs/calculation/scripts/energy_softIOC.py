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
import os
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
parser.add_argument("-p", "--pvout", required=False, default="pvlist.txt", help="Output PV list file")
args = parser.parse_args()

with open(args.conf, "r") as f:
    config = json.load(f)

prefix = config.get("prefix_energy", "ELI:ENERGY")
dipole_current_pv = config.get("dipole_current_pv", "")  # external RB PV on the PS IOC
default_angle = float(config.get("bending_angle_deg", 24.0))
loop_period = float(config.get("loop_period_s", 1.0))

# ---------------------------------------------------------------------------
# PV creation
# ---------------------------------------------------------------------------
builder.SetDeviceName(prefix)

k1_pv = builder.aIn(
    "K1",
    initial_value=K1,
    EGU="Tm/A",
    PREC=6,
    DESC="Dipole calibration constant",
)
i_dip_pv = builder.aIn(
    "I_DIP",
    initial_value=0.0,
    EGU="A",
    PREC=2,
    DESC="Dipole current (mirrored from PS IOC)",
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

builder.LoadDatabase()
softioc.iocInit()


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main():
    k1_pv.set(K1)

    while True:
        try:
            i_dip = float(caget(dipole_current_pv, timeout=0.5))
        except Exception as e:
            print(f"## caget {dipole_current_pv} failed: {e}")
            cothread.Sleep(loop_period)
            continue

        p, e_kin = compute_energy(i_dip, default_angle)

        i_dip_pv.set(i_dip)
        p_pv.set(p)
        e_kin_pv.set(e_kin)

        cothread.Sleep(loop_period)


cothread.Spawn(main)

softioc.dbl()

with open(args.pvout, "w") as f:
    old_stdout = os.dup(1)
    os.dup2(f.fileno(), 1)
    softioc.dbl()
    os.dup2(old_stdout, 1)
    os.close(old_stdout)

softioc.interactive_ioc(globals())
