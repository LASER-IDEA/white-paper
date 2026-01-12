from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Pie, Map, Radar, Gauge, Funnel, HeatMap, TreeMap, Graph, Polar, Boxplot, Calendar

# Color Palette matching the TS version
COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#6366f1']

def traffic_area_chart(data):
    x_data = [d['date'] for d in data]
    y_data = [d['value'] for d in data]
    c = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis("Sorties", y_data, is_smooth=True,
                   areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color=COLORS[0]),
                   itemstyle_opts=opts.ItemStyleOpts(color=COLORS[0]),
                   label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Daily Flight Sorties"),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c

def operation_dual_line(data):
    x_data = [d['name'] for d in data]
    durations = [d['duration'] for d in data]
    distances = [d['distance'] for d in data]

    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("Duration (h)", durations, itemstyle_opts=opts.ItemStyleOpts(color=COLORS[0]), yaxis_index=0)
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="Distance (km)",
                type_="value",
                position="right",
                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color=COLORS[1]))
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Operation Intensity"),
            yaxis_opts=opts.AxisOpts(name="Duration (h)", position="left"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis("Distance (km)", distances, yaxis_index=1, itemstyle_opts=opts.ItemStyleOpts(color=COLORS[1]), is_smooth=True)
    )

    bar.overlap(line)
    return bar

def fleet_stacked_bar(data):
    x_data = [d['name'] for d in data]
    mr = [d['MultiRotor'] for d in data]
    fw = [d['FixedWing'] for d in data]
    hc = [d['Helicopter'] for d in data]

    c = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("MultiRotor", mr, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color=COLORS[0]))
        .add_yaxis("FixedWing", fw, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color=COLORS[1]))
        .add_yaxis("Helicopter", hc, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color=COLORS[2]))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="Fleet Composition"))
    )
    return c

def pareto_chart(data):
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
        .add_yaxis("Volume", volumes, itemstyle_opts=opts.ItemStyleOpts(color=COLORS[0]))
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="Cumulative %",
                type_="value",
                min_=0,
                max_=100,
                position="right",
                axislabel_opts=opts.LabelOpts(formatter="{value} %")
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Market Concentration"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
        )
    )

    line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis("Cumulative %", cumulative, yaxis_index=1, itemstyle_opts=opts.ItemStyleOpts(color=COLORS[2]), is_smooth=True,
                   label_opts=opts.LabelOpts(is_show=False))
    )

    bar.overlap(line)
    return bar

def rose_chart(data):
    c = (
        Pie()
        .add(
            "",
            [list(z) for z in zip([d['name'] for d in data], [d['value'] for d in data])],
            radius=["20%", "75%"],
            rosetype="area",
            label_opts=opts.LabelOpts(is_show=True)
        )
        .set_colors(COLORS)
        .set_global_opts(title_opts=opts.TitleOpts(title="Sector Maturity"))
    )
    return c

def treemap_chart(data):
    c = (
        TreeMap()
        .add("Sector", data, leaf_depth=1)
        .set_global_opts(title_opts=opts.TitleOpts(title="Diversity (Treemap)"))
        .set_series_opts(label_opts=opts.LabelOpts(position="inside"))
    )
    return c

def map_chart(data):
    # Note: Requires standard map assets or custom geojson.
    # We will use 'China' -> 'Guangdong' -> 'Shenzhen' if available, or just fallback to visualmap logic
    c = (
        Map()
        .add("Sorties", [list(z) for z in zip([d['name'] for d in data], [d['value'] for d in data])], "深圳")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Regional Flight Distribution"),
            visualmap_opts=opts.VisualMapOpts(max_=100),
        )
    )
    return c

def polar_clock_chart(data):
    c = (
        Polar()
        .add_schema(
            angleaxis_opts=opts.AngleAxisOpts(data=[d['hour'] for d in data], type_="category")
        )
        .add("Activity", [d['value'] for d in data], type_="bar", itemstyle_opts=opts.ItemStyleOpts(color=COLORS[0]))
        .set_global_opts(title_opts=opts.TitleOpts(title="24H Activity"))
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
    c = (
        Radar()
        .add_schema(schema=[opts.RadarIndicatorItem(name=i['name'], max_=i['max']) for i in data['indicator']])
        .add(data['data'][0]['name'], [data['data'][0]['value']], areastyle_opts=opts.AreaStyleOpts(color=COLORS[0], opacity=0.6))
        .add(data['data'][1]['name'], [data['data'][1]['value']], areastyle_opts=opts.AreaStyleOpts(color=COLORS[1], opacity=0.6))
        .set_global_opts(title_opts=opts.TitleOpts(title="Leading Entities"))
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
