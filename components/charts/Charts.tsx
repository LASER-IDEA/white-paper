import React, { useState } from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, BarChart, Bar, ComposedChart,
  PieChart, Pie, Cell, Treemap, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  ScatterChart, Scatter, ZAxis, Legend, RadialBarChart, RadialBar, FunnelChart, Funnel, LabelList,
  Sector
} from 'recharts';

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
  const total = data.reduce((acc, cur) => acc + cur.volume, 0);
  let cumulative = 0;
  const processedData = data.map(d => {
    cumulative += d.volume;
    return { ...d, cumulative: Math.round((cumulative / total) * 100) };
  });

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
export const NightingaleRoseChart = ({ data }: { data: any[] }) => {
  const maxVal = Math.max(...data.map((d: any) => d.value));
  
  const roseData = data.map((d: any) => ({
    ...d,
    realValue: d.value,
    value: 1
  }));

  const RoseShape = (props: any) => {
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
  };

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
          shape={<RoseShape />}
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
        <Legend verticalAlign="bottom" height={36}/>
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

// 7. Choropleth Map (Regional Balance)
export const ChoroplethMap = ({ data }: { data: any[] }) => {
  const [hovered, setHovered] = useState<any>(null);

  const paths: Record<string, string> = {
    'A区': "M50,50 L200,20 L350,50 L320,130 L80,130 Z",
    'B区': "M20,60 L80,130 L150,200 L120,280 L20,250 Z",
    'C区': "M80,130 L320,130 L280,200 L150,200 Z",
    'D区': "M350,50 L380,80 L380,250 L280,200 L320,130 Z",
    'E区': "M120,280 L150,200 L280,200 L380,250 L200,290 Z"
  };

  const getHeatColor = (value: number) => {
     const opacity = Math.max(0.1, Math.min(1, value / 100));
     return `rgba(14, 165, 233, ${opacity})`;
  };

  const centroids: Record<string, {x: number, y: number}> = {
    'A区': {x: 200, y: 70},
    'B区': {x: 80, y: 170},
    'C区': {x: 200, y: 165},
    'D区': {x: 340, y: 160},
    'E区': {x: 250, y: 245},
  };

  return (
    <div className="w-full h-full relative flex items-center justify-center bg-slate-50 rounded-lg">
      <svg viewBox="0 0 400 300" className="w-full h-full max-w-2xl drop-shadow-lg p-4">
        <defs>
          <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" floodOpacity="0.1"/>
          </filter>
        </defs>
        {data.map((region) => (
          <g key={region.name} 
             onMouseEnter={() => setHovered(region)} 
             onMouseLeave={() => setHovered(null)}
             className="cursor-pointer transition-all duration-300 hover:opacity-90">
             
            <path
              d={paths[region.name] || ""}
              fill={getHeatColor(region.value)}
              stroke="white"
              strokeWidth="2"
              filter="url(#shadow)"
            />
             {centroids[region.name] && (
               <text 
                 x={centroids[region.name].x} 
                 y={centroids[region.name].y} 
                 textAnchor="middle" 
                 fill={region.value > 50 ? 'white' : '#1e293b'}
                 fontSize="12"
                 fontWeight="bold"
                 pointerEvents="none"
               >
                 {region.name}
               </text>
             )}
          </g>
        ))}
      </svg>

      {/* Floating Tooltip */}
      {hovered && (
         <div className="absolute top-4 left-4 bg-white/95 backdrop-blur border border-slate-200 p-3 rounded-lg shadow-xl z-20 animate-fade-in pointer-events-none">
            <p className="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1">区域</p>
            <p className="text-sm font-bold text-slate-800">{hovered.name}</p>
            <div className="mt-2 flex items-center gap-2">
                <span className="text-2xl font-extrabold text-tech-blue-600">{hovered.value}</span>
                <span className="text-xs text-slate-500">密度指数</span>
            </div>
         </div>
      )}

      {/* Legend */}
       <div className="absolute bottom-4 right-4 flex flex-col gap-2 bg-white/80 backdrop-blur p-3 rounded-lg border border-slate-100 text-xs text-slate-600 shadow-sm">
          <div className="font-bold text-slate-400 uppercase text-[10px]">密度地图</div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-sm bg-[#0ea5e9]"></span> 高 (&gt;80)
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-sm bg-[#0ea5e9]" style={{opacity: 0.5}}></span> 中 (40-80)
          </div>
          <div className="flex items-center gap-2">
             <span className="w-3 h-3 rounded-sm bg-[#0ea5e9]" style={{opacity: 0.2}}></span> 低 (&lt;40)
          </div>
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
      <Radar name="活跃度" dataKey="value" stroke="#0ea5e9" fill="#0ea5e9" fillOpacity={0.6} />
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
          <Cell key="val" fill="#0ea5e9" />
          <Cell key="rest" fill="#e5e7eb" />
        </Pie>
        <text x="50%" y="65%" textAnchor="middle" dominantBaseline="middle" className="text-3xl font-bold fill-slate-700">
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
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
        <XAxis dataKey="name" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
        <YAxis tick={{fontSize: 10}} axisLine={false} tickLine={false} />
        <Tooltip cursor={{fill: '#f3f4f6'}} />
        <Bar dataKey="value" fill="#0ea5e9" barSize={40} radius={[4,4,0,0]} />
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
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
      <XAxis dataKey="name" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
      <YAxis tick={{fontSize: 10}} axisLine={false} tickLine={false} />
      <Tooltip />
      <Bar dataKey="value">
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={index === 0 ? '#0ea5e9' : index === 1 ? '#6366f1' : '#f59e0b'} />
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
      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
      <XAxis dataKey="hour" tick={{fontSize: 10}} axisLine={false} tickLine={false} />
      <YAxis tick={{fontSize: 10}} axisLine={false} tickLine={false} />
      <Tooltip />
       <Area type="monotone" dataKey="value" stroke="#334155" fill="url(#colorNight)" />
    </AreaChart>
  </ResponsiveContainer>
);

// 17. Radar (Leading Entity)
export const EntityRadarChart = ({ data }: { data: any[] }) => (
  <ResponsiveContainer width="100%" height="100%">
    <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
      <PolarGrid />
      <PolarAngleAxis dataKey="subject" tick={{fontSize: 10}} />
      <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
      <Radar name="企业 A" dataKey="A" stroke="#0ea5e9" fill="#0ea5e9" fillOpacity={0.6} />
      <Radar name="企业 B" dataKey="B" stroke="#10b981" fill="#10b981" fillOpacity={0.6} />
      <Legend />
      <Tooltip />
    </RadarChart>
  </ResponsiveContainer>
);

// 18. Dashboard (Composite)
export const CompositeDashboardChart = ({ data }: { data: any[] }) => {
    const val = data[0].value;
    return (
     <ResponsiveContainer width="100%" height="100%">
        <RadialBarChart cx="50%" cy="50%" innerRadius="70%" outerRadius="100%" barSize={20} data={[{ name: 'Score', value: val, fill: '#0ea5e9' }]} startAngle={180} endAngle={0}>
          <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} >
            {/* Added to fix TS error about missing children */}
            {null}
          </PolarAngleAxis>
          <RadialBar
            background
            dataKey="value"
            cornerRadius={10}
            label={{ position: 'insideStart', fill: '#fff' }}
          />
          <text x="50%" y="50%" textAnchor="middle" dominantBaseline="middle" className="text-4xl font-bold fill-tech-blue-600">
             {val}
          </text>
          <text x="50%" y="60%" textAnchor="middle" className="text-sm fill-slate-500">
             综合指数
          </text>
        </RadialBarChart>
      </ResponsiveContainer>
    );
}

// Map chart types to components
export const ChartRenderer = ({ type, data, definition }: { type: string, data: any, definition?: string }) => {
    // Add a subtle info icon if definition is present
    const Container = ({ children }: { children: React.ReactNode }) => (
      <div className="w-full h-full relative group">
         {children}
         {definition && (
           <div className="absolute top-0 right-0 p-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
              <div className="bg-slate-800 text-white text-xs p-2 rounded max-w-xs shadow-lg">
                <span className="font-bold block mb-1">定义:</span>
                {definition}
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
