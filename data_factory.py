import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data():
    """Generates mock data for the 18 metrics."""
    data = {}

    # 1. Traffic (Area)
    dates = pd.date_range(start="2023-01-01", periods=30, freq="D")
    data["traffic"] = pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"),
        "value": np.random.randint(100, 500, size=30)
    }).to_dict(orient="records")

    # 2. Operation Intensity (Dual Line)
    regions = ["Nanshan", "Futian", "Luohu", "Baoan", "Longgang"]
    data["operation"] = pd.DataFrame({
        "name": regions,
        "duration": np.random.randint(1000, 5000, size=len(regions)),
        "distance": np.random.randint(5000, 20000, size=len(regions))
    }).to_dict(orient="records")

    # 3. Fleet Structure (Stacked Bar)
    data["fleet"] = pd.DataFrame({
        "name": ["Q1", "Q2", "Q3", "Q4"],
        "MultiRotor": np.random.randint(50, 150, size=4),
        "FixedWing": np.random.randint(20, 80, size=4),
        "Helicopter": np.random.randint(5, 20, size=4)
    }).to_dict(orient="records")

    # 4. Concentration (Pareto)
    companies = [f"Company {i}" for i in range(1, 11)]
    vols = sorted(np.random.randint(50, 500, size=10), reverse=True)
    data["pareto"] = pd.DataFrame({
        "name": companies,
        "volume": vols
    }).to_dict(orient="records")

    # 5. Commercial Maturity (Rose)
    sectors = ["Logistics", "Inspection", "Surveying", "Agriculture", "Emergency", "Tourism"]
    data["rose"] = pd.DataFrame({
        "name": sectors,
        "value": np.random.randint(10, 100, size=len(sectors))
    }).to_dict(orient="records")

    # 6. Diversity (Treemap)
    data["treemap"] = [
        {"name": "Logistics", "value": 40},
        {"name": "Inspection", "value": 30},
        {"name": "Survey", "value": 20},
        {"name": "Agri", "value": 10}
    ]

    # 7. Regional Balance (Map)
    data["map"] = [
        {"name": "Nanshan", "value": np.random.randint(20, 100)},
        {"name": "Futian", "value": np.random.randint(20, 100)},
        {"name": "Luohu", "value": np.random.randint(20, 100)},
        {"name": "Baoan", "value": np.random.randint(20, 100)},
        {"name": "Longgang", "value": np.random.randint(20, 100)}
    ]

    # 8. All Weather (Polar Clock)
    hours = [f"{i}:00" for i in range(24)]
    data["polar"] = pd.DataFrame({
        "hour": hours,
        "value": np.abs(np.sin(np.linspace(0, np.pi*2, 24)) * 100 + np.random.normal(0, 10, 24)).astype(int)
    }).to_dict(orient="records")

    # 9. Seasonal (Box Plot)
    # ECharts boxplot expects [min, Q1, median, Q3, max]
    data["seasonal"] = {
        "categories": ["Spring", "Summer", "Autumn", "Winter"],
        "values": [
            [10, 20, 30, 50, 70],
            [20, 40, 60, 80, 100],
            [15, 30, 45, 60, 80],
            [5, 15, 25, 40, 50]
        ]
    }

    # 10. Efficiency (Gauge)
    data["gauge"] = [{"value": 85, "name": "Efficiency"}]

    # 11. Endurance (Funnel)
    data["funnel"] = [
        {"value": 100, "name": "Plan"},
        {"value": 95, "name": "Takeoff"},
        {"value": 90, "name": "Cruise"},
        {"value": 85, "name": "Mission"},
        {"value": 80, "name": "Return"},
        {"value": 75, "name": "Land"}
    ]

    # 12. Wide Area (Histogram)
    data["histogram"] = pd.DataFrame({
        "name": ["0-5km", "5-10km", "10-20km", "20-50km", ">50km"],
        "value": np.random.randint(10, 100, size=5)
    }).to_dict(orient="records")

    # 13. Micro Circulation (Chord -> Graph/Sankey)
    data["chord"] = {
        "nodes": [{"name": "Nanshan"}, {"name": "Futian"}, {"name": "Luohu"}, {"name": "Baoan"}, {"name": "Longgang"}],
        "links": [
            {"source": "Nanshan", "target": "Futian", "value": 50},
            {"source": "Futian", "target": "Luohu", "value": 40},
            {"source": "Nanshan", "target": "Baoan", "value": 60},
            {"source": "Baoan", "target": "Longgang", "value": 30}
        ]
    }

    # 14. Vertical Airspace (3D Bar -> Bar)
    data["airspace"] = [
        {"name": "<120m", "value": 500},
        {"name": "120-300m", "value": 300},
        {"name": ">300m", "value": 100}
    ]

    # 15. Calendar Heatmap
    # Generate full year 2023
    cal_dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    data["calendar"] = [[d.strftime("%Y-%m-%d"), np.random.randint(100, 1000)] for d in cal_dates]

    # 16. Night Economy (Wave)
    night_hours = [f"{i}:00" for i in range(18, 30)]
    data["night"] = pd.DataFrame({
        "hour": [h if int(h.split(":")[0]) < 24 else f"0{int(h.split(':')[0])-24}:00" for h in night_hours],
        "value": np.random.randint(10, 100, size=len(night_hours))
    }).to_dict(orient="records")

    # 17. Leading Entity (Radar)
    data["radar"] = {
        "indicator": [
             {"name": "Tech", "max": 100},
             {"name": "Scale", "max": 100},
             {"name": "Safe", "max": 100},
             {"name": "Eco", "max": 100},
             {"name": "Grow", "max": 100}
        ],
        "data": [
            {"value": [80, 90, 70, 85, 95], "name": "Company A"},
            {"value": [70, 80, 90, 60, 75], "name": "Company B"}
        ]
    }

    # 18. Dashboard (Composite)
    data["dashboard"] = [{"value": 88.5, "name": "Index"}]

    return data
