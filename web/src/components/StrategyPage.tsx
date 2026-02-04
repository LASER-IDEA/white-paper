import React, { useState } from 'react';
import { Dimension } from '../types';

interface Insight {
  id: string;
  type: 'user' | 'ai';
  dimension: string;
  content: string;
  timestamp: string;
}

const StrategyPage: React.FC = () => {
  const [userInput, setUserInput] = useState('');
  const [insights, setInsights] = useState<Insight[]>([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [filterDim, setFilterDim] = useState<string>('All');

  const dimensions = Object.values(Dimension);

  const handleUserSubmit = () => {
    if (!userInput.trim()) return;

    setIsAnalyzing(true);
    // Simulate API call/Classification
    setTimeout(() => {
      // Mock classification logic
      let classifiedDim = dimensions[0];
      const lowerInput = userInput.toLowerCase();
      if (lowerInput.includes('structure') || lowerInput.includes('company')) classifiedDim = Dimension.StructureEntity;
      else if (lowerInput.includes('time') || lowerInput.includes('space')) classifiedDim = Dimension.TimeSpace;
      else if (lowerInput.includes('efficiency') || lowerInput.includes('quality')) classifiedDim = Dimension.EfficiencyQuality;
      else if (lowerInput.includes('innovation')) classifiedDim = Dimension.InnovationIntegration;

      const newInsight: Insight = {
        id: Date.now().toString(),
        type: 'user',
        dimension: classifiedDim,
        content: userInput,
        timestamp: new Date().toISOString()
      };

      setInsights(prev => [newInsight, ...prev]);
      setUserInput('');
      setIsAnalyzing(false);
    }, 1000);
  };

  const handleGenerateAI = () => {
    setIsGenerating(true);
    // Simulate AI Generation
    setTimeout(() => {
      const newInsights: Insight[] = dimensions.map((dim, idx) => ({
        id: `ai-${Date.now()}-${idx}`,
        type: 'ai',
        dimension: dim,
        content: `**AI Insight for ${dim}**: Based on the data trends, we observe significant positive momentum. Recommended strategy involves focusing on infrastructure optimization and policy support to sustain this growth. (Mock Generated)`,
        timestamp: new Date().toISOString()
      }));

      setInsights(prev => [...newInsights, ...prev]);
      setIsGenerating(false);
    }, 2000);
  };

  const handleDelete = (id: string) => {
    setInsights(prev => prev.filter(i => i.id !== id));
  };

  const filteredInsights = filterDim === 'All'
    ? insights
    : insights.filter(i => i.dimension === filterDim);

  return (
    <div className="w-[210mm] min-h-[297mm] bg-white shadow-2xl mx-auto my-8 p-[15mm] flex flex-col relative print:shadow-none print:m-0 print:w-full">
      <div className="border-b-2 border-slate-100 mb-8 pb-4">
        <h1 className="text-3xl font-bold text-[#002FA7]">Strategic Insights & Planning</h1>
        <p className="text-slate-500 mt-2">Collaborate on strategic planning by adding manual insights or using AI to generate observations.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        {/* User Input Section */}
        <div className="bg-slate-50 p-6 rounded-xl border border-slate-200">
          <h2 className="text-lg font-bold text-[#002FA7] mb-4 flex items-center">
            <span className="mr-2">👤</span> Add User Insight
          </h2>
          <p className="text-xs text-slate-500 mb-3">Your insight will be automatically classified into one of the 5 dimensions.</p>
          <textarea
            className="w-full h-32 p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#002FA7] focus:border-transparent resize-none text-sm"
            placeholder="e.g., The drone delivery network in Shenzhen shows high density in Nanshan district..."
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
          />
          <button
            onClick={handleUserSubmit}
            disabled={isAnalyzing || !userInput.trim()}
            className={`mt-4 w-full py-2 px-4 rounded-lg text-white font-medium transition-colors ${
              isAnalyzing || !userInput.trim() ? 'bg-slate-400 cursor-not-allowed' : 'bg-[#002FA7] hover:bg-[#001F7A]'
            }`}
          >
            {isAnalyzing ? 'Classifying...' : 'Analyze & Add Insight'}
          </button>
        </div>

        {/* AI Generation Section */}
        <div className="bg-slate-50 p-6 rounded-xl border border-slate-200">
          <h2 className="text-lg font-bold text-[#002FA7] mb-4 flex items-center">
            <span className="mr-2">🤖</span> Generate AI Insights
          </h2>
          <p className="text-xs text-slate-500 mb-3">Generate insights for all dimensions based on current data and Blue Book standards.</p>
          <div className="h-32 flex items-center justify-center border border-slate-200 border-dashed rounded-lg bg-white">
             <span className="text-4xl text-slate-200">✨</span>
          </div>
          <button
            onClick={handleGenerateAI}
            disabled={isGenerating}
            className={`mt-4 w-full py-2 px-4 rounded-lg text-white font-medium transition-colors ${
              isGenerating ? 'bg-slate-400 cursor-not-allowed' : 'bg-emerald-600 hover:bg-emerald-700'
            }`}
          >
            {isGenerating ? 'Analyzing...' : 'Generate All Insights'}
          </button>
        </div>
      </div>

      {/* Insights List */}
      <div>
        <div className="flex justify-between items-center mb-6">
           <h2 className="text-xl font-bold text-slate-800">Insights Repository</h2>
           <select
             value={filterDim}
             onChange={(e) => setFilterDim(e.target.value)}
             className="border border-slate-300 rounded-lg px-3 py-1 text-sm focus:ring-[#002FA7]"
           >
             <option value="All">All Dimensions</option>
             {dimensions.map(d => <option key={d} value={d}>{d}</option>)}
           </select>
        </div>

        {filteredInsights.length === 0 ? (
          <div className="text-center py-12 bg-slate-50 rounded-lg border border-slate-100">
            <p className="text-slate-400">No insights found. Add one above or generate with AI.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredInsights.map(insight => (
              <div key={insight.id} className="bg-white border border-slate-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-2">
                   <div className="flex items-center space-x-2">
                      <span className={`px-2 py-0.5 rounded text-xs font-bold uppercase ${insight.type === 'ai' ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-100 text-blue-700'}`}>
                        {insight.type === 'ai' ? 'AI Generated' : 'User Insight'}
                      </span>
                      <span className="text-sm font-semibold text-slate-600">{insight.dimension}</span>
                   </div>
                   <button
                     onClick={() => handleDelete(insight.id)}
                     className="text-slate-400 hover:text-red-500"
                     title="Delete"
                   >
                     ×
                   </button>
                </div>
                <div className="text-slate-800 text-sm leading-relaxed whitespace-pre-wrap">
                  {insight.content}
                </div>
                <div className="mt-3 text-xs text-slate-400 text-right">
                  {new Date(insight.timestamp).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default StrategyPage;
