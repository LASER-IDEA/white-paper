import React, { useState } from 'react';
import ReportPage from './components/ReportPage';
import { getAllData } from './utils/mockData';
import { Dimension } from './types';

const App: React.FC = () => {
  const allData = getAllData();
  const [selectedDimension, setSelectedDimension] = useState<string>('All');

  // Filter Data
  const filteredData = selectedDimension === 'All' 
    ? allData 
    : allData.filter(d => d.dimension === selectedDimension);

  // Group Dimensions for Sidebar
  const dimensions = Object.values(Dimension);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="flex min-h-screen bg-slate-100 font-sans text-slate-900">
      
      {/* Sidebar Navigation (Hidden on Print) */}
      <aside className="w-64 bg-white border-r border-slate-200 fixed h-full overflow-y-auto no-print z-10 hidden md:block">
        <div className="p-6">
          <h1 className="text-xl font-bold text-slate-900 leading-tight">
            Low-Altitude Economy <span className="text-tech-blue-600 block">White Paper</span>
          </h1>
          <p className="text-xs text-slate-400 mt-2">Development Index Dashboard</p>
        </div>

        <nav className="mt-4 px-4 space-y-1">
           <button
              onClick={() => setSelectedDimension('All')}
              className={`w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                selectedDimension === 'All' 
                ? 'bg-slate-900 text-white' 
                : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              Full Report
            </button>
          {dimensions.map((dim) => (
            <button
              key={dim}
              onClick={() => setSelectedDimension(dim)}
              className={`w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                selectedDimension === dim 
                ? 'bg-tech-blue-50 text-tech-blue-700' 
                : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              {dim}
            </button>
          ))}
        </nav>

        <div className="absolute bottom-0 w-full p-4 border-t border-slate-100 bg-white">
          <button 
            onClick={handlePrint}
            className="w-full flex items-center justify-center space-x-2 bg-tech-blue-600 hover:bg-tech-blue-700 text-white py-2.5 rounded-lg shadow-sm transition-all font-medium text-sm"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
            <span>Export PDF</span>
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 ml-0 md:ml-64 p-8 overflow-y-auto">
        <div className="max-w-[210mm] mx-auto">
          
          {/* Cover Page Placeholder (Only visible on All) */}
           {selectedDimension === 'All' && (
             <div className="w-[210mm] h-[297mm] bg-gradient-to-br from-slate-900 to-slate-800 text-white shadow-2xl mx-auto my-8 p-[20mm] flex flex-col justify-between page-break relative overflow-hidden">
                <div className="absolute top-0 right-0 w-96 h-96 bg-tech-blue-500 rounded-full blur-[100px] opacity-20 -mr-20 -mt-20"></div>
                
                <div className="relative z-10">
                   <div className="inline-block px-3 py-1 bg-tech-blue-600/30 border border-tech-blue-500/50 rounded-full text-tech-blue-300 text-xs font-mono mb-6">CONFIDENTIAL INTERNAL REPORT</div>
                   <h1 className="text-6xl font-extrabold leading-tight tracking-tight">
                    Low-Altitude <br/>
                    Economy <br/>
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-tech-blue-400 to-low-altitude-green-400">Development Index</span>
                   </h1>
                   <div className="w-24 h-2 bg-tech-blue-500 mt-8"></div>
                </div>

                <div className="relative z-10">
                  <div className="grid grid-cols-2 gap-12 mb-12">
                     <div>
                       <span className="block text-slate-400 text-sm uppercase mb-1">Period</span>
                       <span className="text-2xl font-bold">Q3 2023</span>
                     </div>
                     <div>
                       <span className="block text-slate-400 text-sm uppercase mb-1">Region</span>
                       <span className="text-2xl font-bold">Shenzhen Pilot Zone</span>
                     </div>
                  </div>
                  <p className="text-slate-400 text-sm max-w-md leading-relaxed">
                    This white paper provides a comprehensive analysis of the low-altitude economy based on the 5D Framework: Scale, Structure, Space, Efficiency, and Innovation.
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
              <p className="text-slate-400">No data found for this dimension.</p>
            </div>
          )}

        </div>
      </main>
    </div>
  );
};

export default App;
