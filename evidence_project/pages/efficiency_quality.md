---
title: 效率与质量
---

# 效率与质量

## 飞行时长分布

```sql duration_dist
select
    case
        when flight_duration < 10 then '0-10 min'
        when flight_duration < 30 then '10-30 min'
        when flight_duration < 60 then '30-60 min'
        else '> 60 min'
    end as duration_bin,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by 1
order by 1
```

<BarChart
    data={duration_dist}
    x=duration_bin
    y=sorties
    title="各飞行时长区间年度飞行架次"
/>

## 飞行里程分布

```sql distance_dist
select
    case
        when flight_distance < 1 then '0-1 km'
        when flight_distance < 5 then '1-5 km'
        when flight_distance < 10 then '5-10 km'
        else '> 10 km'
    end as distance_bin,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by 1
order by 1
```

<BarChart
    data={distance_dist}
    x=distance_bin
    y=sorties
    title="各飞行里程区间年度飞行架次"
/>

## 飞行高度分布

```sql altitude_dist
select
    altitude_interval,
    sum(flight_duration) as total_duration
from low_altitude_economy.flight_data
group by altitude_interval
order by total_duration desc
```

<BarChart
    data={altitude_dist}
    x=altitude_interval
    y=total_duration
    title="各高度区间年度飞行时长"
/>
