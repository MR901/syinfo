"""Visualization helpers for monitoring JSONL outputs.

Provides both matplotlib and plotly backends (plotly optional). If neither is
available, raises a clear error.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List


def _read_jsonl(path: str | Path) -> List[Dict]:
    p = Path(path)
    data: List[Dict] = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return data


def plot_with_matplotlib(path: str | Path) -> None:
    import matplotlib.pyplot as plt

    data = _read_jsonl(path)
    if not data:
        raise RuntimeError("No data to plot")

    x = [d.get("timestamp") for d in data]
    cpu = [d.get("cpu_percent", 0.0) for d in data]
    mem = [d.get("memory_percent", 0.0) for d in data]
    disk = [d.get("disk_percent", 0.0) for d in data]

    plt.figure(figsize=(10, 6))
    plt.plot(x, cpu, label="CPU %")
    plt.plot(x, mem, label="Memory %")
    plt.plot(x, disk, label="Disk %")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Percent")
    plt.title("System Monitor Metrics")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_with_plotly(path: str | Path):
    try:
        import plotly.graph_objects as go
    except Exception as e:
        raise RuntimeError("plotly is not installed. Install with `pip install plotly`." ) from e

    data = _read_jsonl(path)
    if not data:
        raise RuntimeError("No data to plot")

    x = [d.get("timestamp") for d in data]
    cpu = [d.get("cpu_percent", 0.0) for d in data]
    mem = [d.get("memory_percent", 0.0) for d in data]
    disk = [d.get("disk_percent", 0.0) for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=cpu, name="CPU %"))
    fig.add_trace(go.Scatter(x=x, y=mem, name="Memory %"))
    fig.add_trace(go.Scatter(x=x, y=disk, name="Disk %"))
    fig.update_layout(title="System Monitor Metrics", xaxis_title="Time", yaxis_title="Percent")
    return fig


__all__ = ["plot_with_matplotlib", "plot_with_plotly"]


