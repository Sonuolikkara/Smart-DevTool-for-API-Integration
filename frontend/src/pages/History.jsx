import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, Loader, Trash2, Eye } from 'lucide-react'

export default function History() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('analyses')
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)

  useEffect(() => {
    loadHistory()
    loadStats()
  }, [activeTab])

  const loadHistory = async () => {
    setLoading(true)
    try {
      const endpoint = activeTab === 'analyses' 
        ? 'http://localhost:8000/api/history/analyses'
        : 'http://localhost:8000/api/history/generations'
      
      const response = await fetch(endpoint)
      if (response.ok) {
        const data = await response.json()
        setItems(data[activeTab === 'analyses' ? 'analyses' : 'generations'] || [])
      }
    } catch (err) {
      console.error('Error loading history:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/history/statistics')
      if (response.ok) {
        const data = await response.json()
        setStats(data.statistics)
      }
    } catch (err) {
      console.error('Error loading stats:', err)
    }
  }

  const formatDate = (isoDate) => {
    return new Date(isoDate).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
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
          <div className="flex items-center gap-3">
            <button onClick={() => navigate('/')} className="text-slate-400 hover:text-white">
              <ArrowLeft size={24} />
            </button>
            <div>
              <h1 className="text-2xl font-bold">📋 Integration History</h1>
              <p className="text-sm text-slate-400">View all past analyses and code generations</p>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Statistics */}
        {stats && (
          <motion.div
            className="grid md:grid-cols-4 gap-4 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="text-3xl font-bold text-blue-400">{stats.total_analyses}</div>
              <div className="text-sm text-slate-400 mt-1">Total Analyses</div>
            </div>
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="text-3xl font-bold text-green-400">{stats.total_generations}</div>
              <div className="text-sm text-slate-400 mt-1">Code Generations</div>
            </div>
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="text-3xl font-bold text-purple-400">
                {Object.keys(stats.languages_used || {}).length}
              </div>
              <div className="text-sm text-slate-400 mt-1">Languages Used</div>
            </div>
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
              <div className="text-3xl font-bold text-yellow-400">
                {Math.round(stats.avg_endpoints_per_analysis)}
              </div>
              <div className="text-sm text-slate-400 mt-1">Avg Endpoints</div>
            </div>
          </motion.div>
        )}

        {/* Tab Selector */}
        <div className="flex gap-4 mb-6 border-b border-slate-700">
          <button
            onClick={() => setActiveTab('analyses')}
            className={`px-4 py-3 font-semibold transition-all border-b-2 ${
              activeTab === 'analyses'
                ? 'border-blue-500 text-blue-400'
                : 'border-transparent text-slate-400 hover:text-white'
            }`}
          >
            📊 Analyses ({items.length})
          </button>
          <button
            onClick={() => setActiveTab('generations')}
            className={`px-4 py-3 font-semibold transition-all border-b-2 ${
              activeTab === 'generations'
                ? 'border-blue-500 text-blue-400'
                : 'border-transparent text-slate-400 hover:text-white'
            }`}
          >
            💻 Generations ({items.length})
          </button>
        </div>

        {/* Items List */}
        <motion.div
          className="space-y-3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader className="animate-spin mr-2" size={24} />
              <p className="text-slate-400">Loading {activeTab}...</p>
            </div>
          ) : items.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-slate-400 text-lg">No {activeTab} yet</p>
              <p className="text-slate-500 text-sm">Start by analyzing an API to populate history</p>
            </div>
          ) : (
            items.map((item, idx) => (
              <motion.div
                key={item.id}
                className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 hover:border-slate-600 transition-all cursor-pointer"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: idx * 0.05 }}
                onClick={() => {
                  if (activeTab === 'analyses' && item.analysis) {
                    navigate('/results', { state: { analysis: item.analysis } })
                  }
                }}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    {activeTab === 'analyses' ? (
                      <>
                        <div className="font-semibold flex items-center gap-2">
                          <span className="text-blue-400">📊</span>
                          {item.source || 'Unknown Source'}
                        </div>
                        <div className="text-sm text-slate-400 mt-1">
                          {item.endpoints_count} endpoints • {item.auth_method || 'No auth'}
                        </div>
                      </>
                    ) : (
                      <>
                        <div className="font-semibold flex items-center gap-2">
                          <span className="text-purple-400">💻</span>
                          {item.language.charAt(0).toUpperCase() + item.language.slice(1)} - {item.api_name}
                        </div>
                        <div className="text-sm text-slate-400 mt-1">
                          {item.code_length} characters
                        </div>
                      </>
                    )}
                    <div className="text-xs text-slate-500 mt-2">
                      {formatDate(item.timestamp)}
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button className="p-2 rounded-lg bg-slate-700/50 hover:bg-slate-700 transition">
                      <Eye size={18} />
                    </button>
                    <button className="p-2 rounded-lg bg-slate-700/50 hover:bg-slate-700 transition text-red-400 hover:text-red-300">
                      <Trash2 size={18} />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))
          )}
        </motion.div>
      </main>
    </div>
  )
}

