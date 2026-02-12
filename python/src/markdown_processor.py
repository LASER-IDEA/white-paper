"""
Markdown Data Processor for Low-Altitude Economy Index Computation

This script reads aggregated data from markdown files and computes the 20 indices
for the web report generation.

Usage:
    python markdown_processor.py --input data/example.md --output output/metrics.json
    python markdown_processor.py --input data/example.md data/annual_example.md --output output/metrics.json
"""

import re
import json
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from io import StringIO
from datetime import datetime


class MarkdownTableParser:
    """Parser for extracting tables from markdown files."""

    def __init__(self):
        self.tables: Dict[str, pd.DataFrame] = {}
        self.table_titles: Dict[str, str] = {}

    def parse_file(self, filepath: str) -> Dict[str, pd.DataFrame]:
        """Parse a markdown file and extract all tables with their section titles."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by section headers (## or ###)
        sections = re.split(r'\n(?=##\s+\d+[\._])', content)

        for section in sections:
            if not section.strip():
                continue

            # Extract section title
            title_match = re.match(r'##\s*(\d+[\._]?\d*\.?)\s*(.*?)(?:\n|$)', section)
            if not title_match:
                continue

            section_num = title_match.group(1).strip('._')
            section_title = title_match.group(2).strip()

            # Find markdown table in section
            table_match = re.search(
                r'\|[^\n]+\|\n\|[-:\s|]+\|\n((?:\|[^\n]*\|\n?)*)',
                section
            )

            if table_match:
                # Get full table including header
                table_start = section.find('|')
                table_text = section[table_start:]
                # Find end of table
                lines = table_text.split('\n')
                table_lines = []
                for line in lines:
                    if line.strip().startswith('|') and line.strip().endswith('|'):
                        table_lines.append(line)
                    elif table_lines:  # End of table
                        break

                if len(table_lines) >= 2:  # At least header and separator
                    df = self._parse_table_lines(table_lines)
                    if df is not None and not df.empty:
                        key = f"table_{section_num}"
                        self.tables[key] = df
                        self.table_titles[key] = section_title

        return self.tables

    def _parse_table_lines(self, lines: List[str]) -> Optional[pd.DataFrame]:
        """Parse markdown table lines into a DataFrame."""
        if len(lines) < 2:
            return None

        # Parse header
        header = [col.strip() for col in lines[0].split('|')[1:-1]]

        # Skip separator line (lines[1])

        # Parse data rows
        data_rows = []
        for line in lines[2:]:
            if not line.strip():
                continue
            row = [cell.strip() for cell in line.split('|')[1:-1]]
            if len(row) == len(header):
                # Clean up each cell
                cleaned_row = []
                for cell in row:
                    # Handle empty cells
                    if not cell or cell.isspace():
                        cleaned_row.append(None)
                    # Handle values starting with '.' (missing integer part)
                    elif cell.startswith('.') and len(cell) > 1:
                        cleaned_row.append('0' + cell)
                    else:
                        cleaned_row.append(cell)
                data_rows.append(cleaned_row)

        if not data_rows:
            return pd.DataFrame(columns=header)

        df = pd.DataFrame(data_rows, columns=header)

        # Identify string columns (name, code, id, type, percentage columns should stay as strings)
        string_col_patterns = ['name', 'code', 'id', 'type', 'category', 'range', 'time', 'month', 'date', 'percentage', 'entity', 'manufacturer', 'aircraft']

        # Convert columns appropriately
        for col in df.columns:
            col_lower = col.lower()
            is_string_col = any(pattern in col_lower for pattern in string_col_patterns)

            if is_string_col:
                # Keep as string, but clean up None values
                df[col] = df[col].fillna('')
            else:
                # Try to convert to numeric
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df


class IndexComputer:
    """Computes the 20 low-altitude economy indices from parsed markdown data."""

    def __init__(self, tables: Dict[str, pd.DataFrame], titles: Dict[str, str]):
        self.tables = tables
        self.titles = titles
        self.metrics: List[Dict[str, Any]] = []

        # Map table numbers to their purposes based on common column patterns
        self._categorize_tables()

    def _categorize_tables(self):
        """Categorize tables by their content for index computation."""
        self.daily_flights = None
        self.monthly_flights = None
        self.annual_flights = None
        self.annual_daily_avg = None
        self.weekly_flights = None
        self.workday_avg = None
        self.weekend_avg = None
        self.user_type_monthly = None
        self.district_annual = None
        self.top50_entities = None
        self.top50_percentage = None
        self.aircraft_model_annual = None
        self.effective_monthly = None
        self.effective_weekday = None
        self.cross_region = None
        self.hourly_flights = None
        self.hourly_duration = None
        self.duration_ranges = None
        self.distance_ranges = None
        self.monthly_duration = None
        self.district_duration = None
        self.monthly_distance = None
        self.district_distance = None
        self.height_ranges = None
        self.district_height = None
        self.speed_ranges = None
        self.daily_sn = None
        self.annual_sn = None
        self.annual_daily_sn_avg = None
        self.aircraft_category_sn = None
        self.aircraft_type_sn = None
        self.manufacturer_sn = None
        self.entity_sn = None
        self.user_type_daily = None
        self.user_type_annual = None
        self.top5_hourly = None
        self.top5_distance_range = None
        self.top50_height = None
        self.top5_speed = None
        self.top5_max_speed = None
        self.top50_duration = None
        self.top50_distance = None
        self.top50_sn = None
        self.annual_total_duration = None
        self.annual_total_distance = None
        self.user_type_sn = None
        self.annual_effective = None
        self.annual_users = None
        self.hourly_distance = None
        self.monthly_aircraft_type_sn = None
        self.district_user_type_annual = None
        self.top5_hourly_flight = None

        # Match tables by title keywords
        for key, title in self.titles.items():
            df = self.tables.get(key)
            if df is None or df.empty:
                continue

            title_lower = title.lower()

            # **全部样例数据及title和表头，请查阅[white-paper/docs/input/mock-detail.md](../docs/input/mock-detail.md)**

            # 1. Daily flight counts
            if '日度飞行架次' in title or '每日飞行' in title:
                self.daily_flights = df

            # 2. Monthly flight counts
            elif '月度飞行架次' in title and '有效' not in title:
                self.monthly_flights = df

            # 3. Annual flight counts
            elif '年度飞行架次' in title or ('年' in title and 'flight_count' in df.columns and len(df.columns) <= 3):
                if 'flight_count' in df.columns and 'year' in df.columns:
                    self.annual_flights = df

            # 4. Annual daily average
            elif '年日均飞行架次' in title:
                self.annual_daily_avg = df

            # 6. Weekly (by weekday)
            elif '周均飞行架次' in title or 'day_of_week' in str(df.columns):
                self.weekly_flights = df

            # 8. Workday average
            elif '工作日' in title and '日均' in title:
                self.workday_avg = df

            # 10. Weekend average
            elif '周末' in title and '日均' in title:
                self.weekend_avg = df

            # 11. User type monthly
            elif '用户类型' in title and '月合计' in title and '飞行架次' in title:
                self.user_type_monthly = df

            # 13. District annual flights
            elif '行政区' in title and '年合计' in title and '飞行架次' in title and '分用户类型' not in title:
                self.district_annual = df

            # 15. TOP50 entities
            elif 'top50单位' in title_lower and '年合计' in title and '飞行架次' in title and '百分比' not in title:
                if 'flight_count' in df.columns and 'entity_id' in str(df.columns).lower():
                    self.top50_entities = df

            # 16. TOP50 percentage
            elif 'top50单位' in title_lower and '年合计' in title and '飞行架次' in title and '百分比' in title:
                self.top50_percentage = df

            # 18. Aircraft model annual
            elif '各航空器型号' in title and '年合计' in title and '飞行架次' in title:
                self.aircraft_model_annual = df

            # 19. Effective monthly
            elif '有效飞行架次' in title and '月合计' in title:
                self.effective_monthly = df

            # 20. Effective weekday
            elif '有效飞行架次' in title and '每周几' in title and '日均' in title:
                self.effective_weekday = df

            # 22. Cross region
            elif '跨区组合' in title and '年合计' in title and '飞行架次' in title:
                self.cross_region = df

            # 24. Hourly flights
            elif '各时段' in title and '飞行架次' in title and '年合计' in title and 'top5' not in title_lower:
                self.hourly_flights = df

            # 25. Hourly duration
            elif '各时段年合计飞行时长' in title:
                self.hourly_duration = df

            # 26. Duration ranges
            elif '各飞行时长区间' in title and '年合计' in title and '飞行架次' in title:
                self.duration_ranges = df

            # 27. Distance ranges
            elif '各飞行里程区间' in title and '年合计' in title and '飞行架次' in title and 'top5' not in title_lower:
                self.distance_ranges = df

            # 28. Monthly duration
            elif '每月飞行时长' in title or ('月' in title and 'total_duration' in str(df.columns)):
                if 'district' not in str(df.columns).lower():
                    self.monthly_duration = df

            # 29. District duration
            elif '各行政区' in title and '年合计' in title and '飞行时长' in title:
                self.district_duration = df

            # 31. Monthly distance
            elif '每月飞行里程' in title:
                self.monthly_distance = df

            # 32. District distance
            elif '各行政区' in title and '年合计' in title and '飞行里程' in title:
                self.district_distance = df

            # 35. Height ranges
            elif '各高度区间' in title and '年合计' in title and '飞行时长' in title and 'top50' not in title_lower:
                self.height_ranges = df

            # 36. District height
            elif '各行政区' in title and '高度区间' in title and '飞行时长' in title:
                self.district_height = df

            # 37. Speed ranges
            elif '水平速度区间' in title and 'top50' not in title_lower and '年合计' in title and '飞行时长' in title:
                self.speed_ranges = df

            # 38. Daily SN
            elif '每日合计' in title and '活跃sn' in title_lower:
                self.daily_sn = df

            # 39. Annual SN
            elif '今年合计' in title and '活跃sn' in title_lower:
                if 'aircraft' not in title and 'user' not in title_lower and '用户' not in title:
                    self.annual_sn = df

            # 40. Annual daily SN average
            elif '年日均活跃sn' in title_lower:
                self.annual_daily_sn_avg = df

            # 43. Aircraft category SN
            elif '航空器类别' in title and '年合计' in title and '活跃sn' in title_lower:
                self.aircraft_category_sn = df

            # 44. Aircraft type SN
            elif '航空器类型' in title and '年合计' in title and '活跃sn' in title_lower:
                self.aircraft_type_sn = df

            # 62. User type SN
            elif '用户类型' in title and '年合计' in title and '活跃sn' in title_lower:
                self.user_type_sn = df

            # 63. Annual effective flights
            elif '年合计有效飞行架次' in title:
                self.annual_effective = df

            # 64. Annual users
            elif '年合计活跃用户数' in title:
                self.annual_users = df

            # 65. Hourly distance
            elif '各时段' in title and '飞行里程' in title and '年合计' in title and 'top50' not in title_lower:
                self.hourly_distance = df

            # 54.  TOP50 duration
            elif 'top50' in title_lower and '飞行时长' in title and '年合计' in title and '高度' not in title:
                self.top50_duration = df

            # 55. TOP50 distance
            elif 'top50' in title_lower and '飞行里程' in title and '年合计' in title:
                self.top50_distance = df

            # 56. TOP50 SN
            elif 'top50' in title_lower and '年合计' in title and '活跃sn' in title_lower:
                self.top50_sn = df

            # 60. Annual total duration
            elif '年合计飞行时长' in title and '秒' in title and '各' not in title and 'top50' not in title_lower:
                self.annual_total_duration = df

            # 61. Annual total distance
            elif '年合计飞行里程' in title and '各' not in title and 'top50' not in title_lower:
                self.annual_total_distance = df

            # 67. monthly aircraft_type sn
            elif '各航空器类型' in title and '月度' in title and '活跃sn' in title_lower:
                self.monthly_aircraft_type_sn = df

            # 68. annual flight_count by district and uas user type
            elif '年合计' in title and '各行政区' in title and '分用户类型' in title and '飞行架次' in title:
                self.district_user_type_annual = df

            # 49. TOP5 hourly flight counts
            elif 'top5单位' in title_lower and '各时段' in title and '飞行架次' in title and '年合计' in title:
                self.top5_hourly_flight = df

    def _calc_gini(self, values: np.ndarray) -> float:
        """Calculate Gini coefficient."""
        vals = np.array(values, dtype=float)
        vals = vals[~np.isnan(vals)]  # Remove NaN values
        if vals.size == 0 or np.all(vals == 0):
            return 0.0
        vals = np.sort(vals)
        n = vals.size
        index = np.arange(1, n + 1)
        return float((np.sum((2 * index - n - 1) * vals)) / (n * np.sum(vals)))

    def _calc_entropy(self, values: np.ndarray) -> float:
        """Calculate Shannon entropy."""
        vals = np.array(values, dtype=float)
        vals = vals[~np.isnan(vals)]  # Remove NaN values
        total = vals.sum()
        if total <= 0:
            return 0.0
        probs = vals / total
        probs = probs[probs > 0]
        return float(-(probs * np.log(probs)).sum())

    def _calc_simpson_diversity(self, values: np.ndarray) -> float:
        """Calculate Simpson diversity index."""
        vals = np.array(values, dtype=float)
        vals = vals[~np.isnan(vals)]  # Remove NaN values
        total = vals.sum()
        if total <= 0:
            return 0.0
        proportions = vals / total
        return float(1 - np.sum(proportions ** 2))

    def _safe_int(self, value, default: int = 0) -> int:
        """Safely convert a value to int, handling NaN and None."""
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def _safe_float(self, value, default: float = 0.0) -> float:
        """Safely convert a value to float, handling NaN and None."""
        if value is None:
            return default
        try:
            f = float(value)
            return default if np.isnan(f) else f
        except (ValueError, TypeError):
            return default

    def _safe_str(self, value, default: str = "未知") -> str:
        """Safely convert a value to string, handling NaN, None, and empty strings."""
        if value is None:
            return default
        if isinstance(value, float):
            if np.isnan(value):
                return default
            # Format float without unnecessary decimals
            if value == int(value):
                return str(int(value))
            return str(value)
        try:
            s = str(value).strip()
            # Check if it's empty, "nan", or "none" string
            if not s or s.lower() == 'nan' or s.lower() == 'none':
                return default
            return s
        except (ValueError, TypeError):
            return default

    def _is_workday(self, date_str: str) -> bool:
        """Check if a date string represents a workday."""
        try:
            date = pd.to_datetime(date_str)
            # Monday=0, Sunday=6, so workday is 0-4
            return date.weekday() < 5
        except:
            return True  # Default to workday if parsing fails

    def _get_district_name(self, code: str) -> str:
        """Map district code to district name."""
        district_map = {
            '440303': '罗湖区',
            '440304': '福田区',
            '440307': '龙岗区',
            '440308': '盐田区',
            '440309': '龙华区',
            '440305': '南山区',
            '440306': '宝安区',
            '440311': '光明区',
            '440310': '坪山区',
            '440343': '大鹏新区',
            'UNDEFINED': '深圳市外'
        }
        code_str = str(code).strip()
        return district_map.get(code_str, code_str)  # Return name if found, otherwise return code

    def _sigmoid_score(self, x: float, x0: float = 100.0, k: float = 0.1) -> float:
        """
        Sigmoid 归一化函数：
        f(x) = 1 / (1 + e^{-k(x - x0)}) * 100

        其中：
        - x0 为拐点（这里默认 100，对应“基期水平”）
        - k 控制曲线陡峭程度（这里默认 0.1）
        """
        try:
            return float(1.0 / (1.0 + np.exp(-k * (float(x) - x0))) * 100.0)
        except Exception:
            return 50.0

    def _piecewise_growth_score(self, x: float, left: float = -100.0, right: float = 0.0, k: float = 0.1) -> float:
        """
        增长动能的分段打分函数（返回 0-100 分）：

        f(x) = {
          0.5 * ((x + 100) / 100)^2,                x ∈ [-100, 0]
          0.5 + 0.5 * (1 - e^{-0.1 * x}),           x ∈ (0, +∞)
        }

        其中 [-100,0] 为左侧区间，(0,+∞) 为右侧区间。
        """
        try:
            x_val = float(x)
            if x_val <= right:
                # 左段：平滑惩罚区，x>=-100 时单调上升到 0.5
                clamped = max(left, min(right, x_val))
                frac = (clamped - left) / (right - left)  # 将 [-100,0] 归一到 [0,1]
                fx = 0.5 * (frac ** 2)
            else:
                # 右段：指数型加分区，从 0.5 向 1 渐近
                fx = 0.5 + 0.5 * (1.0 - np.exp(-k * x_val))
            return float(fx * 100.0)
        except Exception:
            return 50.0

    def _production_consumption_score(self, x: float) -> float:
        """
        生产/消费属性分段打分函数，返回 0-100 分：

        f(x) = {
          0.75 * x,                               x ∈ [0, 0.8)
          0.6 + 0.5 * (x - 0.8),                 x ∈ [0.8, 1.2]
          1 - 0.2 / (x - 0.2),                   x ∈ (1.2, +∞)
        }
        """
        try:
            xv = float(x)
            if xv <= 0:
                fx = 0.0
            elif xv < 0.8:
                fx = 0.75 * xv
            elif xv <= 1.2:
                fx = 0.6 + 0.5 * (xv - 0.8)
            else:
                # 避免除零：x - 0.2 不应为 0
                denom = xv - 0.2
                if denom == 0:
                    fx = 0.0
                else:
                    fx = 1.0 - 0.2 / denom
            return float(max(0.0, min(1.0, fx)) * 100.0)
        except Exception:
            return 50.0

        # Map user type to Chinese (判断用英文，显示为中文)
    def _get_user_type_name(self, user_type_str) -> str:
        user_type_upper = str(user_type_str).upper().strip()
        if user_type_upper == 'ENTITY':
            return "企业用户"
        elif user_type_upper == 'PERSON':
            return "个人用户"
        elif user_type_upper == 'UNDEFINED':
            return "未知类型"
        else:
            return "未知类型"

    def _create_metric(self, id_: str, title: str, subtitle: str, dimension: str,
                       value: Any, unit: str, chart_type: str, chart_data: Any,
                       key_metrics: Optional[List[Dict]] = None,
                       definition: str = "", insight: str = "", suggestion: str = "",
                       trend: float = 0.0) -> Dict:
        """Create a metric object matching the web TypeScript interface."""
        return {
            "id": id_,
            "title": title,
            "subtitle": subtitle,
            "dimension": dimension,
            "value": value,
            "unit": unit,
            "trend": trend,
            "definition": definition or "基于实际数据计算",
            "insight": insight or "基于上传数据生成的分析。",
            "suggestion": suggestion or "请分析数据趋势。",
            "chartType": chart_type,
            "chartData": chart_data,
            "keyMetrics": key_metrics or []
        }

    def compute_all_indices(self) -> List[Dict[str, Any]]:
        """Compute all 20 indices from the parsed data."""
        self.metrics = []

        # 01 - 低空交通流量指数
        self._compute_traffic_index()

        # 02 - 低空作业强度指数
        self._compute_operation_index()

        # 03 - 活跃运力规模指数
        self._compute_fleet_index()

        # 04 - 增长动能指数
        self._compute_growth_index()

        # 05 - 市场集中度指数 (CR50)
        self._compute_market_concentration()

        # 06 - 商业化成熟指数
        self._compute_commercial_maturity()

        # 07 - 机型生态多元指数
        self._compute_diversity_index()

        # 08 - 区域发展均衡指数
        self._compute_regional_balance()

        # 09 - 全时段运行指数
        self._compute_alltime_index()

        # 10 - 季候稳定性指数
        self._compute_stability_index()

        # 11 - 网络化枢纽指数
        self._compute_hub_index()

        # 12 - 单机作业效能指数
        self._compute_efficiency_index()

        # 13 - 长航时任务占比指数
        self._compute_long_endurance_index()

        # 14 - 广域覆盖能力指数
        self._compute_coverage_index()

        # 15 - 任务完成质量指数
        self._compute_quality_index()

        # 16 - 城市微循环渗透指数
        self._compute_micro_circulation_index()

        # 17 - 立体空域利用效能指数
        self._compute_airspace_index()

        # 18 - 生产/消费属性指数
        self._compute_production_consumption_index()

        # 19 - 低空夜间经济指数
        self._compute_night_economy_index()

        # 20 - 头部企业"领航"指数
        self._compute_leading_enterprise_index()

        # 21 - 综合繁荣度指数 (计算加权总分)
        self._compute_prosperity_index()

        return self.metrics

    def _compute_traffic_index(self):
        """01 - 低空交通流量指数: Monthly average sorties index."""
        chart_data = []
        traffic_index_value = 100.0
        total_flight_count = 0
        base_flight_count = 0

        if self.monthly_flights is not None and not self.monthly_flights.empty:
            df = self.monthly_flights.copy()
            # Find the flight count column
            count_col = None
            for col in df.columns:
                if 'flight_count' in col.lower() or 'count' in col.lower():
                    count_col = col
                    break

            if count_col:
                df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
                df = df.dropna(subset=[count_col])  # Remove rows with no count data

                if not df.empty:
                    # Calculate total flight count (sum of all months)
                    total_flight_count = df[count_col].sum()
                    
                    # Base is the first month's flight count
                    base = df[count_col].iloc[0] if len(df) > 0 else 1
                    base = max(base, 1)
                    base_flight_count = base

                    # Calculate average monthly flight count
                    avg_monthly_count = df[count_col].mean()
                    
                    # Index value = (average monthly count / base month count) * 100
                    traffic_index_value = round((avg_monthly_count / base) * 100, 1)

                    date_col = 'month' if 'month' in df.columns else df.columns[0]
                    for i, (_, row) in enumerate(df.iterrows()):
                        idx_val = round((row[count_col] / base) * 100, 1)
                        date_label = self._safe_str(row[date_col], f"月份{i+1}")
                        chart_data.append({
                            "date": date_label,
                            "value": idx_val
                        })

        # Fallback with sample data if no data available
        if not chart_data:
            months = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
                     '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12']
            chart_data = [{"date": m, "value": 100 + i * 2} for i, m in enumerate(months)]
            traffic_index_value = chart_data[-1]['value']

        # Save for global use
        self.traffic_index_value = traffic_index_value

        # Compute trend: (traffic_index_value - 100) / 100
        trend = (traffic_index_value - 100) / 100

        # Compute keyMetrics
        key_metrics = [
            {"label": "年度累计飞行架次", "value": f"{total_flight_count:,.0f}"},
            {"label": "基期月飞行架次", "value": f"{base_flight_count:,.0f}"}
        ]

        self.metrics.append(self._create_metric(
            "01", "低空交通流量指数", "月均规模", "规模与增长",
            traffic_index_value, "指数", "Area", chart_data,
            key_metrics,
            "以基期月架次为100，计算每月架次指数，衡量平均月架次的相对规模。",
            insight="<b>整体规模跨越式增长，市场基数显著扩大</b>：产业月均运行架次已稳定达到基期水平的1.6倍，实现了约60%"
                    "的规模增长。这标志着低空经济活动的基础流量已跨越关键阈值，市场活跃度从“试点探索”阶段迈入“规模运营”新阶段。规模的大幅提升"
                    "不仅是量的增长，更意味着连接节点（航空器、起降点、用户）的增多，为产业内部网络效应的生成与价值溢出奠定了坚实基础。",
            suggestion="强化网络型基础设施以巩固规模效应。公共投资应优先投向开放、智能的通用基础设施网络（如公共起降场、共享通信导航设施），"
                       "以降低全行业运营成本与门槛，支撑规模持续扩张。",
            trend=trend
        ))

    def _compute_operation_index(self):
        """02 - 低空作业强度指数: Weighted duration/distance index."""
        chart_data = []
        operation_index_value = 100.0
        key_metrics = []

        if self.monthly_duration is not None and self.monthly_distance is not None:
            dur_df = self.monthly_duration.copy()
            dist_df = self.monthly_distance.copy()

            # Find relevant columns
            dur_col = 'total_duration' if 'total_duration' in dur_df.columns else dur_df.columns[-1]
            dist_col = 'total_distance' if 'total_distance' in dist_df.columns else dist_df.columns[-1]
            month_col = 'month' if 'month' in dur_df.columns else dur_df.columns[0]

            dur_df[dur_col] = pd.to_numeric(dur_df[dur_col], errors='coerce')
            dist_df[dist_col] = pd.to_numeric(dist_df[dist_col], errors='coerce')

            # Convert units: seconds to hours, meters to km
            # Apply conversion based on typical value ranges
            dur_df['duration_hrs'] = dur_df[dur_col].apply(
                lambda x: x / 3600 if x > 1000 else x
            )
            dist_df['distance_km'] = dist_df[dist_col].apply(
                lambda x: x / 1000 if x > 10000 else x
            )

            # Calculate base values from first month
            base_duration_hrs = max(dur_df['duration_hrs'].iloc[0], 1) if len(dur_df) > 0 and dur_df['duration_hrs'].iloc[0] > 0 else 1
            base_distance_km = max(dist_df['distance_km'].iloc[0], 1) if len(dist_df) > 0 and dist_df['distance_km'].iloc[0] > 0 else 1

            # Calculate average values using mean()
            avg_duration_hrs = dur_df['duration_hrs'].mean()
            avg_distance_km = dist_df['distance_km'].mean()
            
            # Calculate total for key_metrics
            total_duration_hrs = dur_df['duration_hrs'].sum()
            total_distance_km = dist_df['distance_km'].sum()

            # Build chart_data with relative values
            for i, (_, dur_row) in enumerate(dur_df.iterrows()):
                if i < len(dist_df):
                    dist_row = dist_df.iloc[i]
                    duration_hrs = dur_row['duration_hrs']
                    distance_km = dist_row['distance_km']
                    
                    # Calculate relative values (divided by base month)
                    relative_duration = (duration_hrs / base_duration_hrs if base_duration_hrs > 0 else 1) * 100
                    relative_distance = (distance_km / base_distance_km if base_distance_km > 0 else 1) * 100
                    
                    # Calculate overall: 0.5 * duration + 0.5 * distance
                    overall = 0.5 * relative_duration + 0.5 * relative_distance
                    
                    chart_data.append({
                        "name": self._safe_str(dur_row[month_col], f"月份{i+1}"),
                        "duration": round(relative_duration, 1),
                        "distance": round(relative_distance, 1),
                        "composite": round(overall, 1)
                    })

            if chart_data and base_duration_hrs and base_distance_km:
                operation_index_value = round((0.5 * (avg_duration_hrs / base_duration_hrs) + 0.5 * (avg_distance_km / base_distance_km)) * 100, 2)

                # Compute keyMetrics using original values
                key_metrics = [
                    {"label": "总时长（小时）", "value": f"{total_duration_hrs:,.1f}"},
                    {"label": "基期飞行时长（小时）", "value": f"{base_duration_hrs:,.1f}"},
                    {"label": "总里程（公里）", "value": f"{total_distance_km:,.1f}"},
                    {"label": "基期飞行里程（公里）", "value": f"{base_distance_km:,.1f}"}
                ]
            else:
                key_metrics = [
                    {"label": "总时长（小时）", "value": "待计算"},
                    {"label": "基期飞行时长（小时）", "value": "待计算"},
                    {"label": "总里程（公里）", "value": "待计算"},
                    {"label": "基期飞行里程（公里）", "value": "待计算"}
                ]

        if not chart_data:
            months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
            chart_data = [{"name": m, "duration": 4000 + i * 200, "distance": 12000 + i * 800, "overall": 0.5 * (4000 + i * 200) + 0.5 * (12000 + i * 800)} for i, m in enumerate(months)]
            key_metrics = [
                {"label": "总时长（小时）", "value": "待计算"},
                {"label": "基期飞行时长（小时）", "value": "待计算"},
                {"label": "总里程（公里）", "value": "待计算"},
                {"label": "基期飞行里程（公里）", "value": "待计算"}
            ]

        # Save for global use
        self.operation_index_value = operation_index_value

        # Compute trend: (operation_index_value - 100) / 100
        trend = (operation_index_value - 100) / 100

        self.metrics.append(self._create_metric(
            "02", "低空作业强度指数", "单次价值", "规模与增长",
            round(operation_index_value, 2), "指数", "DualLine", chart_data,
            key_metrics,
            "以基期时长与里程为100，计算每月时长与里程指数，加权计算年度⻜⾏时⻓与⾥程的综合指数。",
            insight="<b>运营深度与强度加速提升，发展质量向好</b>："
                    "深刻揭示出单次飞行的平均时长与里程在显著增加。这标志着低空活动正从“短途、浅层”的探索性飞行，向“更长航时、更远航程”的实质性、"
                    "高价值作业任务演进，产业“价值密度”和“运营深度”正在快速提升，发展质量持续向好。",
            suggestion="定向支持高价值运营场景。一方面规划开放适配长航时作业的空域与航路，建设配套基础设施；另一方面可通过与飞行强度挂钩的激励政策，"
                       "引导资源投向物流干线、应急投送等高价值场景。",
            trend=trend
        ))

    def _compute_fleet_index(self):
        """03 - 活跃运力规模指数: Active aircraft by category."""
        chart_data = []
        total_sn = 0
        base_multirotor = None
        base_fixedwing = None
        base_helicopter = None
        base_compoundwing = None
        base_undefined = None

        # First try annual_sn for total count
        if self.annual_sn is not None and not self.annual_sn.empty:
            sn_col = 'sn_count_year' if 'sn_count_year' in self.annual_sn.columns else self.annual_sn.columns[-1]
            total_sn = self._safe_float(pd.to_numeric(self.annual_sn[sn_col], errors='coerce').sum())

        # Use monthly_aircraft_type_sn for chart data
        if self.monthly_aircraft_type_sn is not None and not self.monthly_aircraft_type_sn.empty:
            df = self.monthly_aircraft_type_sn.copy()
            
            # Ensure column names match
            month_col = 'month' if 'month' in df.columns else df.columns[0]
            type_col = 'aircraft_type' if 'aircraft_type' in df.columns else df.columns[1]
            sn_col = 'sn_count' if 'sn_count' in df.columns else df.columns[-1]
            
            df[sn_col] = pd.to_numeric(df[sn_col], errors='coerce')
            df = df.dropna(subset=[sn_col])
            
            if total_sn == 0:
                total_sn = self._safe_float(df[sn_col].sum())
            
            # Group by month and aggregate by aircraft type
            months = sorted(df[month_col].unique())
            
            # Initialize base values for first month
            base_multirotor = None
            base_fixedwing = None
            base_helicopter = None
            base_compoundwing = None
            base_undefined = None
            
            for month in months:
                month_data = df[df[month_col] == month]
                month_entry = {
                    "name": self._safe_str(month, f"月份{len(chart_data)+1}"),
                    "MultiRotor": 0,
                    "FixedWing": 0,
                    "Helicopter": 0,
                    "CompoundWing": 0,
                    "Undefined": 0
                }
                
                for _, row in month_data.iterrows():
                    aircraft_type = self._safe_str(row[type_col])
                    val = self._safe_float(row[sn_col])
                    
                    # Map aircraft types to chart categories
                    if 'Multi-rotorAircraft' in aircraft_type or 'Multi-rotor' in aircraft_type:
                        month_entry['MultiRotor'] += val
                    elif 'Fixed-wingAircraft' in aircraft_type or 'Fixed-wing' in aircraft_type:
                        month_entry['FixedWing'] += val
                    elif 'Rotorcraft' in aircraft_type:
                        month_entry['Helicopter'] += val
                    elif 'Compound-wingAircraft' in aircraft_type or 'Compound-wing' in aircraft_type:
                        month_entry['CompoundWing'] += val
                    elif 'UNDEFINED' in aircraft_type:
                        month_entry['Undefined'] += val
                
                # Convert to integers for display
                month_entry['MultiRotor'] = int(month_entry['MultiRotor'])
                month_entry['FixedWing'] = int(month_entry['FixedWing'])
                month_entry['Helicopter'] = int(month_entry['Helicopter'])
                month_entry['CompoundWing'] = int(month_entry['CompoundWing'])
                month_entry['Undefined'] = int(month_entry['Undefined'])
                
                # Store base values from first month
                if len(chart_data) == 0:
                    base_multirotor = max(month_entry['MultiRotor'], 1)
                    base_fixedwing = max(month_entry['FixedWing'], 1)
                    base_helicopter = max(month_entry['Helicopter'], 1)
                    base_compoundwing = max(month_entry['CompoundWing'], 1)
                    base_undefined = max(month_entry['Undefined'], 1)
                
                chart_data.append(month_entry)
        
        # Fallback: try aircraft_category_sn if monthly data not available
        if not chart_data and self.aircraft_category_sn is not None and not self.aircraft_category_sn.empty:
            df = self.aircraft_category_sn.copy()
            sn_col = 'sn_count' if 'sn_count' in df.columns else df.columns[-1]
            cat_col = 'aircraft_category' if 'aircraft_category' in df.columns else df.columns[1] if len(df.columns) > 1 else df.columns[0]

            df[sn_col] = pd.to_numeric(df[sn_col], errors='coerce')
            if total_sn == 0:
                total_sn = self._safe_float(df[sn_col].sum())

            # Map to standard categories
            chart_data = [{
                "name": "年度",
                "MultiRotor": 0,
                "FixedWing": 0,
                "Helicopter": 0,
                "CompoundWing": 0,
                "Undefined": 0
            }]

            for _, row in df.iterrows():
                cat = self._safe_str(row[cat_col])
                val = self._safe_float(row[sn_col])
                if '多旋翼' in cat or 'multi' in cat.lower() or 'light' in cat.lower() or 'small' in cat.lower() or 'micro' in cat.lower():
                    chart_data[0]['MultiRotor'] += val
                elif '固定翼' in cat or 'fixed' in cat.lower():
                    chart_data[0]['FixedWing'] += val
                elif '直升' in cat or 'heli' in cat.lower() or 'rotorcraft' in cat.lower():
                    chart_data[0]['Helicopter'] += val
                elif '复合翼' in cat or 'compound' in cat.lower():
                    chart_data[0]['CompoundWing'] += val
                elif 'undefined' in cat.lower():
                    chart_data[0]['Undefined'] += val
            
            # Set base values from annual data (used as first month equivalent)
            base_multirotor = max(chart_data[0]['MultiRotor'], 1)
            base_fixedwing = max(chart_data[0]['FixedWing'], 1)
            base_helicopter = max(chart_data[0]['Helicopter'], 1)
            base_compoundwing = max(chart_data[0]['CompoundWing'], 1)
            base_undefined = max(chart_data[0]['Undefined'], 1)


        if not chart_data:
            chart_data = [{
                "name": "年度",
                "MultiRotor": 2500,
                "FixedWing": 500,
                "Helicopter": 100,
                "CompoundWing": 50,
                "Undefined": 10
            }]
            if total_sn == 0:
                total_sn = 3160
            # Set base values from fallback data
            base_multirotor = 2500
            base_fixedwing = 500
            base_helicopter = 100
            base_compoundwing = 50
            base_undefined = 10

        # Calculate totals for key metrics
        total_multirotor = sum(d.get('MultiRotor', 0) for d in chart_data)
        total_fixedwing = sum(d.get('FixedWing', 0) for d in chart_data)
        total_helicopter = sum(d.get('Helicopter', 0) for d in chart_data)
        total_compoundwing = sum(d.get('CompoundWing', 0) for d in chart_data)
        total_undefined = sum(d.get('Undefined', 0) for d in chart_data)

        # Compute keyMetrics
        key_metrics = [
            {"label": "多旋翼活跃SN数", "value": f"{total_multirotor:,}"},
            {"label": "固定翼活跃SN数", "value": f"{total_fixedwing:,}"},
            {"label": "旋翼机活跃SN数", "value": f"{total_helicopter:,}"},
            {"label": "复合翼活跃SN数", "value": f"{total_compoundwing:,}"},
            {"label": "未知类活跃SN数", "value": f"{total_undefined:,}"}
        ]

        # Calculate index_value: (0.2 * (avg_xxx / base_xxx)) for each type
        month_count = len(chart_data) if chart_data else 12
        if month_count > 0:
            # Calculate averages
            avg_multirotor = total_multirotor / month_count
            avg_fixedwing = total_fixedwing / month_count
            avg_helicopter = total_helicopter / month_count
            avg_compoundwing = total_compoundwing / month_count
            avg_undefined = total_undefined / month_count
            
            # Get base values (first month), or use defaults if not available
            if base_multirotor is None:
                base_multirotor = max(chart_data[0].get('MultiRotor', 1), 1) if chart_data else 1
            if base_fixedwing is None:
                base_fixedwing = max(chart_data[0].get('FixedWing', 1), 1) if chart_data else 1
            if base_helicopter is None:
                base_helicopter = max(chart_data[0].get('Helicopter', 1), 1) if chart_data else 1
            if base_compoundwing is None:
                base_compoundwing = max(chart_data[0].get('CompoundWing', 1), 1) if chart_data else 1
            if base_undefined is None:
                base_undefined = max(chart_data[0].get('Undefined', 1), 1) if chart_data else 1
            
            # Calculate fleet_index_value with 0.2 weight for each type
            numerator = (
                0.2 * avg_multirotor +
                0.2 * avg_fixedwing +
                0.2 * avg_helicopter +
                0.2 * avg_compoundwing +
                0.2 * avg_undefined
            )
            denominator = (
                0.2 * base_multirotor +
                0.2 * base_fixedwing +
                0.2 * base_helicopter +
                0.2 * base_compoundwing +
                0.2 * base_undefined
            )
            fleet_index_value = round((numerator / denominator) * 100, 2) if denominator != 0 else 0.0
        else:
            fleet_index_value = 100.0
        
        # Save for global use
        self.fleet_index_value = fleet_index_value

        trend = (fleet_index_value - 100) / 100

        self.metrics.append(self._create_metric(
            "03", "活跃运力规模指数", "运力结构", "规模与增长",
            fleet_index_value, "指数", "StackedBar", chart_data,
            key_metrics,
            "以基期月活跃SN数为100，计算每月活跃SN数指数，衡量平均月活跃SN数的相对规模。",
            insight="<b>运力供给规模庞大，但结构高度集中，多元化潜力待释放</b>：当前活跃航空器总量庞大，但结构呈现单极驱动特征：多旋翼航空器占比最大，"
                    "而适用于长航时、大载重及载人运输的固定翼、复合翼等机型合计不足300架。这印证了当前市场由成熟的工业级无人机应用主导，"
                    "面向未来的多元化、高级别运力储备明显不足，结构性升级空间广阔。",
            suggestion="以场景创新牵引供给升级，实施结构性产业政策以释放潜力。一方面，通过示范采购创造对eVTOL"
                       "等新型航空器的初始市场需求；另一方面，以研发补贴、适航支持等定向激励，降低先进技术路线的入市成本，引导运力供给向多元化、高级化演进。",
            trend=trend
        ))

    def _compute_growth_index(self):
        """04 - 增长动能指数: Monthly growth rate trend."""
        chart_data = []
        avg_growth_value = 0.0  # Average growth rate for index_value
        latest_growth_value = 0.0  # Latest growth rate for key_metrics

        if self.monthly_flights is not None and not self.monthly_flights.empty:
            df = self.monthly_flights.copy()
            count_col = None
            for col in df.columns:
                if 'flight_count' in col.lower() or 'count' in col.lower():
                    count_col = col
                    break

            if count_col:
                df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
                df = df.dropna(subset=[count_col])
                df['growth_rate'] = df[count_col].pct_change() * 100
                df['growth_rate'] = df['growth_rate'].fillna(0).round(1)

                # Calculate average growth rate using mean() for index_value
                avg_growth_value = round(df['growth_rate'].mean(), 1)
                
                # Get latest growth rate (last month) for key_metrics
                latest_growth_value = round(df['growth_rate'].iloc[-1], 1) if len(df) > 0 else 0.0

                date_col = 'month' if 'month' in df.columns else df.columns[0]
                for i, (_, row) in enumerate(df.iterrows()):
                    chart_data.append({
                        "date": self._safe_str(row[date_col], f"月份{i+1}"),
                        "value": self._safe_float(row['growth_rate'])
                    })

        if not chart_data:
            months = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06']
            chart_data = [{"date": m, "value": round(np.random.uniform(-5, 15), 1)} for m in months]
            # Calculate average of all growth rates for index_value
            avg_growth_value = sum(d.get('value', 0) for d in chart_data) / len(chart_data) if chart_data else 0.0
            # Get latest growth rate (last month) for key_metrics
            latest_growth_value = chart_data[-1]['value'] if chart_data else 0.0

        # Compute keyMetrics
        key_metrics = [{"label": "最新环比增长", "value": f"{latest_growth_value}%"}]

        # 全局保存：平均增长率（单位：%）
        self.avg_growth_value = avg_growth_value

        self.metrics.append(self._create_metric(
            "04", "增长动能指数", "月度增长趋势", "规模与增长",
            avg_growth_value, "指数", "Area", chart_data,
            key_metrics,
            "月度总架次的环比增速的平均值，反映规模扩张速度与趋势强度。",
            insight="<b>增长趋势保持稳健，扩张速度健康</b>：月度总架次环比保持近双位数的健康增长，且建立于已显著扩大的市场规模基数之上。"
                    "这显示出产业内生扩张动力充沛，市场未现疲态，整体发展处于强劲的景气扩张通道之中。",
            suggestion="在当期增长动能充沛的窗口期，政策应主动为下一代高价值场景（如城市空中交通、高端应急物流）破除法规与技术障碍，"
                       "培育新的产业增长极，以实现动能的长期接续与可持续发展。"
        ))

    def _compute_market_concentration(self):
        """05 - 市场集中度指数 (CR₁₀): Top 10 entity market share."""
        chart_data = []
        cr10_pct_value = 0.0
        cr10 = 0.0

        if self.top50_percentage is not None and not self.top50_percentage.empty:
            df = self.top50_percentage.copy()

            # Find relevant columns
            name_col = 'entity_name' if 'entity_name' in df.columns else 'entity_id'
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-2]
            pct_col = 'percentage' if 'percentage' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')

            # 解析百分比列（若有），供 chart_data 与 CR 计算使用
            if 'percentage' in df.columns:
                pct_values = []
                for val in df['percentage']:
                    val_str = str(val).strip().replace('%', '').strip()
                    try:
                        pct_values.append(float(val_str) if val_str else 0.0)
                    except ValueError:
                        pct_values.append(0.0)
                df['pct_numeric'] = pct_values
            else:
                total_count = df[count_col].sum()
                df['pct_numeric'] = (df[count_col] / total_count * 100.0).fillna(0.0) if total_count > 0 else 0.0

            # Get top 10 for chart
            df = df.dropna(subset=[count_col])
            for _, row in df.head(10).iterrows():
                pct = self._safe_float(row.get('pct_numeric', 0.0))
                chart_data.append({
                    "name": self._safe_str(row[name_col])[:10],
                    "volume": self._safe_float(row[count_col]),
                    "percentage": round(pct, 1),
                })

            # CR10 = 前10名占比之和（pct_numeric 已在上面算好）
            top10_pct = df.head(10)['pct_numeric']
            cr10 = top10_pct.sum() if top10_pct.max() < 100 else top10_pct.iloc[-1]
            cr10_pct_value = round(cr10, 1)

        if not chart_data:
            # 兜底：假数据，volume 递减，percentage 按比例
            vols = [1000 - i * 50 for i in range(10)]
            total_vol = sum(vols)
            chart_data = [
                {"name": f"企业{chr(65+i)}", "volume": vols[i], "percentage": round(vols[i] / total_vol * 100, 1)}
                for i in range(10)
            ]
            cr10_pct_value = 100.0
            cr10 = 68.0

        # Compute keyMetrics
        top10_share = f"{round(cr10, 1)}%" if cr10 > 0 else "待计算"

        key_metrics = [
            {"label": "Top 10 份额", "value": top10_share}
        ]

        # 全局保存：CR10 占比（0-100）
        self.cr10_pct_value = cr10_pct_value

        self.metrics.append(self._create_metric(
            "05", "市场集中度指数", "前10强企业市场份额 (CR₁₀)", "结构与主体",
            f"CR₁₀={cr10_pct_value}", "%", "Pareto", chart_data,
            key_metrics,
            "头部10家企业对市场飞行活动的控制力（飞行架次占比）。",
            insight=f"<b>市场呈现中度集中格局，头部效应初步形成但风险可控</b>：指数显示头部10家企业占据总飞行架次的{cr10_pct_value}%，表明市场已脱离完全竞争状态，"
                    "进入 “寡头竞争”与“长尾分布”并存的格局。这反映了领先企业在技术、资本或场景上已形成一定的规模壁垒和市场控制力。"
                    "中度集中有利于通过头部企业的示范与牵引，加速技术扩散和商业模式成熟；但需警惕其潜在的滥用市场地位、抑制创新或导致供给刚性的风险。",
            suggestion="实施“促竞争、防垄断、扶小微”的平衡性监管与产业政策。"
        ))

    def _compute_commercial_maturity(self):
        """06 - 商业化成熟指数: Enterprise user percentage."""
        chart_data = []
        commercial_pct_value = 0.0
        personal_pct = 0.0

        if self.user_type_monthly is not None and not self.user_type_monthly.empty:
            df = self.user_type_monthly.copy()

            # Aggregate by user type
            type_col = 'uav_user_type' if 'uav_user_type' in df.columns else df.columns[1]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            agg = df.groupby(type_col)[count_col].sum().reset_index()

            total = agg[count_col].sum()
            for _, row in agg.iterrows():
                user_type_chinese = self._get_user_type_name(row[type_col])
                user_type_upper = str(row[type_col]).upper().strip()
                chart_data.append({
                    "name": user_type_chinese,
                    "value": self._safe_float(row[count_col])
                })
                if 'ENTITY' in user_type_upper:
                    commercial_pct_value = round(self._safe_float(row[count_col]) / total * 100, 1) if total > 0 else 0
                elif 'PERSON' in user_type_upper:
                    personal_pct = round(self._safe_float(row[count_col]) / total * 100, 1) if total > 0 else 0

        if not chart_data:
            chart_data = [
                {"name": "企业用户", "value": 7000},
                {"name": "个人用户", "value": 2000},
                {"name": "未知类型", "value": 1000}
            ]
            commercial_pct_value = 70.0

        # 全局保存：商业占比（0-100）
        self.commercial_pct_value = commercial_pct_value

        key_metrics = [{"label": "个人用户比例", "value": f"{personal_pct}%"}]

        self.metrics.append(self._create_metric(
            "06", "商业化成熟指数", "用户类型分布", "结构与主体",
            commercial_pct_value, "%", "Rose", chart_data,
            key_metrics,
            "企业用户飞行架次占总飞行架次的比例。",
            insight=f"<b>商业化应用已成绝对主导，但消费级市场基础不容忽视</b>：商业飞行架次占比达{commercial_pct_value}%，标志着产业发展引擎已从早期的个人爱好与娱乐消费，"
                    f"成功转向以企业为主体的生产性应用。这是产业实现经济价值闭环、迈向可持续发展的关键转折。同时，个人用户占比仍保有{personal_pct}%的份额，"
                    "构成了稳定的消费级市场基本盘和广泛的社会认知基础，是培育未来大众市场的潜在土壤。",
            suggestion="巩固并深化主流商业场景的应用标准与供应链，同时审慎试点与规范消费级市场，为未来大众化储备动能。"
        ))

    def _compute_diversity_index(self):
        """07 - 机型生态多元指数: Aircraft model diversity (Simpson index)."""
        chart_data = []
        diversity_index_value = 0.0
        key_metrics = []

        if self.aircraft_model_annual is not None and not self.aircraft_model_annual.empty:
            df = self.aircraft_model_annual.copy()

            name_col = 'aircraft_name' if 'aircraft_name' in df.columns else 'aircraft_model'
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])  # Remove rows with NaN counts
            key_metrics = [{"label": "机型数量", "value": str(len(df))}]
            others_total = 0

            for _, row in df.iterrows():
                size = self._safe_float(row[count_col])
                if size < 2000:
                    # Accumulate to others_total if size < 1000
                    others_total += size
                else:
                    # Add to chart_data if size >= 1000
                    chart_data.append({
                        "name": self._safe_str(row[name_col])[:15],
                        "size": size,
                        "fill": "#0ea5e9"
                    })

            # Add "其他" item if others_total > 0
            if others_total > 0:
                chart_data.append({
                    "name": "其他",
                    "size": others_total,
                    "fill": "#94a3b8"
                })

            # Calculate Simpson diversity
            values = df[count_col].dropna().values
            diversity_index_value = float(f"{self._calc_simpson_diversity(values):.2f}")

        if not chart_data:
            chart_data = [
                {"name": "DJI M300", "size": 4000, "fill": "#0ea5e9"},
                {"name": "其他", "size": 3000, "fill": "#94a3b8"}
            ]
            diversity_index_value = 0.85

        # 全局保存（0-1 区间）
        self.diversity_index_value = diversity_index_value

        self.metrics.append(self._create_metric(
            "07", "机型生态多元指数", "机型多样性", "结构与主体",
            diversity_index_value, "辛普森指数", "Treemap", chart_data,
            key_metrics,
            "运营航空器型号的丰富性与均衡性（航空器型号的辛普森多样性指数）。",
            insight=f"<b>机型多样性表现良好，但需关注多样性背后的均衡性与技术先进性</b>：辛普森多样性指数达到{diversity_index_value}，表明在运营的138种机型构成"
                    "了一个物种相对丰富的技术生态。高多样性有助于增强产业应对特定技术路线失败或单一市场需求波动的韧性。但仍需关注多样性背后的技术均衡性与代际先进性。",
            suggestion="从追求“数量多元”转向引导“质量进阶”，构建梯度化、先进性的机型谱系。"
        ))

    def _compute_regional_balance(self):
        """08 - 区域发展均衡指数: 1 - Gini coefficient of regional flights.
        chart_data: 按区、用户类型展开，每条含 district, uas_user_type, value, district_total。
        """
        chart_data = []
        balance_index_value = 0.0

        if self.district_user_type_annual is not None and not self.district_user_type_annual.empty:
            df = self.district_user_type_annual.copy()
            code_col = 'take_off_district_code'
            type_col = 'uav_user_type'
            count_col = 'flight_count'
            if code_col not in df.columns:
                code_col = df.columns[1] if len(df.columns) > 1 else None
            if type_col not in df.columns:
                type_col = 'uav_user_type' if 'uav_user_type' in df.columns else (df.columns[2] if len(df.columns) > 2 else None)
            if count_col not in df.columns:
                count_col = df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])
            df = df[df[count_col] > 0]

            # 按行政区+用户类型汇总（多年度时求和）
            agg = df.groupby([code_col, type_col])[count_col].sum().reset_index()
            # 各区合计（用于 district_total 与基尼）
            district_totals = df.groupby(code_col)[count_col].sum()

            for _, row in agg.iterrows():
                district_code = self._safe_str(row[code_col])
                district_name = self._get_district_name(district_code)
                user_type_name = self._get_user_type_name(row[type_col])
                value = int(round(self._safe_float(row[count_col])))
                district_total = int(round(district_totals.get(district_code, 0)))
                if value > 0:
                    chart_data.append({
                        "district": district_name,
                        "uas_user_type": user_type_name,
                        "value": value,
                        "district_total": district_total
                    })

            gini = self._calc_gini(district_totals.values)
            balance_index_value = round(1 - gini, 2)

        if not chart_data:
            chart_data = [
                {"district": "南山区", "uas_user_type": "企业用户", "value": 85, "district_total": 1000},
                {"district": "南山区", "uas_user_type": "个人用户", "value": 10, "district_total": 1000},
                {"district": "南山区", "uas_user_type": "未知类型", "value": 950, "district_total": 1000},
                {"district": "宝安区", "uas_user_type": "企业用户", "value": 95, "district_total": 2000},
                {"district": "宝安区", "uas_user_type": "个人用户", "value": 25, "district_total": 2000},
                {"district": "福田区", "uas_user_type": "企业用户", "value": 60, "district_total": 500},
                {"district": "福田区", "uas_user_type": "个人用户", "value": 90, "district_total": 500}
            ]
            balance_index_value = 0.68

        # 全局保存（0-1 区间）
        self.balance_index_value = balance_index_value

        key_metrics = [{"label": "基尼系数", "value": f"{round(1-balance_index_value, 2)}"}]

        self.metrics.append(self._create_metric(
            "08", "区域平衡指数", "空间均衡度", "时空特征",
            balance_index_value, "均衡度", "Map", chart_data,
            key_metrics,
            "1 - 区域飞行架次占比的基尼系数，越高越均衡。",
            insight=f"<b>飞行活动呈现“总体集聚、局部均衡”的分布特征，区域协同发展潜力待释放</b>：基尼系数为{round(1-balance_index_value, 2)}，"
                    "表明低空飞行活动在空间分布上存在中等程度的集聚，符合经济发展和基础设施分布不均衡的初期规律。"
                    f"同时，均衡度达到{balance_index_value}，映射出深圳市低空经济已初步形成以若干"
                    "核心区（如南山、龙华）为引领，其他区域跟进的“多核”发展雏形，但区域间的联动性与功能互补性有待加强。",
            suggestion="实施“强核辐射、廊道联网、错位发展”策略，强化核心枢纽，规划功能廊道，引导区域特色化互补发展。"

        ))

    def _compute_alltime_index(self):
        """09 - 全时段运行指数: 24-hour flight distribution entropy."""
        chart_data = []
        alltime_entropy_index_value = 0.0
        night_share_pct = 0.0
        peak_slot_label = "待计算"

        if self.hourly_flights is not None and not self.hourly_flights.empty:
            df = self.hourly_flights.copy()

            # Find time slot columns
            start_col = 'slot_start_time' if 'slot_start_time' in df.columns else df.columns[1]
            end_col = 'slot_end_time' if 'slot_end_time' in df.columns else df.columns[2]
            count_col = 'order_count' if 'order_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])

            # 在一次遍历中同步计算：chart_data、夜间占比和峰值时段
            def _parse_hour_for_slot(t):
                try:
                    t_str = str(t).strip()
                    if ':' in t_str:
                        hour_str = t_str.split(':')[0]
                        return int(hour_str)
                    return int(float(t_str))
                except Exception:
                    return 12

            total_count = 0.0
            night_total = 0.0
            peak_val = -1.0
            peak_start = ""
            peak_end = ""

            for _, row in df.iterrows():
                # Use time range "start - end" as hour label
                start_label = self._safe_str(row[start_col])
                end_label = self._safe_str(row[end_col])
                hour_label = f"{start_label}"

                val = self._safe_float(row[count_col])
                chart_data.append({
                    "hour": hour_label,
                    "value": val
                })

                # 峰值时段：order_count 最大的时间段
                if val > peak_val:
                    peak_val = val
                    peak_start = start_label
                    peak_end = end_label

                # 夜间：18点-次日6点，即开始时间在该区间的所有 1 小时时段
                h = _parse_hour_for_slot(start_label)
                total_count += val
                if h >= 18 or h < 6:
                    night_total += val

            if total_count > 0:
                night_share_pct = round(night_total / total_count * 100, 1)

            if peak_val >= 0:
                # 峰值时段统一格式为 HH:00-HH:00，不保留秒（假定一定存在 end 字段）
                def _fmt_hhmm(t_str):
                    try:
                        s = str(t_str).strip()
                        if ":" in s:
                            h = int(s.split(":")[0])
                        else:
                            h = int(float(s))
                        return f"{h:02d}:00"
                    except Exception:
                        return str(t_str)

                start_fmt = _fmt_hhmm(peak_start)
                end_fmt = _fmt_hhmm(peak_end)
                peak_slot_label = f"{start_fmt}-{end_fmt}"

            alltime_entropy_index_value = round(self._calc_entropy(df[count_col].dropna().values), 3)

        if not chart_data:
            chart_data = [{"hour": f"{i}:00", "value": 500 if 8 <= i <= 18 else 200} for i in range(24)]
            alltime_entropy_index_value = 2.85

            # 使用默认数据时，同步给出夜间占比 & 峰值时段
            total_default = sum(d["value"] for d in chart_data)
            if total_default > 0:
                night_total_default = sum(
                    d["value"]
                    for d in chart_data
                    if (isinstance(d["hour"], str)
                        and (int(d["hour"].split(':')[0]) >= 18 or int(d["hour"].split(':')[0]) < 6))
                )
                night_share_pct = round(night_total_default / total_default * 100, 1)

            # 峰值时段：value 最大的小时段（默认数据本身已是整点）
            if chart_data:
                peak_item = max(chart_data, key=lambda x: x.get("value", 0))
                try:
                    h = int(str(peak_item["hour"]).split(':')[0])
                    start_h = h % 24
                    end_h = (h + 1) % 24
                    peak_slot_label = f"{start_h:02d}:00-{end_h:02d}:00"
                except Exception:
                    peak_slot_label = str(peak_item.get("hour", "未知"))

        # 全局保存：全时段熵值
        self.alltime_entropy_index_value = alltime_entropy_index_value

        key_metrics = [
            {"label": "夜间（18时-次日6时）占比", "value": f"{night_share_pct:.1f}%"},
            {"label": "峰值时段", "value": peak_slot_label},
        ]

        self.metrics.append(self._create_metric(
            "09", "全时段运行指数", "全时段运行水平", "时空特征",
            alltime_entropy_index_value, "熵值", "Polar", chart_data,
            key_metrics,
            "基于24小时飞行架次分布的信息熵。数值越高意味着昼夜均有飞行。",
            insight=f"<b>日间运行高度集中，夜间经济潜力初步显现但仍是短板</b>：信息熵值为{alltime_entropy_index_value}，表明飞行活动在24小时内具有一定的分布离散度，"
                    "并非完全集中于单一峰值。日间（尤其11:00-12:00为峰值）仍是绝对主力，这符合多数生产性作业的作息规律。值得关注的是，"
                    f"夜间飞行占比已达到{night_share_pct:.1f}%，这是一个积极信号，低空经济的“夜间价值”正在被挖掘，显示“夜间经济”潜力，但全天候运行能力仍是产业成熟度的关键短板。",
            suggestion="完善夜间运行标准与基础设施保障，并通过试点激励政策，稳步拓展城市物流、急救等夜间高价值场景。"
        ))

    def _compute_stability_index(self):
        """10 - 季候稳定性指数: 1 - CV of monthly flights."""
        chart_data = []
        stability_index_value = 0.0
        key_metrics = []

        # 使用 daily_flights，按月聚合后计算箱线图统计量
        if self.daily_flights is not None and not self.daily_flights.empty:
            df = self.daily_flights.copy()

            # 列名约定：| date | flight_count | weekday | is_holiday | is_workday |
            date_col = 'date' if 'date' in df.columns else df.columns[0]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])

            # 只取 YYYY-MM 作为月份标签
            df['month_label'] = df[date_col].astype(str).str.slice(0, 7)

            # 按月计算箱线图的五数概括、平均值和标准差
            grouped = df.groupby('month_label')[count_col]
            monthly_stats = grouped.agg(['min', 'max', 'median', 'mean', 'std',
                                         lambda x: x.quantile(0.25),
                                         lambda x: x.quantile(0.75)])
            # 重命名 quantile 列
            monthly_stats = monthly_stats.rename(
                columns={'<lambda_0>': 'q1', '<lambda_1>': 'q3'}
            )

            # 为每个月增加变异系数列：std / mean
            # 避免除以 0，这里对 mean<=0 的情况设为 0
            monthly_stats['cv'] = monthly_stats.apply(
                lambda r: (r['std'] / r['mean']) if r['mean'] and r['mean'] > 0 else 0,
                axis=1
            )

            # 根据「每日」飞行架次的整体均值与标准差计算变异系数 CV，得到稳定性 1 - CV
            # 这里直接使用已清洗过的 df[count_col]，不再进行额外遍历
            daily_series = df[count_col]
            mean_val = daily_series.mean()
            std_val = daily_series.std()
            cv = std_val / mean_val if mean_val and mean_val > 0 else 0
            stability_index_value = round(1 - cv, 2)

            # 计算最稳定 / 最不稳定月份（按月度 CV 最小 / 最大）
            if not monthly_stats.empty:
                most_stable_month = str(monthly_stats['cv'].idxmin())
                most_unstable_month = str(monthly_stats['cv'].idxmax())
            else:
                most_stable_month = "未知"
                most_unstable_month = "未知"

            key_metrics = [
                {"label": "最稳定月份", "value": most_stable_month},
                {"label": "最不稳定月份", "value": most_unstable_month},
                {"label": "天气影响", "value": "高"},
            ]

            for month, row in monthly_stats.iterrows():
                chart_data.append({
                    "name": month,                       # 例如 "2025-01"
                    "min": self._safe_float(row['min']),
                    "q1": self._safe_float(row['q1']),
                    "median": self._safe_float(row['median']),
                    "q3": self._safe_float(row['q3']),
                    "max": self._safe_float(row['max']),
                    "avg": round(self._safe_float(row['mean']), 1),
                    "std": round(self._safe_float(row['std']), 1),              # 每月标准差
                    "cv": self._safe_float(row['cv']),                          # 每月变异系数 = std/mean
                })

        if not chart_data:
            months = ['1月', '2月', '3月', '4月', '5月', '6月']
            chart_data = [{
                "name": m,
                "min": 300,
                "q1": 400,
                "median": 500,
                "q3": 600,
                "max": 700,
                "avg": 500,
                "std": 50,
                "cv": 0.1,
            } for m in months]
            stability_index_value = 0.92
            # 默认示例下的关键指标
            key_metrics = [
                {"label": "最稳定月份", "value": months[0]},
                {"label": "最不稳定月份", "value": months[-1]},
                {"label": "天气影响", "value": "高"},
            ]

        # 全局保存（0-1 区间）
        self.stability_index_value = stability_index_value

        self.metrics.append(self._create_metric(
            "10", "季候稳定性指数", "季候波动性", "时空特征",
            stability_index_value, "稳定性", "BoxPlot", chart_data,
            key_metrics,
            "1 - 年度每日飞行数据的变异系数。衡量对天气/季节干扰的抵抗力。",
            insight=f"<b>飞行活动受自然气候与重大事件影响显著</b>：变异系数为{stability_index_value}，反映出飞行活动在不同季节和月份之间存在中度波动。"
                    "数据清晰揭示了三大主要影响因素：一是极端天气（如7月、9月台风导致活动骤降）；二是重大活动保障（如11月全运会期间的空域管控）；"
                    "三是可能存在的作业季节性（如4月气候适宜，活动水平高）。这要求产业必须具备应对周期性波动和突发干扰的能力。",
            suggestion="构建空域动态管理与协同机制，发展适应性强的技术装备与商业模式。"
        ))

    def _compute_hub_index(self):
        """11 - 网络化枢纽指数: Network graph of regional connectivity."""
        nodes = []
        links = []
        hub_index_score = 0.0
        core_hub_name = ""
        secondary_hub_name = ""

        if self.cross_region is not None and not self.cross_region.empty:
            df = self.cross_region.copy()

            # Find columns
            start_col = 'take_off_district_code' if 'take_off_district_code' in df.columns else df.columns[1]
            end_col = 'landing_district_code' if 'landing_district_code' in df.columns else df.columns[3]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')

            # Calculate hub metrics
            regions = pd.unique(df[[start_col, end_col]].values.ravel('K'))
            hub_metrics = []

            for r in regions:
                out_flow = df[df[start_col] == r][count_col].sum()
                in_flow = df[df[end_col] == r][count_col].sum()
                total_flow = out_flow + in_flow

                # Count connections
                out_connections = df[df[start_col] == r][end_col].nunique()
                in_connections = df[df[end_col] == r][start_col].nunique()
                degree = out_connections + in_connections

                hub_metrics.append({
                    'region': r,
                    'flow': total_flow,
                    'degree': degree
                })

            hub_df = pd.DataFrame(hub_metrics)

            if not hub_df.empty:
                max_flow = hub_df['flow'].max() or 1
                # total distinct regions as a proxy for max degree (assuming a fully connected scenario)
                max_degree = 20
                hub_df['value'] = (0.6 * hub_df['degree'] / max_degree + 0.4 * hub_df['flow'] / max_flow) * 100
                hub_df = hub_df.sort_values('value', ascending=False).head(8)

                hub_index_score = round(hub_df['value'].max(), 1)

                # Create nodes
                for _, row in hub_df.iterrows():
                    if row['value'] > 70:
                        cat = 0
                        core_hub_name += self._get_district_name(self._safe_str(row['region'])) + ", "
                    elif row['value'] > 40:
                        cat = 1
                        secondary_hub_name += self._get_district_name(self._safe_str(row['region'])) + ", "
                    else:
                        cat = 2

                    region_code = self._safe_str(row['region'])
                    region_name = self._get_district_name(region_code)
                    nodes.append({
                        "name": region_name,
                        "value": round(self._safe_float(row['value']), 1),
                        "symbolSize": max(20, min(60, self._safe_float(row['value']) * 0.6)),
                        "category": cat
                    })

                # Create links between top hubs
                top_regions = set(hub_df['region'].tolist())
                for _, row in df.iterrows():
                    if row[start_col] in top_regions and row[end_col] in top_regions:
                        if row[start_col] != row[end_col]:
                            source_code = self._safe_str(row[start_col])
                            target_code = self._safe_str(row[end_col])
                            links.append({
                                "source": self._get_district_name(source_code),
                                "target": self._get_district_name(target_code),
                                "value": self._safe_float(row[count_col])
                            })

        if not nodes:
            nodes = [
                {"name": "宝安区", "value": 88, "symbolSize": 46, "category": 0},
                {"name": "南山区", "value": 76, "symbolSize": 40, "category": 0},
                {"name": "福田区", "value": 62, "symbolSize": 34, "category": 1}
            ]
            links = [
                {"source": "宝安区", "target": "南山区", "value": 45},
                {"source": "南山区", "target": "福田区", "value": 28}
            ]
            hub_index_score = 88

        chart_data = {
            "nodes": nodes,
            "links": links,
            "categories": [
                {"name": "核心枢纽"},
                {"name": "次级枢纽"},
                {"name": "一般枢纽"}
            ]
        }

        key_metrics = [
            {"label": "核心枢纽：枢纽度 (70,100]", "value": core_hub_name.rstrip(", ")},
            {"label": "次级枢纽：枢纽度(40,70]", "value": secondary_hub_name.rstrip(", ")}
        ]

        # 全局保存：网络枢纽指数得分（0-100）
        self.hub_index_score = hub_index_score

        self.metrics.append(self._create_metric(
            "11", "网络化枢纽指数", "枢纽连接度", "时空特征",
            hub_index_score, "枢纽度", "Graph", chart_data,
            key_metrics,
            "基于起降点航线网络的连接度与流量加权得分，识别航线网络中的关键节点。",
            insight=f"<b>骨干枢纽节点清晰，网络层级初步形成，但“毛细血管”网络有待丰富</b>: 枢纽度高达{hub_index_score}，且龙岗、龙华等区已显现出核心枢纽特征（枢纽度>70），"
                    "表明深圳低空飞行网络并非均质化分布，而是形成了层次化的“枢纽-辐射”结构。核心枢纽承担了大部分的流量集散与航线连接功能，这是网络效率的体现。"
                    "然而，当前网络可能过度依赖少数高等级枢纽，连接众多末端起降点的“最后一公里”航线网络（毛细血管）密度和通达性可能不足，限制了网络服务的覆盖深度与便捷性。",
            suggestion="优化网络结构,提升核心枢纽的综合服务能力,加密布局轻型起降点以丰富网络节点,推动航线网络的商业化与公交化运营试点。"
        ))

    def _compute_efficiency_index(self):
        """12 - 单机作业效能指数: Flights per unique SN."""
        efficiency_index = 0.0

        total_flights = 0
        total_sn = 0
        top50_flights = 0
        top50_sn_total = 0

        if self.annual_flights is not None and not self.annual_flights.empty:
            count_col = 'flight_count' if 'flight_count' in self.annual_flights.columns else self.annual_flights.columns[-1]
            total_flights = self._safe_float(pd.to_numeric(self.annual_flights[count_col], errors='coerce').sum())

        if self.annual_sn is not None and not self.annual_sn.empty:
            sn_col = 'sn_count_year' if 'sn_count_year' in self.annual_sn.columns else self.annual_sn.columns[-1]
            total_sn = self._safe_float(pd.to_numeric(self.annual_sn[sn_col], errors='coerce').sum())

        # 计算 TOP50 效益：分子来自 top50_entities（flight_count 总和），分母来自 top50_sn
        if self.top50_entities is not None and not self.top50_entities.empty:
            df_top50 = self.top50_entities.copy()
            ent_count_col = 'flight_count' if 'flight_count' in df_top50.columns else df_top50.columns[-1]
            df_top50[ent_count_col] = pd.to_numeric(df_top50[ent_count_col], errors='coerce')
            top50_flights = self._safe_float(df_top50[ent_count_col].sum())

        if self.top50_sn is not None and not self.top50_sn.empty:
            df_top50_sn = self.top50_sn.copy()
            # 优先使用 sn_count_year 或包含 "sn" 的列，否则退回最后一列
            if 'sn_count_year' in df_top50_sn.columns:
                top50_sn_col = 'sn_count_year'
            else:
                sn_cols = [c for c in df_top50_sn.columns if 'sn' in str(c).lower()]
                top50_sn_col = sn_cols[0] if sn_cols else df_top50_sn.columns[-1]
            df_top50_sn[top50_sn_col] = pd.to_numeric(df_top50_sn[top50_sn_col], errors='coerce')
            top50_sn_total = self._safe_float(df_top50_sn[top50_sn_col].sum())

        if total_sn > 0:
            efficiency_index = round(total_flights / total_sn, 2)  # 2 decimal places
        else:
            efficiency_index = 0.0

        if top50_sn_total > 0:
            top50_efficiency = round(top50_flights / top50_sn_total, 2)
        else:
            top50_efficiency = 0.0

        # Ensure efficiency_score is properly rounded to avoid floating point precision issues
        efficiency_index = round(efficiency_index, 2)

        # 为展示效果对效率取自然对数（ln），仅对正值取对数，并缩放到 0-10 区间
        ln_efficiency = float(np.log(efficiency_index)) if efficiency_index > 0 else 0.0
        ln_top50_efficiency = float(np.log(top50_efficiency)) if top50_efficiency > 0 else 0.0
        efficiency_score = round(ln_efficiency / ln_top50_efficiency * 100, 2) if ln_top50_efficiency > 0 else 0.0

        chart_data = [
            {"name": "平均效益", "value": f"{ln_efficiency:.2f}"},
            {"name": "TOP50效益", "value": f"{ln_top50_efficiency:.2f}"}
        ]

        key_metrics = [
            {"label": "平均架次/年", "value": f"{efficiency_index:.2f}"},
            {"label": "TOP50企业平均架次/年", "value": f"{top50_efficiency:.2f}"}
        ]

        # 全局保存：单机作业效能得分（直接作为 score 使用）
        self.efficiency_score = efficiency_score

        self.metrics.append(self._create_metric(
            "12", "单机作业效能指数", "资产周转率", "效率与质量",
            efficiency_score, "指数", "Gauge", chart_data,
            key_metrics,
            "每架活跃无人机每年的平均飞行次数。",
            insight=f"<b>整体资产利用率偏低，但头部企业已探索出高效运营范式，市场效率分化显著</b>：平均每架活跃航空器年飞行架次仅为{efficiency_index:.2f}次，表明从整体看，"
                    f"大量的航空器资产仍处于低频率、间歇性的使用状态。然而，TOP50企业的均值高达{top50_efficiency:.2f}架次/年，这揭示了头部企业通过机队专业化管理、"
                    "任务精准调度和商业模式创新，已成功实现了资产的高频、集约化利用。巨大的差距（相差近23倍）凸显了产业内部运营管理水平的两极分化，"
                    "整体效能被大量低效运力所稀释。",
            suggestion="推广头部企业最佳实践，探索建立基于运营效能的激励与约束机制，提升全行业资本使用效率。"
        ))

    def _compute_long_endurance_index(self):
        """13 - 长航时任务占比指数: Percentage of flights > 20 minutes."""
        weighted_avg_duration = 0.0
        chart_data = []
        long_pct_value = 0.0

        if self.duration_ranges is not None and not self.duration_ranges.empty:
            df = self.duration_ranges.copy()

            range_col = 'duration_range_id' if 'duration_range_id' in df.columns else df.columns[1]
            count_col = 'total_flight_count' if 'total_flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])
            total = df[count_col].sum()
            df['proportion'] = df[count_col] / total

            weighted_sum = 0.0
            n_rows = len(df)

            for i, (_, row) in enumerate(df.iterrows()):
                prop = self._safe_float(row['proportion'])
                # 区间中值：最后一个或含 '+' 的区间用 100，否则解析 "a-b" 取 (a+b)/2
                raw = self._safe_str(row[range_col]).strip()
                is_last = (i == n_rows - 1)
                if is_last or '+' in raw or raw.lower().startswith('>'):
                    mid = 100.0
                else:
                    parts = raw.replace(' ', '').split('-')
                    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                        mid = (float(parts[0]) + float(parts[1])) / 2.0
                    else:
                        mid = 0.0
                weighted_sum += mid * prop

                chart_data.append({
                    "name": f"{raw} min",
                    "value": f"{self._safe_float(row[count_col])}",
                    "desc": f"架次（占比：{round(prop * 100, 1)}%）",
                    "fill": "#0ea5e9"
                })

            weighted_avg_duration = round(weighted_sum, 1)

            # Calculate long endurance percentage (assuming ranges like "10-20", "20-30", "30-40", etc., where the
            # first number > 10 is long)
            long_mask = df[range_col].astype(str).str.contains(r'\+') | (
                df[range_col].astype(str).str.match(r'^\d{2,}-') &
                df[range_col].astype(str).str.split('-').str[0].str.extract(r'(\d+)')[0].astype(float).ge(10)
            )
            long_flights = df[long_mask][count_col].sum()
            long_pct_value = round(self._safe_float(long_flights) / total * 100, 1) if total > 0 else 0

        if not chart_data:
            chart_data = [
                {"name": "< 10分钟", "value": 4000, "fill": "#94a3b8"},
                {"name": "10-30分钟", "value": 3000, "fill": "#64748b"},
                {"name": "30-60分钟", "value": 1500, "fill": "#0ea5e9"},
                {"name": "> 60分钟", "value": 500, "fill": "#0284c7"}
            ]
            long_pct_value = 22.2
            weighted_avg_duration = 0.0

        key_metrics = [
            {"label": ">10分钟占比", "value": f"{long_pct_value}%"},
            {"label": "加权平均时长", "value": f"{weighted_avg_duration}分钟"},
        ]

        # 全局保存：长航时任务占比（0-100）
        self.long_pct_value = long_pct_value

        self.metrics.append(self._create_metric(
            "13", "长航时任务占比指数", "高价值任务占比", "效率与质量",
            long_pct_value, "%", "Funnel", chart_data,
            key_metrics,
            "飞行时长超过10分钟的飞行架次比例。",
            insight=f"<b>高价值复杂作业尚处萌芽期，作业模式仍以短途、轻量为主</b>：飞行时长超过10分钟的任务比例仅为{long_pct_value}%，"
                    f"加权平均时长仅为{weighted_avg_duration}分钟，表明当前深圳低空经济活动的主体仍是短航时、快速响应型的轻量级任务，亟待向纵深、高附加值场景突破。",
            suggestion="集中资源攻克技术与管理瓶颈，培育长航时应用生态。"
        ))

    def _compute_coverage_index(self):
        """14 - 广域覆盖能力指数: Weighted average flight distance."""
        chart_data = []
        weight_avg = 0.0
        longterm_pct_value = 0.0

        if self.distance_ranges is not None and not self.distance_ranges.empty:
            df = self.distance_ranges.copy()

            range_col = 'distance_range_id' if 'distance_range_id' in df.columns else df.columns[1]
            count_col = 'total_flight_count' if 'total_flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])

            long_term_flights = 0.0

            for _, row in df.iterrows():
                name_str = self._safe_str(row[range_col])
                count_val = self._safe_float(row[count_col])

                chart_data.append({
                    "name": name_str,
                    "value": count_val,
                })

                # 解析区间起始值，如 "0-10" 中的 0、"10-20" 中的 10；
                # 若起始值 >= 2，则计入长航程累计
                start_str = str(name_str).split('-')[0]
                try:
                    start_val = float(''.join(ch for ch in start_str if (ch.isdigit() or ch == '.')))
                except ValueError:
                    start_val = 0.0
                if start_val >= 2:
                    long_term_flights += count_val

            # Calculate weighted average (using midpoints)
            # This is a rough estimate - actual midpoints depend on range definitions
            total = df[count_col].sum()
            if total > 0:
                weights = df[count_col].fillna(0).values
                # Assume ranges are roughly 0-1, 1-5, 5-10, 10-20, 20+ km
                midpoints = [20 if i == len(weights) - 1 else (i + j) / 2 for i, j in zip(range(0, len(weights)), range(1, len(weights) + 1))]
                weight_avg = round(np.nansum(weights * midpoints) / total, 2)
                longterm_pct_value = round(long_term_flights / total * 100, 1)

        if not chart_data:
            chart_data = [
                {"name": "0-1km", "value": 30},
                {"name": "1-5km", "value": 45},
                {"name": "5-15km", "value": 15},
                {"name": "15km+", "value": 10}
            ]
            weight_avg = 12.5
            longterm_pct_value = 0.0

        key_metrics = [
            {"label": "平均航程", "value": f"{weight_avg}km"},
            {"label": "超视距飞行架次占比(≥2km)", "value": f"{longterm_pct_value}%"},
        ]

        # 全局保存：超视距飞行占比（0-100）
        self.longterm_pct_value = longterm_pct_value

        self.metrics.append(self._create_metric(
            "14", "广域覆盖能力指数", "超视距运行水平", "效率与质量",
            longterm_pct_value, "%", "Histogram", chart_data,
            key_metrics,
            "飞行里程超过2km（超视距）的飞行架次比例。",
            insight=f"<b>超视距运行已成常态，活动半径显著拓展，网络化运行基础扎实</b>：超过{longterm_pct_value}%的飞行架次为航程超过2公里的超视距飞行，平均航程达{weight_avg}公里，"
                    "这是一个里程碑式的积极信号。它表明，低空运行已普遍突破目视范围的物理限制，依赖于数据链路的超视距运行（BVLOS） 已成为主流模式。"
                    "这不仅极大地拓展了单次飞行的作业半径和经济辐射范围，更是构建规模化、网络化低空交通系统的先决条件。",
            suggestion="完善超视距运行法规标准，加快建设城市级智能融合基础设施。"
        ))

    def _compute_quality_index(self):
        """15 - 任务完成质量指数: Task completion quality with control chart."""
        # Calculate completion rate
        completion_pct_value = 92.3  # Default

        if self.annual_effective is not None and self.annual_flights is not None:
            eff_col = 'distinct_order_count' if 'distinct_order_count' in self.annual_effective.columns else self.annual_effective.columns[-1]
            flight_col = 'flight_count' if 'flight_count' in self.annual_flights.columns else self.annual_flights.columns[-1]

            effective = pd.to_numeric(self.annual_effective[eff_col], errors='coerce').sum()
            total = pd.to_numeric(self.annual_flights[flight_col], errors='coerce').sum()

            if total > 0:
                completion_pct_value = round(effective / total * 100, 1)

        # Generate control chart data structure（按月份展示：1月 ~ 12月 的 mock 数据）
        months = [f"{m}月" for m in range(1, 13)]

        traj_data = [
            {
                "time": months[i],
                "deviation": round(np.random.uniform(-0.15, 0.25), 2),
                "mean": 0.0,
                "ucl": 0.25,
                "lcl": -0.25,
            }
            for i in range(12)
        ]

        tqi_history = [
            {
                "time": months[i],
                "tqi": round(completion_pct_value + np.random.uniform(-3, 3), 1),
                "mean": 90,
                "ucl": 98,
                "lcl": 75,
            }
            for i in range(12)
        ]

        plan_actual = [
            {
                "time": months[i],
                "actual": int(500 * (completion_pct_value / 100) + np.random.randint(-20, 20)),
                "planned": 500 + np.random.randint(-30, 30),
            }
            for i in range(12)
        ]

        chart_data = {
            "latestTqi": completion_pct_value,
            "trajData": traj_data,
            "tqiHistory": tqi_history,
            "planActual": plan_actual
        }

        # 全局保存：任务完成率（0-100）
        self.completion_pct_value = completion_pct_value

        self.metrics.append(self._create_metric(
            "15", "任务完成质量指数", "任务达成率", "效率与质量",
            completion_pct_value, "%", "ControlChart", chart_data,
            [{"label": "实际任务有效飞行占比", "value": f"{completion_pct_value}%"}],
            "实际完成的有效飞行架次与计划报备架次的比率。（备注：当前使用实际飞行任务有效架次占比作为结果展示，后续可根据数据情况调整为计划与实际的对比分析）",
            insight="若指数值为高值，则运行高度规范，计划与执行高度统一，产业进入精细化、可预测的管理阶段。从申请、任务规划到飞行执行的整个链条"
                    "实现了高效的数字化协同与闭环管理。运营主体自律性强，监管规则得到普遍遵守，系统运行的可预测性和可靠性高。若指数值为中值，"
                    "运行基本规范但存在波动，计划性与灵活性并存，产业处于规模扩张与管理提升的磨合期。监管框架和市场主体已建立起基本的计划申报与"
                    "执行意识；然而，由于任务复杂性增加、突发需求、空域动态调整或部分运营者能力不足，计划与执行间存在一定偏差。这可能是产业在"
                    "快速发展中，需求的动态性与管理刚性之间矛盾的体现，需要更精细、更弹性的管理体系来适应。若指数值为低值，则运行规范性不足，"
                    "计划与执行脱节严重，产业发展存在无序与风险隐患。",
            suggestion="由于暂未获取完整的飞行计划报备数据，此指数当前仅能基于模拟示例数据开展指标展示与逻辑演示，暂不具备形成有效策略启示的条件。"
        ))

    def _compute_micro_circulation_index(self):
        """16 - 城市微循环渗透指数: Cross-region connectivity."""
        chart_data = []
        micro_index_value = 0.0
        total_cross = 0
        popular_pair = "待计算"
        pair_count = 0

        if self.cross_region is not None and not self.cross_region.empty:
            df = self.cross_region.copy()

            start_col = 'take_off_district_code' if 'take_off_district_code' in df.columns else df.columns[1]
            end_col = 'landing_district_code' if 'landing_district_code' in df.columns else df.columns[3]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')

            # Filter cross-region only
            cross_df = df[df[start_col] != df[end_col]]

            total_cross = cross_df[count_col].sum()
            total_all = df[count_col].sum()
            pair_count = len(cross_df)

            if total_all > 0:
                cross_ratio = total_cross / total_all
                micro_index_value = round(cross_ratio * np.log1p(pair_count/2), 3)

            # Create chord diagram data - need to aggregate by region pairs
            # Group by source-target pairs and sum values
            cross_df['source_name'] = cross_df[start_col].apply(lambda x: self._get_district_name(str(x)))
            cross_df['target_name'] = cross_df[end_col].apply(lambda x: self._get_district_name(str(x)))

            # Aggregate by source-target pairs
            aggregated = cross_df.groupby(['source_name', 'target_name'])[count_col].sum().reset_index()
            
            # Filter out very small values and sort

            # 归一化 value 到 0-100 区间，便于可视化（Chord 图线宽），并同时找出“最热门航线”

            if not aggregated.empty:
                vals = aggregated[count_col].astype(float)
                v_min = vals.min()
                v_max = vals.max()

                # 找到 count 最大的那一对 (source_name, target_name)
                max_idx = vals.idxmax()
                max_row = aggregated.loc[max_idx]
                popular_pair = f"{self._safe_str(max_row['source_name'])}-{self._safe_str(max_row['target_name'])}"

                for _, row in aggregated.iterrows():
                    raw_val = self._safe_float(row[count_col])
                    if raw_val <= 0:
                        continue

                    if v_max > v_min:
                        norm_val = raw_val / v_max * 100.0
                    else:
                        # 所有值相等时，统一给一个中等值
                        norm_val = 50.0

                    chart_data.append({
                        "x": str(row['source_name']),
                        "y": str(row['target_name']),
                        "value": norm_val
                    })

                if not chart_data:
                    chart_data = [
                        {"x": "A区", "y": "B区", "value": 80},
                        {"x": "B区", "y": "C区", "value": 50},
                        {"x": "A区", "y": "C区", "value": 30}
                    ]
                    micro_index_value = 0.65
                    popular_pair = "A区-B区"

        # 全局保存：城市微循环指数原始值
        self.micro_index_value = micro_index_value

        key_metrics = [
            {"label": "跨区流量", "value": f"{total_cross}架次"},
            {"label": "热门航线", "value": popular_pair},
            {"label": "连通对", "value": f"{pair_count // 2}个"},
        ]

        self.metrics.append(self._create_metric(
            "16", "城市微循环渗透指数", "末端连通度", "创新与融合",
            micro_index_value, "连通度", "Chord", chart_data,
            key_metrics,
            "衡量跨区飞行的密度和数量,连接不同行政区的网络化程度，充当城市的'毛细血管'。",
            insight=f"<b>跨区“空中走廊”已初步贯通，但城市末端“毛细循环”尚未激活，渗透深度不足</b>：连通度为{micro_index_value}，核心跨区流量达{total_cross:,}架次，"
                    "特别是龙岗-龙华这类产业核心区间的航线成为热点，标志着连接关键功能区的低空“主动脉”网络已具雏形。然而，"
                    "指数名称所指向的“微循环”——即服务于楼宇、社区、商业综合体的末端精细化即时配送、服务与应急响应网络——其活跃度与密度数据尚不显著。"
                    "当前网络更侧重于区域间的批量物流或通勤，距离实现与城市肌理深度嵌合的“毛细血管”式渗透，仍有较大差距。",
            suggestion="在骨干网络基础上，以场景创新驱动末端渗透，开展城市末端场景的“特许试点”，推动建筑设计与低空接入的融合，构建“最后一公里”的共享服务网络。"
        ))

    def _compute_airspace_index(self):
        """17 - 立体空域利用效能指数: Altitude layer utilization entropy."""
        chart_data = []
        airspace_entropy_index_value = 0.0
        main_altitude = "待计算"
        other_altitude_share_pct = 0.0

        if self.height_ranges is not None and not self.height_ranges.empty:
            df = self.height_ranges.copy()

            range_col = 'height_range_id' if 'height_range_id' in df.columns else df.columns[1]
            dur_col = 'total_flight_duration_seconds' if 'total_flight_duration_seconds' in df.columns else df.columns[-1]

            df[dur_col] = pd.to_numeric(df[dur_col], errors='coerce')
            # 将秒转换为分钟，并保留 1 位小数
            df[dur_col] = (df[dur_col] / 60.0).round(1)
            df = df.dropna(subset=[dur_col])

            for _, row in df.iterrows():
                chart_data.append({
                    "name": self._safe_str(row[range_col]),
                    "value": self._safe_float(row[dur_col])
                })

            airspace_entropy_index_value = round(self._calc_entropy(df[dur_col].dropna().values), 3)

            # 主要高度层：总时长（分钟）最大的高度区间
            try:
                max_idx = df[dur_col].idxmax()
                max_row = df.loc[max_idx]
                raw_alt = self._safe_str(max_row[range_col])
                main_altitude = raw_alt if raw_alt.endswith('m') else f"{raw_alt}米"

                total_dur = df[dur_col].sum()
                main_dur = self._safe_float(max_row[dur_col])
                if total_dur > 0 and main_dur >= 0:
                    main_share = main_dur / total_dur
                    other_altitude_share_pct = round((1 - main_share) * 100, 1)
            except Exception:
                main_altitude = "待计算"
                other_altitude_share_pct = 0.0

        if not chart_data:
            chart_data = [
                {"name": "0-50m", "value": 1000},
                {"name": "50-100m", "value": 3000},
                {"name": "100-150m", "value": 4500},
                {"name": "150-200m", "value": 2000}
            ]
            airspace_entropy_index_value = 0.72
            main_altitude = "100-150米"
            total_default = sum(item["value"] for item in chart_data)
            main_default = 4500
            if total_default > 0:
                other_altitude_share_pct = round((1 - main_default / total_default) * 100, 1)

        # For GroupedBar, need district breakdown if available
        if self.district_height is not None and not self.district_height.empty:
            # Create grouped bar data structure
            df = self.district_height.copy()
            district_codes = df['district_code'].unique().tolist() if 'district_code' in df.columns else []
            # Map district codes to names
            districts = [self._get_district_name(code) for code in district_codes]
            altitudes = df['height_range_id'].unique().tolist() if 'height_range_id' in df.columns else []

            dur_col = 'total_flight_duration_seconds' if 'total_flight_duration_seconds' in df.columns else df.columns[-1]
            # 将秒转换为分钟，并保留 1 位小数
            df[dur_col] = (pd.to_numeric(df[dur_col], errors='coerce') / 60.0).round(1)

            data_points = []
            for _, row in df.iterrows():
                try:
                    alt_idx = altitudes.index(row['height_range_id']) if 'height_range_id' in df.columns else 0
                    dist_code = row['district_code'] if 'district_code' in df.columns else district_codes[0] if district_codes else ''
                    dist_idx = district_codes.index(dist_code) if dist_code in district_codes else 0
                    data_points.append([alt_idx, dist_idx, self._safe_float(row[dur_col])])
                except (ValueError, KeyError):
                    continue

            if districts and altitudes and data_points:
                chart_data = {
                    "districts": districts,
                    "altitudes": altitudes,
                    "data": data_points
                }

        # 全局保存：空域高度熵值
        self.airspace_entropy_index_value = airspace_entropy_index_value

        key_metrics = [
            {"label": "主要高度层", "value": main_altitude},
            {"label": "其他高度层合计占比", "value": f"{other_altitude_share_pct:.1f}%"},
        ]

        self.metrics.append(self._create_metric(
            "17", "立体空域利用效能指数", "垂直空域利用率", "创新与融合",
            airspace_entropy_index_value, "熵值", "GroupedBar", chart_data,
            key_metrics,
            "不同高度层飞行分布（飞行时长）的均匀度。",
            insight=f"<b>空域利用呈现“高度集中、初步分层”特征，精细化、协同化管理潜力巨大</b>：熵值高达{airspace_entropy_index_value}，"
                    f"且{other_altitude_share_pct:.1f}%的飞行活动分布在100米以上高度层，"
                    "这表明深圳的空域利用已突破低高度拥挤，呈现出显著的立体分层利用态势。这为不同速度、不同任务类型的航空器（提供了协同运行的空间基础。"
                    "然而，主要活动仍集中在[0,100)米高度带，更高空域的利用效能和差异化规则有待开发，立体空间的“黄金分层”尚未实现效率最大化。",
            suggestion="从“平面分区”迈向“立体网格”的动态空域管理，开展基于高度层的差异化运行规则研究与实践。"
        ))

    def _compute_production_consumption_index(self):
        """18 - 生产/消费属性指数: Workday vs weekend ratio."""
        chart_data = []
        production_consumption_ratio_value = 1.0

        workday_avg = 0
        weekend_avg = 0

        if self.workday_avg is not None and not self.workday_avg.empty:
            col = 'flight_count_workday_per_day' if 'flight_count_workday_per_day' in self.workday_avg.columns else self.workday_avg.columns[-1]
            workday_avg = pd.to_numeric(self.workday_avg[col], errors='coerce').mean()

        if self.weekend_avg is not None and not self.weekend_avg.empty:
            col = 'flight_count_weekend_per_day' if 'flight_count_weekend_per_day' in self.weekend_avg.columns else self.weekend_avg.columns[-1]
            weekend_avg = pd.to_numeric(self.weekend_avg[col], errors='coerce').mean()

        if weekend_avg > 0:
            production_consumption_ratio_value = round(workday_avg / weekend_avg, 2)

        # Generate calendar data from daily_flights
        if self.daily_flights is not None and not self.daily_flights.empty:
            df = self.daily_flights.copy()
            date_col = 'date' if 'date' in df.columns else df.columns[0]
            count_col = 'flight_count' if 'flight_count' in df.columns else df.columns[1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])

            # Keep original values for display
            # Calculate min/max for color scaling - these will be used by frontend
            min_val = df[count_col].min() if len(df) > 0 else 0
            max_val = df[count_col].max() if len(df) > 0 else 1000

            # Store original values - frontend will need to handle large values dynamically
            # We'll add metadata to help frontend calculate color scale
            for _, row in df.iterrows():
                val = self._safe_float(row[count_col])
                if val > 0:  # Only add non-zero values
                    chart_data.append({
                        "date": self._safe_str(row[date_col]),
                        "value": val  # Original value - frontend should use this for display and color
                    })
            
            # Add metadata for color scaling (will be stored separately if needed)
            # For now, frontend component needs to be updated to handle dynamic ranges

            # Recalculate workday/weekend averages from actual data if not already computed
            if workday_avg == 0 or weekend_avg == 0:
                df['is_workday'] = df[date_col].apply(lambda x: self._is_workday(x))
                workday_data = df[df['is_workday'] == True][count_col]
                weekend_data = df[df['is_workday'] == False][count_col]
                if len(workday_data) > 0:
                    workday_avg = workday_data.mean()
                if len(weekend_data) > 0:
                    weekend_avg = weekend_data.mean()
                if weekend_avg > 0:
                    production_consumption_ratio_value = round(workday_avg / weekend_avg, 2)

        if not chart_data:
            # Generate sample calendar data with reasonable values
            for i in range(365):
                date = datetime(2025, 1, 1) + pd.Timedelta(days=i)
                is_weekend = date.weekday() >= 5
                base = 600 if is_weekend else 850
                chart_data.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "value": base + np.random.randint(-100, 100)
                })
            if production_consumption_ratio_value == 1.0:
                production_consumption_ratio_value = 1.4

        prod_type = "生产型" if production_consumption_ratio_value > 1.2 else ("消费型" if production_consumption_ratio_value < 0.8 else "混合型")

        key_metrics = [{"label": "类型", "value": prod_type}, {"label": "工作日均值（飞行架次）", "value": f"{self._safe_float(workday_avg):.0f}"}]

        # 全局保存：生产/消费属性比值
        self.production_consumption_ratio_value = production_consumption_ratio_value

        self.metrics.append(self._create_metric(
            "18", "低空经济\"生产/消费\"属性指数", "经济活动属性", "创新与融合",
            production_consumption_ratio_value, "比率", "Calendar", chart_data,
            key_metrics,
            "工作日日均架次与周末日均架次的比率。当比率>1.2：生产型；<0.8：消费型；[0.8,1.2]混合型。",
            insight=f"<b>产业属性呈现“均衡混合”特征，兼具生产工具与消费服务双重价值</b>：比值为{production_consumption_ratio_value}，清晰地落在“混合型”区间，表明深圳低空经济的活动在"
                    "工作日（生产驱动）与周末（消费及公共服务驱动）之间保持了良好的平衡。这打破了“低空经济仅是生产工具”或“仅是娱乐消费”的单一认知，"
                    f"显示出产业已深度融入城市运行的全周期。工作日{self._safe_float(workday_avg):.0f}的均值体现了其作为生产要素的扎实基本盘；而周末相近的活跃度则揭示了其在文旅娱乐、个人体验、城市民生。",
            suggestion="实施“稳生产、促消费、优服务”融合策略，在升级生产应用的同时，积极培育消费业态与拓展公共服务场景。"
        ))

    def _compute_night_economy_index(self):
        """19 - 低空夜间经济指数: Night flight percentage (19:00-06:00)."""
        chart_data = []
        night_pct_value = 0.0

        if self.hourly_flights is not None and not self.hourly_flights.empty:
            df = self.hourly_flights.copy()

            start_col = 'slot_start_time' if 'slot_start_time' in df.columns else df.columns[1]
            # Prefer order_count (annual total) over order_count_per_day
            count_col = None
            # First try to find order_count (annual total, not per_day)
            for col in df.columns:
                if 'order_count' in col.lower() and 'per_day' not in col.lower() and 'per' not in col.lower():
                    count_col = col
                    break
            # If not found, try flight_count
            if count_col is None:
                for col in df.columns:
                    if 'flight_count' in col.lower() and 'per_day' not in col.lower() and 'per' not in col.lower():
                        count_col = col
                        break
            # If still not found, use second-to-last column (usually the annual total, not per_day)
            if count_col is None:
                count_col = df.columns[-2] if len(df.columns) > 2 else df.columns[-1]

            df[count_col] = pd.to_numeric(df[count_col], errors='coerce')
            df = df.dropna(subset=[count_col])  # Remove rows with no count data

            # Parse hour from time slot (handle formats like "00:00:00", "00", etc.)
            def parse_hour(t):
                try:
                    t_str = str(t).strip()
                    if ':' in t_str:
                        hour_str = t_str.split(':')[0]
                        return int(hour_str)
                    # Try direct conversion
                    return int(float(t_str))
                except:
                    return 12

            df['hour'] = df[start_col].apply(parse_hour)

            total = df[count_col].sum()
            # Night hours: 19:00-23:59 and 00:00-06:59
            night_mask = (df['hour'] >= 18) | (df['hour'] < 6)
            night_df = df[night_mask].copy()
            night_total = night_df[count_col].sum()

            night_pct_value = round(night_total / total * 100, 1) if total > 0 else 0

            # 夜间峰值时段：夜间时段中飞行架次最大的起止时间段
            night_peak_slot = "待计算"
            if not night_df.empty:
                # 先按 hour 汇总，找到夜间小时中的峰值
                hourly_night = night_df.groupby('hour')[count_col].sum().reset_index()
                peak_row = hourly_night.loc[hourly_night[count_col].idxmax()]
                peak_h = int(self._safe_float(peak_row['hour']))
                start_h = peak_h % 24
                end_h = (peak_h + 1) % 24
                night_peak_slot = f"{start_h:02d}:00-{end_h:02d}:00"

            # Create chart data for all 24 hours, marking night hours
            for hour in range(24):
                hour_data = df[df['hour'] == hour]
                hour_total = hour_data[count_col].sum() if not hour_data.empty else 0
                chart_data.append({
                    "hour": float(hour),
                    "value": self._safe_float(hour_total),
                    "isNight": hour >= 19 or hour < 7
                })

        if not chart_data:
            for h in range(24):
                chart_data.append({
                    "hour": float(h),
                    "value": np.random.randint(300, 600) if (h >= 19 or h < 7) else np.random.randint(500, 800),
                    "isNight": h >= 19 or h < 7
                })
            night_pct_value = 18.5
            night_peak_slot = "22:00-23:00"

        key_metrics = [
            {"label": "夜间占比", "value": f"{night_pct_value}%"},
            {"label": "夜间峰值时段", "value": night_peak_slot},
        ]

        # 全局保存：夜间飞行占比（0-100）
        self.night_pct_value = night_pct_value

        self.metrics.append(self._create_metric(
            "19", "低空夜间经济指数", "夜间活跃度", "创新与融合",
            night_pct_value, "%", "Wave", chart_data,
            key_metrics,
            "发生在18:00至06:00之间的飞行架次占总飞行架次比例。",
            insight=f"<b>夜间运行已形成稳定基本盘，“黄金两小时”凸显商业与民生价值</b>：夜间飞行占比达{night_pct_value}%，表明低空经济已突破“日出而作、日落而息”的传统作业局限。"
                    f"峰值出现在{night_peak_slot}，这恰好对应晚高峰时段，强烈指向其在缓解地面交通压力、满足即时性民生需求（如晚餐配送、紧急购药）方面扮演了独特角色。"
                    "夜间运行不仅是生产时间的简单延伸，更是开辟了服务城市夜间经济、满足特定时效需求的新价值赛道。",
            suggestion="打造低空夜间服务示范区，建立夜间运行安全与环境友好标准，并鼓励创新夜间专属服务产品，塑造产业竞争新优势。"
        ))

    def _compute_leading_enterprise_index(self):
        """20 - 头部企业"领航"指数: Top enterprise performance radar."""
        global leading_entity_name, avg_total_score
        chart_data = []
        leading_score = 0.0

        # 统一设置 Top N 的企业数量
        top_num = 5

        if self.top50_entities is not None and not self.top50_entities.empty:
            base_df = self.top50_entities.copy()

            # 基础表：年度 TOP50 企业架次 | year | entity_id | entity_name | flight_count |
            name_col = 'entity_name' if 'entity_name' in base_df.columns else 'entity_id'
            ent_col = 'entity_id' if 'entity_id' in base_df.columns else base_df.columns[1]
            flights_col = 'flight_count' if 'flight_count' in base_df.columns else base_df.columns[-1]

            base_df[flights_col] = pd.to_numeric(base_df[flights_col], errors='coerce')
            base_df = base_df.dropna(subset=[flights_col])
            base_df = base_df.sort_values(flights_col, ascending=False).head(top_num)

            if not base_df.empty:
                # TopN 企业及其 ID 列表（字符串）
                entity_ids = [self._safe_str(e) for e in base_df[ent_col].tolist()]
                # eid -> 展示名（name_col 对应的中文名，供雷达图图例/键使用）
                entity_id_to_name = {
                    self._safe_str(row[ent_col]): self._safe_str(row[name_col])
                    for _, row in base_df.iterrows()
                }

                # ---------- 架次（flight_count） ----------
                flights_raw = {self._safe_str(row[ent_col]): self._safe_float(row[flights_col])
                               for _, row in base_df.iterrows()}

                # ---------- 时长（top50_duration.total_duration） ----------
                duration_raw = {eid: 0.0 for eid in entity_ids}
                if self.top50_duration is not None and not self.top50_duration.empty:
                    dur_df = self.top50_duration.copy()
                    dur_ent_col = 'entity_id' if 'entity_id' in dur_df.columns else dur_df.columns[1]
                    tot_dur_col = 'total_duration' if 'total_duration' in dur_df.columns else dur_df.columns[-3]
                    dur_df[tot_dur_col] = pd.to_numeric(dur_df[tot_dur_col], errors='coerce')
                    dur_agg = dur_df.groupby(dur_ent_col)[tot_dur_col].sum()
                    for eid in entity_ids:
                        if eid in dur_agg.index:
                            duration_raw[eid] = self._safe_float(dur_agg.loc[eid])

                # ---------- 里程（top50_distance.total_distance） ----------
                distance_raw = {eid: 0.0 for eid in entity_ids}
                if self.top50_distance is not None and not self.top50_distance.empty:
                    dist_df = self.top50_distance.copy()
                    dist_ent_col = 'entity_id' if 'entity_id' in dist_df.columns else dist_df.columns[1]
                    tot_dist_col = 'total_distance' if 'total_distance' in dist_df.columns else dist_df.columns[-3]
                    dist_df[tot_dist_col] = pd.to_numeric(dist_df[tot_dist_col], errors='coerce')
                    dist_agg = dist_df.groupby(dist_ent_col)[tot_dist_col].sum()
                    for eid in entity_ids:
                        if eid in dist_agg.index:
                            distance_raw[eid] = self._safe_float(dist_agg.loc[eid])

                # ---------- 活跃度（top50_sn.sn_count） ----------
                active_raw = {eid: 0.0 for eid in entity_ids}
                if self.top50_sn is not None and not self.top50_sn.empty:
                    sn_df = self.top50_sn.copy()
                    sn_ent_col = 'entity_id' if 'entity_id' in sn_df.columns else sn_df.columns[1]
                    sn_col = 'sn_count' if 'sn_count' in sn_df.columns else sn_df.columns[-1]
                    sn_df[sn_col] = pd.to_numeric(sn_df[sn_col], errors='coerce')
                    sn_agg = sn_df.groupby(sn_ent_col)[sn_col].sum()
                    for eid in entity_ids:
                        if eid in sn_agg.index:
                            active_raw[eid] = self._safe_float(sn_agg.loc[eid])

                # ---------- 夜间占比（top5_hourly_flight.order_count） ----------
                night_raw = {eid: 0.0 for eid in entity_ids}
                if self.top5_hourly_flight is not None and not self.top5_hourly_flight.empty:
                    nh_df = self.top5_hourly_flight.copy()
                    nh_ent_col = 'entity_id' if 'entity_id' in nh_df.columns else nh_df.columns[1]
                    start_col = 'slot_start_time' if 'slot_start_time' in nh_df.columns else nh_df.columns[2]
                    order_col = 'order_count' if 'order_count' in nh_df.columns else nh_df.columns[-1]

                    nh_df[order_col] = pd.to_numeric(nh_df[order_col], errors='coerce')

                    def _parse_hour_safe(val):
                        try:
                            s = str(val).strip()
                            if ':' in s:
                                return int(s.split(':')[0])
                            return int(float(s))
                        except Exception:
                            return 0

                    nh_df['hour'] = nh_df[start_col].apply(_parse_hour_safe)
                    nh_df['is_night'] = (nh_df['hour'] >= 18) | (nh_df['hour'] < 6)

                    for eid in entity_ids:
                        sub = nh_df[nh_df[nh_ent_col] == eid]
                        if sub.empty:
                            continue
                        total_o = sub[order_col].sum()
                        if total_o <= 0:
                            continue
                        night_o = sub[sub['is_night']][order_col].sum()
                        night_raw[eid] = self._safe_float(night_o / total_o * 100.0)  # 夜间占比（%）

                # ---------- 一个通用的 0-100 归一化函数 ----------
                # 改为仅按最大值归一：score = value / max * 100，避免最小值为 0 时的异常情况
                def _normalize_to_100(raw_map):
                    vals = [raw_map.get(eid, 0.0) for eid in entity_ids]
                    v_max = max(vals) if vals else 0.0
                    norm = {}
                    if v_max > 0:
                        for eid in entity_ids:
                            v = raw_map.get(eid, 0.0)
                            norm[eid] = round(v / v_max * 100.0, 1)
                    else:
                        # 全为 0 时统一给 0 分
                        for eid in entity_ids:
                            norm[eid] = 0.0
                    return norm

                flights_score = _normalize_to_100(flights_raw)
                duration_score = _normalize_to_100(duration_raw)
                distance_score = _normalize_to_100(distance_raw)
                active_score = _normalize_to_100(active_raw)
                night_score = _normalize_to_100(night_raw)

                # ---------- 计算 TopN 每个企业的总分（5 个维度等权 0.2） ----------
                total_scores = {}
                for eid in entity_ids:
                    total_scores[eid] = round(
                        0.3 * flights_score.get(eid, 0.0)
                        + 0.3 * duration_score.get(eid, 0.0)
                        + 0.3 * distance_score.get(eid, 0.0)
                        + 0.05 * active_score.get(eid, 0.0)
                        + 0.05 * night_score.get(eid, 0.0),
                        1
                    )

                # 使用 DataFrame 便于后续扩展 / 排序，并计算均值
                total_score_df = pd.DataFrame({
                    "entity_id": entity_ids,
                    "total_score": [total_scores[eid] for eid in entity_ids],
                })

                # 找出综合得分最高的企业名称 & 平均总分
                leading_entity_name = "待计算"
                avg_total_score = 0.0
                if not total_score_df.empty:
                    best_row = total_score_df.loc[total_score_df['total_score'].idxmax()]
                    best_eid = self._safe_str(best_row['entity_id'])
                    # 优先使用 base_df 中的 entity_name（中文名），仅在缺失时退回 entity_id
                    leading_entity_name = entity_id_to_name.get(best_eid, best_eid)
                    avg_total_score = float(total_score_df['total_score'].mean().round(1))

                # 构造雷达图数据：每个维度一行，列为各企业“名称”的得分
                subjects = [
                    ('架次', flights_score),
                    ('时长', duration_score),
                    ('里程', distance_score),
                    ('活跃度', active_score),
                    ('夜间', night_score),
                ]

                for subj, score_map in subjects:
                    row = {"subject": subj, "fullMark": 100}
                    for eid in entity_ids:
                        # 使用 name_col 对应的实体中文名作为键，不再映射到 A/B/C/D/E
                        entity_name = entity_id_to_name.get(eid, self._safe_str(eid))
                        row[entity_name] = score_map.get(eid, 0.0)
                    chart_data.append(row)

                # 保持原有 leading_score 计算方式：Top2 架次份额
                top2 = base_df.nlargest(2, flights_col)
                if len(top2) >= 2:
                    total = self._safe_float(self._safe_float(base_df[flights_col].sum()))
                    top2_share = self._safe_float(top2[flights_col].sum()) / total * 100 if total > 0 else 0
                    leading_score = round(top2_share, 1)

        if not chart_data:
            chart_data = [
                {"subject": "航程", "A": 120, "B": 110, "fullMark": 150},
                {"subject": "时长", "A": 98, "B": 130, "fullMark": 150},
                {"subject": "夜间", "A": 86, "B": 130, "fullMark": 150},
                {"subject": "载重", "A": 99, "B": 100, "fullMark": 150},
                {"subject": "速度", "A": 85, "B": 90, "fullMark": 150}
            ]
            leading_score = 88

        # 领航企业名称 / TopN 平均总分（若计算未成功则回落到默认值）
        try:
            leading_entity_name  # type: ignore[name-defined]
        except NameError:
            leading_entity_name = "待计算"
        try:
            avg_total_score  # type: ignore[name-defined]
        except NameError:
            avg_total_score = 0.0

        key_metrics = [
            {"label": "平均分", "value": f"{avg_total_score}分"},
            {"label": "领航企业", "value": leading_entity_name},
        ]

        # 全局保存：头部企业领航得分（0-100）
        self.leading_score = leading_score

        self.metrics.append(self._create_metric(
            "20", "头部企业“领航”指数", "头部引领力", "创新与融合",
            f"{leading_score:.1f}", "分", "Radar", chart_data,
            key_metrics,
            "头部企业主要运营指标影响力综合得分（架次、时长、里程、活跃度、夜间5个方面）。",
            insight=f"<b>产业呈现“超级领航者”引领的鲜明格局，创新生态的“双刃剑”效应显现“</b>：头部企业综合得分高达{leading_score:.1f}分，远超TOP5企业{avg_total_score}分的平均水平，"
                    "以深圳美团低空物流为代表的领航企业，在<b>架次、里程、时长</b>等关键维度上形成了压倒性影响力。这验证了市场力量在驱动技术迭代、"
                    f"商业模式创新和用户习惯培养上的高效性。头部企业引领效应极强（得分{leading_score:.1f}），是产业创新的主要引擎，但同时也带来了生态多样性不足与依赖度高的潜在风险。",
            suggestion="构建“既鼓励领航又繁荣生态”的治理新范式。"

        ))

    def _compute_prosperity_index(self):
        """综合得分: Weighted aggregate of all indices."""
        # 1）第一类：指数型指标分组（后续可以单独归一化/建模使用）
        traffic_index_value = getattr(self, "traffic_index_value", 100.0)
        operation_index_value = getattr(self, "operation_index_value", 100.0)
        fleet_index_value = getattr(self, "fleet_index_value", 100.0)

        self.index_group_traffic_operation_fleet = [
            traffic_index_value,
            operation_index_value,
            fleet_index_value,
        ]

        # 对三个指数型指标分别计算 Sigmoid 得分（0-100 分）
        self.traffic_index_score = self._sigmoid_score(traffic_index_value)
        self.operation_index_score = self._sigmoid_score(operation_index_value)
        self.fleet_index_score = self._sigmoid_score(fleet_index_value)

        # 2）第二类：指数型（0-1 区间）的指数
        diversity_index_value = getattr(self, "diversity_index_value", 0.5)
        balance_index_value = getattr(self, "balance_index_value", 0.5)
        stability_index_value = getattr(self, "stability_index_value", 0.5)

        # 3）第三类：比例型指标分组

        # 保存原始 0-1 值分组
        self.index_group_diversity_balance_stability = [
            diversity_index_value,
            balance_index_value,
            stability_index_value,
        ]

        # 对这一组的 score 直接乘以 100（仍保持 0-100 分制）
        self.diversity_index_score = diversity_index_value * 100.0
        self.balance_index_score = balance_index_value * 100.0
        self.stability_index_score = stability_index_value * 100.0

        # 3）第三类：比例型指标（0-100，直接作为 score；夜间经济单独缩放）
        cr10_pct_value = getattr(self, "cr10_pct_value", 50.0)
        commercial_pct_value = getattr(self, "commercial_pct_value", 50.0)
        long_pct_value = getattr(self, "long_pct_value", 10.0)
        longterm_pct_value = getattr(self, "longterm_pct_value", 10.0)
        completion_pct_value = getattr(self, "completion_pct_value", 90.0)
        night_pct_value = getattr(self, "night_pct_value", 10.0)

        # 保存原始比例值分组
        self.index_group_ratio = [
            cr10_pct_value,
            commercial_pct_value,
            long_pct_value,
            longterm_pct_value,
            completion_pct_value,
            night_pct_value,
        ]

        # 分数规则：除夜间经济外，其余 score 等于原值；夜间 score = 原值 / 50 * 100
        self.cr10_pct_score = cr10_pct_value
        self.commercial_pct_score = commercial_pct_value
        self.long_pct_score = long_pct_value
        self.longterm_pct_score = longterm_pct_value
        self.completion_pct_score = completion_pct_value
        # 因夜间最大占比是50%，所以除以 50 再乘以 100 进行缩放，使其在 0-100 分制下更有区分度
        self.night_pct_score = (night_pct_value / 50.0) * 100.0

        # 4）第四类：熵值型指标分组
        alltime_entropy_index_value = getattr(self, "alltime_entropy_index_value", 0.0)
        airspace_entropy_index_value = getattr(self, "airspace_entropy_index_value", 0.0)

        # 保存熵值分组
        self.index_group_entropy = [
            alltime_entropy_index_value,
            airspace_entropy_index_value,
        ]

        # 对应的 score：熵值 / log2(N) 归一化到 0-1，再乘以 100
        self.alltime_entropy_score = (
            (alltime_entropy_index_value / np.log2(24.0)) * 100.0 if alltime_entropy_index_value > 0 else 0.0
        )
        self.airspace_entropy_score = (
            (airspace_entropy_index_value / np.log2(10.0)) * 100.0 if airspace_entropy_index_value > 0 else 0.0
        )

        # 5）第五类：得分型指标分组（直接使用已有得分）
        hub_index_score = getattr(self, "hub_index_score", 50.0)
        leading_score = getattr(self, "leading_score", 50.0)

        self.index_group_score = [
            hub_index_score,
            leading_score,
        ]

        # 6）第六类：其他类（增长动能 + 城市微循环 + 单机效能）
        avg_growth_value = getattr(self, "avg_growth_value", 0.0)
        self.avg_growth_score = self._piecewise_growth_score(avg_growth_value, left=-100.0, right=0.0, k=0.1)

        micro_index_value = getattr(self, "micro_index_value", 1.0)
        self.micro_index_score = (micro_index_value / np.log(46.0)) * 100.0 if micro_index_value > 0 else 0.0

        production_consumption_ratio_value = getattr(self, "production_consumption_ratio_value", 1.0)
        self.production_consumption_score = self._production_consumption_score(production_consumption_ratio_value)

        self.index_group_other = [
            avg_growth_value,
            micro_index_value,
            self.efficiency_score,
            production_consumption_ratio_value,
        ]

        # 7）加权综合得分（直接基于 20 个 score 聚合）
        # Weights: 规模(32%) + 结构(18%) + 时空(18%) + 效率(15%) + 创新(17%)

        def _avg_safe(values):
            vals = [float(v) for v in values if v is not None]
            return float(np.mean(vals)) if vals else 0.0

        # 1. 规模与增长（4 个指标）
        scale_score = _avg_safe([
            self.traffic_index_score,
            self.operation_index_score,
            self.fleet_index_score,
            self.avg_growth_score,
        ])

        # 2. 结构与主体（3 个指标）
        structure_score = _avg_safe([
            self.cr10_pct_score,
            self.commercial_pct_score,
            self.diversity_index_score,
        ])

        # 3. 时空特征（4 个指标）
        timespace_score = _avg_safe([
            self.balance_index_score,
            self.alltime_entropy_score,
            self.stability_index_score,
            self.hub_index_score,
        ])

        # 4. 效率与质量（4 个指标）
        efficiency_score_dim = _avg_safe([
            self.efficiency_score,
            self.long_pct_score,
            self.longterm_pct_score,
            self.completion_pct_score,
        ])

        # 5. 创新与融合（5 个指标）
        innovation_score = _avg_safe([
            self.micro_index_score,
            self.airspace_entropy_score,
            self.production_consumption_score,
            self.night_pct_score,
            self.leading_score,
        ])

        # print each dimension score and weight
        print(f"规模与增长得分: {scale_score:.1f} (权重 32%) 其中增长动能得分: {self.avg_growth_score:.1f}, 交通指数得分: {self.traffic_index_score:.1f}, 运营指数得分: {self.operation_index_score:.1f}, 机队指数得分: {self.fleet_index_score:.1f}")
        print(f"结构与主体得分: {structure_score:.1f} (权重 18%) 其中CR10得分: {self.cr10_pct_score:.1f}, 商业应用得分: {self.commercial_pct_score:.1f}, 多样性指数得分: {self.diversity_index_score:.1f}")
        print(f"时空特征得分: {timespace_score:.1f} (权重 18%) 其中平衡指数得分: {self.balance_index_score:.1f}, 全时熵得分: {self.alltime_entropy_score:.1f}, 稳定性得分: {self.stability_index_score:.1f}, 枢纽度得分: {self.hub_index_score:.1f}")
        print(f"效率与质量得分: {efficiency_score_dim:.1f} (权重 15%) 其中效率得分: {self.efficiency_score:.1f}, 长途占比得分: {self.long_pct_score:.1f}, 长期占比得分: {self.longterm_pct_score:.1f}, 完成率得分: {self.completion_pct_score:.1f}")
        print(f"创新与融合得分: {innovation_score:.1f} (权重 17%) 其中微循环指数得分: {self.micro_index_score:.1f}, 空域熵得分: {self.airspace_entropy_score:.1f}, 产消比得分: {self.production_consumption_score:.1f}, 夜间占比得分: {self.night_pct_score:.1f}, 领航指数得分: {self.leading_score:.1f}")

        # 最终综合繁荣度得分（0-100）
        prosperity = round(
            0.32 * scale_score +
            0.18 * structure_score +
            0.18 * timespace_score +
            0.15 * efficiency_score_dim +
            0.17 * innovation_score,
            1,
        )

        self.metrics.append(self._create_metric(
            "", "低空综合繁荣度", "LA-CPI (综合指数)", "综合指数",
            prosperity, "分", "Dashboard", [{"name": "得分", "value": prosperity}],
                [],
            "本指数以“领航（PILOT）”五维模型为内核，系统刻画深圳市低空经济发展的规模水位、结构健康、运行效能、时空韧性及创新潜能。"
            "它既是衡量当前繁荣程度的现状度量衡，也是洞察增长动力与结构均衡性的健康诊断仪，更是预判演进方向与可持续性的趋势导航标，实现对产业发展"
            "阶段的集成评价与前瞻指引。<br><br><b><p style=\"color: #002FA7;\">维度权重设定（总计100%）</p></b><br> "
            "&nbsp;&nbsp;- <td>维度一：规模与增长</td><td>&emsp;|权重：32%</td><td>（产业基本盘与增长势能的核心体现）</td><br> "
            "&nbsp;&nbsp;- <td>维度二：结构与主体</td><td>&emsp;|权重：18%</td><td>（生态健康度与市场韧性的关键支撑）</td><br> "
            "&nbsp;&nbsp;- <td>维度三：时空特征</td><td>&emsp;&emsp;|权重：18%</td><td>（资源利用效率与运行协同性的空间映射）</td><br>"
            "&nbsp;&nbsp;- <td>维度四：效能与质量</td><td>&emsp;|权重：15%</td><td>（价值转化效率与发展质量的核心标志）</td><br>"
            "&nbsp;&nbsp;- <td>维度五：创新与融合</td><td>&emsp;|权重：17%</td><td>（前沿突破与长期竞争力的探测雷达）</td><br><br><p><small>设定说明：权重分配遵循"
            "“立足现实、前瞻引领、动态适配”原则，力求在客观刻画产业当前发展特征的同时，有效引导其向高质量、可持续轨道跃迁。"
            "此系权重体系将随产业发展阶段进行年度动态校准。</small></p>",
            insight="-",
            suggestion="-"
        ))

        # 同标题同指标的续页：无图表、无关键指标、无定义，仅展示 insight 与 suggestion
        self.metrics.append(self._create_metric(
            "", "低空综合繁荣度", "LA-CPI (综合指数)", "综合指数",
            prosperity, "分", "Dashboard",
            chart_data=[],
            key_metrics=[],
            definition="-",
            insight="<b>维度一：规模与增长</b><br>量质齐升，景气扩张。"
                    "月均飞行架次达约基期1.6倍，产业已迈入规模快速放量的新阶段。应保障增长引擎的同时，"
                    "以前瞻政策推动市场从“单一技术路径依赖”转向“多元价值生态繁荣”，从“关注增速”转向“关注增长质量”。<br><br>"
                    f"<b>维度二：结构与主体</b><br>应用主导，生态初显。市场集中度合理，商业应用占比{commercial_pct_value}%，机型多样性指数{diversity_index_value}，健康雏形已具。"
                    "应积极推动从“规模集中”向“结构优化”演进，从“商业单驱”向“商业+消费双轮”过渡，引导机型生态从“数量多元”迈向“质量进阶”。<br><br>"
                    f"<b>维度三：时空特征</b><br>多核引领，网络初具。区域均衡度{balance_index_value}，夜间占比{night_pct_value}%，枢纽度{hub_index_score}，时空分布呈现“日主夜辅、天候敏感”特征。"
                    "应着力推动时空资源从“自然集聚”转向“规划引导”，从“被动适应”转向“主动构建”韧性体系，以实现时空资源更均衡、更协同、更具弹性的配置。<br><br>"
                    "<b>维度四：效能与质量</b><br>整体呈现“基础扎实、效率分化、高值欠缺”的进阶前夜特征。应从关注“资源投入与活动规模” 坚决转向追求“资源产出效率与运行质量”，"
                    "全力破解资产利用率低与高价值任务少的核心矛盾，推动产业从“飞得多” 的初级阶段，迈向“飞得好、飞得值”的高质量发展阶段。<br><br>"
                    "<b>维度五：创新与融合</b><br>产业展现出强大的创新活力与融合潜能，在空域利用、时段拓展、属性混合及企业引领等方面已显现出前沿特征，"
                    "正处在从“技术验证与场景摸索” 向“生态构建与价值深挖”跃迁的关键窗口。应充分利用现有创新势能，推动产业发展从“单点技术应用突破”转向“复杂系统生态融合”，"
                    "从“培育单一领航者”转向“营造繁荣共生的创新雨林”，将技术领先优势转化为可持续的、系统性的产业竞争力。<br><br>",
            suggestion="-",
        ))


def process_markdown_files(input_files: List[str], output_file: str):
    """
    Process markdown files and generate JSON output for web report.

    Args:
        input_files: List of markdown file paths
        output_file: Output JSON file path
    """
    all_tables = {}
    all_titles = {}

    parser = MarkdownTableParser()

    for filepath in input_files:
        print(f"Parsing: {filepath}")
        tables = parser.parse_file(filepath)

        # Merge tables (later files override earlier ones for same keys)
        for key, df in tables.items():
            if not df.empty:
                all_tables[key] = df
                all_titles[key] = parser.table_titles.get(key, "")

        print(f"  Found {len(tables)} tables")

        # Reset parser for next file
        parser = MarkdownTableParser()

    print(f"\nTotal tables parsed: {len(all_tables)}")

    # Compute indices
    print("\nComputing indices...")
    computer = IndexComputer(all_tables, all_titles)
    metrics = computer.compute_all_indices()

    print(f"Computed {len(metrics)} indices")

    # Save output
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print(f"\nOutput saved to: {output_file}")

    # Print summary
    print("\n" + "=" * 60)
    print("INDEX SUMMARY")
    print("=" * 60)
    for m in metrics:
        print(f"  {m['id']} - {m['title']}: {m['value']} {m['unit']}")

    return metrics


def main():
    parser = argparse.ArgumentParser(
        description='Process markdown data files and compute low-altitude economy indices.'
    )
    parser.add_argument(
        '--input', '-i',
        nargs='+',
        required=True,
        help='Input markdown file(s)'
    )
    parser.add_argument(
        '--output', '-o',
        default='output/metrics.json',
        help='Output JSON file (default: output/metrics.json)'
    )

    args = parser.parse_args()

    # Validate input files
    for f in args.input:
        if not Path(f).exists():
            print(f"Error: Input file not found: {f}")
            return 1

    process_markdown_files(args.input, args.output)
    return 0


if __name__ == '__main__':
    exit(main())
