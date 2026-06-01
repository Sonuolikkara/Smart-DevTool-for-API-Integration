import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import DocumentUpload from '../components/DocumentUpload'

export default function Home() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('upload')

  const exampleAPIs = [
    { name: 'Stripe API', color: 'from-blue-500 to-blue-600' },
    { name: 'GitHub API', color: 'from-gray-700 to-gray-800' },
    { name: 'Twilio API', color: 'from-red-500 to-red-600' },
    { name: 'OpenAI API', color: 'from-green-500 to-green-600' },
  ]

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
            <div className="text-3xl">⚡</div>
            <div>
              <h1 className="text-2xl font-bold">Smart DevTool</h1>
              <p className="text-sm text-slate-400">API Integration Assistant</p>
            </div>
          </div>
          <button 
            onClick={() => navigate('/history')}
            className="px-4 py-2 rounded-lg bg-slate-700 hover:bg-slate-600 transition"
          >
            History
          </button>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-16">
        {/* Hero Section */}
        <motion.section 
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        >
          <h2 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Auto-generate SDK Wrappers
          </h2>
          <p className="text-xl text-slate-300 max-w-2xl mx-auto mb-8">
            Transform any API documentation into production-ready wrapper code in seconds.
            <br />
            <span className="text-slate-400">60x faster than manual integration.</span>
          </p>

          {/* Problem/Solution */}
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <motion.div 
              className="bg-slate-800/50 border border-slate-700 rounded-lg p-6"
              whileHover={{ scale: 1.02 }}
            >
              <h3 className="text-lg font-semibold mb-4 text-red-400">❌ Traditional Way</h3>
              <ul className="space-y-2 text-sm text-slate-300 text-left">
                <li>📖 Read API docs (30 min)</li>
                <li>🔐 Understand auth (15 min)</li>
                <li>🔍 Find endpoints (20 min)</li>
                <li>💻 Write wrapper (45 min)</li>
                <li>🐛 Test & debug (30 min)</li>
                <li className="font-semibold pt-2">⏱️ Total: 2+ hours</li>
              </ul>
            </motion.div>

            <motion.div 
              className="bg-slate-800/50 border border-slate-700 rounded-lg p-6"
              whileHover={{ scale: 1.02 }}
            >
              <h3 className="text-lg font-semibold mb-4 text-green-400">✅ Smart DevTool</h3>
              <ul className="space-y-2 text-sm text-slate-300 text-left">
                <li>📄 Paste/upload docs</li>
                <li>🚀 Auto-extract endpoints</li>
                <li>🔑 Detect authentication</li>
                <li>💾 Generate wrapper code</li>
                <li>📋 Ready to copy-paste</li>
                <li className="font-semibold pt-2">⚡ Total: 2 minutes</li>
              </ul>
            </motion.div>
          </div>
        </motion.section>

        {/* Main Input Section */}
        <motion.section 
          className="mb-16"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="bg-gradient-to-br from-slate-800 to-slate-800/50 border border-slate-700 rounded-lg p-8">
            <h3 className="text-2xl font-semibold mb-6">Get Started</h3>
            
            <DocumentUpload />
          </div>
        </motion.section>

        {/* Example APIs */}
        <motion.section 
          className="mb-16"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <h3 className="text-2xl font-semibold mb-8">Try with Example APIs</h3>
          <div className="grid md:grid-cols-4 gap-4">
            {exampleAPIs.map((api, idx) => (
              <motion.button
                key={idx}
                className={`bg-gradient-to-br ${api.color} rounded-lg p-6 font-semibold hover:shadow-lg transition`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {api.name}
              </motion.button>
            ))}
          </div>
        </motion.section>

        {/* Features */}
        <motion.section 
          className="grid md:grid-cols-3 gap-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          {[
            { icon: '📊', title: 'Endpoint Extraction', desc: 'Auto-detect all endpoints from documentation' },
            { icon: '🔐', title: 'Auth Detection', desc: 'Identify authentication methods (Bearer, API Key, OAuth)' },
            { icon: '🌐', title: 'Multi-Language', desc: 'Generate Python, JavaScript, Go, Java, and more' },
          ].map((feature, idx) => (
            <motion.div
              key={idx}
              className="bg-slate-800/50 border border-slate-700 rounded-lg p-6"
              whileHover={{ scale: 1.05 }}
            >
              <div className="text-4xl mb-3">{feature.icon}</div>
              <h4 className="font-semibold mb-2">{feature.title}</h4>
              <p className="text-sm text-slate-400">{feature.desc}</p>
            </motion.div>
          ))}
        </motion.section>
      </main>

      {/* Footer */}
      <motion.footer 
        className="border-t border-slate-700 mt-20 py-8 text-center text-slate-400"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.5 }}
      >
        <p>Built for Claysys AI Hackathon 2024</p>
      </motion.footer>
    </div>
  )
}
