---
name: api-dst
description: Danmarks Statistik Statistikbanken — dstapi client, BULK query pattern, INDHOLD post-processing, code extraction. Use when fetching DST tables (national accounts, I-O, labour, etc.).
---

## Library

```python
from dstapi import DstApi   # pip install dstapi
# https://github.com/alemartinello/dstapi
```

## Request pattern

```python
api = DstApi('TABLE_ID')    # e.g. 'NAIO1F', 'ADAM', 'LBESK'

params = {
    'table':  'TABLE_ID',
    'format': 'BULK',       # always BULK for data
    'lang':   'en',
    'variables': [
        {'code': 'PRISENHED', 'values': ['V']},        # basic prices
        {'code': 'Tid',       'values': ['2019']},     # year (always string)
        {'code': 'DIM3',      'values': ['A', 'B']},   # multiple values as list
    ]
}

df = api.get_data(params=params)
```

## Response post-processing

The value column is always `INDHOLD`; it arrives as strings and must be coerced:

```python
df['INDHOLD'] = pd.to_numeric(df['INDHOLD'], errors='coerce')
```

Variable labels include the code as a prefix separated by a space — strip to get the code:

```python
df['code'] = df['SOME_DIM'].str.split(' ').str[0]
```

## Discovering tables and variable codes

- Table browser: https://www.statistikbanken.dk  
- `api.get_variables()` — returns available dimensions and their codes for a table
- `api.get_data({'table': 'X', 'format': 'BULK', 'lang': 'en', 'variables': []})` with empty variables fetches defaults (useful for a quick preview)

## Common variable codes (NAIO1F — national accounts I-O)

| Code | Meaning |
|------|---------|
| `PRISENHED` | Price unit: `V` = basic prices |
| `Tid` | Year (string) |
| `TILGANG1` | Supply type: `P1_BP` = domestic, `P7AD2121` = imports |
| `TILGANG2` | Supplying product/industry |
| `ANVENDELSE` | Use category; `AA00000` = total output |

## Gotchas

- `Tid` values must always be strings: `str(year)`, not `int`.
- Labels in TILGANG/ANVENDELSE columns are `"CODE Label text"` — always `.str.split(' ').str[0]` before joining or filtering.
- `BULK` format is the only format that returns all rows reliably; `JSON` has pagination issues on large tables.
- Empty `.values` list `[]` fetches all codes for that dimension — useful for exploration, slow for large dimensions.
