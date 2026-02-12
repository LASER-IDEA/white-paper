import React, { useState, useEffect, useRef } from 'react';
import ReportPage from './components/ReportPage';
import BackToTop from './components/BackToTop';
//import { getAllData } from './utils/mockData';
import {getAllComputedData} from './utils/computedData';
import { Dimension } from './types';

const getDimensionIcon = (dimension: string) => {
  const iconClass = "w-5 h-5 mr-3 flex-shrink-0";
  const paths: Record<string, string> = {
    'All': "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
    [Dimension.ScaleGrowth]: "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6",
    [Dimension.StructureEntity]: "M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10",
    [Dimension.TimeSpace]: "M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
    [Dimension.EfficiencyQuality]: "M13 10V3L4 14h7v7l9-11h-7z",
    [Dimension.InnovationIntegration]: "M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
    [Dimension.CompositeIndex]: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
  };

  if (!paths[dimension]) return null;
  return (
    <svg aria-hidden="true" className={iconClass} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={paths[dimension]} />
    </svg>
  );
};

const REPORT_PDF_TITLE = '深圳市低空经济发展指数报告';
const EXPORT_WAIT_MS = 5500;

/** 导出按钮：状态仅在本组件内，避免 App 因 isPrinting 重渲染导致图表恢复初始状态 */
const ExportPdfButton: React.FC = () => {
  const [isPrinting, setIsPrinting] = useState(false);
  const handlePrint = () => {
    setIsPrinting(true);
    const prevTitle = document.title;
    document.title = REPORT_PDF_TITLE;
    setTimeout(() => {
      window.print();
      setTimeout(() => {
        document.title = prevTitle;
        setIsPrinting(false);
      }, 500);
    }, EXPORT_WAIT_MS);
  };
  return (
    <button
      type="button"
      onClick={handlePrint}
      disabled={isPrinting}
      className={`w-full flex items-center justify-center space-x-2 bg-[#002FA7] hover:bg-[#001F7A] text-white py-2.5 rounded-lg shadow-sm transition-all font-medium text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#002FA7] focus-visible:ring-offset-2 ${isPrinting ? 'opacity-75 cursor-not-allowed' : ''}`}
      aria-live="polite"
    >
      {isPrinting ? (
        <>
          <svg className="animate-spin -ml-1 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>正在准备...</span>
        </>
      ) : (
        <>
          <svg aria-hidden="true" className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
          <span>导出 PDF</span>
        </>
      )}
    </button>
  );
};

const App: React.FC = () => {
  //const allData = getAllData();
  const allData = getAllComputedData();

  // Get dimension from URL parameter, default to 'All'
  const getDimensionFromUrl = () => {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('dimension') || 'All';
  };

  const [selectedDimension, setSelectedDimension] = useState<string>(getDimensionFromUrl());
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const mainContentRef = useRef<HTMLElement>(null);
  const isFirstRender = useRef(true);

  // Update selectedDimension when URL changes
  useEffect(() => {
    const handleUrlChange = () => {
      setSelectedDimension(getDimensionFromUrl());
    };

    window.addEventListener('popstate', handleUrlChange);
    return () => window.removeEventListener('popstate', handleUrlChange);
  }, []);

  // Manage focus when dimension changes
  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    // Small timeout to ensure content has updated
    setTimeout(() => {
      mainContentRef.current?.focus();
    }, 0);
  }, [selectedDimension]);

  // Filter Data
  const filteredData = selectedDimension === 'All'
    ? allData
    : allData.filter(d => d.dimension === selectedDimension);

  // Group Dimensions for Sidebar
  const dimensions = Object.values(Dimension);

  const updateDimension = (dimension: string) => {
    setSelectedDimension(dimension);
    setIsMobileMenuOpen(false);
    const url = new URL(window.location.href);
    if (dimension === 'All') {
      url.searchParams.delete('dimension');
    } else {
      url.searchParams.set('dimension', dimension);
    }
    window.history.pushState({}, '', url.toString());
  };

  return (
    <div className="flex flex-col md:flex-row min-h-screen bg-white font-sans text-[#002FA7] print:block print:h-auto print:overflow-visible print:bg-white">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:bg-white focus:text-[#002FA7] focus:shadow-lg focus:rounded-lg focus:ring-2 focus:ring-[#002FA7] focus:outline-none transition-all"
      >
        跳转至主要内容
      </a>

      {/* Mobile Header */}
      <div className="md:hidden sticky top-0 bg-white border-b border-slate-200 z-30 px-4 py-3 flex items-center justify-between shadow-sm no-print print:hidden">
        <h1 className="font-bold text-[#002FA7]">深圳市低空经济发展指数报告</h1>
        <button
          onClick={() => setIsMobileMenuOpen(true)}
          aria-label="打开导航"
          className="p-2 text-slate-600 hover:bg-slate-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#002FA7]"
        >
          <svg aria-hidden="true" className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
        </button>
      </div>

      {/* Mobile Overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden no-print print:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Navigation (Hidden on Print) */}
      <aside className={`w-64 bg-white border-r border-slate-200 fixed h-full flex flex-col no-print z-50 md:z-10 ${isMobileMenuOpen ? 'block' : 'hidden'} md:block`}>
        {/* Mobile Close Button */}
        <button
          onClick={() => setIsMobileMenuOpen(false)}
          className="md:hidden absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#002FA7]"
          aria-label="关闭导航"
        >
           <svg aria-hidden="true" className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
        </button>

        {/* Scrollable Content Area */}
        <div className="flex-1 overflow-y-auto">
          <div className="p-6">
            <h1 className="text-xl font-bold text-[#002FA7] leading-tight">
            深圳市低空经济 <span className="text-[#002FA7] block">发展指数报告</span>
            </h1>
            <p className="text-xs text-slate-500 mt-2">发展指数仪表盘</p>
          </div>

          <nav className="mt-4 px-4 space-y-1 pb-4" aria-label="Main navigation">
             <button
                onClick={() => updateDimension('All')}
                aria-current={selectedDimension === 'All' ? 'page' : undefined}
                className={`w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#002FA7] focus-visible:ring-offset-2 flex items-center ${
                  selectedDimension === 'All'
                  ? 'bg-[#002FA7] text-white'
                  : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                {getDimensionIcon('All')}
                完整报告
              </button>
            {dimensions.map((dim) => (
              <button
                key={dim}
                onClick={() => updateDimension(dim)}
                aria-current={selectedDimension === dim ? 'page' : undefined}
                className={`w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#002FA7] focus-visible:ring-offset-2 flex items-center ${
                  selectedDimension === dim
                  ? 'bg-blue-50 text-[#002FA7] border border-[#002FA7]/20'
                  : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                {getDimensionIcon(dim)}
                {dim}
              </button>
            ))}
          </nav>
        </div>

        {/* Fixed Export Button at Bottom */}
        <div className="flex-shrink-0 w-full p-4 border-t border-slate-200 bg-white">
          <ExportPdfButton />
        </div>
      </aside>

      {/* Main Content Area */}
      <main
        id="main-content"
        ref={mainContentRef}
        tabIndex={-1}
        className="flex-1 ml-0 md:ml-64 p-8 overflow-y-auto outline-none print:ml-0 print:p-0 print:overflow-visible print:h-auto print:static"
      >
        <div className="max-w-[210mm] mx-auto print:max-w-none print:mx-0 print:w-full">

          {/* Cover Page Placeholder (Only visible on All) */}
           {selectedDimension === 'All' && (
             <div className="w-[210mm] h-[297mm] bg-gradient-to-br from-[#002FA7] to-[#001F7A] text-white shadow-2xl mx-auto my-8 p-[20mm] flex flex-col justify-between page-break relative overflow-hidden print:shadow-none print:m-0 print:w-full print:h-[297mm] print:rounded-none">
                <div className="absolute top-0 right-0 w-96 h-96 bg-blue-400 rounded-full blur-[100px] opacity-20 -mr-20 -mt-20 print:opacity-40"></div>

                <div className="relative z-10">
                   {/* <div className="inline-block px-3 py-1 bg-white/20 border border-white/30 rounded-full text-white/90 text-xs font-mono mb-6 print:border-white print:text-white">本页面展示的所有数据均为模拟数据（Mock Data），仅用于演示和开发测试目的。不代表任何真实的市场情况、统计数据或商业信息。</div> */}
                   <h1 className="mt-6 text-4xl font-extrabold leading-tight tracking-tight text-white print:text-white">
                    深圳市低空经济发展指数报告（2025） <br/>
                    <br/>
                    <span className="text-2xl font-normal text-white print:text-white">基于“领航（PILOT）”模型的动态评估与综合洞察</span>
                   </h1>
                   <div className="w-24 h-2 bg-white mt-8"></div>
                </div>

                <div className="relative z-10">
                  <div className="grid grid-cols-2 gap-12 mb-12">
                     <div>
                       <span className="block text-white/70 text-sm uppercase mb-1">统计周期</span>
                       <span className="text-2xl font-bold text-white">2025年度</span>
                     </div>
                     <div>
                       <span className="block text-white/70 text-sm uppercase mb-1">区域</span>
                       <span className="text-2xl font-bold text-white">深圳先行示范区</span>
                     </div>
                  </div>
                  <p className="text-white/70 text-sm leading-relaxed whitespace-nowrap">
                  本报告依托“领航（PILOT）”模型，通过五维指标全景呈现低空经济发展态势，为政策与战略提供数据决策支撑。
                  </p>
                </div>
             </div>
           )}

          {/* Render Pages */}
          {filteredData.map((data, index) => (
            <ReportPage
              key={data.id}
              data={data}
              pageNumber={index + 1}
            />
          ))}

          {filteredData.length === 0 && (
            <div className="flex flex-col items-center justify-center h-96 text-center">
              <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                <svg className="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-slate-900 mb-1">暂无相关数据</h3>
              <p className="text-slate-500 mb-6 max-w-sm">该维度下目前没有可展示的指标数据，您可以查看其他维度或返回完整报告。</p>
              <button
                onClick={() => updateDimension('All')}
                className="inline-flex items-center px-4 py-2 bg-[#002FA7] text-white text-sm font-medium rounded-lg hover:bg-[#001F7A] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#002FA7] transition-colors"
              >
                查看完整报告
              </button>
            </div>
          )}

        </div>
        <BackToTop />
      </main>
    </div>
  );
};

export default App;
