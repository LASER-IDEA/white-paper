import React from 'react';
import { PageProps } from '../types';
import { ChartRenderer } from './charts/Charts';

/** 报告主蓝 #002FA7（标题、竖条、数据洞察等） */
const REPORT_PRIMARY_BLUE = '#002FA7';
/** 报告次蓝 #1e40af（策略启示） */
const REPORT_SECONDARY_BLUE = '#1e40af';

const isEmpty = (v: unknown): boolean => {
  if (v == null) return true;
  if (Array.isArray(v)) return v.length === 0;
  if (typeof v === 'object') return Object.keys(v).length === 0;
  return false;
};
/** 有实际内容才显示：非空且不为 "-" */
const hasText = (s: unknown): boolean => {
  if (s == null) return false;
  const t = String(s).trim();
  return t !== '' && t !== '-';
};

const ReportPage: React.FC<PageProps> = ({ data, pageNumber }) => {
  const isGrowth = data.trend > 0;
  const trendColor = isGrowth ? 'text-low-altitude-green-600' : 'text-red-500';
  const trendIcon = isGrowth ? '↑' : '↓';
  const hasChartData = !isEmpty(data.chartData);
  const hasDefinition = hasText(data.definition);
  const hasInsight = hasText(data.insight);
  const hasSuggestion = hasText(data.suggestion);
  const hasAnyInsight = hasDefinition || hasInsight || hasSuggestion;

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
        </div>
      </div>

      {/* 2. Main Chart Area (Middle 45%) - 仅 chartData 非空时显示 */}
      {hasChartData && (
        <div className="h-[45%] min-h-[360px] w-full min-w-0 bg-slate-50 rounded-xl p-4 mb-6 border border-slate-100 relative print:bg-white print:border-slate-200">
          <ChartRenderer type={data.chartType} data={data.chartData} definition={data.definition} title={data.title} />
        </div>
      )}

      {/* 3. Key Metrics Cards (Middle-Bottom 15%) */}
      {data.keyMetrics && data.keyMetrics.length > 0 && (
        <dl className="h-[15%] grid grid-cols-3 gap-6 mb-8" aria-label="关键指标">
          {data.keyMetrics.map((metric, idx) => (
            <div
              key={idx}
              className="bg-white rounded-lg border border-slate-200 p-4 flex flex-col justify-center shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-300 print:shadow-none print:border-slate-300 print:translate-y-0"
            >
               <dt className="text-sm text-slate-500 uppercase tracking-wide font-medium">{metric.label}</dt>
               <dd className="text-2xl font-bold text-[#002FA7] mt-1">{metric.value}</dd>
            </div>
          ))}
        </dl>
      )}

      {/* 4. Insight Text (Bottom 25%) - 仅当至少有一项有内容时显示整块；各项为空字符串时不显示该子块 */}
      {hasAnyInsight && (
        <div className="flex-1 flex flex-col space-y-4 mt-10">
          {hasDefinition && (
            <div className="flex items-start space-x-3">
              <div className="w-1 h-full min-h-[20px] bg-[#002FA7] rounded-full mt-1 print:print-color-adjust-exact"></div>
              <div>
                <h3 className="block text-[0.825rem] font-bold text-[#002FA7] uppercase mb-1">指数定义</h3>
                <p
                  className="text-[0.8rem] text-slate-700 leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: data.definition! }}
                />
              </div>
            </div>
          )}
          {hasInsight && (
            <div className="flex items-start space-x-3">
              <div className="w-1 h-full min-h-[20px] bg-[#002FA7] rounded-full mt-1 print:print-color-adjust-exact"></div>
              <div>
                <h3 className="block text-[0.825rem] font-bold text-[#002FA7] uppercase mb-1">数据洞察</h3>
                <p
                  className="text-[0.8rem] text-slate-700 leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: data.insight! }}
                />
              </div>
            </div>
          )}
          {hasSuggestion && (
            <div className="flex items-start space-x-3">
              <div className="w-1 h-full min-h-[20px] bg-[#1e40af] rounded-full mt-1 print:print-color-adjust-exact"></div>
              <div>
                <h3 className="block text-[0.825rem] font-bold text-[#1e40af] uppercase mb-1">策略启示</h3>
                <p
                  className="text-[0.8rem] text-slate-700 leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: data.suggestion! }}
                />
              </div>
            </div>
          )}
        </div>
      )}

      {/* Footer / Page Number */}
      <div className="absolute bottom-4 right-[15mm] text-slate-400 text-xs font-mono">
         第 {pageNumber < 10 ? `0${pageNumber}` : pageNumber} 页
      </div>
    </div>
  );
};

export default ReportPage;
