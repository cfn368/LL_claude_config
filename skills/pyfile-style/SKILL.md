---
name: pyfile-style
description: Style conventions for Python research files (py_files/) — module docstring, section separators, imports, constants, function docstrings, dict alignment. Apply when cleaning up or reviewing any .py file in a research project.
---

## When to apply

At the end of a project, run this skill over all `py_files/*.py` (and any other module files) to make them consistent. Files written incrementally during a project diverge in section structure, docstring quality, and formatting — this skill standardises them without touching logic.

---

## Module docstring

Every file opens with a triple-quoted docstring. Format:

```python
"""
Short title — what this module computes
========================================

One short paragraph: what the module does, how it fits in the project.
If it is used by a notebook, say so.

Data sources:
    TABLE_CODE  — description of what is fetched
    TABLE_CODE  — description of what is fetched
"""
```

Rules:
- Title is lowercase after the first word, em-dash separator, then a clause
- `=` underline is exactly as long as the title line
- `Data sources:` block only if the file fetches external data; omit otherwise
- Source lines: four-space indent, table code left-padded to align `—` across rows

---

## Imports

```python
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import py_files.var_groups as var_groups
from py_files.investment_shares import compute_direct_for_year, CACHE_DIR
from py_files.LS_aggregator import sectoral_labor_shares

from dstapi import DstApi
```

Order: stdlib → third-party standard stack (`pandas`, `numpy`, `matplotlib`) → project (`py_files.*`) → domain-specific (`dstapi`, `ET-eds-api`, etc.). Blank line between each group. No comments on import lines.

---

## Section separators

Every logical section (group of related functions, or a data-fetch block, or a calibration block) gets a separator:

```python
# ==================== ==================== ==================== ====================
# 1. section name
```

Two lines: the `==` banner on line 1, the `# N. name` label on line 2. Four groups of exactly 20 `=` signs, separated by single spaces. Section numbers start at 0 for helpers/utilities and 1 for the first substantive section, incrementing within the file.

One blank line before the separator (unless it is the first section), no blank line between the two separator lines, one blank line after the `# N. name` line before the first function.

---

## Function docstrings

Short, factual, return-focused. Two to four lines max. No parameter tables.

```python
def fetch_compensation():
    """
    D.1 compensation of employees from NABP36, current prices.
    Returns long DataFrame: year, branche_code, compensation
    """
```

Do not write: parameter type lists, `Args:` / `Returns:` headers, multi-paragraph explanations. If the function is self-evident from its name and signature, omit the docstring entirely.

---

## Module-level constants

ALL_CAPS names. Group related constants together without blank lines between them. Inline comments only when the value is non-obvious.

```python
C_SUPPLY  = "#1a1a2e"   # dark navy  — supply curve
C_DEMAND  = "#c0392b"   # crimson    — demand curve

DTAU = 0.10   # illustrative 10 pp tax cut
```

Dict-literal calibration blocks: align values within logical pairs on the same line; wrap to the next line when the group changes:

```python
GENERAL = dict(
    alphaK=0.44, alphaL=0.56,
    betaK=0.38,  betaL=0.62,
    phi=0.75,
)
```

---

## Variable → label dicts

Keys left-aligned using spaces so values line up. Commented-out lines stay in with `# ` prefix rather than being deleted (they document considered variables):

```python
model_var = {
    'K':        r'$K$',
    'q':        r'$q$',
    'pI':       r'$p_I$',
    # 'L1C':    r'$L_{C}$',   # excluded from baseline run
    'wC':       r'$w_{C}$',
    'wI':       r'$w_{I}$',
}
```

---

## Multi-parameter function signatures

When a function has more than four parameters, put each on its own line with a trailing comma. Group related parameters together; a blank line between groups is allowed inside the signature for visual clarity:

```python
def temp_tc(T=25, tau_ss=0.0, size=0.01,
            decay=0.10, tail=50, tau_terminal=None
            ):
```

---

## Blank lines

- Two blank lines before and after each section separator block
- One blank line between functions within the same section
- No blank line between the `# ==...==` banner and the `# N. name` line
- No trailing blank lines at the end of a file

---

## End-of-project cleanup checklist

When applying this skill across all `py_files/*.py`:

1. **Docstring** — add or rewrite to match the format above; add `Data sources:` block if the file fetches data.
2. **Imports** — reorder into the four groups; remove unused imports; remove inline import comments.
3. **Section separators** — add separators where logical groups exist; renumber sections 0, 1, 2… consistently within each file.
4. **Constants** — rename to ALL_CAPS where they are module-level; align dict values.
5. **Docstrings** — trim to two-to-four lines; remove `Args:`/`Returns:` boilerplate.
6. **Blank lines** — enforce the rules above.
7. **Do not** reorder functions, rename variables, or change logic.
