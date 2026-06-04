import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Copy, Check, Download, Share2, ArrowLeft, Loader } from 'lucide-react'

export default function CodeGen() {
  const location = useLocation()
  const navigate = useNavigate()
  const [selectedLanguage, setSelectedLanguage] = useState('python')
  const [generatedCode, setGeneratedCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)
  const [languages, setLanguages] = useState([])

  const analysis = location.state?.analysis

  useEffect(() => {
    if (!analysis) {
      navigate('/results')
      return
    }

    // Fetch supported languages
    fetchLanguages()
    // Auto-generate Python by default
    generateCode('python')
  }, [analysis, navigate])

  const fetchLanguages = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/generation/supported-languages')
      if (response.ok) {
        const data = await response.json()
        setLanguages(data.languages)
      }
    } catch (err) {
      console.error('Error fetching languages:', err)
    }
  }

  const generateCode = async (language) => {
    setSelectedLanguage(language)
    setLoading(true)
    setGeneratedCode('')

    try {
      const response = await fetch('http://localhost:8000/api/generation/generate-sdk', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          language,
          endpoints: analysis.endpoints || [],
          api_name: analysis.source?.split('/')[2] || 'API',
          auth_method: analysis.auth_method,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setGeneratedCode(data.code)
      }
    } catch (err) {
      console.error('Generation error:', err)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(generatedCode)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const downloadCode = () => {
    const element = document.createElement('a')
    const file = new Blob([generatedCode], { type: 'text/plain' })
    element.href = URL.createObjectURL(file)
    element.download = `sdk.${selectedLanguage === 'typescript' ? 'ts' : selectedLanguage === 'go' ? 'go' : 'py'}`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
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
            <button onClick={() => navigate('/results')} className="text-slate-400 hover:text-white">
              <ArrowLeft size={24} />
            </button>
            <div>
              <h1 className="text-2xl font-bold">💻 Code Generation</h1>
              <p className="text-sm text-slate-400">SDK wrapper in your language</p>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-4 gap-6">
          {/* Language Selector */}
          <motion.div
            className="lg:col-span-1"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
              <h3 className="font-semibold mb-4">Select Language</h3>
              <div className="space-y-2">
                {languages.map((lang) => (
                  <button
                    key={lang.id}
                    onClick={() => generateCode(lang.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-all ${
                      selectedLanguage === lang.id
                        ? 'bg-blue-600 border-blue-500'
                        : 'bg-slate-700/50 border-slate-600 hover:bg-slate-700'
                    } border`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{lang.icon}</span>
                      <span className="font-semibold">{lang.name}</span>
                    </div>
                    {selectedLanguage === lang.id && (
                      <div className="text-xs text-slate-300 mt-1">
                        {lang.features.join(', ')}
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Code Display */}
          <motion.div
            className="lg:col-span-3"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg overflow-hidden flex flex-col h-[600px]">
              {/* Code Header */}
              <div className="bg-slate-900 border-b border-slate-700 px-6 py-4 flex justify-between items-center">
                <div>
                  <h3 className="font-semibold mb-1">Generated SDK</h3>
                  <p className="text-sm text-slate-400">
                    {generatedCode.length} characters • {selectedLanguage}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={copyToClipboard}
                    disabled={loading}
                    className="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 transition disabled:opacity-50"
                    title="Copy code"
                  >
                    {copied ? <Check size={20} className="text-green-400" /> : <Copy size={20} />}
                  </button>
                  <button
                    onClick={downloadCode}
                    disabled={loading}
                    className="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 transition disabled:opacity-50"
                    title="Download code"
                  >
                    <Download size={20} />
                  </button>
                  <button
                    onClick={() => {}}
                    disabled={loading}
                    className="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 transition disabled:opacity-50"
                    title="Share code"
                  >
                    <Share2 size={20} />
                  </button>
                </div>
              </div>

              {/* Code Area */}
              <div className="flex-1 overflow-auto p-6 font-mono text-sm">
                {loading ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <Loader className="animate-spin mx-auto mb-4" size={40} />
                      <p className="text-slate-400">Generating {selectedLanguage} code...</p>
                    </div>
                  </div>
                ) : generatedCode ? (
                  <pre className="text-slate-300 whitespace-pre-wrap break-words">
                    {generatedCode}
                  </pre>
                ) : (
                  <div className="text-slate-500 text-center py-12">
                    Select a language to generate code
                  </div>
                )}
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-4 mt-6">
              <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
                <div className="text-2xl font-bold text-blue-400">
                  {analysis?.endpoints?.length || 0}
                </div>
                <div className="text-sm text-slate-400">Endpoints Wrapped</div>
              </div>
              <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
                <div className="text-2xl font-bold text-green-400">
                  {Math.round(generatedCode.length / 100) / 10}KB
                </div>
                <div className="text-sm text-slate-400">Code Size</div>
              </div>
              <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4">
                <div className="text-2xl font-bold text-purple-400">5</div>
                <div className="text-sm text-slate-400">Languages</div>
              </div>
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  )
}
