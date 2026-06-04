import { motion } from 'framer-motion';
import { Copy, Check } from 'lucide-react';
import { useState } from 'react';

const methodColors = {
  GET: 'bg-green-500/20 text-green-300 border-green-500/50',
  POST: 'bg-blue-500/20 text-blue-300 border-blue-500/50',
  PUT: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/50',
  PATCH: 'bg-purple-500/20 text-purple-300 border-purple-500/50',
  DELETE: 'bg-red-500/20 text-red-300 border-red-500/50',
  OPTIONS: 'bg-gray-500/20 text-gray-300 border-gray-500/50',
};

export default function EndpointCard({ endpoint, index }) {
  const [copied, setCopied] = useState(false);

  const method = endpoint.method || 'GET';
  const methodColor = methodColors[method] || methodColors.GET;

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-lg p-4 hover:border-blue-500/50 hover:shadow-lg hover:shadow-blue-500/20 transition-all"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3 flex-1">
          {/* Method Badge */}
          <div className={`${methodColor} border px-3 py-1 rounded font-bold text-sm min-w-fit`}>
            {method}
          </div>

          {/* Endpoint Path */}
          <div className="flex-1 min-w-0">
            <p className="text-white font-mono text-sm break-all">{endpoint.path}</p>
            {endpoint.description && (
              <p className="text-slate-400 text-xs mt-1">{endpoint.description}</p>
            )}
          </div>
        </div>

        {/* Copy Button */}
        <button
          onClick={() => handleCopy(endpoint.path)}
          className="ml-2 p-2 text-slate-400 hover:text-blue-400 transition-colors"
          title="Copy endpoint path"
        >
          {copied ? <Check size={16} /> : <Copy size={16} />}
        </button>
      </div>

      {/* Parameters */}
      {endpoint.parameters && endpoint.parameters.length > 0 && (
        <div className="mb-3 pb-3 border-b border-slate-700">
          <p className="text-xs text-slate-400 mb-2">Parameters:</p>
          <div className="flex flex-wrap gap-2">
            {endpoint.parameters.map((param, i) => (
              <span key={i} className="bg-slate-700/50 text-slate-300 text-xs px-2 py-1 rounded">
                <span className="font-mono">{param.name}</span>
                <span className="text-slate-500 ml-1">({param.type})</span>
                {param.required && <span className="text-red-400 ml-1">*</span>}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Footer Info */}
      <div className="flex gap-2 flex-wrap">
        {/* Authentication Badge */}
        {endpoint.requires_auth && (
          <div className="bg-purple-500/20 text-purple-300 text-xs px-2 py-1 rounded border border-purple-500/50">
            🔐 Auth Required
          </div>
        )}

        {/* Response Format Badge */}
        {endpoint.response_format && (
          <div className="bg-cyan-500/20 text-cyan-300 text-xs px-2 py-1 rounded border border-cyan-500/50">
            📋 {endpoint.response_format}
          </div>
        )}

        {/* Rate Limiting Badge */}
        {endpoint.rate_limited && (
          <div className="bg-orange-500/20 text-orange-300 text-xs px-2 py-1 rounded border border-orange-500/50">
            ⏱️ Rate Limited
          </div>
        )}
      </div>
    </motion.div>
  );
}
