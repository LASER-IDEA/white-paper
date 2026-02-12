/**
 * Charts.tsx - Professional Chart Components Library
 *
 * This module provides a comprehensive set of accessible, performant chart components
 * for visualizing Low Altitude Economy data.
 *
 * @improvements
 * - Accessibility: Semantic HTML, better empty states, clear messaging
 * - Performance: Memoized computations, optimized re-renders
 * - Type Safety: TypeScript interfaces for better type checking
 * - Visual: Smooth animations, consistent styling, responsive design
 * - UX: Better empty states, loading indicators, error handling
 *
 * @version 2.0.0
 * @updated 2026
 */

import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, BarChart, Bar, ComposedChart,
  PieChart, Pie, Cell, Treemap, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  ScatterChart, Scatter, ZAxis, Legend, RadialBarChart, RadialBar, FunnelChart, Funnel, LabelList,
  Sector, Label
} from 'recharts';
import * as echarts from 'echarts';

// TypeScript Interfaces for better type safety
interface ChartDataPoint {
  [key: string]: any;  // Flexible type to support various data structures
}

interface ChartProps {
  data: ChartDataPoint[];
  ariaLabel?: string;
}

// Chart container constants
const CHART_MIN_HEIGHT = 280;

// Enhanced color palette
const COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#6366f1'];

// 1. Area Chart (Traffic) - Enhanced with accessibility and performance
export const TrafficAreaChart = ({ data, ariaLabel = "Daily flight sorties area chart" }: ChartProps) => {
  // Memoize empty state check for better performance
  const isEmpty = useMemo(() => !data || data.length === 0, [data]);

  if (isEmpty) {
    return (
      <div
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        role="status"
        aria-label="No data available for chart"
      >
        <p style={{ color: '#64748b', fontSize: '14px' }}>📊 No data available</p>
      </div>
    );
  }

  return (
    <div role="img" aria-label={ariaLabel} style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
      <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
    <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
      <defs>
        <linearGradient id="colorVal" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.8}/>
          <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
        </linearGradient>
      </defs>
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
      <XAxis dataKey="date" tick={{fontSize: 10}} tickLine={false} axisLine={false} />
      <YAxis
        tick={{fontSize: 10}}
        tickLine={false}
        axisLine={false}
        label={{ value: '指数', angle: -90, position: 'insideLeft', offset: 10, fill: '#64748b', fontSize: 11 }}
      />
          <Tooltip
            contentStyle={{
              borderRadius: '8px',
              border: 'none',
              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
              fontSize: '12px'
            }}
            cursor={{ stroke: '#cbd5e1', strokeWidth: 1 }}
          />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#0ea5e9"
            fillOpacity={1}
            fill="url(#colorVal)"
            animationDuration={800}
            animationEasing="ease-in-out"
          />
    </AreaChart>
  </ResponsiveContainer>
    </div>
  );
};

// 2. Dual Line Chart (Operation Intensity) - Enhanced with accessibility
export const DualLineChart = ({ data, ariaLabel = "Operation intensity dual line chart" }: ChartProps) => {
  const isEmpty = useMemo(() => !data || data.length === 0, [data]);

  if (isEmpty) {
    return (
      <div
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        role="status"
        aria-label="No data available for chart"
      >
        <p style={{ color: '#64748b', fontSize: '14px' }}>📊 No data available</p>
      </div>
    );
  }

  return (
    <div role="img" aria-label={ariaLabel} style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
      <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
    <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
      <XAxis dataKey="name" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
          <YAxis
            yAxisId="left"
            tick={{fontSize: 10}}
            axisLine={false}
            tickLine={false}
            label={{
              value: '指数',
              angle: -90,
              position: 'insideLeft',
              style: {fontSize: 10, fill: '#64748b'}
            }}
          />
          <Tooltip
            contentStyle={{
              borderRadius: '8px',
              border: 'none',
              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
              fontSize: '12px'
            }}
            cursor={{ stroke: '#cbd5e1', strokeWidth: 1 }}
          />
          <Line
            yAxisId="left"
            type="monotone"
            dataKey="duration"
            name="时长指数"
            stroke="#0ea5e9"
            strokeWidth={3}
            dot={{r: 4}}
            animationDuration={800}
            animationEasing="ease-in-out"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="distance"
            name="里程指数"
            stroke="#10b981"
            strokeWidth={3}
            dot={{r: 4}}
            animationDuration={800}
            animationEasing="ease-in-out"
          />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="composite"
            name="综合指数"
            stroke="#8b5cf6"
            strokeWidth={3}
            dot={{r: 4}}
            animationDuration={800}
            animationEasing="ease-in-out"
          />
          <Legend wrapperStyle={{ fontSize: '12px' }} />
    </ComposedChart>
  </ResponsiveContainer>
    </div>
  );
};

// 3. Stacked Bar (Fleet) - Enhanced with accessibility and animations
export const StackedBarChart = ({ data, ariaLabel = "Fleet composition stacked bar chart" }: ChartProps) => {
  const isEmpty = useMemo(() => !data || data.length === 0, [data]);

  if (isEmpty) {
    return (
      <div
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        role="status"
        aria-label="No data available for chart"
      >
        <p style={{ color: '#64748b', fontSize: '14px' }}>📊 No data available</p>
      </div>
    );
  }

  return (
    <div role="img" aria-label={ariaLabel} style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
      <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
        <BarChart
        data={data}
        margin={{ top: 20, right: 30, left: 0, bottom: 5 }}
        aria-label={ariaLabel}
        role="img"
      >
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
        <XAxis
          dataKey="name"
          tick={{fontSize: 10}}
          axisLine={false}
          tickLine={false}
          aria-label="Category axis"
        />
        <YAxis
          tick={{fontSize: 10}}
          axisLine={false}
          tickLine={false}
          aria-label="Value axis"
          label={{ value: '活跃SN数', angle: -90, position: 'insideLeft', offset: 10, fill: '#64748b', fontSize: 11 }}
        />
        <Tooltip
          cursor={{fill: '#f3f4f6'}}
          contentStyle={{
            borderRadius: '8px',
            border: 'none',
            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
            fontSize: '12px'
          }}
        />
        <Legend wrapperStyle={{ fontSize: '12px' }} />
        <Bar
          dataKey="MultiRotor"
          name="多旋翼"
          stackId="a"
          fill="#0ea5e9"
          radius={[0,0,0,0]}
          animationDuration={800}
          animationEasing="ease-in-out"
        />
        <Bar
          dataKey="FixedWing"
          name="固定翼"
          stackId="a"
          fill="#fbbf24"
          radius={[0,0,0,0]}
          animationDuration={800}
          animationEasing="ease-in-out"
        />
        <Bar
          dataKey="Helicopter"
          name="直升机"
          stackId="a"
          fill="#8B4513"
          radius={[4,4,0,0]}
          animationDuration={800}
          animationEasing="ease-in-out"
        />
        <Bar
          dataKey="Undefined"
          name="未知"
          stackId="a"
          fill="#10b981"
          radius={[4,4,0,0]}
          animationDuration={800}
          animationEasing="ease-in-out"
        />
        <Bar
          dataKey="CompoundWing"
          name="复合翼"
          stackId="a"
          fill="#8b5cf6"
          radius={[4,4,0,0]}
          animationDuration={800}
          animationEasing="ease-in-out"
        />
    </BarChart>
  </ResponsiveContainer>
    </div>
  );
};

// 5. Pareto (Concentration) - Enhanced with accessibility
export const ParetoChart = ({ data, ariaLabel = "Pareto chart showing concentration analysis" }: ChartProps) => {
  const processedData = useMemo(() => {
    if (!data || data.length === 0) {
      return [];
    }
    // 累计占比使用 chart_data 的 percentage 字段（运行求和），不按 volume 推算
    let cumulative = 0;
    return data.map(d => {
      let pct = 0;
      if (d.percentage != null) {
        const raw = d.percentage;
        const numericValue =
          typeof raw === 'string'
            ? Number(raw.replace(/%/g, '').trim())
            : Number(raw);
        pct = Number.isFinite(numericValue) ? numericValue : 0;
      }
      cumulative += pct;
      return { ...d, cumulative: Math.round(cumulative * 10) / 10 };
    });
  }, [data]);

  if (!processedData || processedData.length === 0) {
  return (
      <div
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        role="status"
        aria-label="No data available for chart"
      >
        <p style={{ color: '#64748b', fontSize: '14px' }}>📊 No data available</p>
      </div>
    );
  }

  return (
    <div role="img" aria-label={ariaLabel} style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
      <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
        <ComposedChart
        data={processedData}
        margin={{ top: 20, right: 20, left: 0, bottom: 80 }}
        aria-label={ariaLabel}
        role="img"
      >
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
        <XAxis
          dataKey="name"
          tick={{ fontSize: 10, angle: -80, textAnchor: 'end' }}
          axisLine={false}
          tickLine={false}
          aria-label="Category axis"
          interval={0}
        />
        <YAxis
          yAxisId="left"
          tick={{fontSize: 10}}
          axisLine={false}
          tickLine={false}
          aria-label="Volume axis"
          label={<Label value="架次" position="insideLeft" angle={-90} offset={5} style={{ fill: '#64748b', fontSize: 10 }} />}
        />
        <YAxis
          yAxisId="right"
          orientation="right"
          tick={{fontSize: 10}}
          axisLine={false}
          tickLine={false}
          unit="%"
          aria-label="Cumulative percentage axis"
          label={<Label value="累计占比" position="insideRight" angle={90} style={{ fill: '#64748b', fontSize: 10 }} />}
        />
        <Tooltip
          contentStyle={{
            borderRadius: '8px',
            border: 'none',
            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
            fontSize: '12px'
          }}
          formatter={(value: number, name: string) => {
            if (name === '飞行量') return [value != null ? `${value}架次` : '—', name];
            if (name === '累计占比') return [value != null ? `${value}%` : '—', name];
            return [value, name];
          }}
        />
        <Bar
          yAxisId="left"
          dataKey="volume"
          name="飞行量"
          fill="#0ea5e9"
          barSize={20}
          radius={[4,4,0,0]}
          animationDuration={800}
          animationEasing="ease-in-out"
        />
        <Line
          yAxisId="right"
          type="monotone"
          dataKey="cumulative"
          name="累计占比"
          stroke="#f59e0b"
          strokeWidth={2}
          dot={{r: 3}}
          animationDuration={800}
          animationEasing="ease-in-out"
        />
      </ComposedChart>
    </ResponsiveContainer>
    </div>
  );
};

// 6. Nightingale Rose Chart (Commercial Maturity)
const RoseShape = (props: any) => {
  const { cx, cy, innerRadius, outerRadius, startAngle, endAngle, fill, payload, maxVal } = props;
  const val = payload.realValue;
  const R = innerRadius + (val / maxVal) * (outerRadius - innerRadius);

  return (
    <Sector
      cx={cx}
      cy={cy}
      innerRadius={innerRadius}
      outerRadius={R}
      startAngle={startAngle}
      endAngle={endAngle}
      fill={fill}
      stroke="#fff"
      strokeWidth={1}
    />
  );
};

export const NightingaleRoseChart = ({ data, ariaLabel = "Nightingale rose chart showing commercial maturity" }: ChartProps) => {
  const { maxVal, roseData, isEmpty } = useMemo(() => {
    if (!data || data.length === 0) {
      return { maxVal: 0, roseData: [], isEmpty: true };
    }

    const maxVal = Math.max(...data.map((d: any) => d.value));

    const roseData = data.map((d: any) => ({
      ...d,
      realValue: d.value,
      value: 1
    }));
    return { maxVal, roseData, isEmpty: false };
  }, [data]);

  const RoseShape = useCallback((props: any) => {
     const { cx, cy, innerRadius, outerRadius, startAngle, endAngle, fill, payload } = props;
     const val = payload.realValue;
     const R = innerRadius + (val / maxVal) * (outerRadius - innerRadius);

     return (
        <Sector
          cx={cx}
          cy={cy}
          innerRadius={innerRadius}
          outerRadius={R}
          startAngle={startAngle}
          endAngle={endAngle}
          fill={fill}
          stroke="#fff"
          strokeWidth={1}
        />
     );
  }, [maxVal]);

  if (isEmpty) {
  return (
      <div
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        role="status"
        aria-label="No data available for chart"
      >
        <p style={{ color: '#64748b', fontSize: '14px' }}>📊 No data available</p>
      </div>
    );
  }

  return (
    <div role="img" aria-label={ariaLabel} style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
      <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
        <PieChart aria-label={ariaLabel} role="img">
        <Pie
          data={roseData}
          cx="50%"
          cy="50%"
          innerRadius={30}
          outerRadius={130}
          dataKey="value"
          shape={<RoseShape maxVal={maxVal} />}
          paddingAngle={0}
          animationDuration={800}
          animationEasing="ease-in-out"
        >
          {roseData.map((entry: any, index: number) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
            formatter={(value: any, name: any, props: any) => [`${props.payload.realValue}架次`, name]}
            contentStyle={{
              borderRadius: '8px',
              border: 'none',
              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
              fontSize: '12px'
            }}
        />
        <Legend
            verticalAlign="bottom"
            height={36}
            wrapperStyle={{ color: '#64748b', fontSize: '12px' }}
            formatter={(_value, entry: any) => {
              const num = entry?.payload?.realValue ?? entry?.payload?.value ?? 0;
              const formatted = Number(num).toLocaleString('zh-CN');
              return `${entry?.payload?.name ?? ''} ${formatted}架次`;
            }}
          />
      </PieChart>
    </ResponsiveContainer>
    </div>
  );
};

// 7. Treemap (Diversity) - Enhanced with accessibility
const CustomTreemapContent = (props: any) => {
  const { root, depth, x, y, width, height, index, name, value } = props;
  
  // Calculate font size based on block size (adaptive)
  const minSize = Math.min(width, height);
  const fontSize = Math.max(8, Math.min(16, minSize * 0.15)); // 8-16px based on block size
  const smallFontSize = Math.max(6, Math.min(12, minSize * 0.12)); // 6-12px for value
  
  // Show text if block is large enough (lower threshold)
  const showText = width > 20 && height > 15;
  const showValue = width > 30 && height > 25 && value;
  
  return (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        style={{
          fill: COLORS[index % COLORS.length],
          stroke: '#fff',
          strokeWidth: 2 / (depth + 1e-10),
          strokeOpacity: 1 / (depth + 1e-10),
        }}
      />
      {showText && (
        <text 
          x={x + width / 2} 
          y={y + height / 2 + fontSize / 3} 
          textAnchor="middle" 
          fill="#fff" 
          fontSize={fontSize} 
          fontWeight={100}
          style={{
            textShadow: '1px 1px 2px rgba(0,0,0,0.5)',
            pointerEvents: 'none',
          }}
        >
          {name}
        </text>
      )}
      {showValue && (
        <text 
          x={x + width / 2} 
          y={y + height / 2 + fontSize + smallFontSize / 2} 
          textAnchor="middle" 
          fill="#fff" 
          fontSize={smallFontSize} 
          fontWeight={100}
          opacity={0.9}
          style={{
            textShadow: '1px 1px 2px rgba(0,0,0,0.5)',
            pointerEvents: 'none',
          }}
        >
          {value}
        </text>
      )}
    </g>
  );
};

export const FleetTreemap = ({ data, ariaLabel = "Fleet diversity treemap chart" }: ChartProps) => {
  const isEmpty = useMemo(() => !data || data.length === 0, [data]);

  if (isEmpty) {
    return (
      <div
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        role="status"
        aria-label="No data available for chart"
      >
        <p style={{ color: '#64748b', fontSize: '14px' }}>📊 No data available</p>
      </div>
    );
  }

  return (
    <div role="img" aria-label={ariaLabel} style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
      <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
    <Treemap
      data={data}
      dataKey="size"
      aspectRatio={4 / 3}
      stroke="#fff"
      fill="#8884d8"
      content={<CustomTreemapContent />}
        animationDuration={800}
        aria-label={ariaLabel}
    />
  </ResponsiveContainer>
    </div>
);
};

// 8. Choropleth Map (Regional Balance) - Advanced ECharts Implementation
export const ChoroplethMap = ({ data }: { data: any[] }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    // Initialize ECharts instance
    chartInstance.current = echarts.init(chartRef.current);

    // Show loading state
    chartInstance.current.showLoading({
      text: '正在加载地图数据...',
      color: '#002FA7',
      textColor: '#64748b',
      maskColor: 'rgba(255, 255, 255, 0.8)',
      zlevel: 0
    });

    // Load Shenzhen GeoJSON data
    fetch('/white-paper/data/shenzhen.json')
      .then(response => response.json())
      .then(geoJson => {
        // Register the map
        echarts.registerMap('Shenzhen', geoJson);

      // Process real data: group by district
      const districtMap = new Map<string, { values: any[], total: number }>();
      
      data.forEach(item => {
        // Prefer explicit district field; fall back to name when district is not provided
        const district = (item as any).district ?? (item as any).name;
        // Skip items that do not have a valid district identifier
        if (!district) {
          return;
        }
        if (!districtMap.has(district)) {
          districtMap.set(district, { values: [], total: 0 });
        }
        districtMap.get(district)!.values.push(item);
        
        // Get total from district_total if available
        const rawTotal = (item as any).district_total;
        const numericTotal = typeof rawTotal === 'number' ? rawTotal : Number(rawTotal);
        if (!Number.isNaN(numericTotal) && numericTotal > 0) {
          districtMap.get(district)!.total = numericTotal;
        }
      });
      
      // Calculate totals for districts without district_total
      districtMap.forEach((districtData, district) => {
        if (!districtData.total || districtData.total <= 0) {
          // Sum all values for this district as fallback
          districtData.total = districtData.values.reduce((sum, item) => {
            const v = typeof item.value === 'number' ? item.value : Number(item.value);
            return sum + (Number.isNaN(v) ? 0 : v);
          }, 0);
        }
      });
      
      // Prepare map data (district name -> total value)
      const mapData = Array.from(districtMap.entries()).map(([district, districtData]) => ({
        name: district,
        value: typeof districtData.total === 'number' ? districtData.total : Number(districtData.total) || 0
      }));
      
      // Calculate density statistics (filter out invalid values)
      const numericValues = mapData
        .map(d => (typeof d.value === 'number' ? d.value : Number(d.value)))
        .filter(v => !Number.isNaN(v));
      const maxValue = numericValues.length ? Math.max(...numericValues) : 1;
      const minValue = numericValues.length ? Math.min(...numericValues) : 0;

      // District coordinates mapping (approximate center of each district)
      const districtCoordinates: Record<string, [number, number]> = {
        '南山区': [113.95, 22.53],
        '宝安区': [113.88, 22.58],
        '福田区': [114.05, 22.54],
        '罗湖区': [114.12, 22.55],
        '龙岗区': [114.25, 22.72],
        '盐田区': [114.25, 22.56],
        '龙华区': [114.03, 22.65],
        '坪山区': [114.35, 22.70],
        '光明区': [113.92, 22.75],
        '大鹏新区': [114.47, 22.58],
      };
      
      // User type color mapping
      const userTypeColors: Record<string, string> = {
        '企业用户': '#3b82f6',
        '个人用户': '#f59e0b',
        '未知类型': '#64748b'
      };

      // Create pie series for each district
      const createPieSeries = (center: [number, number], radius: number, title: string, hubData: any[]) => {
        return {
          name: title,
          type: 'pie',
          coordinateSystem: 'geo',
          tooltip: {
            formatter: `{a}<br/>{b}: {c}架次 ({d}%)`
          },
          label: {
            show: false
          },
          labelLine: {
            show: false
          },
          animationDuration: 1200,
          animationEasing: 'elasticOut',
          radius,
          center,
          data: hubData,
          emphasis: {
            label: {
              show: true,
              fontSize: 12,
              fontWeight: 'bold',
              formatter: '{b}\n{c}架次'
            },
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        };
      };
      
      // Generate pie series for each district
      const pieSeries = Array.from(districtMap.entries())
        .filter(([district]) => districtCoordinates[district]) // Only districts with coordinates
        .map(([district, districtData]) => {
          // Group by user type
          const userTypeData = districtData.values.reduce((acc, item) => {
            const userType = item.uas_user_type || '未知类型';
            acc[userType] = (acc[userType] || 0) + (item.value || 0);
            return acc;
          }, {} as Record<string, number>);
          
          // Convert to pie chart data format
          const pieData = [
            { 
              value: userTypeData['企业用户'] || 0, 
              name: '企业用户', 
              itemStyle: { color: userTypeColors['企业用户'] } 
            },
            { 
              value: userTypeData['个人用户'] || 0, 
              name: '个人用户', 
              itemStyle: { color: userTypeColors['个人用户'] } 
            },
            { 
              value: userTypeData['未知类型'] || 0, 
              name: '未知类型', 
              itemStyle: { color: userTypeColors['未知类型'] } 
            }
          ].filter(item => item.value > 0); // Only show non-zero values
          
          const center = districtCoordinates[district];
          // Smaller radius for district pies (about half of previous size)
          const radius = Math.max(8, Math.min(15, Math.sqrt(districtData.total) * 0.25));
          
          return createPieSeries(center, radius, district, pieData);
        });

        const option = {
          backgroundColor: 'transparent',
          title: {
            text: '深圳无人机飞行密度分布图',
            subtext: '基于区域飞行频率与枢纽分布数据 | 拖拽缩放查看详情\n深圳地图 | 数据更新：2025年',
            left: 'center',
            top: 20,
            textStyle: {
              color: '#002FA7',
              fontSize: 20,
              fontWeight: 'bold'
            },
            subtextStyle: {
              color: '#64748b',
              fontSize: 11,
              lineHeight: 18
            }
          },
          geo: {
            map: 'Shenzhen',
            roam: true,
            aspectScale: Math.cos((22.5 * Math.PI) / 180), // Shenzhen latitude adjustment
            zoom: 1.1,
            center: [114.1, 22.5], // Shenzhen center coordinates
            itemStyle: {
              areaColor: '#f8fafc',
              borderColor: '#cbd5e1',
              borderWidth: 2,
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.1)',
              shadowOffsetX: 2,
              shadowOffsetY: 2
            },
            emphasis: {
              label: {
                show: false
              },
              itemStyle: {
                areaColor: '#dbeafe',
                borderColor: '#002FA7',
                borderWidth: 2.5,
                shadowBlur: 15,
                shadowColor: 'rgba(0, 47, 167, 0.3)'
              }
            },
            label: {
              show: false
            },
            scaleLimit: {
              min: 0.8,
              max: 5
            }
          },
          tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(255, 255, 255, 0.98)',
            borderColor: '#e2e8f0',
            borderWidth: 1,
            borderRadius: 8,
            padding: 12,
            textStyle: {
              color: '#374151'
            },
            shadowBlur: 15,
            shadowColor: 'rgba(0, 0, 0, 0.15)',
            formatter: (params: any) => {
              if (params.componentType === 'series' && params.seriesType === 'map') {
                return `
                  <div style="font-weight: bold; color: #002FA7; margin-bottom: 6px; font-size: 14px;">${params.name}</div>
                  <div style="color: #64748b; margin-bottom: 4px;">飞行密度指数: <span style="color: #002FA7; font-weight: bold; font-size: 16px;">${params.value}</span></div>
                  <div style="color: #64748b; font-size: 12px; padding: 4px 8px; background: ${params.value > 60 ? '#dcfce7' : params.value > 30 ? '#fef3c7' : '#fee2e2'}; border-radius: 4px; display: inline-block;">${params.value > 60 ? '● 高密度飞行区' : params.value > 30 ? '● 中等密度飞行区' : '● 低密度飞行区'}</div>
                `;
              } else if (params.componentType === 'series' && params.seriesType === 'pie') {
                return `
                  <div style="font-weight: bold; color: #002FA7; margin-bottom: 4px;">${params.seriesName}</div>
                  <div>${params.marker}${params.name}: <span style="font-weight: bold;">${params.value}</span>架次 (<span style="color: #002FA7; font-weight: bold;">${params.percent}%</span>)</div>
                `;
              }
              return params.name;
            },
            confine: true
          },
          toolbox: {
            show: true,
            orient: 'horizontal',
            left: 'center',
            bottom: 20,
            feature: {
              dataView: {
                readOnly: false,
                title: '数据视图',
                lang: ['数据视图', '关闭', '刷新'],
                icon: 'path://M17.5,17.3H33 M17.5,17.3H33 M45.4,29.5h-28 M11.5,2v56H51V14.8L38.4,2H11.5z M38.4,2.2v12.7H51 M45.4,41.7h-28',
                buttonColor: '#002FA7',
                buttonTextColor: '#fff'
              },
              restore: {
                title: '重置视图',
                icon: 'path://M30.9,53.2C16.8,53.2,5.3,41.7,5.3,27.6S16.8,2,30.9,2C45,2,56.4,13.5,56.4,27.6S45,53.2,30.9,53.2z M30.9,3.5C17.6,3.5,6.8,14.4,6.8,27.6c0,13.3,10.8,24.1,24.101,24.1C44.2,51.7,55,40.9,55,27.6C54.9,14.4,44.1,3.5,30.9,3.5z M36.9,35.8c0,0.601-0.4,1-0.9,1h-1.3c-0.5,0-0.9-0.399-0.9-1V19.5c0-0.6,0.4-1,0.9-1H36c0.5,0,0.9,0.4,0.9,1V35.8z M27.8,35.8 c0,0.601-0.4,1-0.9,1h-1.3c-0.5,0-0.9-0.399-0.9-1V19.5c0-0.6,0.4-1,0.9-1H27c0.5,0,0.9,0.4,0.9,1L27.8,35.8L27.8,35.8z'
              },
              saveAsImage: {
                title: '保存为图片',
                pixelRatio: 2,
                icon: 'path://M4.7,22.9L29.3,45.5L54.7,23.4M4.6,43.6L4.6,58L53.8,58L53.8,43.6M29.2,45.1L29.2,0',
                backgroundColor: '#fff'
              }
            },
            iconStyle: {
              borderColor: '#002FA7',
              borderWidth: 2
            },
            emphasis: {
              iconStyle: {
                borderColor: '#0ea5e9',
                shadowBlur: 10,
                shadowColor: 'rgba(14, 165, 233, 0.5)'
              }
            }
          },
          visualMap: {
            type: 'continuous',
            min: minValue,
            max: maxValue,
            text: ['高密度', '低密度'],
            realtime: true,
            calculable: true,
            inRange: {
              color: [
                '#eff6ff', // Very light blue
                '#dbeafe', // Light blue
                '#bfdbfe', // Medium light blue
                '#93c5fd', // Medium blue
                '#60a5fa', // Blue
                '#3b82f6', // Bright blue
                '#2563eb', // Dark blue
                '#1d4ed8', // Darker blue
                '#1e40af', // Very dark blue
                '#002FA7'  // Brand blue
              ],
              symbolSize: [30, 100]
            },
            textStyle: {
              color: '#64748b',
              fontSize: 12,
              fontWeight: 'bold'
            },
            orient: 'horizontal',
            left: '50%',
            // 靠下显示，与左下「地图数据来源」块大致水平
            top: '58%',
            itemWidth: 25,
            itemHeight: 140,
            precision: 0,
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            borderColor: '#e2e8f0',
            borderWidth: 1,
            borderRadius: 8,
            padding: 10,
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.1)'
          },
          legend: {
            data: ['企业用户', '个人用户', '未知类型'],
            orient: 'vertical',
            left: 20,
            top: '35%',
            textStyle: {
              color: '#64748b',
              fontSize: 12,
              fontWeight: 'bold'
            },
            itemGap: 10,
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            borderColor: '#e2e8f0',
            borderWidth: 1,
            borderRadius: 8,
            padding: 12,
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.1)'
          },
          series: [
            // Main choropleth map
            {
              name: '深圳各区飞行密度',
              type: 'map',
              map: 'Shenzhen',
              geoIndex: 0,
              aspectScale: Math.cos((22.5 * Math.PI) / 180),
              zoom: 1.1,
              center: [114.1, 22.5],
              label: {
                show: true,
                color: '#002FA7',
                fontSize: 12,
                fontWeight: 'bold',
                formatter: '{b}',
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                padding: [4, 8],
                borderRadius: 4
              },
              emphasis: {
                label: {
                  color: '#ffffff',
                  fontSize: 14,
                  backgroundColor: '#002FA7',
                  padding: [6, 10],
                  shadowBlur: 8,
                  shadowColor: 'rgba(0, 0, 0, 0.3)'
                },
                itemStyle: {
                  areaColor: '#002FA7',
                  borderColor: '#ffffff',
                  borderWidth: 3,
                  shadowBlur: 20,
                  shadowColor: 'rgba(0, 47, 167, 0.5)'
                }
              },
              select: {
                label: {
                  color: '#ffffff',
                  backgroundColor: '#0ea5e9'
                },
                itemStyle: {
                  areaColor: '#0ea5e9',
                  borderColor: '#ffffff',
                  borderWidth: 2
                }
              },
              itemStyle: {
                borderColor: '#ffffff',
                borderWidth: 2,
                shadowBlur: 5,
                shadowColor: 'rgba(0, 0, 0, 0.1)'
              },
              data: mapData
            },

            // Pie charts for each district with real user type data
            ...pieSeries
          ]
        };

        // Set options
        chartInstance.current.setOption(option);
      })
      .then(() => {
        // Hide loading after successful setup
        chartInstance.current.hideLoading();
      })
      .catch(error => {
        console.error('Failed to load Shenzhen map data:', error);
        if (chartInstance.current) {
          chartInstance.current.hideLoading();
        }
      });

    // Cleanup
    return () => {
      if (chartInstance.current) {
        chartInstance.current.dispose();
      }
    };
  }, [data]);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      if (chartInstance.current) {
        chartInstance.current.resize();
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="w-full h-full relative bg-white rounded-lg border border-slate-200 overflow-hidden">
      <div
        ref={chartRef}
        className="w-full h-full"
        style={{
          minHeight: '500px',
          background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)'
        }}
      />

      {/* Additional Info */}
      <div className="absolute bottom-3 left-3 text-xs text-slate-500 bg-white/90 backdrop-blur px-3 py-2 rounded-lg border border-slate-200 shadow-sm">
        <div className="font-medium text-slate-700 mb-1">📊 地图数据来源</div>
        <div>阿里云DataV数据可视化平台 | 2021.5更新</div>
        <div className="text-[10px] text-slate-400 mt-1">包含10个行政区</div>
      </div>

      {/* Navigation hint - 图表最右上 */}
      <div className="absolute top-3 right-3 text-xs text-slate-500 bg-white/90 backdrop-blur px-2 py-1 rounded border border-slate-200">
        🖱️ 拖拽查看 | 🔍 滚轮缩放
      </div>
    </div>
  );
};

// 9. Polar Clock (All time)
export const PolarClockChart = ({ data, ariaLabel = "Polar clock chart showing hourly activity" }: ChartProps) => (
  <div role="img" aria-label={ariaLabel} style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
    <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
      <PolarGrid stroke="#e5e7eb" />
      <PolarAngleAxis dataKey="hour" tick={{ fontSize: 10 }} />
      <PolarRadiusAxis angle={30} domain={[0, 'auto']} tick={false} axisLine={false} />
      <Radar name="活跃度" dataKey="value" stroke="#002FA7" fill="#002FA7" fillOpacity={0.6} />
      <Tooltip />
    </RadarChart>
  </ResponsiveContainer>
  </div>
);

// 10. Box Plot (Seasonal)
export const SeasonalBoxChart = ({ data, ariaLabel = "Seasonal box plot chart" }: ChartProps) => (
  <div
    role="img"
    aria-label={ariaLabel}
    style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}
    className="flex flex-col"
  >
    <div className="flex-1">
      <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
        <ComposedChart data={data} margin={{ top: 20, right: 20, bottom: 30, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
          <XAxis dataKey="name" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
          <YAxis
            tick={{fontSize: 10}}
            axisLine={false}
            tickLine={false}
            label={{ value: '架次', angle: -90, position: 'insideLeft', offset: 10, fill: '#64748b', fontSize: 11 }}
          />
          <Tooltip />
          <Bar dataKey="max" name="最大值" fill="#cbd5e1" barSize={10} stackId="a" />
          <Line type="monotone" dataKey="std" name="标准差" stroke="#facc15" strokeWidth={2} dot={{r:3}} />
          <Line type="monotone" dataKey="avg" name="均值" stroke="#0ea5e9" strokeWidth={3} dot={{r:4}} />
          <Line type="monotone" dataKey="median" name="中位数" stroke="#6366f1" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="q3" name="上四分位" stroke="#f97316" strokeDasharray="4 2" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="q1" name="下四分位" stroke="#22c55e" strokeDasharray="4 2" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="min" name="最小值" stroke="#10b981" strokeDasharray="3 3" dot={false} />
        </ComposedChart>
      </ResponsiveContainer>
    </div>

    {/* 自定义图例：解释各颜色/线型含义 */}
    <div className="mt-2 flex flex-wrap items-center gap-3 text-[11px] text-slate-500 justify-center">
      <div className="flex items-center gap-1">
        <span className="inline-block w-4 h-[3px] rounded-full" style={{ backgroundColor: '#0ea5e9' }} />
        <span>均值</span>
      </div>
      <div className="flex items-center gap-1">
        <span className="inline-block w-4 h-[3px] rounded-full" style={{ backgroundColor: '#facc15' }} />
        <span>标准差</span>
      </div>
      <div className="flex items-center gap-1">
        <span className="inline-block w-4 h-[3px] rounded-full" style={{ backgroundColor: '#6366f1' }} />
        <span>中位数</span>
      </div>
      <div className="flex items-center gap-1">
        <span
          className="inline-block w-4 h-[3px] rounded-full border-t border-dashed"
          style={{ borderColor: '#f97316' }}
        />
        <span>上四分位 (Q3)</span>
      </div>
      <div className="flex items-center gap-1">
        <span
          className="inline-block w-4 h-[3px] rounded-full border-t border-dashed"
          style={{ borderColor: '#22c55e' }}
        />
        <span>下四分位 (Q1)</span>
      </div>
      <div className="flex items-center gap-1">
        <span
          className="inline-block w-4 h-[3px] rounded-full border-t border-dashed"
          style={{ borderColor: '#10b981' }}
        />
        <span>最小值</span>
      </div>
      <div className="flex items-center gap-1">
        <span className="inline-block w-3 h-3 rounded-sm" style={{ backgroundColor: '#cbd5e1' }} />
        <span>最大值柱形</span>
      </div>
    </div>
  </div>
);

// 12. Gauge (Efficiency)
export const GaugeChart = ({ data, ariaLabel = "Efficiency gauge chart" }: ChartProps) => {
  // 仪表盘范围从 0-10，data 形如
  // [{ name: '平均效益', value: '2.84' }, { name: 'TOP50效益', value: '6.01' }]
  const avgItem = data.find(d => d.name === '平均效益') ?? data[0];
  const top50Item = data.find(d => d.name === 'TOP50效益');

  const rawAvgVal = typeof avgItem.value === 'string' ? parseFloat(avgItem.value) : avgItem.value;
  const avgVal = Math.max(0, Math.min(10, Number.isFinite(rawAvgVal) ? rawAvgVal : 0));

  const rawTop50Val = top50Item
    ? (typeof top50Item.value === 'string' ? parseFloat(top50Item.value) : top50Item.value)
    : avgVal;
  const top50Val = Math.max(0, Math.min(10, Number.isFinite(rawTop50Val) ? rawTop50Val : 0));

  return (
    <div role="img" aria-label={ariaLabel} className="flex flex-col" style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
          <PieChart>
            {/* 背景：浅蓝色半圆 */}
            <Pie
              data={[{ name: '背景', value: 10 }]}
              cx="50%"
              cy="70%"
              startAngle={180}
              endAngle={0}
              innerRadius={80}
              outerRadius={120}
              paddingAngle={0}
              dataKey="value"
            >
              <Cell key="bg" fill="#dbeafe" />
            </Pie>

            {/* 平均效益：绿色弧线（按 value/10 占用半圈比例，剩余为透明以露出背景） */}
            <Pie
              data={[
                { name: '平均效益', value: avgVal },
                { name: 'avg_rest', value: Math.max(0, 10 - avgVal) }
              ]}
              cx="50%"
              cy="70%"
              startAngle={180}
              endAngle={0}
              innerRadius={88}
              outerRadius={116}
              paddingAngle={0}
              dataKey="value"
            >
              <Cell key="avg_val" fill="#22c55e" />
              <Cell key="avg_rest" fill="transparent" stroke="none" />
            </Pie>

            {/* TOP50 效益：蓝色弧线（按 value/10 占用半圈比例，剩余为透明以露出背景） */}
            <Pie
              data={[
                { name: 'TOP50效益', value: top50Val },
                { name: 'top50_rest', value: Math.max(0, 10 - top50Val) }
              ]}
              cx="50%"
              cy="70%"
              startAngle={180}
              endAngle={0}
              innerRadius={104}
              outerRadius={132}
              paddingAngle={0}
              dataKey="value"
            >
              <Cell key="top50_val" fill="#3b82f6" />
              <Cell key="top50_rest" fill="transparent" stroke="none" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* 图例：色块与说明水平对齐、紧贴文字；图例与副标题整体居中 */}
      <div className="flex flex-col items-center gap-1 mt-3 mb-4 shrink-0">
        <div className="flex flex-wrap items-center justify-center gap-4">
          <div className="flex items-center gap-1.5">
            <span className="shrink-0 w-3 h-3 rounded-sm bg-[#22c55e]" />
            <span className="text-sm font-medium text-slate-800">平均效益: {avgVal.toFixed(2)}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="shrink-0 w-3 h-3 rounded-sm bg-[#3b82f6]" />
            <span className="text-sm font-medium text-slate-800">TOP50效益: {top50Val.toFixed(2)}</span>
          </div>
        </div>
        <div className="text-xs text-slate-500">单机效益仪表盘（0-10）</div>
      </div>
    </div>
  );
};

// 11. Funnel (Endurance)
export const MissionFunnelChart = ({ data, ariaLabel = "Mission endurance funnel chart" }: ChartProps) => (
  <div role="img" aria-label={ariaLabel} style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
    <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
    <FunnelChart>
      <Tooltip
        content={({ active, payload }) => {
          if (!active || !payload?.length) return null;
          const item = payload[0].payload as { name?: string; value?: string | number; desc?: string };
          const val = item.value ?? '';
          const desc = item.desc ? ` ${item.desc}` : '';
          return (
            <div className="bg-white border border-slate-200 rounded shadow px-2 py-1.5 text-sm">
              <span className="font-medium text-slate-800">{item.name}</span>
              <span className="text-slate-600">: {val}{desc}</span>
            </div>
          );
        }}
      />
      <Funnel
        dataKey="value"
        data={data}
        isAnimationActive
      >
        <LabelList position="right" fill="#000" stroke="none" dataKey="name" />
      </Funnel>
    </FunnelChart>
  </ResponsiveContainer>
  </div>
);

// 12. Histogram (Wide Area)
export const CoverageHistogram = ({ data, ariaLabel = "Coverage area histogram" }: ChartProps) => (
  <div role="img" aria-label={ariaLabel} className="flex flex-col" style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
    <div className="flex-1 min-h-0">
      <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 30, bottom: 25 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 10, fill: '#64748b' }}
            axisLine={false}
            tickLine={false}
            label={{ value: '里程区间(km)', position: 'right', offset: -40, dy: 15, fill: '#64748b', fontSize: 11 }}
          />
          <YAxis
            tick={{ fontSize: 10, fill: '#64748b' }}
            axisLine={false}
            tickLine={false}
            label={{ value: '架次', position: 'left', offset: 5, fill: '#64748b', fontSize: 11 }}
          />
          <Tooltip cursor={{fill: '#f8fafc'}} />
          <Bar dataKey="value" fill="#f59e0b" barSize={40} radius={[4,4,0,0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  </div>
);

// 13. Chord Diagram (Micro Circulation)
export const ChordDiagram = ({ data }: { data: any[] }) => {
  const nodes = Array.from(new Set(data.flatMap((d: any) => [d.x, d.y]))).sort();
  const width = 400;
  const height = 300;
  const cx = width / 2;
  const cy = height / 2;
  const outerRadius = 110;
  const innerRadius = 100;
  const padAngle = 0.05;
  const anglePerNode = (2 * Math.PI) / nodes.length;

  return (
    <div className="w-full h-full flex items-center justify-center">
       <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-full max-w-lg">
         {nodes.map((node, i) => {
            const startAngle = i * anglePerNode + padAngle;
            const endAngle = (i + 1) * anglePerNode - padAngle;
            const x1 = cx + outerRadius * Math.cos(startAngle - Math.PI/2);
            const y1 = cy + outerRadius * Math.sin(startAngle - Math.PI/2);
            const x2 = cx + outerRadius * Math.cos(endAngle - Math.PI/2);
            const y2 = cy + outerRadius * Math.sin(endAngle - Math.PI/2);
            const largeArc = (endAngle - startAngle) > Math.PI ? 1 : 0;
            const midAngle = (startAngle + endAngle) / 2 - Math.PI/2;
            const lx = cx + (outerRadius + 20) * Math.cos(midAngle);
            const ly = cy + (outerRadius + 20) * Math.sin(midAngle);

            return (
              <g key={node as string}>
                <path
                  d={`M ${x1} ${y1} A ${outerRadius} ${outerRadius} 0 ${largeArc} 1 ${x2} ${y2}`}
                  fill="none"
                  stroke={COLORS[i % COLORS.length]}
                  strokeWidth={15}
                  strokeLinecap="round"
                />
                <text x={lx} y={ly} textAnchor="middle" dominantBaseline="middle" fontSize="11" fontWeight="bold" fill="#64748b">
                  {`${node}`}
                </text>
              </g>
            );
         })}

         {data.map((d: any, idx) => {
           if (d.value === 0) return null;
           const sourceIdx = nodes.indexOf(d.x);
           const targetIdx = nodes.indexOf(d.y);
           if (sourceIdx === -1 || targetIdx === -1) return null;
           const sAngle = (sourceIdx + 0.5) * anglePerNode;
           const tAngle = (targetIdx + 0.5) * anglePerNode;
           const spread = 0.3;
           const sPos = sAngle - spread/2 + (spread * (targetIdx / (nodes.length - 1 || 1)));
           const tPos = tAngle - spread/2 + (spread * (sourceIdx / (nodes.length - 1 || 1)));
           const r = innerRadius - 10;
           const sx = cx + r * Math.cos(sPos - Math.PI/2);
           const sy = cy + r * Math.sin(sPos - Math.PI/2);
           const tx = cx + r * Math.cos(tPos - Math.PI/2);
           const ty = cy + r * Math.sin(tPos - Math.PI/2);
           const strokeWidth = Math.max(2, d.value / 6);

           return (
             <path
               key={`${d.x}-${d.y}`}
               d={`M ${sx} ${sy} Q ${cx} ${cy} ${tx} ${ty}`}
               fill="none"
               stroke={COLORS[sourceIdx % COLORS.length]}
               strokeWidth={strokeWidth}
               strokeOpacity={0.4}
               className="hover:stroke-opacity-100 transition-all duration-300"
             >
               <title>{`${d.x} -> ${d.y}: ${d.value}`}</title>
             </path>
           );
         })}
       </svg>
    </div>
  );
};

// 11. Graph (Network Hub - Les Miserables style)
export const NetworkGraph = ({ data }: { data: any }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;
    chartInstance.current = echarts.init(chartRef.current);

    const graph = data || { nodes: [], links: [], categories: [] };
    const nodes = (graph.nodes || []).map((node: any) => ({
      ...node,
      label: {
        show: (node.symbolSize || 0) > 30,
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 12,
        backgroundColor: 'rgba(0, 47, 167, 0.8)',
        padding: [4, 8],
        borderRadius: 4
      }
    }));

    const option: echarts.EChartsOption = {
      backgroundColor: 'transparent',
      title: {
        text: '网络化枢纽结构',
        subtext: '基于起降点航线网络的连接度与流量 | 拖拽节点查看详情',
        top: 20,
        left: 'center',
        textStyle: {
          color: '#002FA7',
          fontSize: 18,
          fontWeight: 'bold'
        },
        subtextStyle: {
          color: '#64748b',
          fontSize: 12
        }
      },
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        textStyle: {
          color: '#374151'
        },
        formatter: (params: any) => {
          if (params.dataType === 'edge') {
            return `
              <div style="font-weight: bold; color: #002FA7; margin-bottom: 4px;">航线连接</div>
              <div>${params.data.source} → ${params.data.target}</div>
              <div style="color: #64748b; margin-top: 4px;">流量: <span style="color: #002FA7; font-weight: bold;">${params.data.value}</span></div>
            `;
          } else {
            return `
              <div style="font-weight: bold; color: #002FA7; margin-bottom: 4px;">${params.data.name}</div>
              <div style="color: #64748b;">枢纽度: <span style="color: #002FA7; font-weight: bold;">${params.data.value}</span></div>
              <div style="color: #64748b;">类别: <span style="color: #002FA7;">${params.data.category !== undefined ? graph.categories[params.data.category]?.name : ''}</span></div>
            `;
          }
        },
        confine: true
      },
      legend: [
        {
          orient: 'vertical',
          left: 20,
          top: 80,
          data: (graph.categories || []).map((a: { name: string }) => a.name),
          textStyle: {
            color: '#64748b',
            fontSize: 12
          },
          itemGap: 12,
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#e2e8f0',
          borderWidth: 1,
          borderRadius: 8,
          padding: 12
        }
      ],
      animationDuration: 2000,
      animationEasingUpdate: 'cubicInOut' as any,
      series: [
        {
          name: 'Network Hub',
          type: 'graph',
          legendHoverLink: true,
          layout: 'force',
          data: nodes,
          links: graph.links || [],
          categories: graph.categories || [],
          roam: true,
          zoom: 1,
          scaleLimit: {
            min: 0.5,
            max: 3
          },
          force: {
            repulsion: 250,
            gravity: 0.08,
            edgeLength: [120, 250],
            layoutAnimation: true,
            friction: 0.6
          },
          label: {
            show: true,
            position: 'right',
            formatter: '{b}',
            fontSize: 11,
            color: '#002FA7',
            fontWeight: 'bold'
          },
          itemStyle: {
            borderColor: '#fff',
            borderWidth: 3,
            shadowBlur: 15,
            shadowColor: 'rgba(0, 47, 167, 0.4)'
          },
          lineStyle: {
            color: 'source',
            curveness: 0.3,
            width: 2,
            opacity: 0.5,
            shadowBlur: 8,
            shadowColor: 'rgba(0, 0, 0, 0.2)'
          },
          emphasis: {
            focus: 'adjacency',
            scale: true,
            lineStyle: {
              width: 6,
              opacity: 1,
              shadowBlur: 12,
              shadowColor: 'rgba(0, 47, 167, 0.6)'
            },
            itemStyle: {
              borderWidth: 4,
              shadowBlur: 25,
              shadowColor: 'rgba(0, 47, 167, 0.6)'
            },
            label: {
              show: true,
              fontSize: 14,
              fontWeight: 'bold'
            }
          },
          select: {
            itemStyle: {
              borderColor: '#f59e0b',
              borderWidth: 4
            }
          }
        }
      ],
      toolbox: {
        show: true,
        feature: {
          restore: {
            title: '重置视图'
          },
          saveAsImage: {
            title: '保存为图片',
            pixelRatio: 2
          }
        },
        right: 20,
        top: 20,
        iconStyle: {
          borderColor: '#64748b'
        },
        emphasis: {
          iconStyle: {
            borderColor: '#002FA7'
          }
        }
      }
    };

    chartInstance.current.setOption(option);

    return () => {
      if (chartInstance.current) {
        chartInstance.current.dispose();
      }
    };
  }, [data]);

  useEffect(() => {
    const handleResize = () => {
      if (chartInstance.current) {
        chartInstance.current.resize();
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="w-full h-full relative bg-gradient-to-br from-blue-50/50 to-indigo-50/50 rounded-lg overflow-hidden border border-slate-200 shadow-sm">
      <div
        ref={chartRef}
        className="w-full h-full"
        style={{ minHeight: '450px' }}
      />
      <div className="absolute bottom-3 right-3 text-xs text-slate-500 bg-white/90 backdrop-blur px-3 py-2 rounded-lg border border-slate-200 shadow-sm">
        ⓘ 拖拽节点 | 滚轮缩放 | 点击高亮邻接节点
    </div>
    {/* 图例：解释绿色 / 蓝色弧线含义 */}
    <div className="mt-2 flex justify-center gap-4 text-xs text-slate-600">
      <div className="flex items-center gap-1">
        <span className="inline-block w-3 h-3 rounded-full" style={{ backgroundColor: '#22c55e' }} />
        <span>平均效益</span>
      </div>
      <div className="flex items-center gap-1">
        <span className="inline-block w-3 h-3 rounded-full" style={{ backgroundColor: '#3b82f6' }} />
        <span>TOP50效益</span>
      </div>
    </div>
    </div>
  );
};

// 15. Quality Control Chart (TQI + Control Chart + Time Series)
export const QualityControlChart = ({ data }: { data: any }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;
    chartInstance.current = echarts.init(chartRef.current);

    const { latestTqi = 0, trajData = [], tqiHistory = [], planActual = [] } = data || {};

    // 过滤明显异常的 TQI 数据点（例如 >100% 的值），避免拉高纵轴
    const safeTqiHistory = Array.isArray(tqiHistory) ? tqiHistory : [];
    const filteredTqiHistory = safeTqiHistory.filter((d: any) => {
      const v = typeof d.tqi === 'number' ? d.tqi : parseFloat(String(d.tqi));
      return !Number.isNaN(v) && v <= 100;
    });
    const timeDomain = new Set(filteredTqiHistory.map((d: any) => d.time));

    const safePlanActual = Array.isArray(planActual) ? planActual : [];
    const filteredPlanActual = safePlanActual.filter((d: any) => timeDomain.has(d.time));

    const option: echarts.EChartsOption = {
      backgroundColor: 'transparent',
      grid: [
        // 左侧单一网格用于 TQI 历史趋势与计划对比；右侧仪表盘使用极坐标，不依赖 grid
        // 将趋势+条形图整体上移并在垂直方向压扁一些
        { id: 'g1', left: '5%', top: '0.3%', width: '60%', height: '45%' }
      ],
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          lineStyle: {
            color: '#002FA7',
            width: 1,
            type: 'dashed'
          },
          crossStyle: {
            color: '#002FA7',
            width: 1,
            type: 'dashed'
          }
        },
        textStyle: { fontSize: 11 },
        padding: 10,
        backgroundColor: 'rgba(255, 255, 255, 0.98)',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        borderRadius: 6,
        shadowBlur: 10,
        shadowColor: 'rgba(0, 0, 0, 0.1)'
      },
      xAxis: [
        {
          gridIndex: 0,
          type: 'category',
          data: filteredTqiHistory.map((d: any) => d.time),
          axisLabel: { fontSize: 9, color: '#64748b', rotate: 0 },
          axisLine: { show: false },
          axisTick: { show: false }
        }
      ],
      yAxis: [
        {
          gridIndex: 0,
          type: 'value',
          name: 'TQI (%)',
          nameTextStyle: { fontSize: 11, color: '#64748b', fontWeight: 'bold' },
          nameGap: 30,
          // 仅显示 0、100、200... 等整数百刻度
          min: 0,
          max: (val: any) => Math.ceil(val.max / 100) * 100,
          interval: 100,
          axisLabel: {
            fontSize: 10,
            color: '#64748b',
          },
          // 不显示最高一个刻度标签（但保留网格线）
          showMaxLabel: false,
          axisLine: { show: false },
          splitLine: { lineStyle: { color: '#f1f5f9', type: 'dashed' } }
        }
      ],
      graphic: [
        { type: 'text', left: '6%', top: '1.9%', style: { text: '架次', fill: '#64748b', fontSize: 11, fontWeight: 'bold' } }
      ],
      dataZoom: [
        {
          type: 'inside',
          xAxisIndex: [0],
          start: 0,
          end: 100,
          zoomOnMouseWheel: true,
          moveOnMouseMove: true
        },
        {
          type: 'slider',
          xAxisIndex: [0],
          start: 0,
          end: 100,
          height: 20,
          bottom: 5,
          borderColor: '#e2e8f0',
          fillerColor: 'rgba(14, 165, 233, 0.2)',
          handleStyle: {
            color: '#002FA7',
            borderColor: '#fff',
            borderWidth: 2
          },
          textStyle: {
            color: '#64748b',
            fontSize: 10
          }
        }
      ],
      series: [
        // 1. TQI 仪表盘（右侧略缩小，给左侧趋势图更多空间）
        {
          type: 'gauge',
          // 将 TQI 仪表盘整体向上移动一些
          center: ['80%', '28%'],
          radius: '30%',
          min: 0,
          max: 100,
          startAngle: 225,
          endAngle: -45,
          splitNumber: 4,
          axisLine: {
            lineStyle: {
              width: 22,
              color: [
                [0.6, '#ef4444'],
                [0.85, '#f59e0b'],
                [1, '#10b981']
              ],
              shadowBlur: 15,
              shadowColor: 'rgba(0, 0, 0, 0.2)'
            }
          },
          pointer: {
            width: 6,
            length: '70%',
            itemStyle: {
              color: '#002FA7',
              shadowBlur: 10,
              shadowColor: 'rgba(0, 47, 167, 0.5)'
            }
          },
          axisTick: {
            show: true,
            splitNumber: 5,
            lineStyle: {
              color: '#fff',
              width: 2
            },
            length: 8
          },
          splitLine: {
            length: 22,
            lineStyle: { color: '#fff', width: 3, shadowBlur: 5, shadowColor: 'rgba(0, 0, 0, 0.2)' }
          },
          axisLabel: {
            distance: 28,
            color: '#64748b',
            fontSize: 11,
            fontWeight: 'bold'
          },
          detail: {
            valueAnimation: true,
            formatter: '{value}%',
            color: '#002FA7',
            fontSize: 20,
            fontWeight: 'bold',
            // 数值标签放在仪表盘最下方
            offsetCenter: [0, '100%'],
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            borderRadius: 8,
            padding: [8, -10],
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.1)'
          },
          data: [{ value: latestTqi, name: 'TQI' }],
          title: {
            show: true,
            offsetCenter: [0, '45%'],
            fontSize: 12,
            color: '#64748b',
            fontWeight: 'bold'
          }
        },
        // 2. TQI 历史趋势
        {
          name: 'TQI',
          type: 'line',
          xAxisIndex: 0,
          yAxisIndex: 0,
          data: filteredTqiHistory.map((d: any) => d.tqi),
          smooth: true,
          lineStyle: { width: 3, color: '#0ea5e9', shadowBlur: 8, shadowColor: 'rgba(14, 165, 233, 0.3)' },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(14, 165, 233, 0.4)' },
              { offset: 1, color: 'rgba(14, 165, 233, 0.05)' }
            ]),
            shadowBlur: 10,
            shadowColor: 'rgba(14, 165, 233, 0.2)'
          },
          itemStyle: { color: '#0ea5e9', borderWidth: 2, borderColor: '#fff' },
          symbolSize: 8,
          showSymbol: true,
          emphasis: {
            focus: 'series',
            itemStyle: {
              borderWidth: 3,
              shadowBlur: 10,
              shadowColor: 'rgba(14, 165, 233, 0.6)'
            }
          },
          markLine: {
            silent: true,
            symbol: 'none',
            lineStyle: { type: 'dashed', width: 2 },
            data: [
              {
                yAxis: filteredTqiHistory[0]?.mean || 90,
                name: 'Mean',
                lineStyle: { color: '#10b981', opacity: 0.8 },
                label: { formatter: 'Mean: {c}%', color: '#10b981', fontSize: 10, distance: 5, fontWeight: 'bold' }
              },
              {
                yAxis: filteredTqiHistory[0]?.ucl || 98,
                name: 'UCL',
                lineStyle: { color: '#f59e0b', opacity: 0.8 },
                label: { formatter: 'UCL: {c}%', color: '#f59e0b', fontSize: 10, distance: 5, fontWeight: 'bold' }
              }
            ]
          }
        },
        // 3. 计划 vs 实际（柱状图）
        {
          name: '实际完成',
          type: 'bar',
          xAxisIndex: 0,
          yAxisIndex: 0,
          data: filteredPlanActual.map((d: any) => d.actual),
          barWidth: '30%',
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(14, 165, 233, 0.8)' },
              { offset: 1, color: 'rgba(14, 165, 233, 0.5)' }
            ]),
            borderRadius: [4, 4, 0, 0],
            shadowBlur: 8,
            shadowColor: 'rgba(14, 165, 233, 0.3)'
          },
          emphasis: {
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(14, 165, 233, 1)' },
                { offset: 1, color: 'rgba(14, 165, 233, 0.7)' }
              ])
            }
          },
          z: 2
        },
        {
          name: '计划报备',
          type: 'bar',
          xAxisIndex: 0,
          yAxisIndex: 0,
          data: filteredPlanActual.map((d: any) => d.planned),
          barWidth: '18%',
          itemStyle: {
            color: 'rgba(100, 116, 139, 0.25)',
            borderColor: '#64748b',
            borderWidth: 1,
            borderType: 'dashed',
            borderRadius: [4, 4, 0, 0]
          },
          emphasis: {
            itemStyle: {
              color: 'rgba(100, 116, 139, 0.35)'
            }
          },
          z: 1
        }
      ],
      legend: {
        data: ['TQI', '实际完成', '计划报备'],
        bottom: '3%',
        left: 'center',
        textStyle: { color: '#64748b', fontSize: 11 },
        itemGap: 20,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#e2e8f0',
        borderWidth: 1,
        borderRadius: 6,
        padding: 10
      },
      toolbox: {
        show: true,
        feature: {
          dataZoom: {
            title: {
              zoom: '区域缩放',
              back: '还原'
            },
            yAxisIndex: false
          },
          restore: {
            title: '重置'
          },
          saveAsImage: {
            title: '保存为图片',
            pixelRatio: 2
          }
        },
        right: 20,
        top: '58%',
        iconStyle: {
          borderColor: '#64748b'
        },
        emphasis: {
          iconStyle: {
            borderColor: '#002FA7'
          }
        }
      }
    };

    chartInstance.current.setOption(option);

    return () => {
      if (chartInstance.current) {
        chartInstance.current.dispose();
      }
    };
  }, [data]);

  useEffect(() => {
    const handleResize = () => {
      if (chartInstance.current) {
        chartInstance.current.resize();
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="w-full h-full relative bg-gradient-to-br from-slate-50 to-blue-50/30 rounded-lg overflow-hidden border border-slate-200 shadow-sm">
      <div
        ref={chartRef}
        className="w-full h-full"
        style={{ minHeight: '550px' }}
      />
      <div className="absolute bottom-3 left-3 text-[11px] leading-snug text-slate-500 bg-white/90 backdrop-blur px-3 py-1.5 rounded-md border border-slate-200 shadow-sm max-w-[60%] text-left">
        因暂未获取完整真实飞行计划报备数据，本指标相关数据均为模拟生成，仅作功能演示与逻辑理解使用，不代表实际运行情况与真实效益。
      </div>
      <div className="absolute bottom-3 right-3 text-xs text-slate-500 bg-white/90 backdrop-blur px-3 py-2 rounded-lg border border-slate-200 shadow-sm">
        ⓘ 拖拽缩放时间轴 | 悬停查看详情
      </div>
    </div>
  );
};

// Color palette for airspace visualization
const AIRSPACE_COLORS = ['#bae6fd', '#7dd3fc', '#38bdf8', '#0ea5e9', '#0284c7', '#0369a1', '#075985'];

// 17. 2D Grouped Bar (Vertical Airspace)
export const AirspaceBarChart = ({ data }: { data: any }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  // 2D rendering function
  const render2D = useCallback((chart: echarts.ECharts, chartData: any) => {
    // Check if it's the structured data format or old array format
    const isStructuredData = chartData && chartData.districts && chartData.altitudes && chartData.data;

    if (isStructuredData) {
      // Convert structured data to 2D grouped bar chart
      // Group data by altitude layer
      const altitudeData: any = {};
      chartData.altitudes.forEach((alt: string, altIdx: number) => {
        altitudeData[alt] = chartData.districts.map((_: string, distIdx: number) => {
          const dataPoint = chartData.data.find((d: number[]) => d[0] === altIdx && d[1] === distIdx);
          return dataPoint ? dataPoint[2] : 0;
        });
      });

      const option: any = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: (params: any) => {
            let result = `${params[0].name}<br/>`;
            params.forEach((item: any) => {
              result += `${item.seriesName}: ${item.value} 分钟<br/>`;
            });
            return result;
          }
        },
        legend: {
          data: chartData.altitudes,
          textStyle: {
            color: '#64748b',
            fontSize: 10
          },
          top: 10
        },
        grid: {
          // 整体条形图（含坐标轴）进一步向左移动；底部留足空间给横轴名称（轴下方）
          left: '6%',
          right: '4%',
          bottom: '10%',
          top: '20%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          axisLabel: {
            color: '#64748b',
            fontSize: 10
          },
          axisLine: {
            lineStyle: { color: '#cbd5e1' }
          },
          splitLine: {
            lineStyle: { color: '#e5e7eb' }
          }
        },
        yAxis: {
          type: 'category',
          data: chartData.districts,
          axisLabel: {
            color: '#64748b',
            fontSize: 10
          },
          axisLine: {
            lineStyle: { color: '#cbd5e1' }
          }
        },
        graphic: [
          {
            type: 'text',
            right: 5,
            bottom: 20,
            style: {
              text: '年度累计时长(分钟)',
              fill: '#64748b',
              fontSize: 11
            }
          }
        ],
        series: chartData.altitudes.map((alt: string, idx: number) => ({
          name: alt,
          type: 'bar',
          data: altitudeData[alt],
          itemStyle: {
            color: AIRSPACE_COLORS[idx % AIRSPACE_COLORS.length]
          }
        }))
      };
      chart.setOption(option);
    } else {
      // Old simple array format
      const option: any = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '15%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '分钟',
          axisLabel: {
            color: '#64748b',
            fontSize: 10
          },
          axisLine: {
            lineStyle: { color: '#cbd5e1' }
          },
          splitLine: {
            lineStyle: { color: '#e5e7eb' }
          }
        },
        yAxis: {
          type: 'category',
          data: chartData.map((d: any) => d.name),
          axisLabel: {
            color: '#64748b',
            fontSize: 10
          },
          axisLine: {
            lineStyle: { color: '#cbd5e1' }
          }
        },
        series: [{
          type: 'bar',
          data: chartData.map((d: any, index: number) => ({
            value: d.value,
            itemStyle: {
              color: index === 0 ? '#f59e0b' : index === 1 ? '#ea580c' : '#dc2626'
            }
          })),
          barWidth: '60%'
        }]
      };
      chart.setOption(option);
    }
  }, []);

  useEffect(() => {
    if (!chartRef.current) return;

    // Initialize chart if not already done
    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current);
    }

    const chart = chartInstance.current;

    // Always use 2D rendering
    render2D(chart, data);
  }, [data, render2D]);

  // Handle resize in separate effect
  useEffect(() => {
    const handleResize = () => {
      if (chartInstance.current) {
        chartInstance.current.resize();
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      // Cleanup chart instance on unmount
      if (chartInstance.current) {
        chartInstance.current.dispose();
        chartInstance.current = null;
      }
    };
  }, []);

  return (
    <div
      ref={chartRef}
      role="img"
      aria-label="Airspace distribution by district horizontal bar chart"
      style={{
        width: '100%',
        height: '100%',
        minHeight: `${CHART_MIN_HEIGHT}px`
      }}
    />
  );
};

// 18. Calendar Heatmap
export const CalendarHeatmap = ({ data }: { data: any[] }) => {
  const [hoveredDay, setHoveredDay] = useState<any>(null);
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
  const dayNames = ['日', '一', '二', '三', '四', '五', '六'];

  // Group data by month
  const monthsData = Array.from({length: 12}, (_, i) => {
    return data.filter(d => new Date(d.date).getMonth() === i);
  });

  // Calculate dynamic min/max from actual data for color scaling
  const values = data.map(d => d.value || 0).filter(v => v > 0);
  const min = values.length > 0 ? Math.min(...values) : 400;
  const max = values.length > 0 ? Math.max(...values) : 1000;
  
  const getHeatColor = (val: number) => {
    // Dynamically scale based on actual data range
    const range = max - min;
    const pct = range > 0 ? Math.max(0, Math.min(1, (val - min) / range)) : 0.5;

    // Gradient: Light Blue (Low) -> Orange -> Red (High)
    // 0 - 0.2: Sky Blues (Background-ish)
    if (pct < 0.2) return '#e0f2fe'; // sky-100
    if (pct < 0.35) return '#bae6fd'; // sky-200

    // 0.35 - 1.0: Warm Colors (Foreground)
    if (pct < 0.5) return '#fed7aa'; // orange-200
    if (pct < 0.7) return '#fb923c'; // orange-400
    if (pct < 0.85) return '#ea580c'; // orange-600
    return '#b91c1c'; // red-700
  };

  return (
    <div className="w-full h-full relative p-2 overflow-hidden">
       {/* Grid of Months */}
       <div className="w-full h-full grid grid-cols-4 grid-rows-3 gap-x-2 gap-y-4">
         {monthsData.map((mDays, mIdx) => {
           if (mDays.length === 0) return null;
           const firstDate = new Date(mDays[0].date);
           const startDay = firstDate.getDay(); // 0-6

           return (
             <div key={mIdx} className="flex flex-col">
               <span className="text-[10px] font-bold text-slate-400 mb-1">{months[mIdx]}</span>
               <div className="flex-1 grid grid-cols-7 grid-rows-6 gap-[1px]">
                  {/* Headers */}
                  {dayNames.map((dn, i) => (
                    <div key={i} className="text-[6px] text-center text-slate-300">{dn}</div>
                  ))}
                  {/* Empty Start Slots */}
                  {Array.from({length: startDay}).map((_, i) => <div key={`empty-${i}`} />)}
                  {/* Days */}
                  {mDays.map((d, i) => (
                    <button
                      key={i}
                      type="button"
                      aria-label={`${d.date}, ${d.value}架次`}
                      className="rounded-[1px] cursor-pointer hover:ring-1 hover:ring-slate-400 transition-all w-full h-full block focus:outline-none focus:ring-2 focus:ring-[#002FA7] focus:z-10"
                      style={{ backgroundColor: getHeatColor(d.value) }}
                      onMouseEnter={(e) => {
                         const rect = e.currentTarget.getBoundingClientRect();
                         setHoveredDay({ ...d, x: rect.left, y: rect.top });
                      }}
                      onMouseLeave={() => setHoveredDay(null)}
                      onFocus={(e) => {
                        const rect = e.currentTarget.getBoundingClientRect();
                        setHoveredDay({ ...d, x: rect.left, y: rect.top });
                      }}
                      onBlur={() => setHoveredDay(null)}
                    />
                  ))}
               </div>
             </div>
           )
         })}
       </div>

       {/* Custom Tooltip */}
       {hoveredDay && (
         <div
           className="fixed bg-slate-800 text-white text-xs p-2 rounded shadow-xl z-50 pointer-events-none transform -translate-x-1/2 -translate-y-full mt-[-8px]"
           style={{ left: hoveredDay.x + 8, top: hoveredDay.y }}
         >
            <div className="font-bold">{hoveredDay.date}</div>
            <div className="flex justify-between gap-4 mt-1">
               <span className="text-slate-400">架次:</span>
               <span className="font-mono">{hoveredDay.value}</span>
            </div>
            <div className="text-[10px] text-slate-500 mt-1">
               {(new Date(hoveredDay.date).getDay() % 6 === 0) ? '周末' : '工作日'}
            </div>
         </div>
       )}

       {/* Legend */}
       <div className="absolute bottom-0 right-0 flex items-center gap-1 text-[8px] text-slate-400 bg-white/80 p-1 rounded">
          <span>少</span>
          <div className="w-2 h-2 bg-[#e0f2fe]"></div>
          <div className="w-2 h-2 bg-[#fed7aa]"></div>
          <div className="w-2 h-2 bg-[#ea580c]"></div>
          <div className="w-2 h-2 bg-[#b91c1c]"></div>
          <span>多</span>
       </div>
    </div>
  );
};

// 19. Waveform (Night Economy)
export const NightWaveChart = ({ data, ariaLabel = "Night economy waveform chart" }: ChartProps) => (
  <div role="img" aria-label={ariaLabel} style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
    <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
    <AreaChart data={data} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
       <defs>
        <linearGradient id="colorNight" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
          <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
        </linearGradient>
      </defs>
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
      <XAxis
        dataKey="hour"
        tick={{fontSize: 10, fill: '#64748b'}}
        axisLine={false}
        tickLine={false}
        // 横坐标右下方标注“时间”，略向左、向下
        label={{
          value: '时间',
          position: 'insideBottomRight',
          offset: 2,
          fill: '#64748b',
          fontSize: 11
        }}
      />
      <YAxis
        tick={{fontSize: 10, fill: '#64748b'}}
        axisLine={false}
        tickLine={false}
        // 纵坐标左侧标注“架次”
        label={{ value: '架次', angle: -90, position: 'insideLeft', offset: 10, fill: '#64748b', fontSize: 11 }}
      />
      <Tooltip />
       <Area type="monotone" dataKey="value" stroke="#f59e0b" fill="url(#colorNight)" />
    </AreaChart>
  </ResponsiveContainer>
  </div>
);

// 雷达图实体颜色（按顺序循环使用）
const RADAR_ENTITY_COLORS = ['#f97316', '#0ea5e9', '#22c55e', '#6366f1', '#eab308', '#ec4899', '#14b8a6', '#f59e0b'];

// 20. Radar (Leading Entity) - 动态解析 data 中除 subject/fullMark 外的键作为实体名，图例与 Tooltip 均显示该名称
export const EntityRadarChart = ({ data, ariaLabel = "Entity comparison radar chart" }: ChartProps) => {
  const isEmpty = useMemo(() => !data || data.length === 0, [data]);

  // 从第一条数据解析出所有实体键（排除 subject、fullMark），顺序与数据一致
  const entityKeys = useMemo(() => {
    if (!data?.length) return [];
    return Object.keys(data[0]).filter((k) => k !== 'subject' && k !== 'fullMark');
  }, [data]);

  const [activeSeries, setActiveSeries] = useState<string[]>([]);
  useEffect(() => {
    setActiveSeries(entityKeys);
  }, [entityKeys.join(',')]);

  if (isEmpty) {
    return (
      <div
        style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        role="status"
        aria-label="No data available for chart"
      >
        <p style={{ color: '#64748b', fontSize: '14px' }}>📊 No data available</p>
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height: '100%', minHeight: `${CHART_MIN_HEIGHT}px` }}>
      <ResponsiveContainer width="100%" height="100%" minHeight={CHART_MIN_HEIGHT}>
        <RadarChart
          cx="50%"
          cy="50%"
          outerRadius="70%"
          data={data}
          aria-label={ariaLabel}
        >
          <PolarGrid stroke="#e5e7eb" />
          <PolarAngleAxis
            dataKey="subject"
            tick={{fontSize: 10, fill: '#64748b'}}
          />
          <PolarRadiusAxis
            angle={30}
            domain={[0, 100]}
            tick={{fontSize: 10, fill: '#64748b'}}
            axisLine={{ stroke: '#e5e7eb' }}
          />
          {entityKeys.map((key, idx) => (
            <Radar
              key={key}
              name={key}
              dataKey={key}
              stroke={RADAR_ENTITY_COLORS[idx % RADAR_ENTITY_COLORS.length]}
              fill={RADAR_ENTITY_COLORS[idx % RADAR_ENTITY_COLORS.length]}
              fillOpacity={0.4}
              animationDuration={800}
              animationEasing="ease-in-out"
              hide={!activeSeries.includes(key)}
            />
          ))}
          <Legend
            wrapperStyle={{ fontSize: '12px' }}
            content={(props: any) => {
              const { payload } = props;
              if (!payload) return null;
              return (
                <div className="flex flex-wrap justify-center gap-3 text-xs text-slate-700">
                  {payload.map((entry: any) => {
                    const key = entry.dataKey as string;
                    const active = activeSeries.includes(key);
                    return (
                      <button
                        key={key}
                        type="button"
                        onClick={() =>
                          setActiveSeries((prev) =>
                            prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]
                          )
                        }
                        className="flex items-center gap-1 cursor-pointer focus:outline-none"
                        style={{ opacity: active ? 1 : 0.35 }}
                      >
                        <span
                          className="inline-block w-3 h-3 rounded-sm"
                          style={{ backgroundColor: entry.color }}
                        />
                        <span>{entry.value}</span>
                      </button>
                    );
                  })}
                </div>
              );
            }}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (!active || !payload || !payload.length) return null;

              const activeItem = payload.reduce(
                (best: any, cur: any) =>
                  !best || (cur && typeof cur.value === 'number' && cur.value > best.value)
                    ? cur
                    : best,
                null
              );

              if (!activeItem) return null;

              const activeKey = activeItem.dataKey as string;
              const activeName = activeItem.name as string;

              const rows = (data as any[]).map((d) => ({
                subject: d.subject,
                value: d[activeKey] as number | undefined,
              }));

              return (
                <div className="rounded-lg border border-slate-200 bg-white px-3 py-2 shadow-md text-xs">
                  <div className="font-semibold text-slate-800 mb-1">{activeName}</div>
                  {rows.map((row) => (
                    <div key={row.subject} className="flex justify-between gap-4">
                      <span className="text-slate-500">{row.subject}</span>
                      <span className="text-slate-800">
                        {row.value != null ? `${row.value.toFixed(1)} 分` : '--'}
                      </span>
                    </div>
                  ))}
                </div>
              );
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

// 18. Dashboard (Composite) - Grade Gauge with ECharts
export const CompositeDashboardChart = ({ data }: { data: any[] }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);
    const val = data[0].value / 100; // Convert to 0-1 range for gauge

    const option = {
      backgroundColor: 'transparent',
      series: [
        // Background arc
        {
          type: 'gauge',
          startAngle: 180,
          endAngle: 0,
          center: ['50%', '75%'],
          radius: '95%',
          min: 0,
          max: 1,
          splitNumber: 8,
          axisLine: {
            lineStyle: {
              width: 2,
              color: [[1, '#f1f5f9']]
            }
          },
          pointer: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          detail: { show: false }
        },
        // Main gauge
        {
          type: 'gauge',
          startAngle: 180,
          endAngle: 0,
          center: ['50%', '75%'],
          radius: '90%',
          min: 0,
          max: 1,
          splitNumber: 8,
          axisLine: {
            lineStyle: {
              width: 12,
              color: [
                [0.25, '#FF6E76'],   // D级 - 红色
                [0.5, '#FDDD60'],    // C级 - 黄色
                [0.75, '#58D9F9'],   // B级 - 蓝色
                [1, '#7CFFB2']       // A级 - 绿色
              ],
              shadowBlur: 20,
              shadowColor: 'rgba(0, 0, 0, 0.15)'
            }
          },
          pointer: {
            icon: 'path://M2.9,0.7L2.9,0.7c1.4,0,2.6,1.2,2.6,2.6v115c0,1.4-1.2,2.6-2.6,2.6l0,0c-1.4,0-2.6-1.2-2.6-2.6V3.3C0.3,1.9,1.4,0.7,2.9,0.7z',
            length: '75%',
            width: 8,
            offsetCenter: [0, '-5%'],
            itemStyle: {
              color: 'auto',
              shadowBlur: 15,
              shadowColor: 'rgba(0, 0, 0, 0.3)',
              shadowOffsetX: 0,
              shadowOffsetY: 3
            }
          },
          axisTick: {
            length: 15,
            lineStyle: {
              color: 'auto',
              width: 2,
              shadowBlur: 5,
              shadowColor: 'rgba(0, 0, 0, 0.1)'
            },
            distance: -15
          },
          splitLine: {
            length: 25,
            lineStyle: {
              color: 'auto',
              width: 5,
              shadowBlur: 8,
              shadowColor: 'rgba(0, 0, 0, 0.2)'
            },
            distance: -25
          },
          axisLabel: {
            color: '#464646',
            fontSize: 16,
            fontWeight: 'bold',
            distance: -65,
            rotate: 'tangential',
            formatter: function (value: number) {
              if (value === 0.875) {
                return 'A级';
              } else if (value === 0.625) {
                return 'B级';
              } else if (value === 0.375) {
                return 'C级';
              } else if (value === 0.125) {
                return 'D级';
              }
              return '';
            }
          },
          title: {
            offsetCenter: [0, '-15%'],
            fontSize: 18,
            color: '#002FA7',
            fontWeight: 'bold'
          },
          detail: {
            fontSize: 36,
            offsetCenter: [0, '-40%'],
            valueAnimation: true,
            formatter: function (value: number) {
              const score = Math.round(value * 100);
              let grade = 'D级';
              if (score >= 75) grade = 'A级';
              else if (score >= 50) grade = 'B级';
              else if (score >= 25) grade = 'C级';

              return grade + '\n' + score;
            },
            color: 'auto',
            fontWeight: 'bold',
            lineHeight: 40,
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            borderRadius: 12,
            padding: [12, 20],
            shadowBlur: 15,
            shadowColor: 'rgba(0, 0, 0, 0.15)'
          },
          data: [
            {
              value: val,
              name: '综合指数等级'
            }
          ]
        },
        // Progress circle effect
        {
          type: 'gauge',
          startAngle: 180,
          endAngle: 0,
          center: ['50%', '75%'],
          radius: '72%',
          min: 0,
          max: 1,
          splitNumber: 100,
          axisLine: {
            lineStyle: {
              width: 4,
              color: [
                [val, {
                  type: 'linear',
                  x: 0, y: 0, x2: 1, y2: 0,
                  colorStops: [
                    { offset: 0, color: val >= 0.75 ? '#7CFFB2' : val >= 0.5 ? '#58D9F9' : val >= 0.25 ? '#FDDD60' : '#FF6E76' },
                    { offset: 1, color: val >= 0.75 ? '#5de3a5' : val >= 0.5 ? '#3cc5f0' : val >= 0.25 ? '#f5c842' : '#ff5560' }
                  ]
                }],
                [1, 'rgba(0, 0, 0, 0.05)']
              ]
            }
          },
          pointer: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
          detail: { show: false }
        }
      ],
      animation: true,
      animationDuration: 2000,
      animationEasing: 'elasticOut'
    };

    chartInstance.current.setOption(option);

    // Cleanup
    return () => {
      if (chartInstance.current) {
        chartInstance.current.dispose();
      }
    };
  }, [data]);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      if (chartInstance.current) {
        chartInstance.current.resize();
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="w-full h-full relative bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 rounded-lg p-4 border border-slate-200 shadow-sm">
      <div
        ref={chartRef}
        className="w-full h-full"
        style={{ minHeight: '300px' }}
      />

      {/* Enhanced Grade Legend */}
      <div className="absolute bottom-4 left-4 right-4">
        <div className="bg-white/95 backdrop-blur rounded-lg p-3 border border-slate-200 shadow-sm">
          <div className="flex justify-center flex-wrap gap-4 text-sm">
          <div className="flex items-center space-x-2">
              <div className="w-5 h-5 rounded-full shadow-md" style={{
                background: 'linear-gradient(135deg, #FF6E76 0%, #ff5560 100%)'
              }}></div>
              <span className="text-slate-700 font-medium">D级 (0-25)</span>
          </div>
          <div className="flex items-center space-x-2">
              <div className="w-5 h-5 rounded-full shadow-md" style={{
                background: 'linear-gradient(135deg, #FDDD60 0%, #f5c842 100%)'
              }}></div>
              <span className="text-slate-700 font-medium">C级 (25-50)</span>
          </div>
          <div className="flex items-center space-x-2">
              <div className="w-5 h-5 rounded-full shadow-md" style={{
                background: 'linear-gradient(135deg, #58D9F9 0%, #3cc5f0 100%)'
              }}></div>
              <span className="text-slate-700 font-medium">B级 (50-75)</span>
          </div>
          <div className="flex items-center space-x-2">
              <div className="w-5 h-5 rounded-full shadow-md" style={{
                background: 'linear-gradient(135deg, #7CFFB2 0%, #5de3a5 100%)'
              }}></div>
              <span className="text-slate-700 font-medium">A级 (75-100)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Info */}
      <div className="absolute top-3 right-3 text-xs text-slate-600 bg-white/90 backdrop-blur px-3 py-1.5 rounded-lg border border-slate-200 shadow-sm font-medium">
        ⓘ 等级评估仪表盘
      </div>
    </div>
  );
};

// Helper component for accessible table view
const SimpleTable = ({ data }: { data: any[] }) => {
  if (!data || !data.length) return null;

  // Extract headers from the first item, ignoring 'children' or object types for simplicity
  const headers = Object.keys(data[0]).filter(k =>
    k !== 'children' &&
    typeof data[0][k] !== 'object' &&
    !k.startsWith('_') // ignore internal properties if any
  );

  return (
    <div className="w-full h-full overflow-auto bg-white p-4 rounded-lg border border-slate-100">
      <table className="w-full text-sm text-left text-slate-600">
        <caption className="sr-only">Data Table View</caption>
        <thead className="text-xs text-slate-500 uppercase bg-slate-50 sticky top-0 z-10">
          <tr>
            {headers.map(h => (
              <th key={h} scope="col" className="px-4 py-3 font-medium tracking-wider whitespace-nowrap">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {data.map((row, i) => (
            <tr key={i} className="hover:bg-slate-50 transition-colors">
              {headers.map(h => (
                <td key={`${i}-${h}`} className="px-4 py-3 whitespace-nowrap font-mono text-xs">
                   {row[h]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Map chart types to components
export const ChartRenderer = ({ type, data, definition, title }: { type: string, data: any, definition?: string, title?: string }) => {
    const [isTableView, setIsTableView] = useState(false);

    // Check if data is suitable for table view (array of objects)
    const hasTableData = useMemo(() => {
        return Array.isArray(data) && data.length > 0 && typeof data[0] === 'object' && !Array.isArray(data[0]);
    }, [data]);

    // Add a subtle info icon if definition is present
    const Container = ({ children }: { children: React.ReactNode }) => (
      <div
        className="w-full h-full min-h-[280px] min-w-0 relative group/container"
        role="figure"
        aria-label={title ? `${title} 图表` : "数据图表"}
      >
         {/* Main Content: Chart or Table */}
         {isTableView && hasTableData ? (
             <SimpleTable data={data} />
         ) : (
             children
         )}

         {/* Controls Area */}
         <div className="absolute top-2 right-2 z-20 flex items-center space-x-2 opacity-0 group-hover/container:opacity-100 focus-within:opacity-100 transition-opacity duration-200">
             {hasTableData && (
                <button
                    onClick={() => setIsTableView(!isTableView)}
                    aria-label={isTableView ? "切换回图表视图" : "切换至表格视图"}
                    title={isTableView ? "查看图表" : "查看数据"}
                    className="w-7 h-7 flex items-center justify-center bg-white/90 backdrop-blur rounded-md shadow-sm border border-slate-200 text-slate-400 hover:text-[#002FA7] hover:border-[#002FA7] hover:bg-white focus:outline-none focus:ring-2 focus:ring-[#002FA7] transition-all"
                >
                    {isTableView ? (
                        <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                    ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                        </svg>
                    )}
                </button>
             )}

         {definition && (
               <div className="relative group/tooltip">
              <button
                aria-label="查看指标定义"
                    className="w-7 h-7 flex items-center justify-center bg-white/90 backdrop-blur rounded-md shadow-sm border border-slate-200 text-slate-400 hover:text-[#002FA7] hover:border-[#002FA7] hover:bg-white focus:outline-none focus:ring-2 focus:ring-[#002FA7] transition-all"
              >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </button>
              <div
                role="tooltip"
                    className="absolute top-8 right-0 w-64 opacity-0 group-hover/tooltip:opacity-100 group-focus-within/tooltip:opacity-100 transition-opacity duration-200 pointer-events-none group-hover/tooltip:pointer-events-auto group-focus-within/tooltip:pointer-events-auto z-30"
              >
                     <div className="bg-slate-800 text-white text-xs p-3 rounded-lg shadow-xl border border-slate-700 relative">
                    {/* Little arrow */}
                        <div className="absolute top-0 right-2 -mt-1 w-2 h-2 bg-slate-800 transform rotate-45 border-t border-l border-slate-700"></div>
                    <div className="font-bold mb-1 border-b border-slate-600 pb-1 text-slate-200">指标定义</div>
                    <p className="leading-relaxed text-slate-300">{definition}</p>
                 </div>
              </div>
           </div>
         )}
         </div>
      </div>
    );

    let ChartComponent;
    // Pass localized aria-label if title is available to override default English labels
    const commonProps = {
      data,
      ariaLabel: title ? `${title} 图表` : undefined
    };

    switch (type) {
        case 'Area': ChartComponent = <TrafficAreaChart {...commonProps} />; break;
        case 'DualLine': ChartComponent = <DualLineChart {...commonProps} />; break;
        case 'StackedBar': ChartComponent = <StackedBarChart {...commonProps} />; break;
        case 'Pareto': ChartComponent = <ParetoChart {...commonProps} />; break;
        case 'Rose': ChartComponent = <NightingaleRoseChart {...commonProps} />; break;
        case 'Treemap': ChartComponent = <FleetTreemap {...commonProps} />; break;
        case 'Map': ChartComponent = <ChoroplethMap data={data} />; break;
        case 'Polar': ChartComponent = <PolarClockChart {...commonProps} />; break;
        case 'BoxPlot': ChartComponent = <SeasonalBoxChart {...commonProps} />; break;
        case 'Gauge': ChartComponent = <GaugeChart {...commonProps} />; break;
        case 'Funnel': ChartComponent = <MissionFunnelChart {...commonProps} />; break;
        case 'Histogram': ChartComponent = <CoverageHistogram {...commonProps} />; break;
        case 'Chord': ChartComponent = <ChordDiagram data={data} />; break;
        case 'Graph': ChartComponent = <NetworkGraph data={data} />; break;
        case 'ControlChart': ChartComponent = <QualityControlChart data={data} />; break;
        case 'GroupedBar':
          // Use AirspaceBarChart for grouped bar (chart #17)
          ChartComponent = <AirspaceBarChart data={data} />;
          break;
        case 'Calendar': ChartComponent = <CalendarHeatmap data={data} />; break;
        case 'Wave': ChartComponent = <NightWaveChart {...commonProps} />; break;
        case 'Radar': ChartComponent = <EntityRadarChart {...commonProps} />; break;
        case 'Dashboard': ChartComponent = <CompositeDashboardChart data={data} />; break;
        default: ChartComponent = <div className="flex items-center justify-center h-full text-red-500">未知图表类型</div>;
    }

    return <Container>{ChartComponent}</Container>;
};
