---
name: api-eds
description: Energi Data Service (energidataservice.dk) — ET-eds-api client, spot prices (get_wp_h, wagg_wp), VE weather-normalised production. Use when fetching Danish electricity prices, production, consumption, or capacity data.
---

## Library

```bash
pip install ET-eds-api
```

```python
from ET_eds_api import get_wp_h, wagg_wp, VE, columns
```

## Spot prices

### get_wp_h — hourly consumption-weighted price

```python
wp_h, q_h, p_area = get_wp_h(start=2023, end=2025)
# wp_h   — hourly consumption-weighted price (pd.Series, index=HourUTC)
# q_h    — hourly gross consumption (MWh)
# p_area — DataFrame with columns: HourUTC | DK1 | DK2

# With caching and EnergyPLAN output
wp_h, q_h, p_area = get_wp_h(start=2023, end=2025, cache=True, save_txt=True)
# save_txt writes to variation_patterns/wp_{start}_{end}.txt
```

### wagg_wp — aggregated prices

```python
wp_d, wp_w, wp_m, wp_y = wagg_wp(start=2023, end=2025)
# Returns daily, weekly, monthly, yearly aggregations
```

**Data sources for prices:**

| Dataset | Period |
|---------|--------|
| `Elspotprices` | up to ~2025-09-30 |
| `DayAheadPrices` | from ~2025-10-01 |

The client stitches these automatically.

## VE — weather-normalised production

Fetches hourly production, aggregates to monthly, deflates by capacity index to isolate the weather signal from capacity growth.

```python
from ET_eds_api import VE, columns

columns()   # prints available value_columns and cap_column options

solar_ve = VE(
    value_columns = ["SolarPowerLt10kW_MWh", "SolarPowerGe10Lt40kW_MWh", "SolarPowerGe40kW_MWh"],
    cap_column    = ["SolarPowerCapacity"],
    col_name      = "solar_VE",
    start         = 2022,           # integer year
    end           = 2025,
    cap_ref       = None,           # None = last observed capacity
    cache         = True,
    save_txt      = False,
)
# Returns DataFrame: HourUTC, month, value, solar_VE_idx, solar_VE
```

### cap_ref — counterfactual capacity

```python
# Normalise to fixed 1 GW — "what would production be at 1 GW installed?"
solar_ve_1gw = VE(..., cap_ref=1_000)
```

- `None` — denominator is last observed capacity
- `float` (MW) — counterfactual fixed capacity; use for reference scenario + diffs

## Raw fetch — data not covered by ET-eds-api

For any EDS dataset not wrapped by the package, fetch directly:

```python
import requests
import pandas as pd

def fetch_eds(dataset: str, params: dict) -> pd.DataFrame:
    url = f"https://api.energidataservice.dk/dataset/{dataset}"
    params.setdefault("limit", 0)       # 0 = no row limit
    params.setdefault("timezone", "UTC")
    r = requests.get(url, params=params)
    r.raise_for_status()
    return pd.DataFrame(r.json()["records"])

# Example — transmission flows
df = fetch_eds("InterconnectionAccountingPoint", {
    "start":   "2024-01-01",
    "end":     "2025-01-01",
    "columns": "HourUTC,ConnectedArea,ExchangeDKK",
    "sort":    "HourUTC asc",
})
```

Dataset names are the path segment from the EDS URL, e.g. `ElspotPrices`, `ProductionConsumptionSettlement`, `CapacityPerMunicipality`. Browse at energidataservice.dk.

## Gotchas

- `start` and `end` are **integer years**, not date strings.
- `get_wp_h` returns **three** values since v0.1.5: `wp_h, q_h, p_area`. Old unpacking `wp_h, q_h = get_wp_h(...)` will break.
- PriceArea is `DK1` or `DK2` — `p_area` has both as columns; `wp_h` is the consumption-weighted average across both.
- Capacity data is monthly; production data is hourly. `VE` aligns on `month`.
