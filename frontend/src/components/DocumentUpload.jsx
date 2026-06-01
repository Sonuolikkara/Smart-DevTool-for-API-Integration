import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function DocumentUpload() {
  const navigate = useNavigate()
  const [inputType, setInputType] = useState('url')
  const [urlInput, setUrlInput] = useState('')
  const [docInput, setDocInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    if ((inputType === 'url' && !urlInput) || (inputType === 'text' && !docInput)) {
      alert('Please provide input')
      return
    }

    setLoading(true)
    try {
      // TODO: Implement API call on Day 2
      setTimeout(() => {
        navigate('/workspace')
      }, 1000)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Input Type Toggle */}
      <div className="flex gap-2">
        {['url', 'text', 'file'].map((type) => (
          <button
            key={type}
            onClick={() => setInputType(type)}
            className={`px-4 py-2 rounded-lg font-semibold transition ${
              inputType === type
                ? 'bg-blue-600 text-white'
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            {type === 'url' && '🔗 URL'}
            {type === 'text' && '📄 Paste Docs'}
            {type === 'file' && '📁 Upload File'}
          </button>
        ))}
      </div>

      {/* URL Input */}
      {inputType === 'url' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <input
            type="url"
            placeholder="Paste API documentation URL (e.g., https://stripe.com/docs/api)"
            value={urlInput}
            onChange={(e) => setUrlInput(e.target.value)}
            className="w-full px-4 py-3 rounded-lg bg-slate-700 border border-slate-600 text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
          />
        </motion.div>
      )}

      {/* Text Input */}
      {inputType === 'text' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <textarea
            placeholder="Paste your API documentation here..."
            value={docInput}
            onChange={(e) => setDocInput(e.target.value)}
            rows={8}
            className="w-full px-4 py-3 rounded-lg bg-slate-700 border border-slate-600 text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 resize-none"
          />
        </motion.div>
      )}

      {/* File Upload */}
      {inputType === 'file' && (
        <motion.div 
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }}
          className="border-2 border-dashed border-slate-600 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 transition"
        >
          <div className="text-3xl mb-2">📤</div>
          <p className="text-slate-300">Drag and drop or click to upload</p>
          <p className="text-sm text-slate-400">PDF, Markdown, or text files</p>
        </motion.div>
      )}

      {/* Options */}
      <div className="bg-slate-700/50 rounded-lg p-4 space-y-3">
        <div>
          <label className="block text-sm font-semibold mb-2">Use Case (optional)</label>
          <input
            type="text"
            placeholder="e.g., Process payments, Authenticate users..."
            className="w-full px-3 py-2 rounded bg-slate-600 border border-slate-500 text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-semibold mb-2">Preferred Language</label>
          <select className="w-full px-3 py-2 rounded bg-slate-600 border border-slate-500 text-white focus:outline-none focus:border-blue-500">
            <option>Python</option>
            <option>JavaScript</option>
            <option>TypeScript</option>
            <option>Go</option>
            <option>Java</option>
          </select>
        </div>
      </div>

      {/* Analyze Button */}
      <motion.button
        onClick={handleAnalyze}
        disabled={loading}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="w-full px-6 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:from-slate-600 disabled:to-slate-700 rounded-lg font-semibold text-lg transition flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity }}
              className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
            />
            Analyzing...
          </>
        ) : (
          <>🚀 Analyze API Documentation</>
        )}
      </motion.button>

      <p className="text-sm text-slate-400 text-center">
        Takes 2-3 seconds to analyze and extract endpoints
      </p>
    </div>
  )
}
