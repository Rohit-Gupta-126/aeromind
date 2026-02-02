'use client';

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [expertMode, setExpertMode] = useState(false);
  const [analytics, setAnalytics] = useState(null);
  const [showAnalytics, setShowAnalytics] = useState(false);
  
  // New state for upload
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  // Fetch analytics on mount and periodically
  useEffect(() => {
    fetchAnalytics();
    const interval = setInterval(fetchAnalytics, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchAnalytics = async () => {
    try {
      const res = await axios.get('http://localhost:8000/analytics');
      setAnalytics(res.data);
    } catch (err) {
      console.log('Analytics not available');
    }
  };

  const askAeroMind = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await axios.post('http://localhost:8000/ask', {
        question: question,
        expert_mode: expertMode
      });
      setResponse(res.data);
      fetchAnalytics(); // Refresh analytics after query
    } catch (err) {
      console.error(err);
      setError('Failed to get response from AeroMind. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  // Handle clicking a suggested follow-up question
  const handleFollowupClick = (followup) => {
    setQuestion(followup);
  };

  // New function to handle file upload
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert(`Successfully uploaded ${file.name} and updated knowledge base!`);
      if (fileInputRef.current) fileInputRef.current.value = ''; // Reset input
    } catch (err) {
      console.error(err);
      setError('Failed to upload file.');
    } finally {
      setUploading(false);
    }
  };

  // Complexity badge color
  const getComplexityColor = (score) => {
    switch(score) {
      case 'SIMPLE': return 'bg-green-900/30 text-green-400 border-green-800';
      case 'MODERATE': return 'bg-yellow-900/30 text-yellow-400 border-yellow-800';
      case 'COMPLEX': return 'bg-red-900/30 text-red-400 border-red-800';
      default: return 'bg-gray-900/30 text-gray-400 border-gray-700';
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans selection:bg-blue-500 selection:text-white">
      <div className="max-w-5xl mx-auto px-6 py-12">
        <motion.header 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8 text-center"
        >
          <h1 className="text-4xl font-bold tracking-tight text-blue-400 mb-2">AeroMind</h1>
          <p className="text-gray-400">Engineering Decision Support System</p>
          <p className="text-xs text-gray-600 mt-1">Powered by Gemini 2.5 Flash</p>
        </motion.header>

        {/* USP: Analytics Dashboard Toggle */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex justify-center mb-6"
        >
          <button
            onClick={() => setShowAnalytics(!showAnalytics)}
            className="text-sm text-gray-400 hover:text-blue-400 transition-colors flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            {showAnalytics ? 'Hide Analytics' : 'Show Analytics'}
          </button>
        </motion.div>

        {/* USP: Analytics Dashboard */}
        <AnimatePresence>
          {showAnalytics && analytics && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-gray-800 rounded-xl shadow-lg border border-gray-700 p-6 mb-8 overflow-hidden"
            >
              <h2 className="text-lg font-semibold text-gray-300 mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
                Query Analytics
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-blue-400">{analytics.total_queries}</div>
                  <div className="text-xs text-gray-500">Total Queries</div>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-green-400">{analytics.queries_by_route?.engineering || 0}</div>
                  <div className="text-xs text-gray-500">Engineering</div>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-yellow-400">{analytics.queries_by_route?.safety || 0}</div>
                  <div className="text-xs text-gray-500">Safety</div>
                </div>
                <div className="bg-gray-900/50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-purple-400">{analytics.avg_response_time_ms?.toFixed(0) || 0}ms</div>
                  <div className="text-xs text-gray-500">Avg Response</div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* File Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-800 rounded-xl shadow-lg border border-gray-700 p-6 mb-8"
        >
          <h2 className="text-lg font-semibold text-gray-300 mb-4">Add Knowledge</h2>
          <div className="flex items-center gap-4">
            <input
              type="file"
              accept=".pdf"
              onChange={handleUpload}
              ref={fileInputRef}
              disabled={uploading}
              className="block w-full text-sm text-gray-400
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-900 file:text-blue-300
                hover:file:bg-blue-800
                cursor-pointer"
            />
            {uploading && <span className="text-blue-400 text-sm animate-pulse">Ingesting...</span>}
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gray-800 rounded-xl shadow-2xl border border-gray-700 p-6 mb-8"
        >
          <form onSubmit={askAeroMind} className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <label htmlFor="question" className="block text-sm font-medium text-gray-300">
                  Engineering Query
                </label>
                {/* USP: Expert Mode Toggle */}
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-500">Expert Mode</span>
                  <button
                    type="button"
                    onClick={() => setExpertMode(!expertMode)}
                    className={`relative w-10 h-5 rounded-full transition-colors ${
                      expertMode ? 'bg-blue-600' : 'bg-gray-700'
                    }`}
                  >
                    <span className={`absolute top-0.5 left-0.5 w-4 h-4 rounded-full bg-white transition-transform ${
                      expertMode ? 'translate-x-5' : ''
                    }`}></span>
                  </button>
                </div>
              </div>
              <textarea
                id="question"
                rows={3}
                className="w-full bg-gray-900 border border-gray-700 rounded-lg p-4 text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
                placeholder="e.g., What are the safety protocols for engine testing?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    askAeroMind(e);
                  }
                }}
              />
            </div>
            <div className="flex justify-between items-center">
              {expertMode && (
                <span className="text-xs text-blue-400 flex items-center gap-1">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z"></path>
                  </svg>
                  Detailed technical responses enabled
                </span>
              )}
              <div className="flex-1"></div>
              <button
                type="submit"
                disabled={loading || !question.trim()}
                className={`px-6 py-2.5 rounded-lg font-medium transition-all flex items-center gap-2 ${
                  loading || !question.trim()
                    ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/20'
                }`}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing...
                  </>
                ) : (
                  'Ask AeroMind'
                )}
              </button>
            </div>
          </form>
        </motion.div>

        {error && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-red-900/20 border border-red-800 text-red-200 p-4 rounded-lg mb-8"
          >
            {error}
          </motion.div>
        )}

        {response && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <div className="bg-gray-800 rounded-xl shadow-2xl border border-gray-700 overflow-hidden">
              <div className="border-b border-gray-700 bg-gray-800/50 px-6 py-4 flex items-center justify-between flex-wrap gap-2">
                <h2 className="font-semibold text-gray-200">Analysis Result</h2>
                <div className="flex items-center gap-3 flex-wrap">
                  {/* USP: Processing Time */}
                  {response.processing_time_ms && (
                    <span className="px-2 py-1 rounded text-xs bg-gray-900/50 text-gray-400 border border-gray-700">
                      ⚡ {response.processing_time_ms}ms
                    </span>
                  )}
                  {/* USP: Complexity Score */}
                  {response.complexity_score && (
                    <span className={`px-2 py-1 rounded text-xs border ${getComplexityColor(response.complexity_score)}`}>
                      {response.complexity_score}
                    </span>
                  )}
                  {response.confidence && (
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${
                      response.confidence.toLowerCase().includes('high') 
                        ? 'bg-green-900/30 text-green-400 border-green-800' 
                        : response.confidence.toLowerCase().includes('medium')
                        ? 'bg-yellow-900/30 text-yellow-400 border-yellow-800'
                        : 'bg-red-900/30 text-red-400 border-red-800'
                    }`}>
                      {response.confidence}
                    </span>
                  )}
                  <span className="text-xs text-gray-500 font-mono">
                    {response.route_selected || 'Direct'}
                  </span>
                </div>
              </div>
              
              {/* USP: Model Used Badge */}
              {response.model_used && (
                <div className="px-6 py-2 bg-gradient-to-r from-blue-900/20 to-transparent border-b border-gray-700/50">
                  <span className="text-xs text-blue-400">
                    🤖 {response.model_used}
                  </span>
                </div>
              )}
              
              <div className="p-6 text-gray-300 leading-relaxed whitespace-pre-wrap">
                {response.answer}
              </div>

              {response.verification_status && (
                 <div className="px-6 py-3 bg-gray-900/50 border-t border-gray-700 text-sm">
                    <span className="text-gray-500">Verification: </span>
                    <span className={
                      response.verification_status === 'PASS' ? 'text-green-400' : 
                      response.verification_status === 'PARTIAL' ? 'text-yellow-400' : 'text-red-400'
                    }>
                      {response.verification_status}
                    </span>
                    {response.verification_notes && (
                      <span className="text-gray-500 ml-2">- {response.verification_notes}</span>
                    )}
                 </div>
              )}
            </div>

            {/* USP: Smart Follow-up Suggestions */}
            {response.suggested_followups && response.suggested_followups.length > 0 && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-gradient-to-r from-blue-900/20 to-purple-900/20 rounded-xl shadow-lg border border-blue-800/30 p-6"
              >
                <h3 className="text-sm font-medium text-blue-300 uppercase tracking-wider mb-3 flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                  Continue Exploring
                </h3>
                <div className="flex flex-wrap gap-2">
                  {response.suggested_followups.map((followup, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleFollowupClick(followup)}
                      className="text-sm bg-gray-800/50 hover:bg-gray-700 text-gray-300 px-4 py-2 rounded-lg border border-gray-700 hover:border-blue-600 transition-all"
                    >
                      {followup}
                    </button>
                  ))}
                </div>
              </motion.div>
            )}

            {response.sources && response.sources.length > 0 && (
              <div className="bg-gray-800 rounded-xl shadow-lg border border-gray-700 p-6">
                <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-4">Source Documents</h3>
                <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {response.sources.map((source, idx) => (
                    <li key={idx} className="flex items-center gap-2 text-sm text-blue-400 bg-gray-900/50 px-3 py-2 rounded border border-gray-700/50">
                      <svg className="w-4 h-4 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                      {source}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
