import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_csv(filepath="data/sample_flight_data.csv", num_rows=500):
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(num_rows)]
    regions = ["Nanshan", "Futian", "Luohu", "Baoan", "Longgang", "Yantian", "Longhua", "Pingshan", "Guangming", "Dapeng"]
    entities = [f"Company {chr(65+i)}" for i in range(20)] # Company A...
    types = ["MultiRotor", "FixedWing", "Helicopter"]
    models = ["M300", "Dragonfish", "P100", "Mavic 3", "Autel Alpha"]
    purposes = ["Logistics", "Inspection", "Personal", "Surveying", "Emergency"]

    data = {
        "date": [d.strftime("%Y-%m-%d") for d in dates],
        "time": [f"{np.random.randint(0, 24):02d}:{np.random.randint(0, 60):02d}:00" for _ in range(num_rows)],
        "region": [np.random.choice(regions) for _ in range(num_rows)],
        "duration": np.random.randint(5, 120, size=num_rows), # minutes
        "distance": np.random.uniform(1, 50, size=num_rows), # km
        "entity": [np.random.choice(entities) for _ in range(num_rows)],
        "aircraft_type": [np.random.choice(types) for _ in range(num_rows)],
        "aircraft_model": [np.random.choice(models) for _ in range(num_rows)],
        "purpose": [np.random.choice(purposes) for _ in range(num_rows)],
        "sn": [f"SN{np.random.randint(1000, 1050)}" for _ in range(num_rows)], # 50 unique aircraft
        "altitude": np.random.randint(50, 500, size=num_rows),
        "start_region": [np.random.choice(regions) for _ in range(num_rows)],
        "end_region": [np.random.choice(regions) for _ in range(num_rows)]
    }

    df = pd.DataFrame(data)
    # Ensure directory exists
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Generated {filepath}")

if __name__ == "__main__":
    generate_mock_csv()
