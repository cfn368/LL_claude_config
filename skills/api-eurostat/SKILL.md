---
name: api-eurostat
description: Eurostat SDMX 2.1 API — direct XML fetch pattern, key structure, _parse helper, main energy/macro datasets. Also covers ComextApi for trade data (DS-045409). Use when fetching Eurostat energy, national accounts, or trade data.
---

## Two access patterns

| Use case | Method |
|----------|--------|
| Energy, GVA, balances | Direct SDMX XML fetch via `requests` + `_parse()` |
| Comext trade (CN codes) | `ComextApi` class |

---

## Direct SDMX fetch

### URL structure

```
https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{DATASET_ID}/{KEY}?startPeriod={YYYY}
```

Key format: `freq.dim1.dim2....geo` — dimension order is dataset-specific. Use `+` to combine multiple values in one position.

### _parse helper

```python
import xml.etree.ElementTree as ET
import requests
import pandas as pd

_G = "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"

def _parse(r) -> pd.DataFrame:
    r.raise_for_status()
    root = ET.fromstring(r.text)
    rows = []
    for series in root.iter(f"{{{_G}}}Series"):
        sk   = series.find(f"{{{_G}}}SeriesKey")
        dims = {v.get('id'): v.get('value') for v in sk.findall(f"{{{_G}}}Value")}
        for obs in series.iter(f"{{{_G}}}Obs"):
            year   = obs.find(f"{{{_G}}}ObsDimension").get('value')
            val_el = obs.find(f"{{{_G}}}ObsValue")
            val    = float(val_el.get('value')) if val_el is not None else None
            rows.append({**dims, 'year': int(year), 'value': val})
    return pd.DataFrame(rows)
```

### Main datasets and key order

| Dataset | Description | Key order |
|---------|-------------|-----------|
| `nrg_ind_re` | Renewable share of final consumption (%) | `freq.nrg_bal.unit.geo` — unit always `PC` |
| `nama_10_a64` | GVA by NACE A64 (CP_MEUR) | `freq.unit.nace_r2.na_item.geo` — unit `CP_MEUR`, na_item `B1G` |
| `nrg_bal_c` | Final energy consumption by sector (TJ) | `freq.nrg_bal.siec.unit.geo` — siec `TOTAL`, unit `TJ` |

### Example fetch

```python
countries = ['DK', 'DE', 'SE', 'NO', 'FI']
nrg_bal   = ['REN_ELC', 'REN_HEAT_CL']   # or single string

key = f"A.{'+'.join(nrg_bal)}.PC.{'+'.join(countries)}"
df  = _parse(requests.get(
    f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nrg_ind_re/{key}?startPeriod=1995"
))
```

### NACE → nrg_bal split rules (GVA fetch)

Some NACE codes are aggregates that must be split before mapping to energy sectors:

- `C24` (metals) → equal split across `FC_IND_IS_E`, `FC_IND_NFM_E`
- `H49` (land transport) → equal split across `FC_TRA_RAIL_E`, `FC_TRA_ROAD_E`, `FC_TRA_PIPE_E`
- `H50` → `FC_TRA_DNAVI_E`, `H51` → `FC_TRA_DAVI_E`

---

## ComextApi — trade data (DS-045409)

```python
from comext_wrapper import ComextApi    # self-built package

api = ComextApi()
api.info()                              # dataset overview + dimension list
api.codes("product", search="wind")    # search CN codes by label
api.codes("partner", aggregates_only=True)  # aggregate partner groups

df = api.get_data(
    reporter     = "DE+FR+DK",
    partner      = "EXT_EU27_2020",    # extra-EU aggregate
    product      = "85024000+85017100",
    flow         = "1+2",              # 1=import, 2=export
    indicators   = "VALUE_IN_EUROS",
    freq         = "M",
    start_period = "2020-01",
)
# Returns tidy DataFrame: freq, reporter, partner, product, flow, indicators, period, value
```

Dimension order in SDMX key: `freq.reporter.partner.product.flow.indicators`

## Gotchas

- Key dimension order is fixed and dataset-specific — wrong order returns HTTP 400 or empty data, not an error message.
- `startPeriod` takes `YYYY` for annual, `YYYY-MM` for monthly.
- EU28 is excluded from `nama_10_a64` GVA fetches (non-member years break the series).
- Comext codelists have version numbers (`CXT_NC/11.0`); Eurostat updates them occasionally — if a codelist fetch returns 404, update the version in `_DIM_CODELISTS`.
- Response can be sparse (JSON-stat with dict values, not a dense list) — `_jsonstat_to_df` handles both; raw `requests` fetches with `_parse` always get dense XML.
