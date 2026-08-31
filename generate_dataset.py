import numpy as np
import csv
import os

rng = np.random.default_rng(42)

DRIVERS = [
    "VER", "PER", "HAM", "RUS", "LEC", "SAI", "NOR", "PIA",
    "ALO", "STR", "GAS", "OCO", "ALB", "SAR", "TSU", "RIC",
    "BOT", "ZHO", "MAG", "HUL",
]
TEAMS = {
    "VER": "Red Bull Racing", "PER": "Red Bull Racing",
    "HAM": "Mercedes", "RUS": "Mercedes",
    "LEC": "Ferrari", "SAI": "Ferrari",
    "NOR": "McLaren", "PIA": "McLaren",
    "ALO": "Aston Martin", "STR": "Aston Martin",
    "GAS": "Alpine", "OCO": "Alpine",
    "ALB": "Williams", "SAR": "Williams",
    "TSU": "RB", "RIC": "RB",
    "BOT": "Sauber", "ZHO": "Sauber",
    "MAG": "Haas", "HUL": "Haas",
}
BASE_PACE = {
    "VER": 0.05, "PER": 0.35, "HAM": 0.30, "RUS": 0.28, "LEC": 0.15, "SAI": 0.25,
    "NOR": 0.10, "PIA": 0.20, "ALO": 0.40, "STR": 0.70, "GAS": 0.55, "OCO": 0.60,
    "ALB": 0.75, "SAR": 1.00, "TSU": 0.65, "RIC": 0.72, "BOT": 0.90, "ZHO": 1.05,
    "MAG": 0.85, "HUL": 0.80,
}

TOTAL_LAPS = 57
THEORETICAL_BEST = 91.200
COMPOUNDS = ["Soft", "Medium", "Hard"]

rows = []
row_id = 1

for driver in DRIVERS:
    team = TEAMS[driver]
    pace_offset = BASE_PACE[driver]

    stint_bounds = sorted(rng.choice(range(12, 46), size=2, replace=False))
    stint_ranges = [
        (1, stint_bounds[0]),
        (stint_bounds[0] + 1, stint_bounds[1]),
        (stint_bounds[1] + 1, TOTAL_LAPS),
    ]
    compounds = rng.choice(COMPOUNDS, size=3, replace=False).tolist()
    deg_rate = {"Soft": 0.045, "Medium": 0.028, "Hard": 0.016}
    compound_bonus = {"Soft": -0.35, "Medium": 0.0, "Hard": 0.30}

    fuel = 110.0
    fuel_burn_per_lap = fuel / TOTAL_LAPS

    for stint_idx, (start_lap, end_lap) in enumerate(stint_ranges):
        compound = compounds[stint_idx]
        for lap in range(start_lap, end_lap + 1):
            tyre_age = lap - start_lap + 1
            is_pit_lap = 1 if (lap == start_lap and stint_idx > 0) else 0

            fuel_effect = (fuel / 110.0) * 0.6
            deg_effect = deg_rate[compound] * tyre_age
            noise = rng.normal(0, 0.12)

            lap_time = (
                THEORETICAL_BEST
                + pace_offset
                + compound_bonus[compound]
                + fuel_effect
                + deg_effect
                + noise
            )
            if is_pit_lap:
                lap_time += rng.normal(22.5, 1.2)

            s1 = lap_time * rng.uniform(0.285, 0.295)
            s2 = lap_time * rng.uniform(0.360, 0.370)
            s3 = lap_time - s1 - s2

            speed_trap = 335 - (lap_time - THEORETICAL_BEST) * 3.1 + rng.normal(0, 2.5)
            track_temp = 33.0 + 4 * np.sin(lap / TOTAL_LAPS * np.pi) + rng.normal(0, 0.4)

            rows.append([
                row_id, lap, driver, team,
                round(lap_time, 3), round(s1, 3), round(s2, 3), round(s3, 3),
                round(speed_trap, 1), compound, tyre_age, is_pit_lap,
                round(fuel, 2), round(track_temp, 1),
            ])
            row_id += 1
            fuel = max(fuel - fuel_burn_per_lap, 0)

HEADER = [
    "id", "lap", "driver", "team",
    "lap_time_sec", "sector1_sec", "sector2_sec", "sector3_sec",
    "speed_trap_kmh", "tyre_compound", "tyre_age_laps", "pit_stop",
    "fuel_load_kg", "track_temp_c",
]

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "f1_telemetry.csv")
with open(out_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(HEADER)
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {out_path}")
