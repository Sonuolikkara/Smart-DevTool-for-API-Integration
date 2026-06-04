import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Link as LinkIcon, Loader } from 'lucide-react';

export default function DocumentUpload({ onAnalysisComplete }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [uploadMode, setUploadMode] = useState('file'); // 'file' or 'url'
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      // Validate file size (max 10MB)
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        return;
      }
      
      // Validate file type
      const validTypes = ['application/pdf', 'text/plain', 'text/markdown', 'text/html', 'application/json'];
      if (!validTypes.includes(selectedFile.type)) {
        setError('File type not supported. Use PDF, TXT, MD, HTML, or JSON');
        return;
      }
      
      setFile(selectedFile);
      setError('');
    }
  };

  const handleFileUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/api/documents/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const data = await response.json();
      setSuccess(`✅ ${data.message}`);
      
      // Trigger analysis
      if (data.file_path) {
        analyzeDocument(data.file_path, data.content_preview);
      }

      setFile(null);
      document.querySelector('input[type="file"]').value = '';
    } catch (err) {
      setError(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleUrlFetch = async () => {
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 25000);

    try {
      const response = await fetch('http://localhost:8000/api/documents/fetch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url.trim() }),
        signal: controller.signal,
      });

      if (!response.ok) {
        const errorData = await response.json();
        const errorMsg = typeof errorData.detail === 'string' 
          ? errorData.detail 
          : JSON.stringify(errorData.detail) || 'Fetch failed';
        throw new Error(errorMsg);
      }

      const data = await response.json();
      setSuccess(`✅ ${data.message}`);
      
      // Trigger analysis
      if (data.content_preview) {
        await analyzeDocument(data.url, data.content_preview);
      } else {
        throw new Error('No content preview returned from server');
      }

      setUrl('');
    } catch (err) {
      const message = err.name === 'AbortError'
        ? 'Fetch timed out. Try a smaller or different URL.'
        : err.message;
      setError(`❌ ${message}`);
      console.error('Fetch error:', err);
    } finally {
      clearTimeout(timeoutId);
      setLoading(false);
    }
  };

  const analyzeDocument = async (source, preview) => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 20000);

    try {
      const response = await fetch('http://localhost:8000/api/analysis/analyze-full', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          documentation: preview || '',
          url: source,
        }),
        signal: controller.signal,
      });

      if (response.ok) {
        const analysisData = await response.json();
        
        // Navigate to results page with analysis data
        navigate('/results', { 
          state: { 
            analysis: { 
              ...analysisData, 
              source: source 
            } 
          } 
        });
        
        // Also call callback if provided (for backward compatibility)
        if (onAnalysisComplete) {
          onAnalysisComplete(analysisData);
        }
      } else {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }
    } catch (err) {
      const message = err.name === 'AbortError'
        ? 'Analysis timed out. Try a shorter document.'
        : err.message;
      console.error('Analysis error:', err);
      setError(`Analysis failed: ${message}`);
    } finally {
      clearTimeout(timeoutId);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg shadow-2xl p-6 border border-slate-700">
      {/* Title */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">📚 Import API Documentation</h2>
        <p className="text-slate-400">Upload a file or provide a URL to your API documentation</p>
      </div>

      {/* Mode Selector */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setUploadMode('file')}
          className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all ${
            uploadMode === 'file'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          <Upload className="inline mr-2" size={18} />
          Upload File
        </button>
        <button
          onClick={() => setUploadMode('url')}
          className={`flex-1 py-3 px-4 rounded-lg font-semibold transition-all ${
            uploadMode === 'url'
              ? 'bg-blue-600 text-white shadow-lg'
              : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
          }`}
        >
          <LinkIcon className="inline mr-2" size={18} />
          Fetch from URL
        </button>
      </div>

      {/* File Upload Mode */}
      {uploadMode === 'file' && (
        <div className="space-y-4">
          <div className="border-2 border-dashed border-slate-600 rounded-lg p-8 text-center hover:border-blue-500 transition-colors cursor-pointer">
            <input
              type="file"
              accept=".pdf,.txt,.md,.html,.json"
              onChange={handleFileChange}
              className="hidden"
              id="file-input"
            />
            <label htmlFor="file-input" className="cursor-pointer block">
              <Upload className="mx-auto mb-2 text-slate-400" size={32} />
              <p className="text-white font-semibold">Click to upload or drag and drop</p>
              <p className="text-slate-400 text-sm mt-1">Supports: PDF, TXT, MD, HTML, JSON (max 10MB)</p>
              {file && (
                <p className="text-blue-400 mt-2 font-semibold">📄 {file.name}</p>
              )}
            </label>
          </div>
          <button
            onClick={handleFileUpload}
            disabled={!file || loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white font-bold py-3 px-4 rounded-lg transition-colors"
          >
            {loading ? (
              <>
                <Loader className="inline mr-2 animate-spin" size={18} />
                Uploading...
              </>
            ) : (
              'Upload Document'
            )}
          </button>
        </div>
      )}

      {/* URL Fetch Mode */}
      {uploadMode === 'url' && (
        <div className="space-y-4">
          <input
            type="url"
            placeholder="https://docs.github.com/en/rest"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
          <p className="text-slate-400 text-sm">
            Enter the URL of the API documentation you want to analyze
          </p>
          <button
            onClick={handleUrlFetch}
            disabled={!url.trim() || loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white font-bold py-3 px-4 rounded-lg transition-colors"
          >
            {loading ? (
              <>
                <Loader className="inline mr-2 animate-spin" size={18} />
                Fetching...
              </>
            ) : (
              'Fetch & Analyze'
            )}
          </button>
        </div>
      )}

      {/* Messages */}
      {error && (
        <div className="mt-4 p-4 bg-red-900/20 border border-red-700 rounded-lg text-red-300">
          {error}
        </div>
      )}

      {success && (
        <div className="mt-4 p-4 bg-green-900/20 border border-green-700 rounded-lg text-green-300">
          {success}
        </div>
      )}

      {/* Info */}
      <div className="mt-6 pt-6 border-t border-slate-700 text-slate-400 text-sm">
        <p className="font-semibold text-white mb-2">📋 Supported Formats:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>GitHub API Documentation</li>
          <li>Swagger/OpenAPI specs (JSON/YAML)</li>
          <li>Markdown documentation</li>
          <li>HTML pages</li>
          <li>Plain text files</li>
        </ul>
      </div>
    </div>
  );
}

