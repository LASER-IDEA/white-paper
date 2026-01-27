import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_mock_csv(filepath=None, num_rows=500):
    if filepath is None:
        # Default to data directory relative to this script
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, "..", "..", "data")
        filepath = os.path.join(data_dir, "sample_flight_data.csv")
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(num_rows)]
    regions = ["Nanshan", "Futian", "Luohu", "Baoan", "Longgang", "Yantian", "Longhua", "Pingshan", "Guangming", "Dapeng"]
    entities = [f"Company {chr(65+i)}" for i in range(30)] # Company A...
    entity_ids = [f"ENT{str(i+1).zfill(4)}" for i in range(len(entities))]
    types = ["MultiRotor", "FixedWing", "Helicopter"]
    models = ["M300", "Dragonfish", "P100", "Mavic 3", "Autel Alpha", "E200", "V50"]
    purposes = ["Logistics", "Inspection", "Personal", "Surveying", "Emergency"]
    user_types = ["企业用户", "个人用户", "未知用户"]

    entity_choices = np.random.choice(len(entities), size=num_rows)
    dates_str = [d.strftime("%Y-%m-%d") for d in dates]
    hours = np.random.randint(0, 24, size=num_rows)
    minutes = np.random.randint(0, 60, size=num_rows)
    durations = np.random.randint(5, 120, size=num_rows)  # minutes
    distances = np.round(np.random.uniform(1, 60, size=num_rows), 2)  # km
    is_holiday = np.random.choice([True, False], size=num_rows, p=[0.1, 0.9])
    is_planned = np.random.choice([True, False], size=num_rows, p=[0.98, 0.02])
    is_effective = is_planned & np.random.choice([True, False], size=num_rows, p=[0.95, 0.05])

    start_regions = np.random.choice(regions, size=num_rows)
    end_regions = []
    for r in start_regions:
        if np.random.rand() < 0.7:
            end_regions.append(r)
        else:
            end_regions.append(np.random.choice(regions))

    data = {
        "date": dates_str,
        "time": [f"{h:02d}:{m:02d}:00" for h, m in zip(hours, minutes)],
        "region": [np.random.choice(regions) for _ in range(num_rows)],
        "duration": durations,
        "distance": distances,
        "entity_id": [entity_ids[i] for i in entity_choices],
        "entity": [entities[i] for i in entity_choices],
        "user_type": [np.random.choice(user_types, p=[0.6, 0.3, 0.1]) for _ in range(num_rows)],
        "aircraft_type": [np.random.choice(types) for _ in range(num_rows)],
        "aircraft_model": [np.random.choice(models) for _ in range(num_rows)],
        "purpose": [np.random.choice(purposes) for _ in range(num_rows)],
        "sn": [f"SN{np.random.randint(1000, 1100)}" for _ in range(num_rows)],
        "altitude": np.random.randint(50, 800, size=num_rows),
        "start_region": start_regions,
        "end_region": end_regions,
        "is_holiday": is_holiday,
        "is_planned": is_planned,
        "is_effective": is_effective
    }

    df = pd.DataFrame(data)
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Generated {filepath}")

if __name__ == "__main__":
    generate_mock_csv()
