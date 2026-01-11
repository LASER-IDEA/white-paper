import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_mock_data():
    """Generates mock data consistent with the TypeScript frontend requirements."""

    # 1. Traffic Data (Area Chart)
    dates = pd.date_range(start="2023-01-01", periods=30, freq="D")
    traffic_data = pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"),
        "value": np.random.randint(100, 500, size=30)
    })

    # 2. Operation Intensity (Dual Line)
    regions = ["Nanshan", "Futian", "Luohu", "Baoan", "Longgang"]
    operation_data = pd.DataFrame({
        "name": regions,
        "duration": np.random.randint(1000, 5000, size=len(regions)),
        "distance": np.random.randint(5000, 20000, size=len(regions))
    })

    # 3. Fleet Structure (Stacked Bar)
    fleet_data = pd.DataFrame({
        "name": ["Q1", "Q2", "Q3", "Q4"],
        "MultiRotor": np.random.randint(50, 150, size=4),
        "FixedWing": np.random.randint(20, 80, size=4),
        "Helicopter": np.random.randint(5, 20, size=4)
    })

    # 4. Concentration (Pareto)
    companies = [f"Company {i}" for i in range(1, 11)]
    pareto_data = pd.DataFrame({
        "name": companies,
        "volume": sorted(np.random.randint(50, 500, size=10), reverse=True)
    })

    # 5. Commercial Maturity (Rose)
    sectors = ["Logistics", "Inspection", "Surveying", "Agriculture", "Emergency", "Tourism"]
    rose_data = pd.DataFrame({
        "name": sectors,
        "value": np.random.randint(10, 100, size=len(sectors))
    })

    # 6. Diversity (Treemap)
    treemap_data = [
        {"name": "Logistics", "size": 40, "value": 40},
        {"name": "Inspection", "size": 30, "value": 30},
        {"name": "Survey", "size": 20, "value": 20},
        {"name": "Agri", "size": 10, "value": 10}
    ]

    # 7. Regional Balance (Map)
    # Using mock geojson structure later, just data here
    map_data = pd.DataFrame({
        "name": ["Nanshan", "Futian", "Luohu", "Baoan", "Longgang", "Yantian", "Longhua", "Pingshan", "Guangming", "Dapeng"],
        "value": np.random.randint(20, 100, size=10)
    })

    # 8. All Weather (Polar Clock) - Hourly
    hours = [f"{i}:00" for i in range(24)]
    polar_data = pd.DataFrame({
        "hour": hours,
        "value": np.abs(np.sin(np.linspace(0, np.pi*2, 24)) * 100 + np.random.normal(0, 10, 24))
    })

    # 9. Seasonal (Box Plot)
    seasonal_data = pd.DataFrame({
        "name": ["Spring", "Summer", "Autumn", "Winter"],
        "min": [10, 20, 15, 5],
        "q1": [20, 40, 30, 15],
        "median": [30, 60, 45, 25],
        "q3": [50, 80, 60, 40],
        "max": [70, 100, 80, 50],
        "avg": [35, 65, 50, 28] # Added for DualLine nature of the request
    })

    # 10. Efficiency (Gauge)
    gauge_data = [{"value": 85, "name": "Efficiency"}]

    # 11. Endurance (Funnel)
    funnel_data = pd.DataFrame({
        "name": ["Plan", "Takeoff", "Cruise", "Mission", "Return", "Land"],
        "value": [100, 95, 90, 85, 80, 75]
    })

    # 12. Wide Area (Histogram)
    histogram_data = pd.DataFrame({
        "name": ["0-5km", "5-10km", "10-20km", "20-50km", ">50km"],
        "value": np.random.randint(10, 100, size=5)
    })

    # 13. Micro Circulation (Chord)
    # Represented as Source-Target matrix or list
    chord_data = [
        {"source": "Nanshan", "target": "Futian", "value": 50},
        {"source": "Futian", "target": "Luohu", "value": 40},
        {"source": "Nanshan", "target": "Baoan", "value": 60},
        {"source": "Baoan", "target": "Longgang", "value": 30}
    ]

    # 14. Vertical Airspace (3D Bar) - Simplified to Bar for now or Heatmap
    # Using 3 categories for height
    airspace_data = pd.DataFrame({
        "name": ["<120m", "120-300m", ">300m"],
        "value": [500, 300, 100]
    })

    # 15. Calendar Heatmap
    cal_dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    calendar_data = pd.DataFrame({
        "date": cal_dates.strftime("%Y-%m-%d"),
        "value": np.random.randint(100, 1000, size=len(cal_dates))
    })

    # 16. Night Economy (Wave/Area)
    night_hours = [f"{i}:00" for i in range(18, 30)] # 18:00 to 06:00 next day
    night_data = pd.DataFrame({
        "hour": [h if int(h.split(":")[0]) < 24 else f"0{int(h.split(':')[0])-24}:00" for h in night_hours],
        "value": np.random.randint(10, 100, size=len(night_hours))
    })

    # 17. Leading Entity (Radar)
    radar_data = pd.DataFrame({
        "subject": ["Tech", "Scale", "Safe", "Eco", "Grow"],
        "A": [80, 90, 70, 85, 95],
        "B": [70, 80, 90, 60, 75]
    })

    # 18. Dashboard (Composite)
    dashboard_data = [{"value": 88.5}]

    return {
        "traffic": traffic_data,
        "operation": operation_data,
        "fleet": fleet_data,
        "pareto": pareto_data,
        "rose": rose_data,
        "treemap": treemap_data,
        "map": map_data,
        "polar": polar_data,
        "seasonal": seasonal_data,
        "gauge": gauge_data,
        "funnel": funnel_data,
        "histogram": histogram_data,
        "chord": chord_data,
        "airspace": airspace_data,
        "calendar": calendar_data,
        "night": night_data,
        "radar": radar_data,
        "dashboard": dashboard_data
    }

if __name__ == "__main__":
    data = generate_mock_data()
    print("Data generated successfully.")
