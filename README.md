# Pitwall

A Streamlit dashboard for exploring lap-by-lap Formula 1 telemetry. Built around a synthetic 2025 Bahrain Grand Prix dataset (20 drivers, 57 laps, 1,140 rows), it combines statistics, race analysis, and a live trackmap into a single interactive tool.

## Features

- **Live trackmap** — every driver placed on a generated circuit outline based on their real cumulative race gap at a selectable lap, with a driver-standings list alongside it.
- **Race statistics** — mean, median, standard deviation, percentiles, min/max across the full field and per driver.
- **Pace & speed analysis** — speed conversions and pace delta across the session.
- **Field analysis** — every driver's pace measured against the leader, and sector time loss against the field's best.
- **Grid filters** — filtering laps by compound, temperature, and pace.
- **Fastest laps & rankings** — the quickest laps and drivers of the session.
- **Six chart types** — line, bar, scatter, histogram, box plot, and heatmap.
- **Head-to-head comparison** — pace summary, overlaid lap-time chart, and a cumulative gap-evolution chart between any two drivers.
- **CSV export** — download the full dataset directly from the dashboard.

## Tech stack

Python, NumPy, Pandas, Streamlit, Matplotlib.

## Project structure

```
Lab_9/
├── app.py                 Streamlit application
├── generate_dataset.py    builds f1_telemetry.csv
├── f1_telemetry.csv       generated dataset (20 drivers x 57 laps)
└── requirements.txt
```

## Running it

```bash
pip install -r requirements.txt
python generate_dataset.py   # only needed if f1_telemetry.csv is missing
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Dataset

`f1_telemetry.csv` is generated with a seeded RNG so results are reproducible. Each row is one driver's lap and includes lap time, sector splits, speed trap, tyre compound and age, pit-stop flag, fuel load, and track temperature. Lap times are modelled from a theoretical best lap plus per-driver pace offset, tyre compound and degradation, fuel load, and random noise, with a pit-lane time penalty applied on in-laps.
