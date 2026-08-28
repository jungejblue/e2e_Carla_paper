"""Plot monitor signals and takeover candidates from one run CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


REQUIRED_COLUMNS = {"time_s", "risk_score", "trigger"}


def _as_boolean(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    return series.astype(str).str.lower().isin({"1", "true", "yes"})


def plot_timeline(input_csv: Path, output_path: Path) -> None:
    frame = pd.read_csv(input_csv)
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    optional_signals = [
        column
        for column in ("action_age_ms", "lateral_error_m", "predicted_ttlc_s")
        if column in frame.columns
    ]
    figure, axes = plt.subplots(
        1 + len(optional_signals),
        1,
        figsize=(10, 2.6 * (1 + len(optional_signals))),
        sharex=True,
        constrained_layout=True,
    )
    if not isinstance(axes, (list, tuple)) and not hasattr(axes, "__len__"):
        axes = [axes]

    main_axis = axes[0]
    main_axis.plot(frame["time_s"], frame["risk_score"], label="risk score")
    triggered = _as_boolean(frame["trigger"])
    main_axis.scatter(
        frame.loc[triggered, "time_s"],
        frame.loc[triggered, "risk_score"],
        color="tab:red",
        s=18,
        label="trigger",
        zorder=3,
    )
    main_axis.set_ylabel("risk score")
    main_axis.grid(alpha=0.3)
    main_axis.legend()

    for axis, signal in zip(axes[1:], optional_signals, strict=True):
        axis.plot(frame["time_s"], frame[signal])
        axis.set_ylabel(signal)
        axis.grid(alpha=0.3)

    axes[-1].set_xlabel("simulation time [s]")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_path", type=Path)
    args = parser.parse_args()
    plot_timeline(args.input_csv, args.output_path)


if __name__ == "__main__":
    main()

