import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Workspace from './pages/Workspace'
import History from './pages/History'
import Results from './pages/Results'
import CodeGen from './pages/CodeGen'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/workspace" element={<Workspace />} />
        <Route path="/history" element={<History />} />
        <Route path="/results" element={<Results />} />
        <Route path="/codegen" element={<CodeGen />} />
      </Routes>
    </div>
  )
}

export default App
