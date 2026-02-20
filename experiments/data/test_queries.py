"""
Test Query Set for LAEV Experiments
Carefully designed queries covering different task types and complexity levels
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """Task types based on visualization taxonomy"""
    TREND_ANALYSIS = "trend_analysis"
    COMPARISON = "comparison"
    DISTRIBUTION = "distribution"
    CORRELATION = "correlation"
    EXPLORATION = "exploration"
    ANOMALY_DETECTION = "anomaly_detection"


class Complexity(Enum):
    """Query complexity levels"""
    SIMPLE = "simple"      # Single attribute, basic chart
    MEDIUM = "medium"      # 2-3 attributes, standard chart
    COMPLEX = "complex"    # Multiple attributes, composite chart


@dataclass
class TestQuery:
    """Structured test query"""
    id: str
    query_en: str
    query_zh: str
    task_type: TaskType
    complexity: Complexity
    expected_attributes: List[str]
    expected_chart_types: List[str]
    description: str


# Test Query Set - 30 queries total
# 5 task types × 2 complexity levels × 3 queries each = 30 queries

TEST_QUERIES: List[TestQuery] = [
    # ========== TREND ANALYSIS (6 queries) ==========
    TestQuery(
        id="TREND-01",
        query_en="Show the trend of flight operations over time",
        query_zh="显示飞行操作随时间的趋势",
        task_type=TaskType.TREND_ANALYSIS,
        complexity=Complexity.SIMPLE,
        expected_attributes=["date", "count"],
        expected_chart_types=["line", "area"],
        description="Basic temporal trend"
    ),
    TestQuery(
        id="TREND-02",
        query_en="How does flight duration change month by month?",
        query_zh="飞行时长如何逐月变化？",
        task_type=TaskType.TREND_ANALYSIS,
        complexity=Complexity.SIMPLE,
        expected_attributes=["date", "duration"],
        expected_chart_types=["line"],
        description="Monthly aggregation trend"
    ),
    TestQuery(
        id="TREND-03",
        query_en="Compare flight trends across different districts throughout the year",
        query_zh="比较各区域全年的飞行趋势",
        task_type=TaskType.TREND_ANALYSIS,
        complexity=Complexity.COMPLEX,
        expected_attributes=["date", "region", "count"],
        expected_chart_types=["line", "multi_line"],
        description="Multi-series temporal trend"
    ),
    
    # ========== COMPARISON (6 queries) ==========
    TestQuery(
        id="COMP-01",
        query_en="Compare total flight duration across regions",
        query_zh="比较各区域的总飞行时长",
        task_type=TaskType.COMPARISON,
        complexity=Complexity.SIMPLE,
        expected_attributes=["region", "duration"],
        expected_chart_types=["bar"],
        description="Basic regional comparison"
    ),
    TestQuery(
        id="COMP-02",
        query_en="Which aircraft type has the highest average flight distance?",
        query_zh="哪种飞机类型的平均飞行距离最长？",
        task_type=TaskType.COMPARISON,
        complexity=Complexity.SIMPLE,
        expected_attributes=["aircraft_type", "distance"],
        expected_chart_types=["bar", "radar"],
        description="Aircraft type comparison"
    ),
    TestQuery(
        id="COMP-03",
        query_en="Rank districts by total operations and show proportion of planned vs unplanned flights",
        query_zh="按总操作量对区域排名，并显示计划与非计划飞行的比例",
        task_type=TaskType.COMPARISON,
        complexity=Complexity.COMPLEX,
        expected_attributes=["region", "count", "is_planned"],
        expected_chart_types=["grouped_bar", "stacked_bar"],
        description="Multi-dimension comparison with proportion"
    ),
    
    # ========== DISTRIBUTION (6 queries) ==========
    TestQuery(
        id="DIST-01",
        query_en="Show the distribution of flight purposes",
        query_zh="显示飞行目的的分布",
        task_type=TaskType.DISTRIBUTION,
        complexity=Complexity.SIMPLE,
        expected_attributes=["purpose", "count"],
        expected_chart_types=["pie", "donut"],
        description="Purpose distribution"
    ),
    TestQuery(
        id="DIST-02",
        query_en="What is the distribution of flight altitudes?",
        query_zh="飞行高度的分布是怎样的？",
        task_type=TaskType.DISTRIBUTION,
        complexity=Complexity.SIMPLE,
        expected_attributes=["altitude"],
        expected_chart_types=["histogram", "boxplot"],
        description="Numerical distribution"
    ),
    TestQuery(
        id="DIST-03",
        query_en="Show the hourly distribution of flights across different user types",
        query_zh="显示不同用户类型的每小时飞行分布",
        task_type=TaskType.DISTRIBUTION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["hour", "user_type", "count"],
        expected_chart_types=["heatmap", "grouped_bar"],
        description="Temporal distribution by category"
    ),
    
    # ========== CORRELATION (6 queries) ==========
    TestQuery(
        id="CORR-01",
        query_en="Is there a relationship between flight duration and distance?",
        query_zh="飞行时长和距离之间有关系吗？",
        task_type=TaskType.CORRELATION,
        complexity=Complexity.SIMPLE,
        expected_attributes=["duration", "distance"],
        expected_chart_types=["scatter"],
        description="Basic correlation"
    ),
    TestQuery(
        id="CORR-02",
        query_en="How does altitude relate to flight duration for different aircraft types?",
        query_zh="对于不同飞机类型，高度与飞行时长的关系如何？",
        task_type=TaskType.CORRELATION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["altitude", "duration", "aircraft_type"],
        expected_chart_types=["scatter", "bubble"],
        description="Multi-variable correlation"
    ),
    TestQuery(
        id="CORR-03",
        query_en="Analyze the correlation between operation distance, duration, and effectiveness across regions",
        query_zh="分析各区域的操作距离、时长和有效性之间的相关性",
        task_type=TaskType.CORRELATION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["distance", "duration", "is_effective", "region"],
        expected_chart_types=["scatter_matrix", "parallel_coordinates"],
        description="Multi-dimensional correlation analysis"
    ),
    
    # ========== EXPLORATION (4 queries) ==========
    TestQuery(
        id="EXPL-01",
        query_en="Give me an overview of the flight operations",
        query_zh="给我飞行操作的概览",
        task_type=TaskType.EXPLORATION,
        complexity=Complexity.SIMPLE,
        expected_attributes=["multiple"],
        expected_chart_types=["dashboard", "summary"],
        description="General exploration"
    ),
    TestQuery(
        id="EXPL-02",
        query_en="Show me key statistics about the dataset",
        query_zh="显示关于数据集的关键统计信息",
        task_type=TaskType.EXPLORATION,
        complexity=Complexity.SIMPLE,
        expected_attributes=["multiple"],
        expected_chart_types=["summary_stats"],
        description="Statistical summary"
    ),
    TestQuery(
        id="EXPL-03",
        query_en="Provide a comprehensive dashboard showing temporal, spatial, and categorical patterns",
        query_zh="提供一个综合仪表板，显示时间、空间和类别模式",
        task_type=TaskType.EXPLORATION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["date", "region", "purpose", "duration"],
        expected_chart_types=["dashboard"],
        description="Comprehensive dashboard"
    ),
    
    # ========== TREND ANALYSIS (additional 2) ==========
    TestQuery(
        id="TREND-04",
        query_en="Compare weekend vs weekday flight patterns throughout the year",
        query_zh="比较全年周末与工作日的飞行模式",
        task_type=TaskType.TREND_ANALYSIS,
        complexity=Complexity.MEDIUM,
        expected_attributes=["date", "is_holiday", "count", "duration"],
        expected_chart_types=["line", "grouped_bar"],
        description="Weekend vs weekday trend comparison"
    ),
    TestQuery(
        id="TREND-05",
        query_en="Show the daily flight volume heatmap across months",
        query_zh="显示各月份每日飞行量的热力图",
        task_type=TaskType.TREND_ANALYSIS,
        complexity=Complexity.COMPLEX,
        expected_attributes=["date", "month", "day", "count"],
        expected_chart_types=["calendar", "heatmap"],
        description="Calendar heatmap of daily flights"
    ),
    
    # ========== COMPARISON (additional 3) ==========
    TestQuery(
        id="COMP-04",
        query_en="Compare average flight duration between different purposes",
        query_zh="比较不同飞行目的的平均时长",
        task_type=TaskType.COMPARISON,
        complexity=Complexity.SIMPLE,
        expected_attributes=["purpose", "duration"],
        expected_chart_types=["bar", "boxplot"],
        description="Purpose-based duration comparison"
    ),
    TestQuery(
        id="COMP-05",
        query_en="Show a radar chart comparing all districts across multiple metrics",
        query_zh="用雷达图比较所有区域的多个指标",
        task_type=TaskType.COMPARISON,
        complexity=Complexity.COMPLEX,
        expected_attributes=["region", "count", "duration", "distance"],
        expected_chart_types=["radar"],
        description="Multi-metric district comparison"
    ),
    TestQuery(
        id="COMP-06",
        query_en="Compare planned vs actual flights for each aircraft model",
        query_zh="比较各飞机型号的计划与实际飞行量",
        task_type=TaskType.COMPARISON,
        complexity=Complexity.MEDIUM,
        expected_attributes=["aircraft_model", "is_planned", "is_effective"],
        expected_chart_types=["grouped_bar", "funnel"],
        description="Plan vs actual by aircraft model"
    ),
    
    # ========== DISTRIBUTION (additional 3) ==========
    TestQuery(
        id="DIST-04",
        query_en="What is the distribution of flight distances?",
        query_zh="飞行距离的分布是怎样的？",
        task_type=TaskType.DISTRIBUTION,
        complexity=Complexity.SIMPLE,
        expected_attributes=["distance"],
        expected_chart_types=["histogram", "density"],
        description="Distance distribution"
    ),
    TestQuery(
        id="DIST-05",
        query_en="Show the treemap of flights by region and purpose",
        query_zh="按区域和目的显示飞行的树状图",
        task_type=TaskType.DISTRIBUTION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["region", "purpose", "count"],
        expected_chart_types=["treemap", "sunburst"],
        description="Hierarchical distribution"
    ),
    TestQuery(
        id="DIST-06",
        query_en="Show flight altitude distribution by aircraft type",
        query_zh="按飞机类型显示飞行高度分布",
        task_type=TaskType.DISTRIBUTION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["aircraft_type", "altitude"],
        expected_chart_types=["violin", "boxplot"],
        description="Altitude distribution by type"
    ),
    
    # ========== CORRELATION (additional 2) ==========
    TestQuery(
        id="CORR-04",
        query_en="Is there a correlation between flight altitude and distance?",
        query_zh="飞行高度和距离之间有相关性吗？",
        task_type=TaskType.CORRELATION,
        complexity=Complexity.SIMPLE,
        expected_attributes=["altitude", "distance"],
        expected_chart_types=["scatter"],
        description="Altitude vs distance correlation"
    ),
    TestQuery(
        id="CORR-05",
        query_en="Analyze the relationship between enterprise size and operation frequency",
        query_zh="分析企业规模与操作频率的关系",
        task_type=TaskType.CORRELATION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["entity_id", "count", "duration"],
        expected_chart_types=["bubble", "scatter"],
        description="Enterprise size vs frequency"
    ),
    
    # ========== EXPLORATION (additional 1) ==========
    TestQuery(
        id="EXPL-04",
        query_en="What insights can you find about emergency operations?",
        query_zh="关于应急救援操作你能发现什么洞察？",
        task_type=TaskType.EXPLORATION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["purpose", "duration", "region", "time"],
        expected_chart_types=["multi_view"],
        description="Targeted exploration"
    ),
    
    # ========== ANOMALY DETECTION (4 queries total) ==========
    TestQuery(
        id="ANOM-01",
        query_en="Are there any unusual patterns in flight operations?",
        query_zh="飞行操作中是否有异常模式？",
        task_type=TaskType.ANOMALY_DETECTION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["date", "duration", "count"],
        expected_chart_types=["control_chart"],
        description="Anomaly detection"
    ),
    TestQuery(
        id="ANOM-02",
        query_en="Identify outliers in flight distance by region",
        query_zh="识别各区域飞行距离的异常值",
        task_type=TaskType.ANOMALY_DETECTION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["region", "distance"],
        expected_chart_types=["boxplot", "scatter"],
        description="Outlier detection"
    ),
    TestQuery(
        id="ANOM-03",
        query_en="Detect unusual altitude patterns for logistics flights",
        query_zh="检测物流配送飞行的异常高度模式",
        task_type=TaskType.ANOMALY_DETECTION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["purpose", "altitude", "aircraft_type"],
        expected_chart_types=["control_chart", "scatter"],
        description="Purpose-specific anomaly detection"
    ),
    TestQuery(
        id="ANOM-04",
        query_en="Find flights with unusually long duration for their distance",
        query_zh="找出相对于距离飞行时长异常长的记录",
        task_type=TaskType.ANOMALY_DETECTION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["duration", "distance", "ratio"],
        expected_chart_types=["scatter", "highlight_table"],
        description="Duration-distance ratio anomaly"
    ),
    
    # ========== COMPOSITION/SUMMARY (2 queries) ==========
    TestQuery(
        id="SUMM-01",
        query_en="Create a management report showing key performance indicators",
        query_zh="创建显示关键绩效指标的管理报告",
        task_type=TaskType.EXPLORATION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["count", "duration", "distance", "effectiveness"],
        expected_chart_types=["kpi_dashboard", "scorecard"],
        description="KPI dashboard for management"
    ),
    TestQuery(
        id="SUMM-02",
        query_en="Generate a comprehensive analysis comparing all dimensions",
        query_zh="生成一个比较所有维度的综合分析",
        task_type=TaskType.EXPLORATION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["all"],
        expected_chart_types=["multi_panel", "story"],
        description="Comprehensive multi-dimensional analysis"
    ),
    
    # ========== TREND ANALYSIS (3 new queries, total: 8) ==========
    TestQuery(
        id="TREND-06",
        query_en="Show UAM corridor throughput during peak hours",
        query_zh="显示高峰时段UAM走廊的吞吐量",
        task_type=TaskType.TREND_ANALYSIS,
        complexity=Complexity.MEDIUM,
        expected_attributes=["corridor_id", "hour", "throughput", "peak_status"],
        expected_chart_types=["line", "area"],
        description="UAM corridor throughput trend analysis"
    ),
    TestQuery(
        id="TREND-07",
        query_en="Analyze seasonal patterns in emergency response flights",
        query_zh="分析应急救援飞行的季节性模式",
        task_type=TaskType.TREND_ANALYSIS,
        complexity=Complexity.COMPLEX,
        expected_attributes=["date", "season", "purpose", "count", "response_time"],
        expected_chart_types=["line", "heatmap", "calendar"],
        description="Seasonal trend analysis for emergency flights"
    ),
    TestQuery(
        id="TREND-08",
        query_en="Show night vs day operations trend throughout the year",
        query_zh="显示全年夜间与日间操作的趋势",
        task_type=TaskType.TREND_ANALYSIS,
        complexity=Complexity.MEDIUM,
        expected_attributes=["date", "time_period", "count", "operation_type"],
        expected_chart_types=["line", "grouped_bar"],
        description="Day vs night operations trend"
    ),
    
    # ========== COMPARISON (2 new queries, total: 8) ==========
    TestQuery(
        id="COMP-07",
        query_en="Compare eVTOL vs multirotor efficiency across different routes",
        query_zh="比较eVTOL与多旋翼在不同路线上的效率",
        task_type=TaskType.COMPARISON,
        complexity=Complexity.COMPLEX,
        expected_attributes=["aircraft_type", "route_id", "efficiency", "energy_consumption", "passenger_capacity"],
        expected_chart_types=["radar", "grouped_bar", "scatter"],
        description="Aircraft type efficiency comparison"
    ),
    TestQuery(
        id="COMP-08",
        query_en="Compare safety metrics across different operators",
        query_zh="比较不同运营商的安全指标",
        task_type=TaskType.COMPARISON,
        complexity=Complexity.MEDIUM,
        expected_attributes=["operator_id", "safety_score", "incident_count", "compliance_rate"],
        expected_chart_types=["bar", "radar", "scorecard"],
        description="Operator safety metrics comparison"
    ),
    
    # ========== DISTRIBUTION (2 new queries, total: 8) ==========
    TestQuery(
        id="DIST-07",
        query_en="Analyze vertiport utilization rates by time of day",
        query_zh="按时间段分析垂直机场利用率",
        task_type=TaskType.DISTRIBUTION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["vertiport_id", "hour", "utilization_rate", "capacity"],
        expected_chart_types=["heatmap", "bar", "area"],
        description="Vertiport temporal utilization distribution"
    ),
    TestQuery(
        id="DIST-08",
        query_en="Show the distribution of fleet management states",
        query_zh="显示机队管理状态的分布",
        task_type=TaskType.DISTRIBUTION,
        complexity=Complexity.SIMPLE,
        expected_attributes=["fleet_status", "count", "aircraft_count"],
        expected_chart_types=["pie", "donut", "bar"],
        description="Fleet management state distribution"
    ),
    
    # ========== CORRELATION (3 new queries, total: 8) ==========
    TestQuery(
        id="CORR-06",
        query_en="Show the relationship between weather conditions and flight cancellations",
        query_zh="显示天气状况与航班取消之间的关系",
        task_type=TaskType.CORRELATION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["weather_condition", "visibility", "wind_speed", "cancellation_rate", "delay_minutes"],
        expected_chart_types=["scatter", "heatmap", "bubble"],
        description="Weather impact on flight operations correlation"
    ),
    TestQuery(
        id="CORR-07",
        query_en="Analyze the correlation between vertiport capacity and flight frequency",
        query_zh="分析垂直机场容量与航班频率的相关性",
        task_type=TaskType.CORRELATION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["vertiport_id", "capacity", "flight_frequency", "turnaround_time"],
        expected_chart_types=["scatter", "trend_line"],
        description="Vertiport capacity vs utilization correlation"
    ),
    TestQuery(
        id="CORR-08",
        query_en="Is there a relationship between pilot certification level and flight effectiveness?",
        query_zh="飞行员认证级别与飞行有效性之间有关系吗？",
        task_type=TaskType.CORRELATION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["pilot_certification", "flight_effectiveness", "experience_hours"],
        expected_chart_types=["scatter", "boxplot"],
        description="Pilot certification vs effectiveness correlation"
    ),
    
    # ========== EXPLORATION (2 new queries, total: 8) ==========
    TestQuery(
        id="EXPL-05",
        query_en="Provide insights on regulatory compliance metrics across all operators",
        query_zh="提供所有运营商的法规合规指标洞察",
        task_type=TaskType.EXPLORATION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["operator_id", "compliance_score", "violation_count", "audit_date", "certification_status"],
        expected_chart_types=["dashboard", "scorecard", "treemap"],
        description="Regulatory compliance overview"
    ),
    TestQuery(
        id="EXPL-06",
        query_en="What patterns exist in battery usage and charging cycles for eVTOL fleet?",
        query_zh="eVTOL机队的电池使用和充电周期存在什么模式？",
        task_type=TaskType.EXPLORATION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["aircraft_id", "battery_level", "charging_cycles", "flight_hours", "route_distance"],
        expected_chart_types=["multi_view", "dashboard", "line"],
        description="Fleet battery and charging exploration"
    ),
    
    # ========== ANOMALY DETECTION (4 new queries, total: 8) ==========
    TestQuery(
        id="ANOM-05",
        query_en="Detect vertiports with unusually low utilization compared to capacity",
        query_zh="检测相对于容量利用率异常低的垂直机场",
        task_type=TaskType.ANOMALY_DETECTION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["vertiport_id", "utilization_rate", "expected_rate", "capacity"],
        expected_chart_types=["scatter", "control_chart", "highlight_table"],
        description="Vertiport underutilization anomaly detection"
    ),
    TestQuery(
        id="ANOM-06",
        query_en="Identify flights with abnormal energy consumption patterns",
        query_zh="识别具有异常能耗模式的航班",
        task_type=TaskType.ANOMALY_DETECTION,
        complexity=Complexity.COMPLEX,
        expected_attributes=["flight_id", "energy_consumption", "distance", "aircraft_type", "weather"],
        expected_chart_types=["scatter", "boxplot", "control_chart"],
        description="Energy consumption anomaly detection"
    ),
    TestQuery(
        id="ANOM-07",
        query_en="Find eVTOL aircraft with unusual maintenance frequency patterns",
        query_zh="找出维护频率模式异常的eVTOL飞机",
        task_type=TaskType.ANOMALY_DETECTION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["aircraft_id", "maintenance_count", "flight_hours", "aircraft_age"],
        expected_chart_types=["scatter", "boxplot"],
        description="Maintenance pattern anomaly detection"
    ),
    TestQuery(
        id="ANOM-08",
        query_en="Detect corridor congestion anomalies during non-peak hours",
        query_zh="检测非高峰时段的走廊拥堵异常",
        task_type=TaskType.ANOMALY_DETECTION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["corridor_id", "congestion_level", "hour", "expected_congestion"],
        expected_chart_types=["control_chart", "heatmap"],
        description="Corridor congestion anomaly detection"
    ),
    
    # ========== ADDITIONAL DOMAIN-SPECIFIC QUERIES (2 queries) ==========
    TestQuery(
        id="COMP-09",
        query_en="Compare regulatory compliance rates between UAM and general aviation operators",
        query_zh="比较UAM与通用航空运营商的法规合规率",
        task_type=TaskType.COMPARISON,
        complexity=Complexity.COMPLEX,
        expected_attributes=["operator_type", "compliance_rate", "violation_type", "inspection_score"],
        expected_chart_types=["grouped_bar", "stacked_bar", "radar"],
        description="UAM vs GA compliance comparison"
    ),
    TestQuery(
        id="CORR-09",
        query_en="Analyze the relationship between fleet size and operational efficiency",
        query_zh="分析机队规模与运营效率之间的关系",
        task_type=TaskType.CORRELATION,
        complexity=Complexity.MEDIUM,
        expected_attributes=["fleet_size", "operational_efficiency", "utilization_rate", "operator_id"],
        expected_chart_types=["scatter", "trend_line", "bubble"],
        description="Fleet size vs efficiency correlation"
    ),
]


def get_queries_by_task(task_type: TaskType) -> List[TestQuery]:
    """Get all queries for a specific task type"""
    return [q for q in TEST_QUERIES if q.task_type == task_type]


def get_queries_by_complexity(complexity: Complexity) -> List[TestQuery]:
    """Get all queries for a specific complexity level"""
    return [q for q in TEST_QUERIES if q.complexity == complexity]


def get_all_queries() -> List[TestQuery]:
    """Get all test queries"""
    return TEST_QUERIES


def get_query_statistics() -> Dict[str, Any]:
    """Get statistics about the query set"""
    stats = {
        "total": len(TEST_QUERIES),
        "by_task": {},
        "by_complexity": {},
        "by_chart_type": {}
    }
    
    for q in TEST_QUERIES:
        # By task
        task = q.task_type.value
        stats["by_task"][task] = stats["by_task"].get(task, 0) + 1
        
        # By complexity
        comp = q.complexity.value
        stats["by_complexity"][comp] = stats["by_complexity"].get(comp, 0) + 1
        
        # By chart type
        for ct in q.expected_chart_types:
            stats["by_chart_type"][ct] = stats["by_chart_type"].get(ct, 0) + 1
    
    return stats


if __name__ == "__main__":
    import json
    
    print("Test Query Set Statistics:")
    print(json.dumps(get_query_statistics(), indent=2))
    
    print("\n\nSample Queries:")
    for q in TEST_QUERIES[:5]:
        print(f"\n[{q.id}] {q.task_type.value} ({q.complexity.value})")
        print(f"  EN: {q.query_en}")
        print(f"  ZH: {q.query_zh}")
        print(f"  Expected: {q.expected_chart_types}")
