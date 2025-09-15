"""Visualization helpers for monitoring JSONL outputs.

Provides matplotlib backend. If matplotlib is unavailable, save/show will be skipped.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union


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


def _normalize_data(data_or_path: Union[str, Path, List[Dict]]) -> List[Dict]:
    if isinstance(data_or_path, (str, Path)):
        return _read_jsonl(data_or_path)
    if isinstance(data_or_path, list):
        return data_or_path
    return []


essential_keys = ("timestamp", "cpu_percent", "memory_percent", "disk_percent")


def plot_data_with_matplotlib(
    data_or_path: Union[str, Path, List[Dict]],
    save_to: Optional[str] = None,
    show: bool = False,
) -> Optional[str]:
    """Plot CPU/Memory/Disk using matplotlib from data or a JSONL path.

    If save_to is provided, saves a PNG and returns its path; optionally shows the plot.
    Returns None if plotting is not available.
    """
    try:
        import matplotlib
        if not show:
            matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter
    except Exception:
        return None

    data = _normalize_data(data_or_path)
    if not data:
        return None

    # Filter to entries containing required keys
    cleaned = [d for d in data if all(k in d for k in essential_keys)]
    if not cleaned:
        return None

    x = [d.get("timestamp") for d in cleaned]
    cpu = [d.get("cpu_percent", 0.0) for d in cleaned]
    mem = [d.get("memory_percent", 0.0) for d in cleaned]
    disk = [d.get("disk_percent", 0.0) for d in cleaned]

    # Prepare optional network data (bytes counters)
    has_net = any(isinstance(d.get("network_io"), dict) for d in cleaned)
    if has_net:
        sent = [int((d.get("network_io") or {}).get("bytes_sent", 0) or 0) for d in cleaned]
        recv = [int((d.get("network_io") or {}).get("bytes_recv", 0) or 0) for d in cleaned]
    else:
        sent, recv = [], []

    # Layout: two rows if network data present; otherwise single plot
    if has_net:
        fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 8), height_ratios=[2, 1])
        ax_top, ax_bottom = axs
    else:
        fig, ax_top = plt.subplots(1, 1, figsize=(10, 6))
        ax_bottom = None

    # Top plot: CPU/Memory/Disk
    ax_top.plot(x, cpu, label="CPU %")
    ax_top.plot(x, mem, label="Memory %")
    ax_top.plot(x, disk, label="Disk %")
    ax_top.set_ylabel("Percent")
    ax_top.set_title("System Monitor Metrics")
    ax_top.legend(loc="upper left")
    for label in ax_top.get_xticklabels():
        label.set_rotation(45)
        label.set_ha("right")

    # Bottom plot: Network IO (bytes counters) with human-readable formatter
    if has_net and ax_bottom is not None:
        ax_bottom.plot(x, sent, label="Bytes Sent", color="#1f77b4")
        ax_bottom.plot(x, recv, label="Bytes Received", color="#ff7f0e")
        ax_bottom.set_ylabel("Network IO (bytes)")
        ax_bottom.legend(loc="upper left")

        # Use HumanReadable to format ticks nicely
        try:
            from syinfo.core.utils import HumanReadable  # local import to avoid heavy deps

            def _fmt_bytes(y, pos):
                try:
                    return HumanReadable.bytes_to_size(int(y))
                except Exception:
                    return str(y)

            ax_bottom.yaxis.set_major_formatter(FuncFormatter(_fmt_bytes))
        except Exception:
            pass

    fig.tight_layout()

    saved_path: Optional[str] = None
    try:
        if save_to:
            save_path = Path(save_to)
            if save_path.exists() and save_path.is_dir():
                from datetime import datetime as _dt

                fname = f"monitor-{_dt.now().strftime('%Y%m%d-%H%M%S')}.png"
                save_path = save_path / fname
            else:
                parent = save_path.parent if save_path.suffix else save_path
                try:
                    parent.mkdir(parents=True, exist_ok=True)
                except Exception:
                    pass
                if not save_path.suffix:
                    save_path = parent / "monitor-plot.png"
            fig.savefig(str(save_path), dpi=120)
            saved_path = str(save_path)
        if show:
            plt.show()
    finally:
        try:
            import matplotlib.pyplot as _plt
            _plt.close(fig)
        except Exception:
            pass

    return saved_path


def plot_with_matplotlib(path: str | Path) -> None:
    # Backward-compatible wrapper that shows the plot
    _ = plot_data_with_matplotlib(path, save_to=None, show=True)


__all__ = [
    "plot_with_matplotlib",
    "plot_data_with_matplotlib",
]


