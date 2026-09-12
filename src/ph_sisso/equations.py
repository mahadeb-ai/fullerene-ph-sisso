"""Rounded manuscript equations for prediction only; this module performs no fitting."""

from __future__ import annotations
import numpy as np
import pandas as pd


def regime_from_atoms(atoms: pd.Series | np.ndarray) -> np.ndarray:
    values = np.asarray(atoms, dtype=float)
    return np.where(values <= 36, "small", np.where(values <= 76, "intermediate", "large"))


def distortion_main(frame: pd.DataFrame, regime: str | None = None) -> np.ndarray:
    """Evaluate the three main-text distortion-energy branches."""
    if regime is None:
        output = np.empty(len(frame), dtype=float)
        labels = regime_from_atoms(frame["Atoms"])
        for name in ("small", "intermediate", "large"):
            mask = labels == name
            output[mask] = distortion_main(frame.loc[mask], name)
        return output
    q = frame["Charge"].to_numpy(float)
    if regime == "small":
        return (0.09 * frame["life_b0_N"] / frame["life_b2_M_q2"] + 3.98 * np.exp(q) + 23.087).to_numpy(float)
    if regime == "intermediate":
        return (-1526.29 * frame["life_b2_M_q2"] / frame["life_b0_N"] + 4.06 * np.exp(q) + 48.62).to_numpy(float)
    if regime == "large":
        return (0.44 * frame["life_b1_N"] + 2.56 * frame["life_b2_ell_max"] / frame["life_b2_M_q2"] + 3.78 * np.exp(q) + 0.44 * q - 1.26).to_numpy(float)
    raise ValueError(f"Unknown regime: {regime}")


def distortion_supplementary(frame: pd.DataFrame, regime: str | None = None) -> np.ndarray:
    """Evaluate the three higher-complexity Supplementary distortion branches."""
    if regime is None:
        output = np.empty(len(frame), dtype=float)
        labels = regime_from_atoms(frame["Atoms"])
        for name in ("small", "intermediate", "large"):
            mask = labels == name
            output[mask] = distortion_supplementary(frame.loc[mask], name)
        return output
    q = frame["Charge"].to_numpy(float)
    if regime == "small":
        return (0.075 * frame["life_b0_N"] / frame["life_b2_M_q2"] - 4.65 * frame["life_b2_M_q2"] + 4.65 * q + 2.36 * q**2 + 30.19).to_numpy(float)
    if regime == "intermediate":
        ell = frame["life_b2_ell_max"]
        return (1.58 * frame["life_b1_N"] - 1.58 * ell - 2.21 * ell**2 + 4.09 * np.exp(q) + 11.05).to_numpy(float)
    if regime == "large":
        return (0.42 * frame["life_b2_N"] - 22963.23 * frame["life_b0_H_r3"] / frame["life_b0_H_r-2"] + 0.42 * q + 3.79 * np.exp(q) + 22982.48).to_numpy(float)
    raise ValueError(f"Unknown regime: {regime}")


def fermi_main(frame: pd.DataFrame, charge: int) -> np.ndarray:
    """Evaluate the main-text Fermi equation for Q=+1 or Q=-1."""
    if charge == 1:
        return 0.90 * frame["death_b2_H_r2"].to_numpy(float) - 11.26
    if charge == -1:
        return -1.06 * frame["death_b2_H_r-2"].to_numpy(float) + 2.08
    raise ValueError("The main Fermi equation is unsupported for Q=0")


def fermi_supplementary(frame: pd.DataFrame, charge: int) -> np.ndarray:
    """Evaluate Supplementary Fermi equations, including the canonical product form."""
    if charge == 1:
        descriptor = (frame["life_b2_N"] / frame["life_b0_N"] * frame["death_b2_H_r2"] * frame["death_b1_M_q-2"]**2 * frame["death_b2_M_q-2"]**2)
        return (2699.60 * descriptor - 10.21).to_numpy(float)
    if charge == -1:
        rho_prime = frame["life_b0_N"] / frame["life_b1_N"]
        mu_prime_squared = 1.0 / (frame["death_b1_M_q2"] * frame["death_b1_M_q-2"])
        return (16.48 * rho_prime * -1.0 * mu_prime_squared + 29.87).to_numpy(float)
    raise ValueError("The Supplementary Fermi equation is unsupported for Q=0")

