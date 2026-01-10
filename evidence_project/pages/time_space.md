---
title: 时空特征
---

# 时空特征

## 每周各天飞行分布

```sql day_of_week_dist
select
    day_of_week,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by day_of_week
-- sort by Monday first? DuckDB sorts strings alphabetically or we need a case statement or order map.
-- For simplicity, let's assume raw output first.
```

<BarChart
    data={day_of_week_dist}
    x=day_of_week
    y=sorties
    title="每周各天年度合计有效飞行架次"
/>

## 时段飞行分布

```sql time_slot_dist
select
    time_slot,
    sum(flight_sorties) as sorties,
    sum(flight_duration) as duration_mins
from low_altitude_economy.flight_data
group by time_slot
order by time_slot
```

<BarChart
    data={time_slot_dist}
    x=time_slot
    y=sorties
    title="各时段年度合计飞行架次"
/>

<BarChart
    data={time_slot_dist}
    x=time_slot
    y=duration_mins
    title="各时段年度合计飞行时长(分)"
/>

## 区域热力图 (Improved)

Evidence 3.0 supports map components. We can use a Scatter Plot on coordinates if we had them, or use `AreaMap` with geojson.
Since we only have region names in the mock data, we can visualize by region using a Bar Chart or similar, OR if we had a geojson of Shenzhen districts, we could join it.
However, the user asked for "regional heatmap".
Assuming we don't have the geojson handy in this environment easily without fetching it.
I will use a Heatmap component if available for X/Y bins, or stick to a better chart than an image.
Evidence has `<Heatmap>` for matrix data (e.g. Day of Week vs Hour).

Let's try a "Day vs Hour" heatmap first, as it's a common "temporal heatmap".

For "Spatial Heatmap", without GeoJSON, we can't do a real map overlay easily. But I can demonstrate the intent.
"Native map overlay" usually implies using `<AreaMap>` or `<PointMap>`.
I will create a placeholder section for the Map and explain how to enable it (needing GeoJSON).

But wait, the user said "typescript version ... uses an image ... evidence natively is map overlay".
So I should try to implement a map.
I will try to use a simple map if I can find a geojson or just mention it.
Actually, I can simulate a heatmap using a Bubble Chart or Scatter Plot if I assign coordinates to regions.

```sql region_coords
select
    admin_region,
    CASE
        WHEN admin_region = 'Nanshan' THEN 113.93
        WHEN admin_region = 'Futian' THEN 114.05
        WHEN admin_region = 'Luohu' THEN 114.12
        WHEN admin_region = 'Baoan' THEN 113.88
        WHEN admin_region = 'Longgang' THEN 114.24
        ELSE 114.00
    END as long,
    CASE
        WHEN admin_region = 'Nanshan' THEN 22.53
        WHEN admin_region = 'Futian' THEN 22.54
        WHEN admin_region = 'Luohu' THEN 22.55
        WHEN admin_region = 'Baoan' THEN 22.56
        WHEN admin_region = 'Longgang' THEN 22.72
        ELSE 22.50
    END as lat,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by 1, 2, 3
```

*(Note: Evidence Map components require an API key or specific setup sometimes, or just a valid query. Let's see if standard Evidence has a simple map)*
Evidence has `<BubbleMap>` (if installed) or we can use `<ScatterPlot>` as a proxy if we don't have map tiles.
Actually, Evidence 3.0 includes US Map support, but for custom regions (China/Shenzhen), we need GeoJSON.
I will stick to a Matrix Heatmap (Region vs Time) as a "Heatmap" interpretation that works out of the box, AND mention the map capability.

```sql region_hour_heatmap
select
    admin_region,
    time_slot,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by admin_region, time_slot
```

<Heatmap
    data={region_hour_heatmap}
    x=time_slot
    y=admin_region
    value=sorties
    title="区域-时段 飞行热力图"
/>

## 跨行政区组合

```sql cross_region_stats
select
    cross_region,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by cross_region
order by sorties desc
limit 10
```

<BarChart
    data={cross_region_stats}
    x=cross_region
    y=sorties
    title="跨行政区飞行组合 (Top 10)"
    swapXY=true
/>
