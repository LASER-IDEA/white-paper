---
title: 规模与增长
---

# 规模与增长

## 每日飞行数据趋势

```sql daily_trend
select
    date,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by date
order by date
```

<LineChart
    data={daily_trend}
    x=date
    y=sorties
    title="每日飞行架次趋势"
/>

## 月均与周均数据

```sql monthly_avg
select
    strftime(date, '%Y-%m') as month,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by 1
order by 1
```

<BarChart
    data={monthly_avg}
    x=month
    y=sorties
    title="每月合计飞行架次"
/>

## 节假日 vs 非节假日

```sql holiday_comparison
select
    is_holiday,
    sum(flight_sorties) as total_sorties,
    avg(flight_sorties) as avg_sorties
from low_altitude_economy.flight_data
group by is_holiday
```

<BarChart
    data={holiday_comparison}
    x=is_holiday
    y=total_sorties
    title="节假日 vs 非节假日 飞行总架次"
/>

## 行政区年度飞行架次

```sql region_yearly
select
    admin_region,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by admin_region
order by sorties desc
```

<BarChart
    data={region_yearly}
    x=admin_region
    y=sorties
    title="各行政区年度飞行架次"
    swapXY=true
/>
