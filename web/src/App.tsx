import React, { useState, useEffect } from 'react';
import ReportPage from './components/ReportPage';
import BackToTop from './components/BackToTop';
import { getAllData } from './utils/mockData';
import { Dimension } from './types';

const App: React.FC = () => {
  const allData = getAllData();

  // Get dimension from URL parameter, default to 'All'
  const getDimensionFromUrl = () => {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('dimension') || 'All';
  };

  const [selectedDimension, setSelectedDimension] = useState<string>(getDimensionFromUrl());
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Update selectedDimension when URL changes
  useEffect(() => {
    const handleUrlChange = () => {
      setSelectedDimension(getDimensionFromUrl());
    };

    window.addEventListener('popstate', handleUrlChange);
    return () => window.removeEventListener('popstate', handleUrlChange);
  }, []);

  // Filter Data
  const filteredData = selectedDimension === 'All'
    ? allData
    : allData.filter(d => d.dimension === selectedDimension);

  // Group Dimensions for Sidebar
  const dimensions = Object.values(Dimension);

  const handlePrint = () => {
    window.print();
  };

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

      {/* Mobile Header */}
      <div className="md:hidden sticky top-0 bg-white border-b border-slate-200 z-30 px-4 py-3 flex items-center justify-between shadow-sm">
        <h1 className="font-bold text-[#002FA7]">低空经济白皮书</h1>
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
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Navigation (Hidden on Print) */}
      <aside className={`w-64 bg-white border-r border-slate-200 fixed h-full overflow-y-auto no-print z-50 md:z-10 ${isMobileMenuOpen ? 'block' : 'hidden'} md:block`}>
        {/* Mobile Close Button */}
        <button
          onClick={() => setIsMobileMenuOpen(false)}
          className="md:hidden absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#002FA7]"
          aria-label="关闭导航"
        >
           <svg aria-hidden="true" className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
        </button>

        <div className="p-6">
          <h1 className="text-xl font-bold text-[#002FA7] leading-tight">
            低空经济 <span className="text-[#002FA7] block">白皮书</span>
          </h1>
          <p className="text-xs text-slate-500 mt-2">发展指数仪表盘</p>
        </div>

        <nav className="mt-4 px-4 space-y-1" aria-label="Main navigation">
           <button
              onClick={() => updateDimension('All')}
              aria-current={selectedDimension === 'All' ? 'page' : undefined}
              className={`w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#002FA7] focus-visible:ring-offset-2 ${
                selectedDimension === 'All'
                ? 'bg-[#002FA7] text-white'
                : 'text-slate-600 hover:bg-slate-50'
              }`}
            >
              完整报告
            </button>
          {dimensions.map((dim) => (
            <button
              key={dim}
              onClick={() => updateDimension(dim)}
              aria-current={selectedDimension === dim ? 'page' : undefined}
              className={`w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#002FA7] focus-visible:ring-offset-2 ${
                selectedDimension === dim
                ? 'bg-blue-50 text-[#002FA7] border border-[#002FA7]/20'
                : 'text-slate-600 hover:bg-slate-50'
              }`}
            >
              {dim}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-0 w-full p-4 border-t border-slate-200 bg-white">
          <button
            onClick={handlePrint}
            className="w-full flex items-center justify-center space-x-2 bg-[#002FA7] hover:bg-[#001F7A] text-white py-2.5 rounded-lg shadow-sm transition-all font-medium text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#002FA7] focus-visible:ring-offset-2"
          >
            <svg aria-hidden="true" className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
            <span>导出 PDF</span>
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 ml-0 md:ml-64 p-8 overflow-y-auto print:ml-0 print:p-0 print:overflow-visible print:h-auto print:static">
        <div className="max-w-[210mm] mx-auto print:max-w-none print:mx-0 print:w-full">

          {/* Cover Page Placeholder (Only visible on All) */}
           {selectedDimension === 'All' && (
             <div className="w-[210mm] h-[297mm] bg-gradient-to-br from-[#002FA7] to-[#001F7A] text-white shadow-2xl mx-auto my-8 p-[20mm] flex flex-col justify-between page-break relative overflow-hidden print:shadow-none print:m-0 print:w-full print:rounded-none">
                <div className="absolute top-0 right-0 w-96 h-96 bg-blue-400 rounded-full blur-[100px] opacity-20 -mr-20 -mt-20 print:opacity-40"></div>

                <div className="relative z-10">
                   <div className="inline-block px-3 py-1 bg-white/20 border border-white/30 rounded-full text-white/90 text-xs font-mono mb-6 print:border-white print:text-white">本页面展示的所有数据均为模拟数据（Mock Data），仅用于演示和开发测试目的。不代表任何真实的市场情况、统计数据或商业信息。</div>
                   <h1 className="text-6xl font-extrabold leading-tight tracking-tight text-white print:text-white">
                    低空经济 <br/>
                    <br/>
                    <span className="text-white print:text-white">发展指数白皮书</span>
                   </h1>
                   <div className="w-24 h-2 bg-white mt-8"></div>
                </div>

                <div className="relative z-10">
                  <div className="grid grid-cols-2 gap-12 mb-12">
                     <div>
                       <span className="block text-white/70 text-sm uppercase mb-1">统计周期</span>
                       <span className="text-2xl font-bold text-white">2023年第三季度</span>
                     </div>
                     <div>
                       <span className="block text-white/70 text-sm uppercase mb-1">区域</span>
                       <span className="text-2xl font-bold text-white">深圳先行示范区</span>
                     </div>
                  </div>
                  <p className="text-white/70 text-sm max-w-md leading-relaxed">
                    本白皮书基于规模、结构、时空、效率、创新5D框架，提供低空经济的综合分析。
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
            <div className="flex items-center justify-center h-96">
              <p className="text-slate-400">该维度暂无数据。</p>
            </div>
          )}

        </div>
        <BackToTop />
      </main>
    </div>
  );
};

export default App;
