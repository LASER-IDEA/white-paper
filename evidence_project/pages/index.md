---
title: 低空经济发展指数白皮书
---

# 低空经济发展指数白皮书

<img src="/cover-image-placeholder" alt="Cover Image" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 2rem;" />

## 摘要

本白皮书基于规模、结构、时空、效率、创新5D框架，提供低空经济的综合分析。

## 关键指标概览

```sql total_flights
select sum(flight_sorties) as total_sorties from low_altitude_economy.flight_data
```

```sql avg_daily_flights
select sum(flight_sorties) / count(distinct date) as avg_flights from low_altitude_economy.flight_data
```

<BigValue
  data={total_flights}
  value=total_sorties
  title="总飞行架次"
/>

<BigValue
  data={avg_daily_flights}
  value=avg_flights
  title="日均飞行架次"
  fmt="0.0"
/>

## 目录

1. [规模与增长](./scale_growth)
2. [结构与主体](./structure_entity)
3. [时空特征](./time_space)
4. [效率与质量](./efficiency_quality)
5. [创新与融合](./innovation_integration)
