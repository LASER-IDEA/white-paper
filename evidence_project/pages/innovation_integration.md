---
title: 创新与融合
---

# 创新与融合

## 活跃SN数 (按航空器类别)

```sql active_sn
select
    aircraft_category,
    count(distinct entity_id) as active_sns
from low_altitude_economy.flight_data
group by aircraft_category
```

<BarChart
    data={active_sn}
    x=aircraft_category
    y=active_sns
    title="按航空器类别统计年度活跃SN数"
/>

## 区域-高度 融合分析

```sql region_altitude
select
    admin_region,
    altitude_interval,
    sum(flight_duration) as duration
from low_altitude_economy.flight_data
group by admin_region, altitude_interval
```

<Heatmap
    data={region_altitude}
    x=admin_region
    y=altitude_interval
    value=duration
    title="各行政区不同高度区间合计飞行时长"
/>

## 飞行里程 TOP 5 Entity

```sql top_entities_distance
-- This query might be complex if we want top 5 for EACH distance interval,
-- or just top 5 overall.
-- "各飞行里程区间的年合计飞行架次 TOP5的entity_id" implies: For each distance bin, find top 5 entities.
-- Visualizing this is tricky in one chart.
-- Let's define distance bins first.
with bins as (
    select
        entity_id,
        case
            when flight_distance < 1 then '0-1 km'
            when flight_distance < 5 then '1-5 km'
            when flight_distance < 10 then '5-10 km'
            else '> 10 km'
        end as distance_bin,
        sum(flight_sorties) as sorties
    from low_altitude_economy.flight_data
    group by 1, 2
),
ranked as (
    select
        *,
        row_number() over (partition by distance_bin order by sorties desc) as rn
    from bins
)
select * from ranked where rn <= 5
order by distance_bin, sorties desc
```

<DataTable data={top_entities_distance} title="各里程区间 Top 5 活跃主体" />
