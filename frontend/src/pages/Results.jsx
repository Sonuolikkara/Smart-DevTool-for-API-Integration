import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, Download, Share2, Copy } from 'lucide-react'
import EndpointCard from '../components/EndpointCard'

export default function Results() {
  const location = useLocation()
  const navigate = useNavigate()
  const [analysis, setAnalysis] = useState(null)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (location.state?.analysis) {
      setAnalysis(location.state.analysis)
    } else {
      navigate('/')
    }
  }, [location.state, navigate])

  if (!analysis) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <p className="text-slate-400">Loading...</p>
      </div>
    )
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <motion.header 
        className="border-b border-slate-700 backdrop-blur-sm sticky top-0 z-40"
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button 
              onClick={() => navigate('/')}
              className="p-2 hover:bg-slate-700 rounded-lg transition"
            >
              <ArrowLeft size={20} />
            </button>
            <div>
              <h1 className="text-2xl font-bold">API Analysis Results</h1>
              <p className="text-sm text-slate-400">{analysis.source || 'API Documentation'}</p>
            </div>
          </div>
          <div className="flex gap-2">
            <button className="px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 transition flex items-center gap-2">
              <Download size={18} />
              Export
            </button>
            <button className="px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 transition flex items-center gap-2">
              <Share2 size={18} />
              Share
            </button>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-12">
        {/* Summary Stats */}
        <motion.div 
          className="grid md:grid-cols-4 gap-4 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
            <div className="text-3xl font-bold text-blue-400">{analysis.endpoints?.length || 0}</div>
            <p className="text-slate-400 text-sm">Total Endpoints</p>
          </div>
          
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
            <div className="text-2xl font-bold text-green-400">{analysis.auth_method || 'None'}</div>
            <p className="text-slate-400 text-sm">Auth Method</p>
          </div>
          
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
            <div className="text-2xl font-bold text-purple-400">{analysis.response_format || 'JSON'}</div>
            <p className="text-slate-400 text-sm">Response Format</p>
          </div>
          
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
            <div className="text-3xl font-bold text-yellow-400">{analysis.security_score || 'N/A'}</div>
            <p className="text-slate-400 text-sm">Security Score</p>
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          className="flex gap-4 mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.05 }}
        >
          <button
            onClick={() => navigate('/codegen', { state: { analysis } })}
            className="flex-1 md:flex-none px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg font-semibold hover:shadow-lg transition-all flex items-center justify-center gap-2"
          >
            💻 Generate Code
          </button>
          <button
            onClick={() => navigate('/history')}
            className="flex-1 md:flex-none px-6 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold transition-all flex items-center justify-center gap-2"
          >
            📋 View History
          </button>
        </motion.div>

        {/* Analysis Details */}
        <motion.div 
          className="grid md:grid-cols-2 gap-8 mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          {/* Authentication */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <span>🔐</span> Authentication
            </h3>
            <div className="space-y-3">
              <div>
                <p className="text-slate-400 text-sm">Primary Method</p>
                <p className="text-white font-semibold">{analysis.auth_method || 'None'}</p>
              </div>
              {analysis.auth_methods && analysis.auth_methods.length > 0 && (
                <div>
                  <p className="text-slate-400 text-sm">All Methods Found</p>
                  <div className="flex gap-2 flex-wrap mt-2">
                    {analysis.auth_methods.map((method, idx) => (
                      <span key={idx} className="px-3 py-1 bg-blue-900/30 border border-blue-700 text-blue-300 rounded text-sm">
                        {method}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Response Format */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <span>📊</span> Response Format
            </h3>
            <div className="space-y-3">
              <div>
                <p className="text-slate-400 text-sm">Primary Format</p>
                <p className="text-white font-semibold">{analysis.response_format || 'JSON'}</p>
              </div>
              {analysis.all_formats && analysis.all_formats.length > 0 && (
                <div>
                  <p className="text-slate-400 text-sm">All Formats Detected</p>
                  <div className="flex gap-2 flex-wrap mt-2">
                    {analysis.all_formats.map((format, idx) => (
                      <span key={idx} className="px-3 py-1 bg-purple-900/30 border border-purple-700 text-purple-300 rounded text-sm">
                        {format}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Security Analysis */}
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 md:col-span-2">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <span>🛡️</span> Security Analysis
            </h3>
            <div className="grid md:grid-cols-4 gap-4">
              <div className="flex items-center gap-2">
                <span className={analysis.rate_limited ? '✅' : '⚠️'}>Rate Limited</span>
              </div>
              <div className="flex items-center gap-2">
                <span className={analysis.requires_https ? '✅' : '⚠️'}>HTTPS Required</span>
              </div>
              <div className="flex items-center gap-2">
                <span className={analysis.requires_auth ? '✅' : '⚠️'}>Auth Required</span>
              </div>
              <div className="flex items-center gap-2">
                <span className={analysis.cors_enabled ? '✅' : '⚠️'}>CORS Enabled</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Endpoints */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <span>📍</span> Extracted Endpoints ({analysis.endpoints?.length || 0})
          </h2>

          {analysis.endpoints && analysis.endpoints.length > 0 ? (
            <div className="grid md:grid-cols-2 gap-4">
              {analysis.endpoints.map((endpoint, idx) => (
                <EndpointCard key={idx} endpoint={endpoint} index={idx} />
              ))}
            </div>
          ) : (
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-8 text-center">
              <p className="text-slate-400">No endpoints extracted. Try analyzing a different documentation.</p>
            </div>
          )}
        </motion.div>

        {/* Quick Copy Section */}
        {analysis.endpoints && analysis.endpoints.length > 0 && (
          <motion.div 
            className="mt-12 bg-slate-800/50 border border-slate-700 rounded-lg p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <h3 className="text-lg font-semibold mb-4">Quick Copy All Endpoints</h3>
            <div className="bg-slate-900 rounded p-4 font-mono text-xs text-slate-300 max-h-48 overflow-y-auto mb-4">
              {analysis.endpoints.map((endpoint, idx) => (
                <div key={idx}>{endpoint.method} {endpoint.path}</div>
              ))}
            </div>
            <button
              onClick={() => copyToClipboard(
                analysis.endpoints.map(e => `${e.method} ${e.path}`).join('\n')
              )}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg flex items-center gap-2 transition"
            >
              <Copy size={18} />
              {copied ? 'Copied!' : 'Copy All'}
            </button>
          </motion.div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-700 mt-20 py-8 text-center text-slate-400">
        <p>Ready to generate SDK wrappers? Head to Day 4!</p>
      </footer>
    </div>
  )
}
