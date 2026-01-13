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

def traffic_area_chart(data):
    """
    Traffic Area Chart - Professional implementation inspired by Charts.tsx
    Shows daily flight sorties with smooth area visualization
    """
    x_data = [d['date'] for d in data]
    y_data = [d['value'] for d in data]

    c = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "架次",
            y_data,
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

def operation_dual_line(data):
    """
    Dual Line Chart - Professional implementation inspired by Charts.tsx
    Shows operation duration and distance with dual Y-axes
    """
    x_data = [d['name'] for d in data]
    durations = [d['duration'] for d in data]
    distances = [d['distance'] for d in data]

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
    x_data = [d['name'] for d in data]
    mr = [d['MultiRotor'] for d in data]
    fw = [d['FixedWing'] for d in data]
    hc = [d['Helicopter'] for d in data]

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
    x_data = [d['name'] for d in data]
    volumes = [d['volume'] for d in data]
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
    max_val = max([d['value'] for d in data])

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
    # Since pyecharts Python doesn't support custom GeoJSON registration,
    # we'll create a horizontal bar chart showing regional flight density
    # with Shenzhen district names and color-coded bars

    district_names = [d['name'] for d in data]
    density_values = [d['value'] for d in data]

    # Create color mapping based on density levels
    def get_bar_color(value):
        if value >= 80:
            return '#dc2626'  # red-600 - high density
        elif value >= 60:
            return '#ea580c'  # orange-600 - medium-high
        elif value >= 40:
            return '#ca8a04'  # yellow-600 - medium
        elif value >= 20:
            return '#65a30d'  # lime-600 - low-medium
        else:
            return '#0891b2'  # cyan-600 - low

    c = (
        Bar()
        .add_xaxis(district_names)
        .add_yaxis(
            "飞行密度指数",
            density_values,
            itemstyle_opts=opts.ItemStyleOpts(
                color=lambda x: get_bar_color(density_values[x])
            ),
            label_opts=opts.LabelOpts(
                position="right",
                formatter="{c}"
            )
        )
        .reversal_axis()  # Make it horizontal
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="深圳各区无人机飞行密度分布",
                subtitle="Regional Flight Density Distribution in Shenzhen"
            ),
            xaxis_opts=opts.AxisOpts(
                name="密度指数",
                name_location="center",
                name_gap=30
            ),
            yaxis_opts=opts.AxisOpts(
                name="行政区",
                name_location="center",
                name_gap=50
            ),
            legend_opts=opts.LegendOpts(is_show=False),
            toolbox_opts=opts.ToolboxOpts(
                feature=opts.ToolBoxFeatureOpts(
                    save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(title="保存为图片"),
                    restore=opts.ToolBoxFeatureRestoreOpts(title="重置"),
                    data_view=opts.ToolBoxFeatureDataViewOpts(title="数据视图", is_read_only=False)
                )
            )
        )
    )
    return c

def polar_clock_chart(data):
    """
    Polar Clock Chart - Professional implementation inspired by Charts.tsx
    Shows 24-hour activity distribution in polar coordinates
    """
    hours = [d['hour'] for d in data]
    values = [d['value'] for d in data]

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

def funnel_chart(data):
    c = (
        Funnel()
        .add("Mission", [list(z) for z in zip([d['name'] for d in data], [d['value'] for d in data])],
             gap=2,
             tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
             label_opts=opts.LabelOpts(is_show=True, position="inside"))
        .set_colors(COLORS)
        .set_global_opts(title_opts=opts.TitleOpts(title="Mission Endurance"))
    )
    return c

def histogram_chart(data):
    c = (
        Bar()
        .add_xaxis([d['name'] for d in data])
        .add_yaxis("Count", [d['value'] for d in data], category_gap=0, itemstyle_opts=opts.ItemStyleOpts(color=COLORS[0]))
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
    c = (
        Bar()
        .add_xaxis([d['name'] for d in data])
        .add_yaxis("Sorties", [d['value'] for d in data], itemstyle_opts=opts.ItemStyleOpts(color=COLORS[4]))
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
    c = (
        Line()
        .add_xaxis([d['hour'] for d in data])
        .add_yaxis("Activity", [d['value'] for d in data], is_smooth=True,
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
