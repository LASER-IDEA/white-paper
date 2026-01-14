import pandas as pd
import numpy as np
import json
from datetime import datetime

def reconstruct_streamlit_data(ts_data):
    """
    Reconstructs the dictionary required by charts_lib from the list of MetricData objects (ts_data).
    """
    streamlit_data = {}

    # Map ID to key
    # IDs are "01", "02"... etc.
    # We need to match what streamlit_app.py uses:
    # "traffic", "operation", "fleet", "pareto", "rose", "treemap", "map",
    # "polar", "calendar", "night", "chord", "seasonal", "gauge", "funnel",
    # "histogram", "radar", "airspace", "dashboard"

    id_map = {
        "01": "traffic",
        "02": "operation", # Note: TS data for 02 is Monthly, Streamlit original was Region.
                           # Charts lib operation_dual_line expects 'name' (regions usually), 'duration', 'distance'.
                           # data_processor.py 'process_csv' sets 'operation' as Region stats.
                           # BUT 'ts_data' set it as Monthly stats.
                           # This creates a conflict if we reconstruct strictly from TS data.
                           # To support "View", TS data needs to contain compatible data.
                           # Let's check: process_csv sets ts_data[1].chartData = monthly_ops.
                           # streamlit_data['operation'] = region_stats.
                           # If we reload from JSON, we get monthly stats.
                           # Can operation_dual_line handle monthly stats? Yes, as long as it has 'name', 'duration', 'distance'.
                           # It will just show Months on X-axis instead of Regions. This is acceptable for "viewing exported data".
        "03": "fleet",
        "04": "pareto",
        "05": "rose",
        "06": "treemap",
        "07": "map",
        "08": "polar",
        "09": "seasonal", # TS data has [{name, min, q1...}], charts_lib.seasonal_boxplot expects {categories:[], values:[]}
        "10": "gauge",
        "11": "funnel",
        "12": "histogram",
        "13": "chord", # TS data: [{x, y, value}]. charts_lib expects {nodes: [], links: []}
        "14": "airspace",
        "15": "calendar", # TS data: [{date, value}]. charts_lib expects [[date, value], ...]
        "16": "night",
        "17": "radar", # TS data: [{subject, fullMark, A, B}]. charts_lib expects {indicator: [], data: []}
        "18": "dashboard"
    }

    metric_dict = {m['id']: m for m in ts_data}

    for mid, key in id_map.items():
        if mid not in metric_dict:
            continue

        m_data = metric_dict[mid]['chartData']

        # Handle format conversions
        if key == "seasonal":
            # Convert TS [{name, min, q1...}] back to {categories: [], values: []}
            cats = [d['name'] for d in m_data]
            vals = [[d['min'], d['q1'], d['median'], d['q3'], d['max']] for d in m_data]
            streamlit_data[key] = {"categories": cats, "values": vals}

        elif key == "chord":
            # Convert TS [{x, y, value}] back to {nodes: [], links: []}
            links = [{"source": d['x'], "target": d['y'], "value": d['value']} for d in m_data]
            # Extract unique nodes
            node_names = set([d['x'] for d in m_data] + [d['y'] for d in m_data])
            nodes = [{"name": n} for n in node_names]
            streamlit_data[key] = {"nodes": nodes, "links": links}

        elif key == "calendar":
            # Convert TS [{date, value}] back to [[date, value]]
            streamlit_data[key] = [[d['date'], d['value']] for d in m_data]

        elif key == "radar":
            # Convert TS [{subject, fullMark, EntA: val, EntB: val}] back to {indicator: [], data: []}
            # Need to identify entity names.
            if not m_data:
                streamlit_data[key] = {"indicator": [], "data": []}
                continue

            first = m_data[0]
            # Keys that are not subject or fullMark
            entities = [k for k in first.keys() if k not in ['subject', 'fullMark']]

            indicators = [{"name": d['subject'], "max": d.get('fullMark', 100)} for d in m_data]

            data_list = []
            for ent in entities:
                vals = [d[ent] for d in m_data]
                data_list.append({"name": ent, "value": vals})

            streamlit_data[key] = {"indicator": indicators, "data": data_list}

        else:
            # Direct copy for others (Area, Bar, etc.)
            streamlit_data[key] = m_data

    return streamlit_data

def process_csv(df):
    """
    Process the uploaded CSV file and generate data for Streamlit and TypeScript export.
    Assumes df has columns (or Chinese equivalents):
    - date (YYYY-MM-DD)
    - time (HH:MM:SS)
    - region
    - duration (minutes)
    - distance (km)
    - aircraft_type
    - aircraft_model
    - entity (Company Name)
    - purpose
    - sn (Serial Number)
    - altitude (m)
    - start_region
    - end_region
    """

    # 1. Standardization & Validation
    # Map Chinese columns to English if present
    column_map = {
        "日期": "date",
        "时间": "time",
        "区域": "region",
        "行政区": "region",
        "时长": "duration",
        "飞行时长": "duration",
        "里程": "distance",
        "飞行里程": "distance",
        "企业": "entity",
        "企业名称": "entity",
        "航空器类型": "aircraft_type",
        "机型": "aircraft_model",
        "用途": "purpose",
        "SN": "sn",
        "sn": "sn",
        "高度": "altitude",
        "飞行高度": "altitude",
        "起始区域": "start_region",
        "结束区域": "end_region"
    }

    # Normalize current columns
    df.columns = [c.strip() for c in df.columns]

    # Rename columns based on map
    new_columns = {}
    for col in df.columns:
        if col in column_map:
            new_columns[col] = column_map[col]
        # Also handle already normalized English columns (lowercase)
        elif col.lower() in column_map.values():
             # Find which key maps to this value to ensure consistency?
             # No, just standardizing to the value.
             pass

    df = df.rename(columns=new_columns)
    # Lowercase all remaining columns for safety
    df.columns = [c.lower() for c in df.columns]

    required_cols = ['date', 'region', 'duration', 'distance', 'entity']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col} (or equivalent Chinese column)")

    # Convert date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # Drop rows with invalid dates
    df = df.dropna(subset=['date'])

    df['month'] = df['date'].dt.strftime('%Y-%m')
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')

    # Handle Time
    if 'time' in df.columns:
        # Try to parse time, handle errors
        df['hour'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.hour
        df['hour'] = df['hour'].fillna(12).astype(int) # Default to noon if missing
    else:
        df['hour'] = 12

    # Handle other optional columns
    if 'aircraft_type' not in df.columns: df['aircraft_type'] = 'Unknown'
    if 'aircraft_model' not in df.columns: df['aircraft_model'] = 'Unknown'
    if 'purpose' not in df.columns: df['purpose'] = 'Other'
    if 'sn' not in df.columns: df['sn'] = df.index.astype(str)
    if 'altitude' not in df.columns: df['altitude'] = 100
    if 'start_region' not in df.columns: df['start_region'] = df['region']
    if 'end_region' not in df.columns: df['end_region'] = df['region']

    # --- Compute Indicators for Streamlit (matching data_factory.py) ---
    streamlit_data = {}

    # 1. Traffic (Daily Sorties)
    daily_counts = df.groupby('date_str').size().reset_index(name='value')
    streamlit_data['traffic'] = daily_counts.rename(columns={'date_str': 'date'}).to_dict(orient='records')

    # 2. Operation (Region-based duration/distance - matching current Streamlit usage)
    # data_factory uses "name" for region
    region_stats = df.groupby('region')[['duration', 'distance']].sum().reset_index()
    streamlit_data['operation'] = region_stats.rename(columns={'region': 'name'}).to_dict(orient='records')

    # 3. Fleet (Stacked Bar)
    # data_factory uses Q1, Q2.. and types as columns.
    # We will aggregate by Month for x-axis
    fleet_pivot = df.pivot_table(index='month', columns='aircraft_type', values='sn', aggfunc='count', fill_value=0).reset_index()
    fleet_pivot = fleet_pivot.rename(columns={'month': 'name'})
    # Ensure common columns exist
    for col in ['MultiRotor', 'FixedWing', 'Helicopter']:
        if col not in fleet_pivot.columns:
            fleet_pivot[col] = 0
    streamlit_data['fleet'] = fleet_pivot.to_dict(orient='records')

    # 4. Pareto (Concentration - Top Companies)
    company_vols = df.groupby('entity').size().reset_index(name='volume').sort_values('volume', ascending=False)
    # Top 50 calculation for Metrics
    top_50_vol = company_vols.head(50)['volume'].sum()
    total_vol = len(df)
    cr50_pct = round(top_50_vol / total_vol * 100, 1) if total_vol > 0 else 0

    # Top 10 for display chart
    streamlit_data['pareto'] = company_vols.head(10).rename(columns={'entity': 'name'}).to_dict(orient='records')

    # 5. Rose (Commercial Maturity - Sectors)
    sector_counts = df.groupby('purpose').size().reset_index(name='value')
    streamlit_data['rose'] = sector_counts.rename(columns={'purpose': 'name'}).to_dict(orient='records')

    # 6. Treemap (Diversity - Models)
    model_counts = df.groupby('aircraft_model').size().reset_index(name='value')
    streamlit_data['treemap'] = model_counts.rename(columns={'aircraft_model': 'name'}).to_dict(orient='records')

    # 7. Map (Regional Balance)
    # data_factory: name=Region, value=Density
    region_counts = df.groupby('region').size().reset_index(name='value')
    streamlit_data['map'] = region_counts.rename(columns={'region': 'name'}).to_dict(orient='records')

    # 8. Polar (All Weather - Hourly)
    hour_counts = df.groupby('hour').size().reset_index(name='value')
    # Fill missing hours
    full_hours = pd.DataFrame({'hour': range(24)})
    hour_counts = full_hours.merge(hour_counts, on='hour', how='left').fillna(0)
    hour_counts['hour_str'] = hour_counts['hour'].apply(lambda x: f"{x}:00")
    streamlit_data['polar'] = hour_counts[['hour_str', 'value']].rename(columns={'hour_str': 'hour'}).to_dict(orient='records')

    # 9. Seasonal (Boxplot)
    # Group dates by quarter
    df['quarter'] = df['date'].dt.quarter
    quarters = {1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'}
    seasonal_data = {'categories': [], 'values': []}
    for q in sorted(df['quarter'].dropna().unique()):
        q_data = df[df['quarter'] == q].groupby('date_str').size()
        if not q_data.empty:
            seasonal_data['categories'].append(quarters[int(q)])
            seasonal_data['values'].append([
                int(q_data.min()), int(q_data.quantile(0.25)), int(q_data.median()), int(q_data.quantile(0.75)), int(q_data.max())
            ])
    if not seasonal_data['categories']:
         seasonal_data = {"categories": ["No Data"], "values": [[0,0,0,0,0]]}
    streamlit_data['seasonal'] = seasonal_data

    # 10. Gauge (Efficiency)
    # Avg sorties per SN
    unique_sn = df['sn'].nunique()
    total_flights = len(df)
    efficiency = round(total_flights / unique_sn, 1) if unique_sn > 0 else 0
    # Normalize to 0-100 for gauge? Or just pass value. data_factory passes 85.
    # Let's cap at 100 for visual or scale it.
    # But chart just shows value.
    streamlit_data['gauge'] = [{"value": efficiency, "name": "Efficiency"}]

    # 11. Funnel (Endurance - Duration Intervals)
    # data_factory used "Plan", "Takeoff"... but Charts funnel just shows name/value.
    # We will use duration intervals: <10, 10-30, 30-60, >60
    bins = [0, 10, 30, 60, 9999]
    labels = ['<10m', '10-30m', '30-60m', '>60m']
    df['dur_bin'] = pd.cut(df['duration'], bins=bins, labels=labels)
    funnel_df = df.groupby('dur_bin', observed=False).size().reset_index(name='value')
    streamlit_data['funnel'] = funnel_df.rename(columns={'dur_bin': 'name'}).to_dict(orient='records')

    # 12. Histogram (Wide Area - Distance Intervals)
    bins_dist = [0, 1, 5, 10, 20, 50, 9999]
    labels_dist = ['0-1km', '1-5km', '5-10km', '10-20km', '20-50km', '>50km']
    df['dist_bin'] = pd.cut(df['distance'], bins=bins_dist, labels=labels_dist)
    hist_df = df.groupby('dist_bin', observed=False).size().reset_index(name='value')
    streamlit_data['histogram'] = hist_df.rename(columns={'dist_bin': 'name'}).to_dict(orient='records')

    # 13. Chord (Micro Circulation - Region Flows)
    chord_flows = df.groupby(['start_region', 'end_region']).size().reset_index(name='value')
    # Top 5 regions
    top_regions = df['region'].value_counts().head(5).index.tolist()
    # Filter for top regions to avoid clutter
    chord_flows = chord_flows[chord_flows['start_region'].isin(top_regions) & chord_flows['end_region'].isin(top_regions)]
    nodes = [{"name": r} for r in top_regions]
    links = chord_flows.rename(columns={'start_region': 'source', 'end_region': 'target'}).to_dict(orient='records')
    streamlit_data['chord'] = {"nodes": nodes, "links": links}

    # 14. Airspace (Vertical - Altitude Intervals)
    bins_alt = [0, 120, 300, 9999]
    labels_alt = ['<120m', '120-300m', '>300m']
    df['alt_bin'] = pd.cut(df['altitude'], bins=bins_alt, labels=labels_alt)
    alt_df = df.groupby('alt_bin', observed=False).size().reset_index(name='value')
    streamlit_data['airspace'] = alt_df.rename(columns={'alt_bin': 'name'}).to_dict(orient='records')

    # 15. Calendar (Heatmap)
    # list of [date_str, value]
    cal_data = df.groupby('date_str').size().reset_index(name='value')
    streamlit_data['calendar'] = cal_data.values.tolist()

    # 16. Night (Night Economy)
    # Hours 18-29 (next day 5am).
    # Simplified: Just take hours 18-23 and 0-6.
    night_mask = (df['hour'] >= 18) | (df['hour'] <= 6)
    night_df = df[night_mask].groupby('hour').size().reset_index(name='value')
    # Format hours as strings for x-axis
    night_df['hour'] = night_df['hour'].astype(str) + ":00"
    streamlit_data['night'] = night_df.to_dict(orient='records')

    # 17. Radar (Leading Entity)
    # Compare top 2 entities on metrics: Distance, Duration, Count, Altitude, Speed (Distance/Duration)
    top_2_entities = df['entity'].value_counts().head(2).index.tolist()
    radar_data = {"indicator": [
        {"name": "Volume", "max": 100},
        {"name": "Total Dist", "max": 100},
        {"name": "Total Dur", "max": 100},
        {"name": "Avg Alt", "max": 100},
        {"name": "Avg Dist", "max": 100}
    ], "data": []}

    # Normalize for radar
    for ent in top_2_entities:
        ent_data = df[df['entity'] == ent]
        stats = [
            len(ent_data),
            ent_data['distance'].sum(),
            ent_data['duration'].sum(),
            ent_data['altitude'].mean(),
            ent_data['distance'].mean()
        ]
        radar_data["data"].append({"value": stats, "name": ent})

    # Scale values to 0-100 relative to max of both
    if len(radar_data['data']) > 0:
        for i in range(5):
            vals = [d['value'][i] for d in radar_data['data']]
            max_val = max(vals) if vals else 1
            if max_val == 0: max_val = 1
            for d in radar_data['data']:
                d['value'][i] = round((d['value'][i] / max_val) * 100, 1)

    streamlit_data['radar'] = radar_data

    # 18. Dashboard (Score)
    # Dummy score
    streamlit_data['dashboard'] = [{"value": 92.5, "name": "Index"}]


    # --- Compute Data for TypeScript Export (MetricData[]) ---
    # We construct a list of objects matching types.MetricData
    # Note: Enum 'Dimension' values are strings in Python

    ts_data = []

    # Helper to create metric object
    def create_metric(id_, title, subtitle, dim, val, unit, chart_type, chart_data):
        return {
            "id": id_,
            "title": title,
            "subtitle": subtitle,
            "dimension": dim,
            "value": val,
            "unit": unit,
            "trend": 0.0,
            "definition": "Computed from CSV",
            "insight": "Data generated from uploaded CSV.",
            "suggestion": "Analyze the trends.",
            "chartType": chart_type,
            "chartData": chart_data,
            "keyMetrics": []
        }

    # 1. Scale & Growth
    # Traffic
    ts_data.append(create_metric(
        "01", "低空交通流量指数", "日均飞行架次趋势", "规模与增长",
        len(df), "架次", "Area",
        streamlit_data['traffic']
    ))
    # Operation
    # For TS export, we use Monthly aggregation to match utils/mockData.ts structure
    monthly_ops = df.groupby('month')[['duration', 'distance']].sum().reset_index()
    monthly_ops = monthly_ops.rename(columns={'month': 'name'}).to_dict(orient='records')
    ts_data.append(create_metric(
        "02", "运行强度指数", "飞行时长与里程关联度", "规模与增长",
        round(df['duration'].sum()/60, 1), "小时", "DualLine",
        monthly_ops
    ))
    # Fleet
    ts_data.append(create_metric(
        "03", "活跃机队规模指数", "活跃航空器分类统计", "规模与增长",
        df['sn'].nunique(), "活跃架数", "StackedBar",
        streamlit_data['fleet']
    ))

    # 2. Structure & Entity
    # Pareto
    # Update value to show CR50
    ts_data.append(create_metric(
        "04", "市场集中度指数 (CR50)", "前50强企业市场份额", "结构与主体",
        f"CR50={cr50_pct}%", "", "Pareto",
        streamlit_data['pareto']
    ))
    # Rose
    ts_data.append(create_metric(
        "05", "商业成熟度指数", "用户类型分布", "结构与主体",
        len(sector_counts), "Types", "Rose",
        streamlit_data['rose']
    ))
    # Treemap
    ts_data.append(create_metric(
        "06", "机队多样性指数", "航空器型号分布", "结构与主体",
        len(model_counts), "Models", "Treemap",
        streamlit_data['treemap']
    ))

    # 3. Time & Space
    # Map
    ts_data.append(create_metric(
        "07", "区域平衡指数", "地理飞行密度平衡", "时空特征",
        len(region_counts), "Regions", "Map",
        streamlit_data['map']
    ))
    # Polar
    ts_data.append(create_metric(
        "08", "全天候运行指数", "24小时飞行分布", "时空特征",
        "", "", "Polar",
        streamlit_data['polar']
    ))
    # Seasonal (Boxplot)
    ts_data.append(create_metric(
        "09", "季节稳定性指数", "月度飞行波动性", "时空特征",
        "", "", "BoxPlot",
        streamlit_data['seasonal'] # Note: TS expects different BoxPlot format probably, but we'll use this
    ))
    # TS BoxPlot format in utils/mockData: { name: string, min, avg, max } - ours is {categories, values}
    # Let's fix it for TS
    ts_boxplot = []
    for i, cat in enumerate(seasonal_data['categories']):
        vals = seasonal_data['values'][i]
        # Calculate Average (vals has min, q1, median, q3, max)
        q_data = df[df['quarter'] == int(cat.replace('Q',''))].groupby('date_str').size() if cat != "No Data" else pd.Series([0])
        avg_val = int(q_data.mean()) if not q_data.empty else 0

        ts_boxplot.append({
            "name": cat, "min": vals[0], "q1": vals[1], "median": vals[2], "q3": vals[3], "max": vals[4], "avg": avg_val
        })
    ts_data[-1]['chartData'] = ts_boxplot

    # 4. Efficiency & Quality
    # Gauge
    ts_data.append(create_metric(
        "10", "单机效率指数", "活跃航空器人均架次", "效率与质量",
        efficiency, "架次/年", "Gauge",
        streamlit_data['gauge']
    ))
    # Funnel
    ts_data.append(create_metric(
        "11", "长航时任务指数", "高价值任务比例", "效率与质量",
        "", "", "Funnel",
        streamlit_data['funnel']
    ))
    # Histogram
    ts_data.append(create_metric(
        "12", "广域覆盖指数", "飞行航程分布", "效率与质量",
        round(df['distance'].mean(), 1), "km", "Histogram",
        streamlit_data['histogram']
    ))

    # 5. Innovation & Integration
    # Chord
    # TS Chord format: array of links? utils/mockData: {x, y, value}
    ts_chord = []
    for link in links:
        ts_chord.append({"x": link['source'], "y": link['target'], "value": link['value']})
    ts_data.append(create_metric(
        "13", "城市微循环指数", "跨区连通性", "创新与融合",
        len(links), "Conn", "Chord",
        ts_chord
    ))
    # Airspace (3DBar -> Bar)
    ts_data.append(create_metric(
        "14", "立体空域效率", "垂直空域利用率", "创新与融合",
        "", "", "3DBar",
        streamlit_data['airspace']
    ))
    # Calendar
    # TS Calendar format: {date: 'iso', value: num}
    ts_calendar = [{"date": d[0], "value": d[1]} for d in cal_data.values.tolist()]
    ts_data.append(create_metric(
        "15", "生产/消费属性", "工作日与周末活动对比", "创新与融合",
        "", "", "Calendar",
        ts_calendar
    ))
    # Night
    ts_data.append(create_metric(
        "16", "低空夜间经济指数", "夜间飞行占比", "创新与融合",
        "", "", "Wave",
        streamlit_data['night']
    ))
    # Radar
    # TS Radar format: [{subject, A, B, fullMark}]
    # We have streamlit format: {indicator: [], data: [{value: [], name}]}
    # Convert to TS format
    ts_radar = []
    indicators = streamlit_data['radar']['indicator']
    data_points = streamlit_data['radar']['data']
    if len(data_points) >= 2:
        for i, ind in enumerate(indicators):
            item = {"subject": ind['name'], "fullMark": 100}
            item[data_points[0]['name']] = data_points[0]['value'][i]
            item[data_points[1]['name']] = data_points[1]['value'][i]
            ts_radar.append(item)

    ts_data.append(create_metric(
        "17", "龙头主体影响力指数", "头部企业技术领导力", "创新与融合",
        "", "", "Radar",
        ts_radar
    ))

    # Dashboard
    ts_data.append(create_metric(
        "18", "低空综合繁荣度", "LA-PI (综合指数)", "创新与融合",
        92.5, "分", "Dashboard",
        [{"name": "得分", "value": 92.5}]
    ))

    return streamlit_data, ts_data
