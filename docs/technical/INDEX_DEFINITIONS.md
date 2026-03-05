# Low Altitude Economy Index Definitions

## Overview
This document provides comprehensive definitions for all 21 indices computed in the Low Altitude Economy monitoring system. Each index includes mathematical formulas, normalization rules, data requirements, and validation criteria.

---

## Dimension 1: Scale & Growth (规模与增长)

### Index 01: Low-Altitude Traffic Index (低空交通流量指数)
**Definition**: Measures relative scale of monthly average flights compared to base period.

**Formula**:
```
Traffic_Index(t) = (Monthly_Avg_Flights(t) / Base_Period_Avg) × 100
```

**Normalization**:
- Base period: First month in dataset
- Base value set to 100
- Range: [0, ∞)

**Data Requirements**:
- `date_str`: Flight date (YYYY-MM-DD format)
- Minimum 1 month of data

**Validation**:
- Index should be > 0
- Sudden changes > 50% may indicate data quality issues

---

### Index 02: Operation Intensity Index (低空作业强度指数)
**Definition**: Weighted combination of flight duration and distance metrics.

**Formula**:
```
Duration_Normalized(t) = Total_Duration(t) / Base_Duration
Distance_Normalized(t) = Total_Distance(t) / Base_Distance
Intensity_Index(t) = (0.5 × Duration_Normalized(t) + 0.5 × Distance_Normalized(t)) × 100
```

**Normalization**:
- Base period: First month in dataset
- Equal weighting (50/50) for duration and distance
- Range: [0, ∞)

**Data Requirements**:
- `duration`: Flight duration in minutes
- `distance`: Flight distance in kilometers
- `month`: Month identifier

**Validation**:
- Duration should be > 0
- Distance should be > 0
- Index should be positive

---

### Index 03: Active Fleet Scale Index (活跃运力规模指数)
**Definition**: Count of unique aircraft with flight records in the period.

**Formula**:
```
Active_Fleet(t) = COUNT(DISTINCT aircraft_sn WHERE has_flight_in_period(t))
Active_Fleet_By_Type(t, type) = COUNT(DISTINCT aircraft_sn WHERE aircraft_type = type AND has_flight_in_period(t))
```

**Classification**:
- MultiRotor: Multi-rotor drones
- FixedWing: Fixed-wing aircraft
- Helicopter: Rotorcraft

**Data Requirements**:
- `sn`: Aircraft serial number (unique identifier)
- `aircraft_type`: Type classification
- `month`: Month identifier

**Validation**:
- Active fleet should be ≤ total registered fleet
- Count should be non-negative integer

---

### Index 04: Growth Momentum Index (增长动能指数)
**Definition**: Month-over-month percentage change in total flights.

**Formula**:
```
Growth_Rate(t) = ((Flights(t) - Flights(t-1)) / Flights(t-1)) × 100
```

**Range**: (-100%, ∞)
- Negative values indicate contraction
- Positive values indicate growth

**Data Requirements**:
- Monthly flight counts
- Minimum 2 months of data

**Validation**:
- Extreme values (> 100% or < -50%) should be flagged
- First month shows 0% (no previous period)

---

## Dimension 2: Structure & Entity (结构与主体)

### Index 05: Market Concentration Index (CR50) (市场集中度指数)
**Definition**: Market share of top 50 companies.

**Formula**:
```
CR50 = (Σ(Flights of Top 50 Companies) / Total_Flights) × 100
```

**Range**: [0%, 100%]
- High concentration (> 70%): Oligopolistic market
- Medium concentration (40-70%): Moderately competitive
- Low concentration (< 40%): Highly competitive

**Data Requirements**:
- `entity`: Company/operator identifier
- Minimum 1 flight per entity

**Validation**:
- CR50 should be ≤ 100%
- If fewer than 50 companies exist, use all companies

---

### Index 06: Commercial Maturity Index (商业化成熟指数)
**Definition**: Percentage of flights operated by enterprise users.

**Formula**:
```
Commercial_Maturity = (Enterprise_Flights / Total_Flights) × 100
```

**User Type Classification**:
- Enterprise (企业用户): Commercial operators
- Individual (个人用户): Personal/recreational users
- Government (政府用户): Public sector
- Unknown (未知用户): Unclassified

**Range**: [0%, 100%]

**Data Requirements**:
- `user_type`: User classification

**Validation**:
- Sum of all user type percentages should = 100%

---

### Index 07: Aircraft Ecosystem Diversity Index (机型生态多元指数)
**Definition**: Simpson's Diversity Index for aircraft models.

**Formula**:
```
Simpson_Index = 1 - Σ(share_i²)

where:
share_i = Flights_of_Model_i / Total_Flights
```

**Range**: [0, 1]
- 0: Complete homogeneity (single model)
- 1: Perfect diversity (infinite models, equal distribution)

**Data Requirements**:
- `aircraft_model`: Aircraft model identifier

**Validation**:
- Index should be in [0, 1]
- More models → higher diversity

---

## Dimension 3: Time & Space (时空特征)

### Index 08: Regional Balance Index (区域发展均衡指数)
**Definition**: Geographic distribution balance measured by Gini coefficient.

**Formula**:
```
Gini = Σ(i=1 to n) Σ(j=1 to n) |flights_i - flights_j| / (2n² × mean_flights)

Balance_Index = 1 - Gini
```

**Range**: [0, 1]
- 0: Extreme inequality (all flights in one region)
- 1: Perfect equality (all regions have equal flights)

**Data Requirements**:
- `region`: Geographic region identifier
- Minimum 2 regions

**Validation**:
- Index should be in [0, 1]
- Gini coefficient should be in [0, 1]

---

### Index 09: All-Time Operation Index (全时段运行指数)
**Definition**: Shannon entropy of hourly flight distribution.

**Formula**:
```
H = -Σ(p_i × ln(p_i))

where:
p_i = Flights_in_Hour_i / Total_Flights
```

**Range**: [0, ln(24)] ≈ [0, 3.18]
- 0: All flights in single hour
- 3.18: Uniform distribution across 24 hours

**Data Requirements**:
- `hour`: Hour of day (0-23)
- Derived from `start_time` timestamp

**Validation**:
- Entropy should be ≥ 0
- Higher entropy indicates better temporal distribution

---

### Index 10: Seasonal Stability Index (季候稳定性指数)
**Definition**: Coefficient of variation for monthly flight totals.

**Formula**:
```
CV = σ / μ

Stability_Index = 1 - CV

where:
σ = standard deviation of monthly flights
μ = mean of monthly flights
```

**Range**: (-∞, 1]
- Negative: High volatility (CV > 1)
- 0-0.5: Moderate stability
- > 0.8: High stability

**Data Requirements**:
- Monthly flight counts
- Minimum 3 months of data

**Validation**:
- Values close to 1 indicate stability
- Negative values indicate extreme volatility

---

### Index 11: Hub Connectivity Index (网络化枢纽指数)
**Definition**: Weighted score combining network degree and flow volume.

**Formula**:
```
Degree(r) = COUNT(DISTINCT connected_regions(r))
Flow(r) = Σ(flights FROM r OR TO r)

Hub_Score(r) = (0.6 × (Degree(r) / Max_Degree) + 0.4 × (Flow(r) / Max_Flow)) × 100
```

**Weights**:
- Connectivity (degree): 60%
- Flow volume: 40%

**Range**: [0, 100]

**Data Requirements**:
- `start_region`: Origin region
- `end_region`: Destination region

**Validation**:
- Score should be in [0, 100]
- Hub with highest score should be identified

---

## Dimension 4: Efficiency & Quality (效能与质量)

### Index 12: Per-Aircraft Efficiency Index (单机作业效能指数)
**Definition**: Average flights per active aircraft.

**Formula**:
```
Efficiency = Total_Flights / Unique_Aircraft_Count
```

**Range**: [0, ∞)
- Normalized to [0, 100] for gauge display

**Data Requirements**:
- `sn`: Aircraft serial number
- Total flight count

**Validation**:
- Efficiency should be > 0
- Extremely high values (> 1000) may indicate data issues

---

### Index 13: Long-Endurance Task Ratio (长航时任务占比指数)
**Definition**: Percentage of flights exceeding 30 minutes duration.

**Formula**:
```
Long_Endurance_Ratio = (COUNT(Flights WHERE duration > 30) / Total_Flights) × 100
```

**Duration Bins**:
- < 10 minutes
- 10-30 minutes
- 30-60 minutes
- > 60 minutes

**Range**: [0%, 100%]

**Data Requirements**:
- `duration`: Flight duration in minutes

**Validation**:
- Ratio should be in [0%, 100%]

---

### Index 14: Coverage Index (广域覆盖能力指数)
**Definition**: Weighted average flight distance.

**Formula**:
```
Coverage = Σ(midpoint_i × count_i) / Σ(count_i)

where:
midpoint_i = midpoint of distance bin i
count_i = number of flights in bin i
```

**Distance Bins** (km):
- 0-1 (midpoint: 0.5)
- 1-5 (midpoint: 3)
- 5-10 (midpoint: 7.5)
- 10-20 (midpoint: 15)
- 20-50 (midpoint: 35)
- > 50 (midpoint: 60)

**Range**: [0, ∞) km

**Data Requirements**:
- `distance`: Flight distance in kilometers

**Validation**:
- Coverage should be ≥ 0
- Should align with actual distance distribution

---

### Index 15: Task Completion Quality Index (任务完成质量指数)
**Definition**: Percentage of planned flights successfully completed.

**Formula**:
```
TQI = (Completed_Planned_Flights / Total_Planned_Flights) × 100

where:
Completed_Planned_Flights = COUNT(WHERE is_planned = TRUE AND is_effective = TRUE)
Total_Planned_Flights = COUNT(WHERE is_planned = TRUE)
```

**Range**: [0%, 100%]
- > 90%: Excellent
- 80-90%: Good
- < 80%: Needs improvement

**Control Chart Parameters**:
- Mean: 90%
- UCL (Upper Control Limit): 98%
- LCL (Lower Control Limit): 75%

**Data Requirements**:
- `is_planned`: Boolean flag
- `is_effective`: Boolean flag

**Validation**:
- TQI should be in [0%, 100%]
- Values consistently below LCL require investigation

---

## Dimension 5: Innovation & Integration (创新与融合)

### Index 16: Micro-circulation Index (城市微循环渗透指数)
**Definition**: Cross-region connectivity weighted by route diversity.

**Formula**:
```
Cross_Region_Ratio = Cross_Region_Flights / Total_Flights
Route_Pairs = COUNT(DISTINCT (start_region, end_region))

Micro_Circulation = Cross_Region_Ratio × ln(1 + Route_Pairs)
```

**Range**: [0, ∞)

**Data Requirements**:
- `start_region`: Origin
- `end_region`: Destination

**Validation**:
- Index should be ≥ 0
- Higher values indicate better integration

---

### Index 17: Airspace Utilization Efficiency (立体空域利用效能指数)
**Definition**: Shannon entropy of altitude distribution.

**Formula**:
```
H = -Σ(p_i × ln(p_i))

where:
p_i = Duration_at_Altitude_i / Total_Duration
```

**Altitude Bins** (meters):
- < 120m
- 120-300m
- 300-600m
- > 600m

**Range**: [0, ln(4)] ≈ [0, 1.39]

**Data Requirements**:
- `altitude`: Flight altitude in meters
- `duration`: Time spent at altitude

**Validation**:
- Entropy should be ≥ 0
- Uniform distribution → maximum entropy

---

### Index 18: Production/Consumption Ratio (生产/消费属性指数)
**Definition**: Ratio of workday to weekend flight activity.

**Formula**:
```
Production_Consumption_Ratio = Workday_Avg_Flights / Weekend_Avg_Flights
```

**Interpretation**:
- > 1.2: Production-driven economy
- 0.8-1.2: Balanced/mixed economy
- < 0.8: Consumption-driven economy

**Range**: [0, ∞)

**Data Requirements**:
- `is_workday`: Boolean flag
- Daily flight counts

**Validation**:
- Ratio should be > 0
- NaN if no weekend data

---

### Index 19: Night Economy Index (低空夜间经济指数)
**Definition**: Percentage of flights during night hours (19:00-06:00).

**Formula**:
```
Night_Economy = (Night_Flights / Total_Flights) × 100

where:
Night_Flights = COUNT(WHERE hour ≥ 19 OR hour ≤ 6)
```

**Range**: [0%, 100%]

**Data Requirements**:
- `hour`: Hour of day (0-23)

**Validation**:
- Percentage should be in [0%, 100%]

---

### Index 20: Leading Enterprise Index (头部企业"领航"指数)
**Definition**: Market share of top 5 companies in high-value tasks.

**Formula**:
```
High_Value_Flights = COUNT(WHERE duration > 30 OR distance > 20)
Top5_High_Value = Σ(Flights of Top 5 Companies in High_Value_Flights)

Leading_Index = (Top5_High_Value / High_Value_Flights) × 100
```

**High-Value Criteria**:
- Duration > 30 minutes OR
- Distance > 20 km

**Range**: [0%, 100%]

**Data Requirements**:
- `entity`: Company identifier
- `duration`: Flight duration
- `distance`: Flight distance

**Validation**:
- Index should be in [0%, 100%]
- Should be ≥ general market concentration

---

### Index 21: Comprehensive Prosperity Index (低空综合繁荣度 LA-PI)
**Definition**: Weighted aggregation of all dimensional scores.

**Formula**:
```
LA-PI = 0.40 × Scale_Score + 
        0.20 × Structure_Score + 
        0.20 × Innovation_Score + 
        0.10 × TimeSpace_Score + 
        0.10 × Efficiency_Score
```

**Dimension Weights**:
- Scale & Growth: 40%
- Structure & Entity: 20%
- Innovation & Integration: 20%
- Time & Space: 10%
- Efficiency & Quality: 10%

**Range**: [0, 100]

**Scoring Bands**:
- 85-100: Excellent
- 70-85: Good
- 50-70: Moderate
- < 50: Needs improvement

**Validation**:
- Composite score should be in [0, 100]
- Sub-scores should be normalized to [0, 100]

---

## Data Quality Requirements

### Required Columns
| Column | Type | Description | Validation |
|--------|------|-------------|------------|
| `date_str` | String | YYYY-MM-DD format | Valid date |
| `sn` | String | Aircraft serial number | Non-empty |
| `duration` | Float | Minutes | > 0 |
| `distance` | Float | Kilometers | ≥ 0 |
| `altitude` | Float | Meters | ≥ 0 |
| `aircraft_type` | String | MultiRotor/FixedWing/Helicopter | Valid type |
| `aircraft_model` | String | Model identifier | Non-empty |
| `entity` | String | Operator/company | Non-empty |
| `user_type` | String | Enterprise/Individual/etc. | Valid type |
| `region` | String | Geographic region | Non-empty |
| `start_region` | String | Origin region | Non-empty |
| `end_region` | String | Destination region | Non-empty |
| `is_planned` | Boolean | Planned flight flag | True/False |
| `is_effective` | Boolean | Completed flag | True/False |

### Derived Columns
| Column | Derivation | Description |
|--------|------------|-------------|
| `month` | From `date_str` | YYYY-MM format |
| `hour` | From `start_time` | 0-23 |
| `is_workday` | From `date_str` | Mon-Fri, excluding holidays |
| `is_weekend` | From `date_str` | Sat-Sun |

### Missing Data Handling
- **Critical fields** (date, sn): Reject record
- **Numeric fields** (duration, distance): Use median imputation
- **Categorical fields** (type, region): Use "Unknown" category
- **Boolean fields**: Use safe defaults (False for flags)

---

## Performance Benchmarks

### Computation Time (for 100K records)
- Single index: < 100ms
- All indices: < 2s
- With visualization data: < 5s

### Memory Usage
- Raw data: ~50MB per 100K records
- Processed data: ~20MB
- Visualization data: ~5MB

### Optimization Strategies
1. Use vectorized pandas operations
2. Cache intermediate results
3. Lazy evaluation for unused indices
4. Parallel computation for independent indices

---

## Change Log

### Version 1.0 (2024-02-04)
- Initial comprehensive index definitions
- Added mathematical formulas for all 21 indices
- Documented validation criteria
- Specified data quality requirements

---

## References
- Low Altitude Economy White Paper (202X)
- Statistical Methods: Simpson Index, Gini Coefficient, Shannon Entropy
- Control Chart Theory: Shewhart Control Charts
