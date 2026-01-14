from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts.globals import ChartType

# 1. 获取深圳各区坐标 (示例数据)
# 实际应用中，可以使用 pyecharts-china-cities-pinyin 获取更全的 [x, y]
# 假设我们有以下坐标:
shenzhen_coords = {
    "罗湖区": [114.1, 22.55],
    "福田区": [114.05, 22.52],
    "南山区": [113.9, 22.53],
    "宝安区": [113.8, 22.6],
    "龙岗区": [114.4, 22.7],
    "盐田区": [114.22, 22.55],
    "龙华区": [114.03, 22.68],
    "大鹏新区": [114.47, 22.52],
    "坪山区": [114.35, 22.69],
    "光明区": [113.91, 22.79],
}

# 2. 准备数据
data_pair = [
    ("罗湖区", 10), ("福田区", 20), ("南山区", 15), ("宝安区", 25), ("龙岗区", 12), ("盐田区", 13), ("龙华区", 14), ("大鹏新区", 15), ("坪山区", 16), ("光明区", 17)
]

# faker do not have shenzhen_district, so we have to make it ourselves
# Note: 大鹏新区 was merged into 龙岗区 in 2011, so it's not in the current Shenzhen map data
shenzhen_district = ["南山区", "福田区", "宝安区", "龙岗区", "罗湖区", "盐田区","龙华区","大鹏新区","坪山区","光明区"]
shenzhen_district_values = [55, 66, 77, 88, 99, 100, 110, 120, 130, 140]

coordinate_info = {
    "罗湖区": [114.14302, 22.265995],
    "福田区": [114.055036, 22.522871],
    "南山区": [113.930413, 22.533783],
    "宝安区": [113.88311, 22.55372],
    "龙岗区": [114.247137, 22.71919],
    "盐田区": [114.236519, 22.555035],
    "龙华区": [114.018697, 22.663336],
    "大鹏新区": [114.480942, 22.587862],
    "坪山区": [114.346251, 22.690985],
    "光明区": [113.936841, 22.748404],
}

map = Geo()
for district, coords in coordinate_info.items():
    lon, lat = coords  # [longitude, latitude]
    map.add_coordinate(name=district, longitude=lon, latitude=lat)
map.add_schema(maptype="深圳").add(
    "geo",
    [list(z) for z in zip(shenzhen_district, shenzhen_district_values)],
    type_=ChartType.HEATMAP,
).set_series_opts(label_opts=opts.LabelOpts(is_show=False)).set_global_opts(
    visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title="Geo-深圳地图")
).render("geo_guangdong.html")
# from pyecharts import options as opts
# from pyecharts.charts import Geo
# from pyecharts.globals import ChartType, SymbolType

# c = (
#     Geo()
#     .add_schema(maptype="深圳")
#     .add(
#         "",
#         [("南山区", 55), ("福田区", 66), ("宝安区", 77), ("龙岗区", 88),("罗湖区", 99),("盐田区", 100),("大鹏新区", 110)],
#         type_=ChartType.EFFECT_SCATTER,
#         color="white",
#     )
#     .add(
#         "geo",
#         [("南山区", "福田区"), ("南山区", "宝安区"), ("南山区", "龙岗区"),("南山区", "罗湖区"),("南山区", "盐田区"),("南山区", "大鹏新区")],
#         type_=ChartType.LINES,
#         effect_opts=opts.EffectOpts(
#             symbol=SymbolType.ARROW, symbol_size=6, color="blue"
#         ),
#         linestyle_opts=opts.LineStyleOpts(curve=0.2),
#     )
#     .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#     .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Lines"))
#     .render("geo_lines.html")
# )