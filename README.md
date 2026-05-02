# LL Claude Config

Global Claude Code configuration for Linus Lindquist. Syncs across projects via `~/.claude/`.

## Structure

```
CLAUDE.md           — identity, technical level, response style, analytical defaults
skills/
  notebook-setup/   — setup.py scaffold and notebook preamble pattern
  notebook-style/   — cell structure, markdown conventions, LaTeX in notebooks
  econ-plotting/    — matplotlib-only standards: AEJ style, SEC_PALETTE, legend rules
    assets/
      matplotlibrc  — drop-in rcParams file
      template.py   — single-panel and grid-with-legend templates
  api-dst/          — Danmarks Statistik (dstapi), BULK query pattern
  api-eds/          — Energi Data Service (ET-eds-api): prices + VE production
  api-eurostat/     — Eurostat SDMX + ComextApi for trade data
  pyfile-style/     — py_files/ conventions: docstring, section separators, imports, cleanup checklist
```

## What's gitignored

Everything in `~/.claude/` except this repo's content. Claude Code runtime state (sessions, projects, credentials, memory) is excluded via allowlist `.gitignore`.
