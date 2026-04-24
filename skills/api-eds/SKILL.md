---
name: api-eds
description: Energi Data Service (energidataservice.dk) — ET-eds-api client, VE weather-normalised production, capacity index pattern. Use when fetching Danish electricity production, consumption, or capacity data.
---

## Library

`ET-eds-api` — self-built PyPI package. Two main endpoints:

| Endpoint | Dataset |
|----------|---------|
| `ProductionConsumptionSettlement` | Hourly production/consumption by technology (MWh) |
| `CapacityPerMunicipality` | Monthly installed capacity by technology and municipality |

```python
from et_eds_api import VE, columns   # or from ._cache import fetch for raw access
```

## Discover available columns

```python
columns()   # prints value_columns (ProductionConsumptionSettlement) and cap_column options
```

## VE — weather-normalised production

`VE` fetches hourly production, aggregates to monthly, and deflates by a capacity index to isolate the weather signal from capacity growth.

```python
df = VE(
    value_columns = ['SolarPower_MWh', 'OnshoreWindPower_MWh'],  # summed into 'value'
    cap_column    = ['SolarCapacity_MW'],    # capacity series to build deflator
    col_name      = 'VE_sol',               # output column name
    start         = '2015-01-01',
    end           = '2024-01-01',
    cap_ref       = None,   # None = last observed capacity; pass a float for counterfactual
    verbose       = True,
    cache         = False,
    save_txt      = False,  # True = write EnergyPLAN-compatible .txt
)
# Returns DataFrame: HourUTC, month, value, VE_sol_idx, VE_sol
```

### cap_ref parameter

The key analytical lever. Controls the denominator of the capacity index:

- `None` — last observed capacity (default). Deflator normalises to "what would production be at current capacity?"
- `float` — counterfactual capacity. Use to answer "what would production be at X GW?" — the reference scenario + diffs pattern.

## Raw fetch

For endpoints not covered by `VE`:

```python
from et_eds_api._cache import fetch

df = fetch(
    "https://api.energidataservice.dk/dataset/ElspotPrices",
    {
        "start":    "2020-01-01",
        "end":      "2024-01-01",
        "timezone": "UTC",
        "columns":  "HourUTC,PriceArea,SpotPriceDKK",
        "sort":     "HourUTC asc",
        "limit":    0,      # 0 = no limit, returns all rows
    }
)
```

## Gotchas

- `limit: 0` is required to get all rows — the default page limit is 100.
- `timezone: "UTC"` always. Local time (CET/CEST) introduces DST gaps.
- PriceArea is `DK1` or `DK2` — filter before aggregating if you want one area.
- Capacity data is monthly; production data is hourly. The `VE` merge aligns on `month`.
- `save_txt=True` writes an EnergyPLAN-compatible fixed-format text file — useful when piping into EnergyPLAN simulations.
