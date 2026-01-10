---
title: 结构与主体
---

# 结构与主体

## 用户类型分布

```sql user_type_dist
select
    user_type,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by user_type
```

<BarChart
    data={user_type_dist}
    x=user_type
    y=sorties
    title="各类用户类型飞行架次"
/>

## 企业飞行架次 TOP 10

```sql enterprise_top
select
    enterprise_name,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
where user_type = 'Enterprise'
group by enterprise_name
order by sorties desc
limit 10
```

<BarChart
    data={enterprise_top}
    x=enterprise_name
    y=sorties
    title="企业年度合计飞行架次 (TOP 10)"
    swapXY=true
/>

## 航空器型号分布

```sql model_dist
select
    aircraft_model,
    sum(flight_sorties) as sorties
from low_altitude_economy.flight_data
group by aircraft_model
order by sorties desc
```

<BarChart
    data={model_dist}
    x=aircraft_model
    y=sorties
    title="各航空器型号年度飞行架次"
/>
