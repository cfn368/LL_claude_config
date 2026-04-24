---
name: notebook-style
description: Conventions for structuring research Jupyter notebooks — cell order, markdown patterns, section headers, sub-section labels, code comments, LaTeX equations. Apply when writing or reviewing any notebook.
---

## Cell structure (top to bottom)

```
[code]      setup cell — from py_files.setup import *; setup_notebook()
[markdown]  # Section Title   ← H1, one per major section
[markdown]  description paragraph — what this section does, including LaTeX equations
[markdown]  *`1. sub-section label`*   ← italic backtick, lowercase
[markdown]  *short sentence describing what the next code cell does*
[code]      # 1. step name   ← numbered comment matching sub-section label
            code...
[markdown]  *`2. sub-section label`*
[markdown]  *short descriptor*
[code]      # 2. step name
            code...
```

## Rules

**Setup cell** — always first, always two lines:
```python
from py_files.setup import *
setup_notebook()
```

**Section headers** — `# Title` in a standalone markdown cell. One H1 per logical section, no deeper headings.

**Sub-section labels** — italic backtick style: `*\`1. label\``*`. Lowercase, numbered. Go directly above the code cell they label.

**Descriptor cells** — one italic sentence immediately before each code cell, explaining what it does. Use LaTeX inline (`$...$`) or display (`$$...$$`) freely.

**Code cells** — numbered comments match the sub-section label (`# 1. calibrate`, `# 2. simulate`). One conceptual step per cell. Parameters go at the top of the cell, not scattered.

**Executed output** — keep in the notebook. Notebook output is the primary documentation for non-Python readers.

**LaTeX** — equations belong in markdown descriptor cells, not in comments. Use display math (`$$...$$`) for named equations; inline (`$...$`) for variable references.

## Example

```markdown
# Impulse response functions
```
```markdown
Simulates a permanent capital income tax cut... The tax cut follows geometric convergence,

$$
    (1-\tau_t) = (1-\tau_T) + \rho^t\left[(1-\tau_0) - (1-\tau_T)\right]
$$
```
```markdown
*`1. calibration and simulation`*
```
```markdown
*calibrate to zero SS wage premia and target labour supply elasticity $\varepsilon_{nI} = (1-s_L)\phi$*
```
```python
# 1. calibrate
m = CapIncModel_single()
out = m.calibrate(target_elas=m.phi)

# 2. pin baseline SS
T=30; tau0=0.0; tauT=-0.1; rho=0.80
ss0 = m.solve_steady_state(tau=tau0)
```
