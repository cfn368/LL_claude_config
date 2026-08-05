---
name: notebook-setup
description: Generic setup.py scaffold and notebook preamble pattern — autoreload, AEJ matplotlib style, standard imports. Use when creating a new research notebook or setup.py.
---

## Notebook entry (top cell, always)

```python
from py_files.setup import *
setup_notebook()
```

## Generic setup.py scaffold

Copy for new projects; add project-specific imports below the marked section.

```python
# py_files/setup.py
from __future__ import annotations

# stdlib
import math
from dataclasses import dataclass
from functools import reduce
from io import StringIO

# third-party
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.interpolate import interp1d

# optional soft imports
try:
    from IPython.display import display
except Exception:
    display = None

try:
    import requests
except Exception:
    requests = None

# ── project-specific imports go here ─────────────────────────────────────────


# ── notebook environment ──────────────────────────────────────────────────────

def enable_autoreload(mode: int = 2) -> None:
    try:
        from IPython import get_ipython
    except Exception:
        return
    ip = get_ipython()
    if ip is None:
        return
    ip.run_line_magic("load_ext", "autoreload")
    ip.run_line_magic("autoreload", str(int(mode)))


TEXT_COLOR = "#3F6469"   # same hue as facecolor, much lower lightness


def set_aej(**kwargs) -> None:
    """Colour-washed, spineless matplotlib style. See skills/econ-plotting/ for full spec."""
    import matplotlib as mpl
    mpl.rcParams.update({
        "font.family":          "serif",
        "font.style":           "italic",
        "font.size":            15,
        "figure.dpi":           150,
        "figure.facecolor":     "#EAF1F2",
        "axes.facecolor":       "#EAF1F2",
        "axes.linewidth":       1.0,
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        "axes.spines.left":     False,
        "axes.spines.bottom":   False,
        "text.color":           TEXT_COLOR,
        "axes.labelcolor":      TEXT_COLOR,
        "xtick.color":          TEXT_COLOR,
        "ytick.color":          TEXT_COLOR,
        "lines.linewidth":      1.2,
        "xtick.direction":      "out",
        "ytick.direction":      "out",
        "legend.frameon":       False,
        "legend.fancybox":      False,
        "legend.borderaxespad": 0.4,
        "legend.handlelength":  2.0,
        "legend.handletextpad": 0.6,
        "legend.labelspacing":  0.35,
        "savefig.bbox":         "tight",
        "savefig.dpi":          300,
        **kwargs,
    })


def setup_notebook(*, autoreload: int = 2, aej: bool = True, **aej_kwargs) -> None:
    enable_autoreload(autoreload)
    if aej:
        set_aej(**aej_kwargs)


__all__ = [
    "enable_autoreload", "set_aej", "setup_notebook", "TEXT_COLOR",
    "np", "pd", "plt", "mpl", "mticker", "math",
    "StringIO", "dataclass", "reduce", "display", "requests",
    "Line2D", "Patch", "interp1d",
]
```

## Conventions

- One setup cell per notebook, at top.
- Autoreload mode 2: reloads all modules on execution.
- Project imports in `setup.py`, not scattered across notebook cells.
- Plotting standards live in `skills/econ-plotting/` — `set_aej()` is the bridge.
