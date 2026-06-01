import { motion } from 'framer-motion'

export default function History() {
  return (
    <motion.div 
      className="min-h-screen p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <h1 className="text-4xl font-bold text-white">Integration History</h1>
      <p className="text-slate-400 mt-2">View and manage past integrations - Coming Day 6</p>
    </motion.div>
  )
}
