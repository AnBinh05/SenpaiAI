import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './services/auth'
import Layout from './components/Layout'
import Login from './pages/Login'
import Chat from './pages/Chat'
import Grammar from './pages/Grammar'
import Library from './pages/Library'
import Profile from './pages/Profile'
import LoadingSpinner from './components/LoadingSpinner'

function App() {
  const { user, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    )
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/chat" replace />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/grammar" element={<Grammar />} />
        <Route path="/library" element={<Library />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="*" element={<Navigate to="/chat" replace />} />
      </Routes>
    </Layout>
  )
}

export default App


