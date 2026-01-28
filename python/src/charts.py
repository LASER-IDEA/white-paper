import os
import math
import json
from typing import List, Dict, Any, Optional
from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Pie, Map, Radar, Gauge, Funnel, HeatMap, TreeMap, Graph, Polar, Boxplot, Calendar

# Enhanced color scheme - warm colors for contrast with Klein blue theme
# Matching the professional color palette from Charts.tsx
COLORS = ['#f59e0b', '#ea580c', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d']

# Professional styling constants matching Charts.tsx quality
CHART_CONFIG = {
    'title_color': '#002FA7',
    'text_color': '#64748b',
    'grid_color': '#e2e8f0',
    'tooltip_bg': 'rgba(255, 255, 255, 0.95)',
    'tooltip_border': '#e2e8f0',
    'animation_duration': 1000,
    'font_size': 12,
    'title_font_size': 16,
    'axis_line_color': '#e2e8f0',
    'split_line_color': '#e2e8f0'
}

# Accessibility improvements
CHART_CONFIG_A11Y = {
    **CHART_CONFIG,
    'animation_duration': 800,  # Slightly faster for better UX
    'animation_easing': 'cubicOut',  # Smoother easing function
}

def traffic_area_chart(data: List[Dict[str, Any]]) -> Line:
    """
    Traffic Area Chart - Professional implementation with accessibility improvements
    Shows daily flight sorties with smooth area visualization
    
    Args:
        data: List of dictionaries containing 'date' and 'value' keys
        
    Returns:
        Line chart with area styling
    """
    if not data:
        # Return empty chart with message
        c = Line()
        c.set_global_opts(
            title_opts=opts.TitleOpts(
                title="每日飞行架次",
                subtitle="暂无数据",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['title_font_size']
                )
            )
        )
        return c
    
    x_data, y_data = zip(*[(d['date'], d['value']) for d in data])

    c = (
        Line()
        .add_xaxis(list(x_data))
        .add_yaxis(
            "架次",
            list(y_data),
            is_smooth=True,
            symbol="none",
            areastyle_opts=opts.AreaStyleOpts(
                opacity=0.8,
                color={
                    "type": "linear",
                    "x": 0,
                    "y": 0,
                    "x2": 0,
                    "y2": 1,
                    "colorStops": [
                        {"offset": 0.05, "color": COLORS[0]},
                        {"offset": 0.95, "color": COLORS[0] + "00"}
                    ]
                }
            ),
            linestyle_opts=opts.LineStyleOpts(
                width=2,
                color=COLORS[0]
            ),
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="每日飞行架次",
                subtitle="Daily Flight Sorties",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=CHART_CONFIG['axis_line_color'])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=CHART_CONFIG['axis_line_color'])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=CHART_CONFIG['split_line_color'],
                        width=1,
                        type_="dashed"
                    )
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            ),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    return c

def growth_area_chart(data):
    """
    Growth Momentum Area Chart
    Shows month-over-month growth rate trend
    """
    if not data:
        return Line()
    x_data, y_data = zip(*[(d['date'], d['value']) for d in data])
    c = (
        Line()
        .add_xaxis(list(x_data))
        .add_yaxis(
            "增长率",
            list(y_data),
            is_smooth=True,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.6, color=COLORS[1]),
            linestyle_opts=opts.LineStyleOpts(width=2, color=COLORS[1]),
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="增长动能指数", subtitle="月度增长率趋势"),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(formatter="{value}%")
            )
        )
    )
    return c

def operation_dual_line(data):
    """
    Dual Line Chart - Professional implementation inspired by Charts.tsx
    Shows operation duration and distance with dual Y-axes
    """
    x_data, durations, distances = zip(*[(d['name'], d['duration'], d['distance']) for d in data])

    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis(
            "时长",
            durations,
            itemstyle_opts=opts.ItemStyleOpts(
                color=COLORS[0],
                border_radius=[4, 4, 0, 0]
            ),
            bar_width="40%",
            yaxis_index=0,
            label_opts=opts.LabelOpts(is_show=False)
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="里程 (公里)",
                name_location="center",
                name_gap=50,
                type_="value",
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=COLORS[1])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False)
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="运营强度分析",
                subtitle="时长与里程对比",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=CHART_CONFIG['axis_line_color'])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(
                name="时长 (小时)",
                name_location="center",
                name_gap=50,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=COLORS[0])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=CHART_CONFIG['split_line_color'],
                        width=1,
                        type_="dashed"
                    )
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            ),
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                )
            )
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "里程",
            distances,
            yaxis_index=1,
            itemstyle_opts=opts.ItemStyleOpts(color=COLORS[1]),
            linestyle_opts=opts.LineStyleOpts(
                width=3,
                color=COLORS[1]
            ),
            symbol="circle",
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False)
        )
    )

    bar.overlap(line)
    return bar

def fleet_stacked_bar(data):
    """
    Stacked Bar Chart - Professional implementation inspired by Charts.tsx
    Shows fleet composition by aircraft type with stacked visualization
    """
    x_data, mr, fw, hc = zip(*[(d['name'], d['MultiRotor'], d['FixedWing'], d['Helicopter']) for d in data])

    c = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis(
            "多旋翼",
            mr,
            stack="fleet",
            itemstyle_opts=opts.ItemStyleOpts(
                color=COLORS[0],
                border_radius=[0, 0, 0, 0]
            ),
            bar_width="60%",
            label_opts=opts.LabelOpts(is_show=False)
        )
        .add_yaxis(
            "固定翼",
            fw,
            stack="fleet",
            itemstyle_opts=opts.ItemStyleOpts(
                color=COLORS[1],
                border_radius=[0, 0, 0, 0]
            ),
            label_opts=opts.LabelOpts(is_show=False)
        )
        .add_yaxis(
            "直升机",
            hc,
            stack="fleet",
            itemstyle_opts=opts.ItemStyleOpts(
                color=COLORS[2],
                border_radius=[4, 4, 0, 0]
            ),
            label_opts=opts.LabelOpts(is_show=False)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="机队构成分析",
                subtitle="无人机类型分布",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=CHART_CONFIG['axis_line_color'])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="数量",
                name_location="center",
                name_gap=30,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=CHART_CONFIG['axis_line_color'])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=CHART_CONFIG['split_line_color'],
                        width=1,
                        type_="dashed"
                    )
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="shadow",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            ),
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                )
            )
        )
    )
    return c

def pareto_chart(data):
    """
    Pareto Chart - Professional implementation inspired by Charts.tsx
    Shows 80/20 rule with volume bars and cumulative percentage line
    """
    x_data, volumes = zip(*[(d['name'], d['volume']) for d in data])
    total = sum(volumes)
    cumulative = []
    curr = 0
    for v in volumes:
        curr += v
        cumulative.append(round(curr/total * 100, 1))

    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis(
            "飞行量",
            volumes,
            itemstyle_opts=opts.ItemStyleOpts(
                color=COLORS[0],
                border_radius=[4, 4, 0, 0]
            ),
            bar_width="30%",
            yaxis_index=0,
            label_opts=opts.LabelOpts(is_show=False)
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="累计占比 (%)",
                name_location="center",
                name_gap=40,
                type_="value",
                min_=0,
                max_=100,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=COLORS[2])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size'],
                    formatter="{value}%"
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False)
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="飞行集中度分析",
                subtitle="帕累托图 - 80/20法则",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=CHART_CONFIG['axis_line_color'])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(
                name="飞行量",
                name_location="center",
                name_gap=30,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=COLORS[0])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=CHART_CONFIG['split_line_color'],
                        width=1,
                        type_="dashed"
                    )
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            ),
            legend_opts=opts.LegendOpts()
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "累计占比",
            cumulative,
            yaxis_index=1,
            itemstyle_opts=opts.ItemStyleOpts(color=COLORS[2]),
            linestyle_opts=opts.LineStyleOpts(
                width=2,
                color=COLORS[2]
            ),
            symbol="circle",
            symbol_size=4,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False)
        )
    )

    bar.overlap(line)
    return bar

def rose_chart(data):
    """
    Nightingale Rose Chart - Professional implementation inspired by Charts.tsx
    Shows sector maturity with custom rose shape and professional styling
    """
    if not data:
        return Pie()

    max_val = max(d.get('value', 0) for d in data)

    # Create rose data with custom scaling
    rose_data = []
    for d in data:
        rose_data.append({
            'name': d['name'],
            'value': d['value'],
            'realValue': d['value']
        })

    def rose_shape(props):
        cx, cy = props['cx'], props['cy']
        inner_radius = props['innerRadius']
        outer_radius = props['outerRadius']
        start_angle = props['startAngle']
        end_angle = props['endAngle']
        fill = props['fill']

        # Custom rose calculation
        val = props['payload']['realValue']
        radius = inner_radius + (val / max_val) * (outer_radius - inner_radius)

        return f'''
            <g>
                <path d="M {cx + inner_radius * math.cos(start_angle * math.pi / 180)} {cy + inner_radius * math.sin(start_angle * math.pi / 180)}
                        L {cx + radius * math.cos(start_angle * math.pi / 180)} {cy + radius * math.sin(start_angle * math.pi / 180)}
                        A {radius} {radius} 0 0 1 {cx + radius * math.cos(end_angle * math.pi / 180)} {cy + radius * math.sin(end_angle * math.pi / 180)}
                        L {cx + inner_radius * math.cos(end_angle * math.pi / 180)} {cy + inner_radius * math.sin(end_angle * math.pi / 180)}
                        A {inner_radius} {inner_radius} 0 0 0 {cx + inner_radius * math.cos(start_angle * math.pi / 180)} {cy + inner_radius * math.sin(start_angle * math.pi / 180)} Z"
                        fill="{fill}" stroke="#fff" strokeWidth="2"/>
            </g>
        '''

    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip([d['name'] for d in data], [d['value'] for d in data])],
            radius=["30%", "80%"],
            rosetype="area",
            label_opts=opts.LabelOpts(
                is_show=False  # Hide labels for cleaner look
            )
        )
        .set_colors(COLORS)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="商业成熟度分析",
                subtitle="夜莺玫瑰图 - 扇形成熟度",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter="{a}<br/>{b}: {c} ({d}%)",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            ),
            legend_opts=opts.LegendOpts()
        )
    )
    return c

def treemap_chart(data):
    """
    Treemap Chart - Professional implementation inspired by Charts.tsx
    Shows diversity with hierarchical rectangles and custom content
    """
    # Prepare data with size property
    treemap_data = []
    for item in data:
        if isinstance(item, dict):
            treemap_data.append({
                'name': item.get('name', ''),
                'value': item.get('size', item.get('value', 0))
            })

    c = (
        TreeMap()
        .add("多样性分析", treemap_data, leaf_depth=1)
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="多样性分析",
                subtitle="树状图 - 机队类型分布",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                formatter="{b}: {c}",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            )
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="inside",
                formatter="{b}\n{c}"
            )
        )
    )
    return c

def map_chart(data):
    """
    Map Chart - Using streamlit-echarts with custom Shenzhen GeoJSON
    Returns ECharts options for st_echarts, following the reference example
    """
    # Load Shenzhen GeoJSON data
    try:
        shenzhen_path = os.path.join(os.path.dirname(__file__), "..", "data", "shenzhen.json")
        with open(shenzhen_path, "r", encoding='utf-8-sig') as f:
            shenzhen_geojson = json.loads(f.read())
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load GeoJSON data ({e}), using fallback")
        return fallback_map_chart(data)

    # Prepare map data (following the reference example structure)
    map_data = [{'name': d['name'], 'value': d['value']} for d in data]

    # Create ECharts options following the reference example
    options = {
        "title": {
            "text": "深圳各区无人机飞行密度分布图",
            "subtext": "基于区域飞行频率与地理位置数据\n深圳坐标系：WGS84 | 数据更新：2024年",
            "left": "center",
            "top": 20,
            "textStyle": {
                "color": CHART_CONFIG['title_color'],
                "fontSize": CHART_CONFIG['title_font_size'],
                "fontWeight": "bold"
            },
            "subtextStyle": {
                "color": CHART_CONFIG['text_color'],
                "fontSize": 11,
                "lineHeight": 18
            }
        },
        "tooltip": {
            "trigger": "item",
            "showDelay": 0,
            "transitionDuration": 0.2,
            "formatter": "function (params) {\n"
                        f"    var value = (params.value + '').split('.');\n"
                        f"    value = value[0].replace(/(\\d{{1,3}})(?=(\\d{{3}})+(?!\\d))/g, '$1,');\n"
                        f"    return params.seriesName + '<br/>' + params.name + ': ' + value;\n"
                        f"}}"
        },
        "toolbox": {
            "show": True,
            "left": "left",
            "top": "top",
            "feature": {
                "dataView": {"readOnly": False, "title": "数据视图"},
                "restore": {"title": "重置"},
                "saveAsImage": {"title": "保存为图片"}
            }
        },
        "visualMap": {
            "left": "right",
            "min": min([d['value'] for d in data]),
            "max": max([d['value'] for d in data]),
            "inRange": {
                "color": [
                    "#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8",
                    "#ffffbf", "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"
                ]
            },
            "text": ["高密度", "低密度"],
            "calculable": True
        },
        "series": [
            {
                "name": "深圳各区飞行密度",
                "type": "map",
                "roam": True,
                "map": "Shenzhen",
                "emphasis": {"label": {"show": True}},
                "data": map_data
            }
        ]
    }

    # Return both the options and the map object (following reference example)
    from streamlit_echarts import Map
    map_obj = Map(
        "Shenzhen",
        shenzhen_geojson,
        {}
    )

    return {"options": options, "map": map_obj}

def hub_graph_chart(data):
    """
    Networked Hub Index - Graph Visualization
    Shows network structure with nodes and links
    """
    if not data or "nodes" not in data or "links" not in data:
        return Graph()

    nodes = data.get("nodes", [])
    links = data.get("links", [])
    categories = data.get("categories", [{"name": "Hub"}])

    # Prepare node data with styling
    node_data = []
    for node in nodes:
        node_data.append(
            opts.GraphNode(
                name=node.get("name", ""),
                symbol_size=node.get("symbolSize", 30),
                value=node.get("value", 0),
                category=node.get("category", 0)
            )
        )

    # Prepare link data
    link_data = []
    for link in links:
        link_data.append(
            opts.GraphLink(
                source=link.get("source", ""),
                target=link.get("target", ""),
                value=link.get("value", 1)
            )
        )

    # Prepare categories
    category_data = [opts.GraphCategory(name=cat.get("name", "")) for cat in categories]

    c = (
        Graph()
        .add(
            "枢纽网络",
            node_data,
            link_data,
            categories=category_data,
            layout="force",
            repulsion=2000,
            edge_length=[100, 200],
            is_roam=True,
            is_draggable=True,
            label_opts=opts.LabelOpts(
                is_show=True,
                position="right",
                color=CHART_CONFIG['title_color'],
                font_size=11,
                font_weight="bold"
            ),
            linestyle_opts=opts.LineStyleOpts(
                color="source",
                curve=0.3,
                width=2,
                opacity=0.6
            ),
            itemstyle_opts=opts.ItemStyleOpts(
                border_color="#fff",
                border_width=2
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="网络化枢纽结构",
                subtitle="基于起降点航线网络的连接度与流量",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            ),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_left="left",
                pos_top="80px",
                textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            )
        )
    )
    return c


def fallback_map_chart(data):
    """
    Fallback map visualization when GeoJSON is not available
    """
    district_names, density_values = zip(*[(d['name'], d['value']) for d in data])

    c = (
        Bar()
        .add_xaxis(district_names)
        .add_yaxis(
            "飞行密度指数",
            density_values,
            itemstyle_opts=opts.ItemStyleOpts(color=COLORS[0]),
            label_opts=opts.LabelOpts(
                position="right",
                formatter="{c}"
            )
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="深圳各区无人机飞行密度分布",
                subtitle="GeoJSON文件未找到，使用柱状图显示",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            )
        )
    )
    return c

def polar_clock_chart(data):
    """
    Polar Clock Chart - Professional implementation inspired by Charts.tsx
    Shows 24-hour activity distribution in polar coordinates
    """
    hours, values = zip(*[(d['hour'], d['value']) for d in data])

    c = (
        Polar()
        .add_schema(
            angleaxis_opts=opts.AngleAxisOpts(
                data=hours,
                type_="category",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=CHART_CONFIG['axis_line_color'])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                )
            ),
            radiusaxis_opts=opts.RadiusAxisOpts(
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=CHART_CONFIG['axis_line_color'])
                ),
                axislabel_opts=opts.LabelOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=CHART_CONFIG['font_size']
                ),
                splitline_opts=opts.SplitLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=CHART_CONFIG['split_line_color'],
                        width=1,
                        type_="dashed"
                    )
                )
            )
        )
        .add(
            "活跃度",
            values,
            type_="bar",
            itemstyle_opts=opts.ItemStyleOpts(
                color=COLORS[0]
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="24小时活跃度",
                subtitle="极地图 - 全天活动分布",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                formatter="{a}<br/>{b}时: {c}",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            ),
            legend_opts=opts.LegendOpts()
        )
    )
    return c

def seasonal_boxplot(data):
    c = (
        Boxplot()
        .add_xaxis(data["categories"])
        .add_yaxis("Sorties",
                   data["values"],
                   tooltip_opts=opts.TooltipOpts(formatter="{b}: {c}")
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Seasonal Variability"))
    )
    return c

def gauge_chart(data):
    c = (
        Gauge()
        .add("", [("Efficiency", data[0]["value"])], min_=0, max_=100,
             axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[(0.3, COLORS[1]), (0.7, COLORS[0]), (1, COLORS[3])], width=30
                )
             ))
        .set_global_opts(title_opts=opts.TitleOpts(title="Efficiency Index"))
    )
    return c

def quality_control_chart(data):
    """
    Quality Control Chart - Three-in-one visualization
    Shows: Control Chart + Gauge + Time Series Trend
    Returns ECharts options for st_echarts
    """
    if not data:
        return None

    latest_tqi = data.get("latestTqi", 92.3)
    traj_data = data.get("trajData", [])
    tqi_history = data.get("tqiHistory", [])
    plan_actual = data.get("planActual", [])

    # Build options dict for st_echarts
    options = {
        "title": [
            {
                "text": "航迹偏离度控制图",
                "left": "6%",
                "top": "2%",
                "textStyle": {
                    "fontSize": 13,
                    "fontWeight": "bold",
                    "color": CHART_CONFIG['title_color']
                }
            },
            {
                "text": "任务完成质量指数",
                "left": "60%",
                "top": "2%",
                "textStyle": {
                    "fontSize": 13,
                    "fontWeight": "bold",
                    "color": CHART_CONFIG['title_color']
                }
            },
            {
                "text": "TQI 历史趋势",
                "left": "6%",
                "top": "58%",
                "textStyle": {
                    "fontSize": 13,
                    "fontWeight": "bold",
                    "color": CHART_CONFIG['title_color']
                }
            }
        ],
        "grid": [
            {"id": "g1", "left": "6%", "top": "10%", "width": "42%", "height": "34%"},
            {"id": "g2", "left": "60%", "top": "10%", "width": "35%", "height": "34%"},
            {"id": "g3", "left": "6%", "top": "66%", "width": "90%", "height": "28%"}
        ],
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "line"},
            "textStyle": {"fontSize": 11},
            "padding": 8,
            "backgroundColor": "rgba(255, 255, 255, 0.95)",
            "borderColor": "#e5e7eb",
            "borderWidth": 1
        },
        "xAxis": [
            {
                "gridIndex": 0,
                "type": "category",
                "data": [d.get("time", "") for d in traj_data],
                "axisLabel": {"fontSize": 9, "color": CHART_CONFIG['text_color'], "rotate": 0},
                "axisLine": {"show": False},
                "axisTick": {"show": False}
            },
            {
                "gridIndex": 2,
                "type": "category",
                "data": [d.get("time", "") for d in tqi_history],
                "axisLabel": {"fontSize": 9, "color": CHART_CONFIG['text_color'], "rotate": 0},
                "axisLine": {"show": False},
                "axisTick": {"show": False}
            }
        ],
        "yAxis": [
            {
                "gridIndex": 0,
                "type": "value",
                "name": "偏离度",
                "nameTextStyle": {"fontSize": 10, "color": CHART_CONFIG['text_color']},
                "nameGap": 30,
                "axisLabel": {"fontSize": 9, "color": CHART_CONFIG['text_color']},
                "axisLine": {"show": False},
                "splitLine": {"lineStyle": {"color": "#f1f5f9", "type": "dashed"}}
            },
            {
                "gridIndex": 2,
                "type": "value",
                "name": "TQI (%)",
                "nameTextStyle": {"fontSize": 10, "color": CHART_CONFIG['text_color']},
                "nameGap": 30,
                "axisLabel": {"fontSize": 9, "color": CHART_CONFIG['text_color']},
                "axisLine": {"show": False},
                "splitLine": {"lineStyle": {"color": "#f1f5f9", "type": "dashed"}}
            }
        ],
        "series": [
            # 1. Trajectory Deviation Control Chart
            {
                "name": "航迹偏离度",
                "type": "line",
                "xAxisIndex": 0,
                "yAxisIndex": 0,
                "data": [d.get("deviation", 0) for d in traj_data],
                "smooth": False,
                "lineStyle": {"width": 2, "color": "#0ea5e9"},
                "itemStyle": {"color": "#0ea5e9"},
                "markLine": {
                    "silent": True,
                    "symbol": "none",
                    "lineStyle": {"type": "dashed", "width": 1.5},
                    "data": [
                        {
                            "yAxis": traj_data[0].get("ucl", 0.25) if traj_data else 0.25,
                            "name": "UCL",
                            "lineStyle": {"color": "#ef4444", "opacity": 0.7},
                            "label": {"formatter": "UCL", "color": "#ef4444", "fontSize": 9, "distance": 5}
                        },
                        {
                            "yAxis": traj_data[0].get("mean", 0) if traj_data else 0,
                            "name": "Mean",
                            "lineStyle": {"color": "#10b981", "opacity": 0.7},
                            "label": {"formatter": "Mean", "color": "#10b981", "fontSize": 9, "distance": 5}
                        },
                        {
                            "yAxis": traj_data[0].get("lcl", -0.25) if traj_data else -0.25,
                            "name": "LCL",
                            "lineStyle": {"color": "#ef4444", "opacity": 0.7},
                            "label": {"formatter": "LCL", "color": "#ef4444", "fontSize": 9, "distance": 5}
                        }
                    ]
                }
            },
            # 2. TQI Gauge
            {
                "type": "gauge",
                "center": ["77%", "27%"],
                "radius": "35%",
                "min": 0,
                "max": 100,
                "startAngle": 225,
                "endAngle": -45,
                "splitNumber": 4,
                "axisLine": {
                    "lineStyle": {
                        "width": 18,
                        "color": [
                            [0.6, "#ef4444"],
                            [0.85, "#f59e0b"],
                            [1, "#10b981"]
                        ]
                    }
                },
                "pointer": {
                    "width": 5,
                    "length": "65%",
                    "itemStyle": {"color": CHART_CONFIG['title_color']}
                },
                "axisTick": {"show": False},
                "splitLine": {
                    "length": 18,
                    "lineStyle": {"color": "#fff", "width": 2}
                },
                "axisLabel": {
                    "distance": 25,
                    "color": CHART_CONFIG['text_color'],
                    "fontSize": 10
                },
                "detail": {
                    "valueAnimation": True,
                    "formatter": "{value}%",
                    "color": CHART_CONFIG['title_color'],
                    "fontSize": 18,
                    "fontWeight": "bold",
                    "offsetCenter": [0, "70%"]
                },
                "data": [{"value": latest_tqi, "name": "TQI"}]
            },
            # 3. TQI History Line
            {
                "name": "TQI",
                "type": "line",
                "xAxisIndex": 1,
                "yAxisIndex": 1,
                "data": [d.get("tqi", 0) for d in tqi_history],
                "smooth": True,
                "lineStyle": {"width": 3, "color": "#0ea5e9"},
                "areaStyle": {
                    "color": {
                        "type": "linear",
                        "x": 0, "y": 0, "x2": 0, "y2": 1,
                        "colorStops": [
                            {"offset": 0, "color": "rgba(14, 165, 233, 0.3)"},
                            {"offset": 1, "color": "rgba(14, 165, 233, 0)"}
                        ]
                    }
                },
                "itemStyle": {"color": "#0ea5e9"},
                "markLine": {
                    "silent": True,
                    "symbol": "none",
                    "lineStyle": {"type": "dashed", "width": 1.5},
                    "data": [
                        {
                            "yAxis": tqi_history[0].get("mean", 90) if tqi_history else 90,
                            "name": "Mean",
                            "lineStyle": {"color": "#10b981", "opacity": 0.7},
                            "label": {"formatter": "Mean: {c}%", "color": "#10b981", "fontSize": 9, "distance": 5}
                        },
                        {
                            "yAxis": tqi_history[0].get("ucl", 98) if tqi_history else 98,
                            "name": "UCL",
                            "lineStyle": {"color": "#f59e0b", "opacity": 0.7},
                            "label": {"formatter": "UCL: {c}%", "color": "#f59e0b", "fontSize": 9, "distance": 5}
                        }
                    ]
                }
            },
            # 4. Actual Sorties Bar
            {
                "name": "实际完成",
                "type": "bar",
                "xAxisIndex": 1,
                "yAxisIndex": 1,
                "data": [d.get("actual", 0) for d in plan_actual],
                "barWidth": "30%",
                "itemStyle": {"color": "rgba(14, 165, 233, 0.6)"},
                "z": 1
            },
            # 5. Planned Sorties Bar
            {
                "name": "计划报备",
                "type": "bar",
                "xAxisIndex": 1,
                "yAxisIndex": 1,
                "data": [d.get("planned", 0) for d in plan_actual],
                "barWidth": "30%",
                "itemStyle": {"color": "rgba(100, 116, 139, 0.3)"},
                "z": 0
            }
        ],
        "legend": {
            "data": ["TQI", "实际完成", "计划报备"],
            "bottom": "1%",
            "left": "center",
            "textStyle": {"color": CHART_CONFIG['text_color'], "fontSize": 10}
        }
    }

    return options

def funnel_chart(data):
    c = (
        Funnel()
        .add("Mission", [[d['name'], d['value']] for d in data],
             gap=2,
             tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
             label_opts=opts.LabelOpts(is_show=True, position="inside"))
        .set_colors(COLORS)
        .set_global_opts(title_opts=opts.TitleOpts(title="Mission Endurance"))
    )
    return c

def histogram_chart(data):
    x_data, y_data = zip(*[(d['name'], d['value']) for d in data])
    c = (
        Bar()
        .add_xaxis(list(x_data))
        .add_yaxis("Count", list(y_data), category_gap=0, itemstyle_opts=opts.ItemStyleOpts(color=COLORS[0]))
        .set_global_opts(title_opts=opts.TitleOpts(title="Flight Distance Distribution"))
    )
    return c

def chord_chart(data):
    nodes = data["nodes"]
    links = data["links"]
    c = (
        Graph()
        .add("", nodes, links, repulsion=4000, layout="circular",
             label_opts=opts.LabelOpts(is_show=True, position="right"),
             linestyle_opts=opts.LineStyleOpts(curve=0.3))
        .set_global_opts(title_opts=opts.TitleOpts(title="Micro Circulation"))
    )
    return c

def airspace_bar(data):
    x_data, y_data = zip(*[(d['name'], d['value']) for d in data])
    c = (
        Bar()
        .add_xaxis(list(x_data))
        .add_yaxis("Sorties", list(y_data), itemstyle_opts=opts.ItemStyleOpts(color=COLORS[4]))
        .set_global_opts(title_opts=opts.TitleOpts(title="Vertical Airspace"))
    )
    return c

def calendar_heatmap(data):
    c = (
        Calendar()
        .add("", data, calendar_opts=opts.CalendarOpts(range_="2023"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Flight Intensity Calendar"),
            visualmap_opts=opts.VisualMapOpts(
                max_=1000, min_=100, orient="horizontal", is_piecewise=False
            ),
        )
    )
    return c

def night_wave_chart(data):
    x_data, y_data = zip(*[(d['hour'], d['value']) for d in data])
    c = (
        Line()
        .add_xaxis(list(x_data))
        .add_yaxis("Activity", list(y_data), is_smooth=True,
                   areastyle_opts=opts.AreaStyleOpts(opacity=0.6, color=COLORS[5]),
                   linestyle_opts=opts.LineStyleOpts(width=2))
        .set_global_opts(title_opts=opts.TitleOpts(title="Night Economy"))
    )
    return c

def radar_chart(data):
    """
    Radar Chart - Professional implementation inspired by Charts.tsx
    Shows leading entity comparison with radar visualization
    """
    indicators = [opts.RadarIndicatorItem(name=i['name'], max_=i['max']) for i in data['indicator']]

    c = (
        Radar()
        .add_schema(
            schema=indicators,
            shape="polygon",
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True,
                areastyle_opts=opts.AreaStyleOpts(
                    color=["rgba(250, 250, 250, 0.1)", "rgba(200, 200, 200, 0.1)"]
                )
            ),
            splitline_opt=opts.SplitLineOpts(
                is_show=True,
                linestyle_opts=opts.LineStyleOpts(
                    color=CHART_CONFIG['split_line_color'],
                    width=1,
                    type_="dashed"
                )
            ),
            textstyle_opts=opts.TextStyleOpts(
                color=CHART_CONFIG['text_color'],
                font_size=CHART_CONFIG['font_size']
            )
        )
        .add(
            data['data'][0]['name'],
            [data['data'][0]['value']],
            areastyle_opts=opts.AreaStyleOpts(
                color=COLORS[0],
                opacity=0.6
            ),
            linestyle_opts=opts.LineStyleOpts(
                color=COLORS[0],
                width=2
            ),
            symbol="circle"
        )
        .add(
            data['data'][1]['name'],
            [data['data'][1]['value']],
            areastyle_opts=opts.AreaStyleOpts(
                color=COLORS[1],
                opacity=0.6
            ),
            linestyle_opts=opts.LineStyleOpts(
                color=COLORS[1],
                width=2
            ),
            symbol="circle"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="领先企业对比",
                subtitle="雷达图 - 多维度分析",
                title_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['title_color'],
                    font_size=CHART_CONFIG['title_font_size'],
                    font_weight="bold"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    color=CHART_CONFIG['text_color'],
                    font_size=12
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="item",
                background_color=CHART_CONFIG['tooltip_bg'],
                border_color=CHART_CONFIG['tooltip_border'],
                textstyle_opts=opts.TextStyleOpts(color="#374151")
            ),
            legend_opts=opts.LegendOpts()
        )
    )
    return c

def dashboard_chart(data):
    val = data[0]['value']
    c = (
        Gauge()
        .add(
            "",
            [("Score", val)],
            min_=0,
            max_=100,
            split_number=10,
            radius="80%",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[(0.3, "#67e0e3"), (0.7, "#37a2da"), (1, "#fd666d")], width=30
                )
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Composite Index"),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    return c
