import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, BarChart, Bar, ComposedChart,
  PieChart, Pie, Cell, Treemap, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  ScatterChart, Scatter, ZAxis, Legend, RadialBarChart, RadialBar, FunnelChart, Funnel, LabelList,
  Sector
} from 'recharts';
import * as echarts from 'echarts';

const COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#6366f1'];

// 1. Area Chart (Traffic)
export const TrafficAreaChart = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
      <defs>
        <linearGradient id="colorVal" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.8}/>
          <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
        </linearGradient>
      </defs>
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
      <XAxis dataKey="date" tick={{fontSize: 10}} tickLine={false} axisLine={false} />
      <YAxis tick={{fontSize: 10}} tickLine={false} axisLine={false} />
      <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
      <Area type="monotone" dataKey="value" stroke="#0ea5e9" fillOpacity={1} fill="url(#colorVal)" />
    </AreaChart>
  </ResponsiveContainer>
);

// 2. Dual Line Chart (Operation Intensity)
export const DualLineChart = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
      <XAxis dataKey="name" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
      <YAxis yAxisId="left" tick={{fontSize: 10}} axisLine={false} tickLine={false} label={{ value: '时长 (小时)', angle: -90, position: 'insideLeft', style: {fontSize: 10, fill: '#64748b'} }} />
      <YAxis yAxisId="right" orientation="right" tick={{fontSize: 10}} axisLine={false} tickLine={false} label={{ value: '里程 (公里)', angle: 90, position: 'insideRight', style: {fontSize: 10, fill: '#64748b'} }} />
      <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
      <Line yAxisId="left" type="monotone" dataKey="duration" name="时长" stroke="#0ea5e9" strokeWidth={3} dot={{r: 4}} />
      <Line yAxisId="right" type="monotone" dataKey="distance" name="里程" stroke="#10b981" strokeWidth={3} dot={{r: 4}} />
      <Legend />
    </ComposedChart>
  </ResponsiveContainer>
);

// 3. Stacked Bar (Fleet)
export const StackedBarChart = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
      <XAxis dataKey="name" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
      <YAxis tick={{fontSize: 10}} axisLine={false} tickLine={false} />
      <Tooltip cursor={{fill: '#f3f4f6'}} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
      <Legend />
      <Bar dataKey="MultiRotor" name="多旋翼" stackId="a" fill="#0ea5e9" radius={[0,0,0,0]} />
      <Bar dataKey="FixedWing" name="固定翼" stackId="a" fill="#10b981" radius={[0,0,0,0]} />
      <Bar dataKey="Helicopter" name="直升机" stackId="a" fill="#f59e0b" radius={[4,4,0,0]} />
    </BarChart>
  </ResponsiveContainer>
);

// 4. Pareto (Concentration)
export const ParetoChart = ({ data }: { data: any[] }) => {
  const processedData = React.useMemo(() => {
    const total = data.reduce((acc, cur) => acc + cur.volume, 0);
    let cumulative = 0;
    return data.map(d => {
      cumulative += d.volume;
      return { ...d, cumulative: Math.round((cumulative / total) * 100) };
    });
  }, [data]);

  return (
    <ResponsiveContainer width="100%" height="100%">
      <ComposedChart data={processedData} margin={{ top: 20, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
        <XAxis dataKey="name" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
        <YAxis yAxisId="left" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
        <YAxis yAxisId="right" orientation="right" tick={{fontSize: 10}} axisLine={false} tickLine={false} unit="%" />
        <Tooltip />
        <Bar yAxisId="left" dataKey="volume" name="飞行量" fill="#0ea5e9" barSize={20} radius={[4,4,0,0]} />
        <Line yAxisId="right" type="monotone" dataKey="cumulative" name="累计占比" stroke="#f59e0b" strokeWidth={2} dot={{r: 3}} />
      </ComposedChart>
    </ResponsiveContainer>
  );
};

// 5. Nightingale Rose Chart (Commercial Maturity)
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

export const NightingaleRoseChart = ({ data }: { data: any[] }) => {
  const { maxVal, roseData } = useMemo(() => {
    const maxVal = Math.max(...data.map((d: any) => d.value));

    const roseData = data.map((d: any) => ({
      ...d,
      realValue: d.value,
      value: 1
    }));
    return { maxVal, roseData };
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

  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={roseData}
          cx="50%"
          cy="50%"
          innerRadius={30}
          outerRadius={130}
          dataKey="value"
          shape={<RoseShape maxVal={maxVal} />}
          paddingAngle={0}
        >
          {roseData.map((entry: any, index: number) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip
            formatter={(value: any, name: any, props: any) => [props.payload.realValue, name]}
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
        />
        <Legend verticalAlign="bottom" height={36} wrapperStyle={{color: '#64748b'}}/>
      </PieChart>
    </ResponsiveContainer>
  );
};

// 6. Treemap (Diversity)
const CustomTreemapContent = (props: any) => {
  const { root, depth, x, y, width, height, index, name, value } = props;
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
      {width > 50 && height > 30 && (
        <text x={x + width / 2} y={y + height / 2 + 7} textAnchor="middle" fill="#fff" fontSize={12} fontWeight="bold">
           {name}
        </text>
      )}
    </g>
  );
};

export const FleetTreemap = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <Treemap
      data={data}
      dataKey="size"
      aspectRatio={4 / 3}
      stroke="#fff"
      fill="#8884d8"
      content={<CustomTreemapContent />}
    />
  </ResponsiveContainer>
);

// 7. Choropleth Map (Regional Balance) - Advanced ECharts Implementation
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

      // Calculate density statistics
      const values = data.map(d => d.value);
      const maxValue = Math.max(...values);
      const minValue = Math.min(...values);

      // Create pie series for major airports/hubs
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

        const option = {
          title: {
            text: '深圳无人机飞行密度分布图',
            subtext: '基于区域飞行频率与枢纽分布数据\n深圳坐标系：WGS84 | 数据更新：2024年',
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
              borderColor: '#e2e8f0',
              borderWidth: 1.5
            },
            emphasis: {
              label: {
                show: false
              },
              itemStyle: {
                areaColor: '#e0f2fe'
              }
            },
            label: {
              show: false
            }
          },
          tooltip: {
            trigger: 'item',
            formatter: (params: any) => {
              if (params.componentType === 'series' && params.seriesType === 'map') {
                return `
                  <div style="font-weight: bold; color: #002FA7;">${params.name}</div>
                  <div style="color: #64748b;">飞行密度指数: <span style="color: #002FA7; font-weight: bold;">${params.value}</span></div>
                  <div style="color: #64748b; font-size: 12px;">${params.value > 60 ? '高密度飞行区' : params.value > 30 ? '中等密度飞行区' : '低密度飞行区'}</div>
                `;
              } else if (params.componentType === 'series' && params.seriesType === 'pie') {
                return `
                  <div style="font-weight: bold; color: #002FA7;">${params.seriesName}</div>
                  <div>${params.marker}${params.name}: ${params.value}架次 (${params.percent}%)</div>
                `;
              }
              return params.name;
            },
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            borderColor: '#e2e8f0',
            borderWidth: 1,
            textStyle: {
              color: '#374151'
            }
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
                lang: ['数据视图', '关闭', '刷新']
              },
              restore: {
                title: '重置'
              },
              saveAsImage: {
                title: '保存为图片',
                pixelRatio: 2
              }
            },
            iconStyle: {
              borderColor: '#64748b'
            },
            emphasis: {
              iconStyle: {
                borderColor: '#002FA7'
              }
            }
          },
          visualMap: {
            type: 'continuous',
            min: minValue,
            max: maxValue,
            text: ['高密度', '低密度'],
            realtime: false,
            calculable: true,
            inRange: {
              color: [
                '#dbeafe', // Very light blue
                '#bfdbfe', // Light blue
                '#93c5fd', // Medium light blue
                '#60a5fa', // Medium blue
                '#3b82f6', // Blue
                '#2563eb', // Dark blue
                '#1d4ed8', // Darker blue
                '#1e40af'  // Very dark blue
              ]
            },
            textStyle: {
              color: '#64748b'
            },
            orient: 'horizontal',
            left: 'center',
            bottom: 60,
            itemWidth: 20,
            itemHeight: 100,
            precision: 0
          },
          legend: {
            data: ['物流配送', '应急救援', '城市巡航', '其他'],
            orient: 'vertical',
            left: 20,
            top: 'center',
            textStyle: {
              color: '#64748b',
              fontSize: 12
            },
            itemGap: 8
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
                fontSize: 11,
                fontWeight: 'bold',
                formatter: '{b}'
              },
              emphasis: {
                label: {
                  color: '#ffffff',
                  fontSize: 12
                },
                itemStyle: {
                  areaColor: '#002FA7',
                  borderColor: '#ffffff',
                  borderWidth: 2
                }
              },
              itemStyle: {
                borderColor: '#ffffff',
                borderWidth: 1.5
              },
              data: data.map(item => ({
                name: item.name,
                value: item.value
              }))
            },

            // Pie charts for major hubs with realistic data
            // Shenzhen Bao'an International Airport area
            createPieSeries([113.82, 22.64], 25, '宝安机场枢纽', [
              { value: 45, name: '物流配送', itemStyle: { color: '#f59e0b' } },
              { value: 25, name: '应急救援', itemStyle: { color: '#ea580c' } },
              { value: 20, name: '城市巡航', itemStyle: { color: '#dc2626' } },
              { value: 10, name: '其他', itemStyle: { color: '#b91c1c' } }
            ]),
            // Shenzhen Futian CBD area
            createPieSeries([114.05, 22.54], 20, '福田中心区', [
              { value: 35, name: '城市巡航', itemStyle: { color: '#3b82f6' } },
              { value: 20, name: '物流配送', itemStyle: { color: '#f59e0b' } },
              { value: 15, name: '应急救援', itemStyle: { color: '#ea580c' } },
              { value: 5, name: '其他', itemStyle: { color: '#64748b' } }
            ]),
            // Shenzhen Nanshan Tech Park
            createPieSeries([113.95, 22.53], 18, '南山科技园', [
              { value: 40, name: '物流配送', itemStyle: { color: '#f59e0b' } },
              { value: 18, name: '城市巡航', itemStyle: { color: '#3b82f6' } },
              { value: 12, name: '应急救援', itemStyle: { color: '#ea580c' } },
              { value: 8, name: '其他', itemStyle: { color: '#64748b' } }
            ]),
            // Shenzhen Logistics Hub
            createPieSeries([113.88, 22.58], 22, '深圳物流枢纽', [
              { value: 50, name: '物流配送', itemStyle: { color: '#f59e0b' } },
              { value: 15, name: '应急救援', itemStyle: { color: '#ea580c' } },
              { value: 10, name: '城市巡航', itemStyle: { color: '#3b82f6' } },
              { value: 5, name: '其他', itemStyle: { color: '#64748b' } }
            ])
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
        <div className="font-medium text-slate-700 mb-1">📊 数据来源</div>
        <div>深圳民航数据 | 2024年更新</div>
        <div className="text-[10px] text-slate-400 mt-1">包含6个主要行政区</div>
      </div>

      {/* Navigation hint */}
      <div className="absolute top-3 right-3 text-xs text-slate-500 bg-white/90 backdrop-blur px-2 py-1 rounded border border-slate-200">
        🖱️ 拖拽查看 | 🔍 滚轮缩放
      </div>
    </div>
  );
};

// 8. Polar Clock (All Weather)
export const PolarClockChart = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
      <PolarGrid stroke="#e5e7eb" />
      <PolarAngleAxis dataKey="hour" tick={{ fontSize: 10 }} />
      <PolarRadiusAxis angle={30} domain={[0, 'auto']} tick={false} axisLine={false} />
      <Radar name="活跃度" dataKey="value" stroke="#002FA7" fill="#002FA7" fillOpacity={0.6} />
      <Tooltip />
    </RadarChart>
  </ResponsiveContainer>
);

// 9. Box Plot (Seasonal)
export const SeasonalBoxChart = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <ComposedChart data={data} margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
      <XAxis dataKey="name" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
      <YAxis tick={{fontSize: 10}} axisLine={false} tickLine={false} />
      <Tooltip />
      <Bar dataKey="max" fill="#cbd5e1" barSize={10} stackId="a" />
       <Line type="monotone" dataKey="avg" stroke="#0ea5e9" strokeWidth={3} dot={{r:4}} />
       <Line type="monotone" dataKey="min" stroke="#10b981" strokeDasharray="3 3" dot={false} />
    </ComposedChart>
  </ResponsiveContainer>
);

// 10. Gauge (Efficiency)
export const GaugeChart = ({ data }: { data: any[] }) => {
  const val = data[0].value;
  const pieData = [
    { name: '效率', value: val },
    { name: '剩余', value: 100 - val }
  ];
  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={pieData}
          cx="50%"
          cy="70%"
          startAngle={180}
          endAngle={0}
          innerRadius={80}
          outerRadius={120}
          paddingAngle={0}
          dataKey="value"
        >
          <Cell key="val" fill="#f59e0b" />
          <Cell key="rest" fill="#fef3c7" />
        </Pie>
        <text x="50%" y="65%" textAnchor="middle" dominantBaseline="middle" className="text-3xl font-bold fill-[#7f1d1d]">
          {val}
        </text>
         <text x="50%" y="50%" textAnchor="middle" className="text-sm fill-slate-500">
          效率
        </text>
      </PieChart>
    </ResponsiveContainer>
  );
};

// 11. Funnel (Endurance)
export const MissionFunnelChart = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <FunnelChart>
      <Tooltip />
      <Funnel
        dataKey="value"
        data={data}
        isAnimationActive
      >
        <LabelList position="right" fill="#000" stroke="none" dataKey="name" />
      </Funnel>
    </FunnelChart>
  </ResponsiveContainer>
);

// 12. Histogram (Wide Area)
export const CoverageHistogram = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
        <XAxis dataKey="name" tick={{fontSize: 10, fill: '#64748b'}} axisLine={false} tickLine={false} />
        <YAxis tick={{fontSize: 10, fill: '#64748b'}} axisLine={false} tickLine={false} />
        <Tooltip cursor={{fill: '#f8fafc'}} />
        <Bar dataKey="value" fill="#f59e0b" barSize={40} radius={[4,4,0,0]} />
    </BarChart>
  </ResponsiveContainer>
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
                  {`区域 ${node.replace('区', '')}`}
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

// 14. 3D Bar (Vertical Airspace)
export const AirspaceBarChart = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
      <XAxis dataKey="name" tick={{fontSize: 10, fill: '#64748b'}} axisLine={false} tickLine={false} />
      <YAxis tick={{fontSize: 10, fill: '#64748b'}} axisLine={false} tickLine={false} />
      <Tooltip />
      <Bar dataKey="value">
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={index === 0 ? '#f59e0b' : index === 1 ? '#ea580c' : '#dc2626'} />
        ))}
      </Bar>
    </BarChart>
  </ResponsiveContainer>
);

// 15. Calendar Heatmap
export const CalendarHeatmap = ({ data }: { data: any[] }) => {
  const [hoveredDay, setHoveredDay] = useState<any>(null);
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
  const dayNames = ['日', '一', '二', '三', '四', '五', '六'];

  // Group data by month
  const monthsData = Array.from({length: 12}, (_, i) => {
    return data.filter(d => new Date(d.date).getMonth() === i);
  });

  const getHeatColor = (val: number) => {
    // scale roughly 500 - 1000 in mock data
    // Map 400 (min) to 1000 (max)
    const min = 400;
    const max = 1000;
    const pct = Math.max(0, Math.min(1, (val - min) / (max - min)));

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
                    <div
                      key={i}
                      className="rounded-[1px] cursor-pointer hover:ring-1 hover:ring-slate-400 transition-all"
                      style={{ backgroundColor: getHeatColor(d.value) }}
                      onMouseEnter={(e) => {
                         const rect = e.currentTarget.getBoundingClientRect();
                         setHoveredDay({ ...d, x: rect.left, y: rect.top });
                      }}
                      onMouseLeave={() => setHoveredDay(null)}
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

// 16. Waveform (Night Economy)
export const NightWaveChart = ({ data }: { data: any[] }) => (
    <ResponsiveContainer width="100%" height="100%">
    <AreaChart data={data} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
       <defs>
        <linearGradient id="colorNight" x1="0" y1="0" x2="0" y2="1">
          <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
          <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
        </linearGradient>
      </defs>
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
      <XAxis dataKey="hour" tick={{fontSize: 10, fill: '#64748b'}} axisLine={false} tickLine={false} />
      <YAxis tick={{fontSize: 10, fill: '#64748b'}} axisLine={false} tickLine={false} />
      <Tooltip />
       <Area type="monotone" dataKey="value" stroke="#f59e0b" fill="url(#colorNight)" />
    </AreaChart>
  </ResponsiveContainer>
);

// 17. Radar (Leading Entity)
export const EntityRadarChart = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
      <PolarGrid />
      <PolarAngleAxis dataKey="subject" tick={{fontSize: 10, fill: '#64748b'}} />
      <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
      <Radar name="企业 A" dataKey="A" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.6} />
      <Radar name="企业 B" dataKey="B" stroke="#ea580c" fill="#ea580c" fillOpacity={0.6} />
      <Legend />
      <Tooltip />
    </RadarChart>
  </ResponsiveContainer>
);

// 18. Dashboard (Composite) - Grade Gauge with ECharts
export const CompositeDashboardChart = ({ data }: { data: any[] }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstance = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);
    const val = data[0].value / 100; // Convert to 0-1 range for gauge

    const option = {
      series: [
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
              width: 8,
              color: [
                [0.25, '#FF6E76'],   // D级 - 红色
                [0.5, '#FDDD60'],    // C级 - 黄色
                [0.75, '#58D9F9'],   // B级 - 蓝色
                [1, '#7CFFB2']       // A级 - 绿色
              ]
            }
          },
          pointer: {
            icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
            length: '12%',
            width: 20,
            offsetCenter: [0, '-60%'],
            itemStyle: {
              color: 'auto'
            }
          },
          axisTick: {
            length: 12,
            lineStyle: {
              color: 'auto',
              width: 2
            }
          },
          splitLine: {
            length: 20,
            lineStyle: {
              color: 'auto',
              width: 5
            }
          },
          axisLabel: {
            color: '#464646',
            fontSize: 14,
            distance: -60,
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
            offsetCenter: [0, '-10%'],
            fontSize: 16,
            color: '#002FA7',
            fontWeight: 'bold'
          },
          detail: {
            fontSize: 30,
            offsetCenter: [0, '-35%'],
            valueAnimation: true,
            formatter: function (value: number) {
              const score = Math.round(value * 100);
              let grade = 'D级';
              if (score >= 75) grade = 'A级';
              else if (score >= 50) grade = 'B级';
              else if (score >= 25) grade = 'C级';

              return grade + '\n' + score;
            },
            color: '#002FA7',
            fontWeight: 'bold',
            lineHeight: 32
          },
          data: [
            {
              value: val,
              name: '综合指数等级'
            }
          ]
        }
      ]
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
    <div className="w-full h-full relative bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-4">
      <div
        ref={chartRef}
        className="w-full h-full"
        style={{ minHeight: '300px' }}
      />

      {/* Grade Legend */}
      <div className="absolute bottom-4 left-4 right-4">
        <div className="flex justify-center space-x-6 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded" style={{backgroundColor: '#FF6E76'}}></div>
            <span className="text-slate-600">D级 (0-25)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded" style={{backgroundColor: '#FDDD60'}}></div>
            <span className="text-slate-600">C级 (25-50)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded" style={{backgroundColor: '#58D9F9'}}></div>
            <span className="text-slate-600">B级 (50-75)</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 rounded" style={{backgroundColor: '#7CFFB2'}}></div>
            <span className="text-slate-600">A级 (75-100)</span>
          </div>
        </div>
      </div>

      {/* Info */}
      <div className="absolute top-2 right-2 text-xs text-slate-500 bg-white/80 px-2 py-1 rounded">
        等级评估仪表盘
      </div>
    </div>
  );
};

// Map chart types to components
export const ChartRenderer = ({ type, data, definition, title }: { type: string, data: any, definition?: string, title?: string }) => {
    // Add a subtle info icon if definition is present
    const Container = ({ children }: { children: React.ReactNode }) => (
      <div className="w-full h-full relative" role="figure" aria-label={title ? `${title} 统计图` : "统计图"}>
         {children}
         {definition && (
           <div className="absolute top-2 right-2 z-20 flex flex-col items-end group">
              <button
                aria-label="查看指标定义"
                className="w-5 h-5 flex items-center justify-center bg-white/80 backdrop-blur rounded-full shadow-sm border border-slate-200 text-slate-400 hover:text-[#002FA7] hover:border-[#002FA7] hover:bg-white focus:outline-none focus:ring-2 focus:ring-[#002FA7] focus:ring-offset-1 transition-all"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-3.5 h-3.5">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </button>
              <div
                role="tooltip"
                className="absolute top-6 right-0 w-64 opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 transition-opacity duration-200 pointer-events-none group-hover:pointer-events-auto group-focus-within:pointer-events-auto"
              >
                 <div className="mt-2 bg-slate-800 text-white text-xs p-3 rounded-lg shadow-xl border border-slate-700 relative">
                    {/* Little arrow */}
                    <div className="absolute top-0 right-1.5 -mt-1 w-2 h-2 bg-slate-800 transform rotate-45 border-t border-l border-slate-700"></div>
                    <div className="font-bold mb-1 border-b border-slate-600 pb-1 text-slate-200">指标定义</div>
                    <p className="leading-relaxed text-slate-300">{definition}</p>
                 </div>
              </div>
           </div>
         )}
      </div>
    );

    let ChartComponent;
    switch (type) {
        case 'Area': ChartComponent = <TrafficAreaChart data={data} />; break;
        case 'DualLine': ChartComponent = <DualLineChart data={data} />; break;
        case 'StackedBar': ChartComponent = <StackedBarChart data={data} />; break;
        case 'Pareto': ChartComponent = <ParetoChart data={data} />; break;
        case 'Rose': ChartComponent = <NightingaleRoseChart data={data} />; break;
        case 'Treemap': ChartComponent = <FleetTreemap data={data} />; break;
        case 'Map': ChartComponent = <ChoroplethMap data={data} />; break;
        case 'Polar': ChartComponent = <PolarClockChart data={data} />; break;
        case 'BoxPlot': ChartComponent = <SeasonalBoxChart data={data} />; break;
        case 'Gauge': ChartComponent = <GaugeChart data={data} />; break;
        case 'Funnel': ChartComponent = <MissionFunnelChart data={data} />; break;
        case 'Histogram': ChartComponent = <CoverageHistogram data={data} />; break;
        case 'Chord': ChartComponent = <ChordDiagram data={data} />; break;
        case '3DBar': ChartComponent = <AirspaceBarChart data={data} />; break;
        case 'Calendar': ChartComponent = <CalendarHeatmap data={data} />; break;
        case 'Wave': ChartComponent = <NightWaveChart data={data} />; break;
        case 'Radar': ChartComponent = <EntityRadarChart data={data} />; break;
        case 'Dashboard': ChartComponent = <CompositeDashboardChart data={data} />; break;
        default: ChartComponent = <div className="flex items-center justify-center h-full text-red-500">未知图表类型</div>;
    }

    return <Container>{ChartComponent}</Container>;
};
