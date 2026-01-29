import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data():
    """Generates mock data for the 20 indices."""
    data = {}
    months = pd.date_range(start="2023-01-01", periods=12, freq="MS").strftime("%Y-%m")

    # 1. Traffic (Area)
    base = 100
    data["traffic"] = pd.DataFrame({
        "date": months,
        "value": [base + i * 5 + np.random.randint(-5, 8) for i in range(12)]
    }).to_dict(orient="records")

    # 2. Operation Intensity (Dual Line)
    data["operation"] = pd.DataFrame({
        "name": months,
        "duration": np.random.randint(3000, 8000, size=12),
        "distance": np.random.randint(12000, 26000, size=12)
    }).to_dict(orient="records")

    # 3. Active Fleet (Stacked Bar)
    data["fleet"] = pd.DataFrame({
        "name": months,
        "MultiRotor": np.random.randint(800, 1400, size=12),
        "FixedWing": np.random.randint(150, 350, size=12),
        "Helicopter": np.random.randint(50, 120, size=12)
    }).to_dict(orient="records")

    # 4. Growth Momentum (Area)
    data["growth"] = pd.DataFrame({
        "date": months,
        "value": np.random.randint(-5, 18, size=12)
    }).to_dict(orient="records")

    # 5. Concentration (Pareto)
    companies = [f"Company {i}" for i in range(1, 11)]
    vols = sorted(np.random.randint(50, 500, size=10), reverse=True)
    data["pareto"] = pd.DataFrame({
        "name": companies,
        "volume": vols
    }).to_dict(orient="records")

    # 6. Commercial Maturity (Rose)
    user_types = ["企业用户", "个人用户", "未知用户"]
    data["rose"] = pd.DataFrame({
        "name": user_types,
        "value": [520, 260, 80]
    }).to_dict(orient="records")

    # 7. Aircraft Diversity (Treemap)
    data["treemap"] = [
        {"name": "DJI M300", "value": 400},
        {"name": "Autel Dragonfish", "value": 220},
        {"name": "XAG P100", "value": 180},
        {"name": "EHang 216", "value": 120},
        {"name": "其他", "value": 260}
    ]

    # 8. Regional Balance (Map)
    data["map"] = [
        {"name": "南山区", "value": np.random.randint(20, 100)},
        {"name": "福田区", "value": np.random.randint(20, 100)},
        {"name": "罗湖区", "value": np.random.randint(20, 100)},
        {"name": "宝安区", "value": np.random.randint(20, 100)},
        {"name": "龙岗区", "value": np.random.randint(20, 100)},
        {"name": "盐田区", "value": np.random.randint(20, 100)}
    ]

    # 9. All-Time Operation (Polar Clock)
    hours = [f"{i}:00" for i in range(24)]
    data["polar"] = pd.DataFrame({
        "hour": hours,
        "value": np.abs(np.sin(np.linspace(0, np.pi * 2, 24)) * 100 + np.random.normal(0, 8, 24)).astype(int)
    }).to_dict(orient="records")

    # 10. Seasonal Stability (Box Plot)
    data["seasonal"] = {
        "categories": list(months),
        "values": [[10, 20, 30, 45, 60] for _ in range(12)]
    }

    # 11. Networked Hub (Graph)
    regions = ["宝安区", "南山区", "福田区", "龙岗区", "罗湖区"]
    hub_values = [88, 72, 65, 58, 40]
    data["hub"] = {
        "categories": [
            {"name": "核心枢纽"},
            {"name": "区域枢纽"},
            {"name": "末端节点"}
        ],
        "nodes": [
            {"name": "宝安区", "value": 88, "symbolSize": 46, "category": 0},
            {"name": "南山区", "value": 76, "symbolSize": 40, "category": 0},
            {"name": "福田区", "value": 62, "symbolSize": 34, "category": 1},
            {"name": "龙岗区", "value": 54, "symbolSize": 30, "category": 1},
            {"name": "罗湖区", "value": 38, "symbolSize": 24, "category": 2}
        ],
        "links": [
            {"source": "宝安区", "target": "南山区", "value": 45},
            {"source": "南山区", "target": "福田区", "value": 28},
            {"source": "宝安区", "target": "龙岗区", "value": 22},
            {"source": "福田区", "target": "罗湖区", "value": 16},
            {"source": "龙岗区", "target": "罗湖区", "value": 12}
        ]
    }

    # 12. Per-Unit Efficiency (Gauge)
    data["gauge"] = [{"value": 78, "name": "Efficiency"}]

    # 13. Long-Endurance (Funnel)
    data["funnel"] = [
        {"value": 1200, "name": "<10m"},
        {"value": 900, "name": "10-30m"},
        {"value": 400, "name": "30-60m"},
        {"value": 150, "name": ">60m"}
    ]

    # 14. Wide-Area Coverage (Histogram)
    data["histogram"] = pd.DataFrame({
        "name": ["0-1km", "1-5km", "5-10km", "10-20km", "20-50km", ">50km"],
        "value": np.random.randint(10, 120, size=6)
    }).to_dict(orient="records")

    # 15. Task Completion Quality (Control Chart)
    data["quality"] = {
        "latestTqi": 92.3,
        # Trajectory deviation data (24 hours)
        "trajData": [
            {"time": "00:00", "deviation": 0.08, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "02:00", "deviation": -0.05, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "04:00", "deviation": 0.12, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "06:00", "deviation": 0.15, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "08:00", "deviation": 0.22, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "10:00", "deviation": 0.18, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "12:00", "deviation": 0.28, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},  # Out of control
            {"time": "14:00", "deviation": 0.20, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "16:00", "deviation": 0.10, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "18:00", "deviation": 0.05, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "20:00", "deviation": -0.03, "mean": 0.0, "ucl": 0.25, "lcl": -0.25},
            {"time": "22:00", "deviation": 0.02, "mean": 0.0, "ucl": 0.25, "lcl": -0.25}
        ],
        # TQI history (30 days)
        "tqiHistory": [
            {"time": "01-01", "tqi": 88.5, "mean": 90, "ucl": 98, "lcl": 75},
            {"time": "01-05", "tqi": 89.2, "mean": 90, "ucl": 98, "lcl": 75},
            {"time": "01-08", "tqi": 91.0, "mean": 90, "ucl": 98, "lcl": 75},
            {"time": "01-12", "tqi": 90.5, "mean": 90, "ucl": 98, "lcl": 75},
            {"time": "01-15", "tqi": 92.3, "mean": 90, "ucl": 98, "lcl": 75},
            {"time": "01-18", "tqi": 93.1, "mean": 90, "ucl": 98, "lcl": 75},
            {"time": "01-22", "tqi": 91.8, "mean": 90, "ucl": 98, "lcl": 75},
            {"time": "01-25", "tqi": 92.5, "mean": 90, "ucl": 98, "lcl": 75},
            {"time": "01-27", "tqi": 92.3, "mean": 90, "ucl": 98, "lcl": 75}
        ],
        # Plan vs Actual (30 days)
        "planActual": [
            {"time": "01-01", "actual": 445, "planned": 500},
            {"time": "01-05", "actual": 468, "planned": 520},
            {"time": "01-08", "actual": 520, "planned": 560},
            {"time": "01-12", "actual": 485, "planned": 530},
            {"time": "01-15", "actual": 540, "planned": 580},
            {"time": "01-18", "actual": 565, "planned": 600},
            {"time": "01-22", "actual": 498, "planned": 540},
            {"time": "01-25", "actual": 525, "planned": 560},
            {"time": "01-27", "actual": 510, "planned": 550}
        ]
    }

    # 16. Micro Circulation (Chord)
    data["chord"] = {
        "nodes": [{"name": "南山区"}, {"name": "福田区"}, {"name": "宝安区"}, {"name": "龙岗区"}],
        "links": [
            {"source": "南山区", "target": "福田区", "value": 50},
            {"source": "福田区", "target": "宝安区", "value": 40},
            {"source": "宝安区", "target": "龙岗区", "value": 30},
            {"source": "龙岗区", "target": "南山区", "value": 20}
        ]
    }

    # 17. Airspace Efficiency (Grouped Bar)
    # Generate structured data matching web format for grouped bar visualization
    districts = ['宝安区', '南山区', '福田区', '龙岗区', '罗湖区', '盐田区']
    altitudes = ['0-50m', '50-100m', '100-150m', '150-200m', '200-250m', '250-300m', '300m+']
    
    # Generate data in format: [altitude_idx, district_idx, value]
    airspace_data = []
    for alt_idx in range(len(altitudes)):
        for dist_idx in range(len(districts)):
            # Higher values for mid-range altitudes (100-150m), decreasing for others
            if alt_idx == 2:  # 100-150m
                base_value = 1200
            elif alt_idx == 1:  # 50-100m
                base_value = 850
            elif alt_idx == 3:  # 150-200m
                base_value = 680
            else:
                base_value = 300
            
            # Vary by district (higher activity in first few districts)
            district_factor = 1.0 - (dist_idx * 0.15)
            value = int(base_value * district_factor * (0.8 + np.random.random() * 0.4))
            airspace_data.append([alt_idx, dist_idx, value])
    
    data["airspace"] = {
        "districts": districts,
        "altitudes": altitudes,
        "data": airspace_data
    }

    # 18. Calendar Heatmap
    cal_dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    data["calendar"] = [[d.strftime("%Y-%m-%d"), np.random.randint(100, 1000)] for d in cal_dates]

    # 19. Night Economy (Wave)
    night_hours = [f"{i}:00" for i in range(19, 25)] + [f"{i}:00" for i in range(0, 7)]
    data["night"] = pd.DataFrame({
        "hour": night_hours,
        "value": np.random.randint(10, 120, size=len(night_hours))
    }).to_dict(orient="records")

    # 20. Leading Entity (Radar)
    data["radar"] = {
        "indicator": [
            {"name": "长航时", "max": 100},
            {"name": "长里程", "max": 100},
            {"name": "夜间", "max": 100},
            {"name": "航程均值", "max": 100},
            {"name": "时长均值", "max": 100}
        ],
        "data": [
            {"value": [80, 90, 70, 85, 95], "name": "Company A"},
            {"value": [70, 75, 88, 60, 72], "name": "Company B"}
        ]
    }

    return data
