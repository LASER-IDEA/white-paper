import React from 'react';
import { PageProps } from '../types';
import { ChartRenderer } from './charts/Charts';

const ReportPage: React.FC<PageProps> = ({ data, pageNumber }) => {
  const isGrowth = data.trend > 0;
  const trendColor = isGrowth ? 'text-low-altitude-green-600' : 'text-red-500';
  const trendIcon = isGrowth ? '↑' : '↓';
  
  return (
    <div className="w-[210mm] h-[297mm] bg-white shadow-2xl mx-auto my-8 p-[15mm] flex flex-col relative page-break overflow-hidden print:shadow-none print:m-0 print:border-none print:w-full print:h-[297mm]">
      {/* 1. Header Area (Top 15%) */}
      <div className="h-[12%] flex justify-between items-start border-b-2 border-slate-100 mb-6">
        <div className="flex flex-col">
           <span className="text-xs font-bold tracking-widest text-slate-500 uppercase">{data.dimension}</span>
           <h1 className="text-3xl font-bold text-[#002FA7] mt-1">{data.id} {data.title}</h1>
           <h2 className="text-lg text-slate-600 font-light">{data.subtitle}</h2>
        </div>
        <div className="flex flex-col items-end">
            <div className="flex items-baseline space-x-2">
                <span className="text-5xl font-extrabold text-[#002FA7] tracking-tight">{data.value}</span>
                <span className="text-sm text-slate-600">{data.unit}</span>
            </div>
             <div
               className={`flex items-center ${trendColor} font-medium mt-1`}
               role="img"
               aria-label={`${Math.abs(data.trend * 100).toFixed(1)}% 环比${isGrowth ? '增长' : '下降'}`}
             >
                <span className="mr-1 text-lg" aria-hidden="true">{trendIcon}</span>
                <span className="text-slate-600" aria-hidden="true">{Math.abs(data.trend * 100).toFixed(1)}% 环比</span>
            </div>
        </div>
      </div>

      {/* 2. Main Chart Area (Middle 45%) */}
      <div className="h-[45%] w-full bg-slate-50 rounded-xl p-4 mb-6 border border-slate-100 relative print:bg-white print:border-slate-200">
         <ChartRenderer type={data.chartType} data={data.chartData} definition={data.definition} title={data.title} />
      </div>

      {/* 3. Key Metrics Cards (Middle-Bottom 15%) */}
      <div className="h-[15%] grid grid-cols-3 gap-6 mb-8">
        {data.keyMetrics.map((metric, idx) => (
          <div key={idx} className="bg-white rounded-lg border border-slate-200 p-4 flex flex-col justify-center shadow-sm print:shadow-none print:border-slate-300">
             <span className="text-sm text-slate-500 uppercase tracking-wide font-medium">{metric.label}</span>
             <span className="text-2xl font-bold text-[#002FA7] mt-1">{metric.value}</span>
          </div>
        ))}
      </div>

      {/* 4. Insight Text (Bottom 25%) */}
      <div className="flex-1 flex flex-col space-y-4">
         <div className="flex items-start space-x-3">
             <div className="w-1 h-full min-h-[20px] bg-slate-400 rounded-full mt-1 print:print-color-adjust-exact"></div>
             <div>
                 <h3 className="block text-xs font-bold text-slate-500 uppercase mb-1">指标定义</h3>
                 <p className="text-sm text-slate-700 leading-relaxed">{data.definition}</p>
             </div>
         </div>
         <div className="flex items-start space-x-3">
             <div className="w-1 h-full min-h-[20px] bg-[#002FA7] rounded-full mt-1 print:print-color-adjust-exact"></div>
             <div>
                 <h3 className="block text-xs font-bold text-[#002FA7] uppercase mb-1">数据洞察</h3>
                 <p className="text-sm text-slate-700 leading-relaxed">{data.insight}</p>
             </div>
         </div>
         <div className="flex items-start space-x-3">
             <div className="w-1 h-full min-h-[20px] bg-[#1e40af] rounded-full mt-1 print:print-color-adjust-exact"></div>
             <div>
                 <h3 className="block text-xs font-bold text-[#1e40af] uppercase mb-1">策略建议</h3>
                 <p className="text-sm text-slate-700 leading-relaxed">{data.suggestion}</p>
             </div>
         </div>
      </div>

      {/* Footer / Page Number */}
      <div className="absolute bottom-4 right-[15mm] text-slate-400 text-xs font-mono">
         第 {pageNumber < 10 ? `0${pageNumber}` : pageNumber} 页
      </div>
    </div>
  );
};

export default ReportPage;
