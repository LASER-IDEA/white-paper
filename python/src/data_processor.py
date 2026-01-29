import pandas as pd
import numpy as np
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

def reconstruct_streamlit_data(ts_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Reconstructs the dictionary required by charts_lib from the list of MetricData objects (ts_data).
    
    Args:
        ts_data: List of metric data dictionaries with 'id' and 'chartData' keys
        
    Returns:
        Dictionary mapping chart keys to their data
    """
    streamlit_data: Dict[str, Any] = {}

    # Map ID to key
    # IDs are "01", "02"... etc.
    # We need to match what streamlit_app.py uses:
    # "traffic", "operation", "fleet", "pareto", "rose", "treemap", "map",
    # "polar", "calendar", "night", "chord", "seasonal", "gauge", "funnel",
    # "histogram", "radar", "airspace", "dashboard"

    id_map = {
        "01": "traffic",
        "02": "operation",
        "03": "fleet",
        "04": "growth",
        "05": "pareto",
        "06": "rose",
        "07": "treemap",
        "08": "map",
        "09": "polar",
        "10": "seasonal",  # TS data has [{name, min, q1...}], charts_lib.seasonal_boxplot expects {categories:[], values:[]}
        "11": "hub",
        "12": "gauge",
        "13": "funnel",
        "14": "histogram",
        "15": "quality",
        "16": "chord",     # TS data: [{x, y, value}]. charts_lib expects {nodes: [], links: []}
        "17": "airspace",
        "18": "calendar",  # TS data: [{date, value}]. charts_lib expects [[date, value], ...]
        "19": "night",
        "20": "radar"      # TS data: [{subject, fullMark, A, B}]. charts_lib expects {indicator: [], data: []}
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

        elif key == "hub":
            # Convert TS graph {nodes, links, categories} to bar data for Streamlit
            if isinstance(m_data, dict) and "nodes" in m_data:
                streamlit_data[key] = [
                    {"name": n.get("name", ""), "value": n.get("value", n.get("symbolSize", 0))}
                    for n in m_data.get("nodes", [])
                ]
            else:
                streamlit_data[key] = m_data

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
        "企业ID": "entity_id",
        "企业编号": "entity_id",
        "航空器类型": "aircraft_type",
        "航空器类别": "aircraft_type",
        "机型": "aircraft_model",
        "用途": "purpose",
        "用户类型": "user_type",
        "SN": "sn",
        "sn": "sn",
        "高度": "altitude",
        "飞行高度": "altitude",
        "起始区域": "start_region",
        "结束区域": "end_region",
        "是否节假日": "is_holiday",
        "是否有效": "is_effective",
        "是否计划": "is_planned"
    }

    df.columns = [c.strip() for c in df.columns]
    new_columns = {}
    for col in df.columns:
        if col in column_map:
            new_columns[col] = column_map[col]
    df = df.rename(columns=new_columns)
    df.columns = [c.lower() for c in df.columns]

    required_cols = ['date', 'region', 'duration', 'distance', 'entity']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col} (or equivalent Chinese column)")

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    df['month'] = df['date'].dt.strftime('%Y-%m')
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
    df['weekday'] = df['date'].dt.weekday
    df['is_weekend'] = df['weekday'] >= 5

    if 'time' in df.columns:
        df['hour'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.hour
        df['hour'] = df['hour'].fillna(12).astype(int)
    else:
        df['hour'] = 12

    if 'aircraft_type' not in df.columns: df['aircraft_type'] = 'Unknown'
    if 'aircraft_model' not in df.columns: df['aircraft_model'] = 'Unknown'
    if 'purpose' not in df.columns: df['purpose'] = 'Other'
    if 'user_type' not in df.columns: df['user_type'] = '未知用户'
    if 'entity_id' not in df.columns:
        codes = pd.factorize(df['entity'])[0] + 1
        df['entity_id'] = [f"ENT{c:04d}" for c in codes]
    if 'sn' not in df.columns: df['sn'] = df.index.astype(str)
    if 'altitude' not in df.columns: df['altitude'] = 100
    if 'start_region' not in df.columns: df['start_region'] = df['region']
    if 'end_region' not in df.columns: df['end_region'] = df['region']
    if 'is_holiday' not in df.columns: df['is_holiday'] = False
    if 'is_effective' not in df.columns: df['is_effective'] = True
    if 'is_planned' not in df.columns: df['is_planned'] = True

    def normalize_bool(series, default=False):
        if series is None:
            return pd.Series([default] * len(df))
        if series.dtype == bool:
            return series.fillna(default)
        return series.fillna(default).astype(str).str.lower().isin(
            ['1', 'true', 'yes', 'y', 't', '是']
        )

    df['is_holiday'] = normalize_bool(df['is_holiday'], default=False)
    df['is_effective'] = normalize_bool(df['is_effective'], default=True)
    df['is_planned'] = normalize_bool(df['is_planned'], default=True)
    df['is_workday'] = ~(df['is_weekend'] | df['is_holiday'])

    region_map = {
        'Nanshan': '南山区',
        'Futian': '福田区',
        'Luohu': '罗湖区',
        'Baoan': '宝安区',
        'Longgang': '龙岗区',
        'Yantian': '盐田区',
        'Longhua': '龙华区',
        'Pingshan': '坪山区',
        'Guangming': '光明区',
        'Dapeng': '大鹏新区',
    }
    df['region'] = df['region'].map(region_map).fillna(df['region'])
    df['start_region'] = df['start_region'].map(region_map).fillna(df['start_region'])
    df['end_region'] = df['end_region'].map(region_map).fillna(df['end_region'])

    def normalize_user_type(val):
        if pd.isna(val):
            return '未知用户'
        s = str(val)
        if '企业' in s or '公司' in s:
            return '企业用户'
        if '个人' in s:
            return '个人用户'
        if '未知' in s:
            return '未知用户'
        return s

    df['user_type'] = df['user_type'].apply(normalize_user_type)

    def calc_gini(values):
        vals = np.array(values, dtype=float)
        if vals.size == 0 or np.all(vals == 0):
            return 0.0
        vals = np.sort(vals)
        n = vals.size
        index = np.arange(1, n + 1)
        return (np.sum((2 * index - n - 1) * vals)) / (n * np.sum(vals))

    def calc_entropy(values):
        vals = np.array(values, dtype=float)
        total = vals.sum()
        if total <= 0:
            return 0.0
        probs = vals / total
        probs = probs[probs > 0]
        return float(-(probs * np.log(probs)).sum())

    streamlit_data = {}

    # --- 1. 低空交通流量指数 ---
    daily_counts = df.groupby('date_str').size().reset_index(name='value')
    daily_counts['month'] = pd.to_datetime(daily_counts['date_str']).dt.strftime('%Y-%m')
    monthly_avg = daily_counts.groupby('month')['value'].mean().reset_index(name='avg')
    base_avg = monthly_avg['avg'].iloc[0] if not monthly_avg.empty else 1
    traffic_index = monthly_avg.copy()
    traffic_index['value'] = (traffic_index['avg'] / base_avg * 100).round(1)
    streamlit_data['traffic'] = traffic_index.rename(columns={'month': 'date'})[['date', 'value']].to_dict(orient='records')

    # --- 2. 低空作业强度指数 ---
    monthly_ops = df.groupby('month')[['duration', 'distance']].sum().reset_index()
    monthly_ops['duration'] = (monthly_ops['duration'] / 60).round(1)
    streamlit_data['operation'] = monthly_ops.rename(columns={'month': 'name'}).to_dict(orient='records')
    base_dur = monthly_ops['duration'].iloc[0] if not monthly_ops.empty else 1
    base_dist = monthly_ops['distance'].iloc[0] if not monthly_ops.empty else 1
    op_index_series = (
        0.5 * (monthly_ops['duration'] / max(base_dur, 1e-6)) +
        0.5 * (monthly_ops['distance'] / max(base_dist, 1e-6))
    ) * 100

    # --- 3. 活跃运力规模指数 ---
    fleet_pivot = df.pivot_table(
        index='month',
        columns='aircraft_type',
        values='sn',
        aggfunc=pd.Series.nunique,
        fill_value=0
    ).reset_index()
    fleet_pivot = fleet_pivot.rename(columns={'month': 'name'})
    for col in ['MultiRotor', 'FixedWing', 'Helicopter']:
        if col not in fleet_pivot.columns:
            fleet_pivot[col] = 0
    streamlit_data['fleet'] = fleet_pivot.to_dict(orient='records')

    # --- 4. 增长动能指数 ---
    monthly_total = df.groupby('month').size().reset_index(name='total')
    monthly_total['growth_rate'] = (monthly_total['total'].pct_change().fillna(0) * 100).round(1)
    streamlit_data['growth'] = monthly_total.rename(columns={'month': 'date', 'growth_rate': 'value'})[['date', 'value']].to_dict(orient='records')

    # --- 5. 市场集中度指数 (CR50) ---
    company_vols = df.groupby('entity').size().reset_index(name='volume').sort_values('volume', ascending=False)
    top_50_vol = company_vols.head(50)['volume'].sum()
    total_vol = len(df)
    cr50_pct = round(top_50_vol / total_vol * 100, 1) if total_vol > 0 else 0
    streamlit_data['pareto'] = company_vols.head(10).rename(columns={'entity': 'name'}).to_dict(orient='records')

    # --- 6. 商业化成熟指数 ---
    user_counts = df.groupby('user_type').size().reset_index(name='value')
    streamlit_data['rose'] = user_counts.rename(columns={'user_type': 'name'}).to_dict(orient='records')
    enterprise_cnt = user_counts[user_counts['user_type'] == '企业用户']['value'].sum()
    commercial_pct = round(enterprise_cnt / total_vol * 100, 1) if total_vol > 0 else 0

    # --- 7. 机型生态多元指数 ---
    model_counts = df.groupby('aircraft_model').size().reset_index(name='value')
    streamlit_data['treemap'] = model_counts.rename(columns={'aircraft_model': 'name'}).to_dict(orient='records')
    model_share = model_counts['value'] / model_counts['value'].sum() if not model_counts.empty else pd.Series([])
    diversity_index = round(1 - np.sum(model_share ** 2), 3) if not model_counts.empty else 0

    # --- 8. 区域发展均衡指数 ---
    region_counts = df.groupby('region').size().reset_index(name='value')
    streamlit_data['map'] = region_counts.rename(columns={'region': 'name'}).to_dict(orient='records')
    gini = calc_gini(region_counts['value'].values)
    balance_index = round(1 - gini, 3)

    # --- 9. 全时段运行指数 ---
    hour_counts = df.groupby('hour').size().reset_index(name='value')
    full_hours = pd.DataFrame({'hour': range(24)})
    hour_counts = full_hours.merge(hour_counts, on='hour', how='left').fillna(0)
    hour_counts['hour_str'] = hour_counts['hour'].apply(lambda x: f"{x}:00")
    streamlit_data['polar'] = hour_counts[['hour_str', 'value']].rename(columns={'hour_str': 'hour'}).to_dict(orient='records')
    alltime_entropy = round(calc_entropy(hour_counts['value'].values), 3)

    # --- 10. 季候稳定性指数 ---
    seasonal_data = {'categories': [], 'values': []}
    for m in sorted(daily_counts['month'].unique()):
        m_data = daily_counts[daily_counts['month'] == m]['value']
        if not m_data.empty:
            seasonal_data['categories'].append(m)
            seasonal_data['values'].append([
                int(m_data.min()), int(m_data.quantile(0.25)), int(m_data.median()), int(m_data.quantile(0.75)), int(m_data.max())
            ])
    if not seasonal_data['categories']:
        seasonal_data = {"categories": ["No Data"], "values": [[0, 0, 0, 0, 0]]}
    streamlit_data['seasonal'] = seasonal_data
    month_stats = monthly_total['total']
    stability_index = round(1 - (month_stats.std() / month_stats.mean()), 3) if len(month_stats) > 1 and month_stats.mean() != 0 else 0

    # --- 11. 网络化枢纽指数 ---
    flows = df.groupby(['start_region', 'end_region']).size().reset_index(name='value')
    regions = pd.unique(df[['start_region', 'end_region']].values.ravel('K'))
    hub_rows = []
    for r in regions:
        out_neighbors = set(flows[flows['start_region'] == r]['end_region'].tolist())
        in_neighbors = set(flows[flows['end_region'] == r]['start_region'].tolist())
        neighbors = (out_neighbors | in_neighbors) - {r}
        degree = len(neighbors)
        flow = flows[(flows['start_region'] == r) | (flows['end_region'] == r)]['value'].sum()
        hub_rows.append({'name': r, 'degree': degree, 'flow': flow})
    hub_df = pd.DataFrame(hub_rows)
    max_degree = hub_df['degree'].max() if not hub_df.empty else 1
    max_flow = hub_df['flow'].max() if not hub_df.empty else 1
    hub_df['value'] = (0.6 * (hub_df['degree'] / max(max_degree, 1e-6)) + 0.4 * (hub_df['flow'] / max(max_flow, 1e-6))) * 100
    hub_df = hub_df.sort_values('value', ascending=False).head(10)

    # Create graph structure for visualization
    nodes = []
    for idx, row in hub_df.iterrows():
        # Categorize nodes based on hub value
        if row['value'] >= 70:
            category = 0  # Core hub
        elif row['value'] >= 50:
            category = 1  # Regional hub
        else:
            category = 2  # Terminal node

        symbol_size = max(20, min(60, int(row['value'] * 0.6)))  # Scale symbol size
        nodes.append({
            'name': row['name'],
            'value': round(row['value'], 1),
            'symbolSize': symbol_size,
            'category': category
        })

    # Filter flows to only include top hubs
    top_hubs = set(hub_df['name'].tolist())
    filtered_flows = flows[
        (flows['start_region'].isin(top_hubs)) &
        (flows['end_region'].isin(top_hubs)) &
        (flows['start_region'] != flows['end_region'])
    ]

    links = []
    for _, row in filtered_flows.iterrows():
        links.append({
            'source': row['start_region'],
            'target': row['end_region'],
            'value': int(row['value'])
        })

    streamlit_data['hub'] = {
        'nodes': nodes,
        'links': links,
        'categories': [
            {'name': '核心枢纽'},
            {'name': '区域枢纽'},
            {'name': '末端节点'}
        ]
    }
    hub_index = round(hub_df['value'].max(), 1) if not hub_df.empty else 0

    # --- 12. 单机作业效能指数 ---
    unique_sn = df['sn'].nunique()
    total_flights = len(df)
    efficiency = round(total_flights / unique_sn, 1) if unique_sn > 0 else 0
    gauge_value = min(100, efficiency)
    streamlit_data['gauge'] = [{"value": gauge_value, "name": "Efficiency"}]

    # --- 13. 长航时任务占比指数 ---
    bins = [0, 10, 30, 60, 9999]
    labels = ['<10m', '10-30m', '30-60m', '>60m']
    df['dur_bin'] = pd.cut(df['duration'], bins=bins, labels=labels)
    funnel_df = df.groupby('dur_bin', observed=False).size().reset_index(name='value')
    streamlit_data['funnel'] = funnel_df.rename(columns={'dur_bin': 'name'}).to_dict(orient='records')
    long_endurance_pct = round((df['duration'] > 30).mean() * 100, 1) if total_flights > 0 else 0

    # --- 14. 广域覆盖能力指数 ---
    bins_dist = [0, 1, 5, 10, 20, 50, 9999]
    labels_dist = ['0-1km', '1-5km', '5-10km', '10-20km', '20-50km', '>50km']
    df['dist_bin'] = pd.cut(df['distance'], bins=bins_dist, labels=labels_dist)
    hist_df = df.groupby('dist_bin', observed=False).size().reset_index(name='value')
    streamlit_data['histogram'] = hist_df.rename(columns={'dist_bin': 'name'}).to_dict(orient='records')
    bin_midpoints = [0.5, 3, 7.5, 15, 35, 60]
    dist_weights = hist_df['value'].values if not hist_df.empty else np.array([])
    coverage_index = round(
        np.sum(dist_weights * np.array(bin_midpoints)) / max(np.sum(dist_weights), 1),
        2
    ) if dist_weights.size else 0

    # --- 15. 任务完成质量指数 ---
    planned = df[df['is_planned']].shape[0]
    completed = df[df['is_planned'] & df['is_effective']].shape[0]
    completion_pct = round(completed / planned * 100, 1) if planned > 0 else 0

    # Generate control chart data
    # 1. Trajectory deviation by hour (simulated with flight duration variance)
    df['hour'] = pd.to_datetime(df['start_time']).dt.hour
    hourly_stats = df.groupby('hour')['duration'].agg(['mean', 'std']).reset_index()

    # Select 12 key hours for trajectory deviation
    key_hours = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
    traj_data = []
    for h in key_hours:
        hour_data = hourly_stats[hourly_stats['hour'] == h]
        if not hour_data.empty:
            # Normalize deviation (using std as proxy for deviation)
            deviation = hour_data['std'].values[0] / hourly_stats['std'].mean() * 0.15 if hourly_stats['std'].mean() > 0 else 0.08
        else:
            deviation = 0.08
        traj_data.append({
            'time': f'{h:02d}:00',
            'deviation': round(deviation, 2),
            'mean': 0.0,
            'ucl': 0.25,
            'lcl': -0.25
        })

    # 2. TQI history (daily completion rate trend)
    if 'date_str' in df.columns:
        daily_completion = df[df['is_planned']].groupby('date_str').apply(
            lambda x: (x['is_effective'].sum() / len(x) * 100) if len(x) > 0 else 0
        ).reset_index(name='tqi')
        daily_completion = daily_completion.sort_values('date_str').tail(9)

        tqi_history = []
        for _, row in daily_completion.iterrows():
            tqi_history.append({
                'time': row['date_str'][5:],  # MM-DD format
                'tqi': round(row['tqi'], 1),
                'mean': 90,
                'ucl': 98,
                'lcl': 75
            })
    else:
        # Fallback if no date_str
        tqi_history = [
            {'time': f'01-{i:02d}', 'tqi': round(completion_pct + np.random.uniform(-3, 3), 1),
             'mean': 90, 'ucl': 98, 'lcl': 75}
            for i in range(1, 10)
        ]

    # 3. Plan vs Actual (daily planned and actual sorties)
    if 'date_str' in df.columns:
        daily_planned = df[df['is_planned']].groupby('date_str').size().reset_index(name='planned')
        daily_actual = df[df['is_planned'] & df['is_effective']].groupby('date_str').size().reset_index(name='actual')
        plan_actual_df = pd.merge(daily_planned, daily_actual, on='date_str', how='left').fillna(0)
        plan_actual_df = plan_actual_df.sort_values('date_str').tail(9)

        plan_actual = []
        for _, row in plan_actual_df.iterrows():
            plan_actual.append({
                'time': row['date_str'][5:],  # MM-DD format
                'actual': int(row['actual']),
                'planned': int(row['planned'])
            })
    else:
        # Fallback
        plan_actual = [
            {'time': f'01-{i:02d}', 'actual': int(planned * 0.92 + np.random.randint(-20, 20)),
             'planned': int(planned + np.random.randint(-30, 30))}
            for i in range(1, 10)
        ]

    streamlit_data['quality'] = {
        'latestTqi': completion_pct,
        'trajData': traj_data,
        'tqiHistory': tqi_history,
        'planActual': plan_actual
    }

    # --- 16. 城市微循环渗透指数 ---
    cross_flows = df[df['start_region'] != df['end_region']]
    cross_ratio = cross_flows.shape[0] / total_flights if total_flights > 0 else 0
    cross_pairs = cross_flows.groupby(['start_region', 'end_region']).size().reset_index(name='value')
    pair_count = cross_pairs.shape[0]
    micro_index = round(cross_ratio * np.log1p(pair_count), 3)
    top_regions = df['region'].value_counts().head(6).index.tolist()
    chord_flows = cross_pairs[cross_pairs['start_region'].isin(top_regions) & cross_pairs['end_region'].isin(top_regions)]
    nodes = [{"name": r} for r in top_regions]
    links = chord_flows.rename(columns={'start_region': 'source', 'end_region': 'target'}).to_dict(orient='records')
    streamlit_data['chord'] = {"nodes": nodes, "links": links}

    # --- 17. 立体空域利用效能指数 ---
    bins_alt = [0, 120, 300, 600, 9999]
    labels_alt = ['<120m', '120-300m', '300-600m', '>600m']
    df['alt_bin'] = pd.cut(df['altitude'], bins=bins_alt, labels=labels_alt)
    alt_df = df.groupby('alt_bin', observed=False)['duration'].sum().reset_index(name='value')
    streamlit_data['airspace'] = alt_df.rename(columns={'alt_bin': 'name'}).to_dict(orient='records')
    airspace_entropy = round(calc_entropy(alt_df['value'].values), 3)

    # --- 18. 生产/消费属性指数 ---
    cal_data = daily_counts.rename(columns={'date_str': 'date'})[['date', 'value']]
    streamlit_data['calendar'] = cal_data.values.tolist()
    workday_avg = daily_counts[daily_counts['date_str'].isin(df[df['is_workday']]['date_str'])]['value'].mean()
    weekend_avg = daily_counts[daily_counts['date_str'].isin(df[~df['is_workday']]['date_str'])]['value'].mean()
    prod_cons_ratio = round((workday_avg / weekend_avg), 2) if weekend_avg and not np.isnan(weekend_avg) else 0

    # --- 19. 低空夜间经济指数 ---
    night_mask = (df['hour'] >= 19) | (df['hour'] <= 6)
    night_df = df[night_mask].groupby('hour').size().reset_index(name='value')
    night_df['hour'] = night_df['hour'].astype(str) + ":00"
    streamlit_data['night'] = night_df.to_dict(orient='records')
    night_pct = round(night_mask.mean() * 100, 1) if total_flights > 0 else 0

    # --- 20. 头部企业“领航”指数 ---
    high_value_mask = (df['duration'] > 30) | (df['distance'] > 20)
    high_value = df[high_value_mask]
    top5 = high_value['entity'].value_counts().head(5)
    leading_pct = round(top5.sum() / max(len(high_value), 1) * 100, 1) if not high_value.empty else 0
    top2 = high_value['entity'].value_counts().head(2).index.tolist()
    radar_data = {"indicator": [
        {"name": "长航时", "max": 100},
        {"name": "长里程", "max": 100},
        {"name": "夜间", "max": 100},
        {"name": "航程均值", "max": 100},
        {"name": "时长均值", "max": 100}
    ], "data": []}
    for ent in top2:
        ent_data = df[df['entity'] == ent]
        stats = [
            (ent_data['duration'] > 30).sum(),
            (ent_data['distance'] > 20).sum(),
            ((ent_data['hour'] >= 19) | (ent_data['hour'] <= 6)).sum(),
            ent_data['distance'].mean(),
            ent_data['duration'].mean()
        ]
        radar_data["data"].append({"value": stats, "name": ent})
    if radar_data['data']:
        for i in range(5):
            vals = [d['value'][i] for d in radar_data['data']]
            max_val = max(vals) if vals else 1
            max_val = max(max_val, 1e-6)
            for d in radar_data['data']:
                d['value'][i] = round((d['value'][i] / max_val) * 100, 1)
    streamlit_data['radar'] = radar_data

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
    ts_data.append(create_metric(
        "01", "低空交通流量指数", "月均架次指数趋势", "规模与增长",
        traffic_index['value'].iloc[-1] if not traffic_index.empty else 0, "指数", "Area",
        streamlit_data['traffic']
    ))
    ts_data.append(create_metric(
        "02", "低空作业强度指数", "飞行时长与里程关联度", "规模与增长",
        round(op_index_series.iloc[-1], 1) if not monthly_ops.empty else 0, "指数", "DualLine",
        streamlit_data['operation']
    ))
    ts_data.append(create_metric(
        "03", "活跃运力规模指数", "活跃航空器分类统计", "规模与增长",
        unique_sn, "活跃架数", "StackedBar",
        streamlit_data['fleet']
    ))
    ts_data.append(create_metric(
        "04", "增长动能指数", "月度增长率趋势", "规模与增长",
        monthly_total['growth_rate'].iloc[-1] if not monthly_total.empty else 0, "%", "Area",
        streamlit_data['growth']
    ))

    # 2. Structure & Entity
    ts_data.append(create_metric(
        "05", "市场集中度指数 (CR50)", "前50强企业市场份额", "结构与主体",
        f"CR50={cr50_pct}%", "", "Pareto",
        streamlit_data['pareto']
    ))
    ts_data.append(create_metric(
        "06", "商业化成熟指数", "企业/个人用户结构", "结构与主体",
        commercial_pct, "%", "Rose",
        streamlit_data['rose']
    ))
    ts_data.append(create_metric(
        "07", "机型生态多元指数", "航空器型号分布", "结构与主体",
        diversity_index, "辛普森", "Treemap",
        streamlit_data['treemap']
    ))

    # 3. Time & Space
    ts_data.append(create_metric(
        "08", "区域发展均衡指数", "地理飞行密度均衡", "时空特征",
        balance_index, "均衡度", "Map",
        streamlit_data['map']
    ))
    ts_data.append(create_metric(
        "09", "全时段运行指数", "24小时飞行分布", "时空特征",
        alltime_entropy, "熵值", "Polar",
        streamlit_data['polar']
    ))
    ts_data.append(create_metric(
        "10", "季候稳定性指数", "月度飞行波动性", "时空特征",
        stability_index, "稳定性", "BoxPlot",
        streamlit_data['seasonal']
    ))
    ts_boxplot = []
    for i, cat in enumerate(seasonal_data['categories']):
        vals = seasonal_data['values'][i]
        m_data = daily_counts[daily_counts['month'] == cat]['value']
        avg_val = int(m_data.mean()) if not m_data.empty else 0
        ts_boxplot.append({
            "name": cat, "min": vals[0], "q1": vals[1], "median": vals[2], "q3": vals[3], "max": vals[4], "avg": avg_val
        })
    ts_data[-1]['chartData'] = ts_boxplot
    hub_nodes = []
    hub_links = []
    if not hub_df.empty:
        thresholds = sorted(hub_df['value'].tolist(), reverse=True)
        core_threshold = thresholds[0] if thresholds else 0
        secondary_threshold = thresholds[2] if len(thresholds) > 2 else core_threshold
        categories = [{"name": "核心枢纽"}, {"name": "次级枢纽"}, {"name": "一般枢纽"}]
        for _, row in hub_df.iterrows():
            if row['value'] >= core_threshold:
                cat = 0
            elif row['value'] >= secondary_threshold:
                cat = 1
            else:
                cat = 2
            hub_nodes.append({
                "name": row['name'],
                "value": round(row['value'], 1),
                "symbolSize": int(max(18, min(60, row['value']))),
                "category": cat
            })
        hub_names = [n["name"] for n in hub_nodes]
        hub_flow = flows[flows['start_region'].isin(hub_names) & flows['end_region'].isin(hub_names)]
        hub_flow = hub_flow.sort_values('value', ascending=False).head(20)
        hub_links = hub_flow.rename(columns={'start_region': 'source', 'end_region': 'target'}).to_dict(orient='records')
    ts_data.append(create_metric(
        "11", "网络化枢纽指数", "起降点连接度与流量", "时空特征",
        hub_index, "枢纽度", "Graph",
        {"nodes": hub_nodes, "links": hub_links, "categories": [{"name": "核心枢纽"}, {"name": "次级枢纽"}, {"name": "一般枢纽"}]}
    ))

    # 4. Efficiency & Quality
    ts_data.append(create_metric(
        "12", "单机作业效能指数", "活跃航空器年度使用率", "效率与质量",
        efficiency, "架次/年", "Gauge",
        streamlit_data['gauge']
    ))
    ts_data.append(create_metric(
        "13", "长航时任务占比指数", "高价值任务比例", "效率与质量",
        long_endurance_pct, "%", "Funnel",
        streamlit_data['funnel']
    ))
    ts_data.append(create_metric(
        "14", "广域覆盖能力指数", "飞行航程分布", "效率与质量",
        coverage_index, "km", "Histogram",
        streamlit_data['histogram']
    ))
    ts_data.append(create_metric(
        "15", "任务完成质量指数", "有效飞行完成率", "效率与质量",
        completion_pct, "%", "Gauge",
        streamlit_data['quality']
    ))

    # 5. Innovation & Integration
    ts_chord = []
    for link in links:
        ts_chord.append({"x": link['source'], "y": link['target'], "value": link['value']})
    ts_data.append(create_metric(
        "16", "城市微循环渗透指数", "跨区连通性", "创新与融合",
        micro_index, "渗透度", "Chord",
        ts_chord
    ))
    ts_data.append(create_metric(
        "17", "立体空域利用效能指数", "垂直空域利用率", "创新与融合",
        airspace_entropy, "熵值", "GroupedBar",
        streamlit_data['airspace']
    ))
    ts_calendar = [{"date": d[0], "value": d[1]} for d in cal_data.values.tolist()]
    ts_data.append(create_metric(
        "18", "低空经济“生产/消费”属性指数", "工作日与周末活跃对比", "创新与融合",
        prod_cons_ratio, "比率", "Calendar",
        ts_calendar
    ))
    ts_data.append(create_metric(
        "19", "低空夜间经济指数", "夜间飞行占比", "创新与融合",
        night_pct, "%", "Wave",
        streamlit_data['night']
    ))
    ts_radar = []
    indicators = streamlit_data['radar']['indicator']
    data_points = streamlit_data['radar']['data']
    if len(data_points) >= 2:
        for i, ind in enumerate(indicators):
            ts_radar.append({
                "subject": ind['name'],
                "fullMark": 100,
                "A": data_points[0]['value'][i],
                "B": data_points[1]['value'][i]
            })
    ts_data.append(create_metric(
        "20", "头部企业“领航”指数", "高价值任务领导力", "创新与融合",
        leading_pct, "%", "Radar",
        ts_radar
    ))

    return streamlit_data, ts_data
