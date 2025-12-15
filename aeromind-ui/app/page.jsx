'use client';

import { useState, useRef } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // New state for upload
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  const askAeroMind = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await axios.post('http://localhost:8000/ask', {
        question: question
      });
      setResponse(res.data);
    } catch (err) {
      console.error(err);
      setError('Failed to get response from AeroMind. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
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

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans selection:bg-blue-500 selection:text-white">
      <div className="max-w-4xl mx-auto px-6 py-12">
        <motion.header 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12 text-center"
        >
          <h1 className="text-4xl font-bold tracking-tight text-blue-400 mb-2">AeroMind</h1>
          <p className="text-gray-400">Engineering Decision Support System</p>
        </motion.header>

        {/* NEW: File Upload Section */}
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
              <label htmlFor="question" className="block text-sm font-medium text-gray-300 mb-2">
                Engineering Query
              </label>
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
            <div className="flex justify-end">
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
              <div className="border-b border-gray-700 bg-gray-800/50 px-6 py-4 flex items-center justify-between">
                <h2 className="font-semibold text-gray-200">Analysis Result</h2>
                <div className="flex items-center gap-3">
                  {response.confidence && (
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${
                      response.confidence.toLowerCase() === 'high' 
                        ? 'bg-green-900/30 text-green-400 border-green-800' 
                        : 'bg-yellow-900/30 text-yellow-400 border-yellow-800'
                    }`}>
                      {response.confidence} Confidence
                    </span>
                  )}
                  <span className="text-xs text-gray-500 font-mono">
                    {response.route_selected || 'Direct'}
                  </span>
                </div>
              </div>
              
              <div className="p-6 text-gray-300 leading-relaxed whitespace-pre-wrap">
                {response.answer}
              </div>

              {response.verification_status && (
                 <div className="px-6 py-3 bg-gray-900/50 border-t border-gray-700 text-sm">
                    <span className="text-gray-500">Verification: </span>
                    <span className={response.verification_status === 'Verified' ? 'text-green-400' : 'text-yellow-400'}>
                      {response.verification_status}
                    </span>
                    {response.verification_notes && (
                      <span className="text-gray-500 ml-2">- {response.verification_notes}</span>
                    )}
                 </div>
              )}
            </div>

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
