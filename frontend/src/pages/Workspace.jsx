import { motion } from 'framer-motion'

export default function Workspace() {
  return (
    <motion.div 
      className="min-h-screen p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <h1 className="text-4xl font-bold text-white">Workspace</h1>
      <p className="text-slate-400 mt-2">Editor and code generation workspace - Coming Day 2</p>
    </motion.div>
  )
}
