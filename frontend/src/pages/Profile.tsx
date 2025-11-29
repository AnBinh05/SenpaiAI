import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useMutation, useQueryClient } from 'react-query'
import { 
  User, 
  Save, 
  Loader2, 
  Target, 
  Trophy,
  Calendar,
  BookOpen,
  MessageCircle
} from 'lucide-react'
import { authAPI } from '../services/api'
import { useAuth } from '../services/auth'
import { formatDate, getJLPTDescription } from '../utils/helpers'
import LoadingSpinner from '../components/LoadingSpinner'
import toast from 'react-hot-toast'

interface ProfileFormData {
  username: string
  current_jlpt_level: string
  learning_goals: string[]
}

const JLPT_LEVELS = ['N5', 'N4', 'N3', 'N2', 'N1']

export default function Profile() {
  const { user, refreshUser, logout, isLoading: authLoading } = useAuth()
  const queryClient = useQueryClient()
  const [newGoal, setNewGoal] = useState('')

  const form = useForm<ProfileFormData>({
    defaultValues: {
      username: user?.username || '',
      current_jlpt_level: user?.current_jlpt_level || 'N5',
      learning_goals: user?.learning_goals || [],
    }
  })

  // Update form when user data changes
  useEffect(() => {
    if (user) {
      form.reset({
        username: user.username || '',
        current_jlpt_level: user.current_jlpt_level || 'N5',
        learning_goals: user.learning_goals || [],
      })
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.id, user?.username, user?.current_jlpt_level, user?.learning_goals])

  const updateProfileMutation = useMutation(
    (data: ProfileFormData) => authAPI.updateMe(data).then(res => res.data),
    {
      onSuccess: async () => {
        // Refresh user data in AuthContext
        await refreshUser()
        toast.success('Profile updated successfully!')
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Failed to update profile')
      },
    }
  )

  const handleSubmit = (data: ProfileFormData) => {
    updateProfileMutation.mutate(data)
  }

  const addGoal = () => {
    if (!newGoal.trim()) return
    
    const currentGoals = form.getValues('learning_goals')
    if (currentGoals.includes(newGoal.trim())) {
      toast.error('This goal already exists')
      return
    }
    
    form.setValue('learning_goals', [...currentGoals, newGoal.trim()])
    setNewGoal('')
  }

  const removeGoal = (index: number) => {
    const currentGoals = form.getValues('learning_goals')
    form.setValue('learning_goals', currentGoals.filter((_, i) => i !== index))
  }

  const handleExportData = async () => {
    try {
      const response = await authAPI.exportData()
      const data = response.data
      
      // Create beautiful HTML report
      const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SenpaiAI - Learning Data Report</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.1);
      overflow: hidden;
    }
    .header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 40px;
      text-align: center;
    }
    .header h1 {
      font-size: 2.5em;
      margin-bottom: 10px;
    }
    .header p {
      opacity: 0.9;
      font-size: 1.1em;
    }
    .content {
      padding: 40px;
    }
    .section {
      margin-bottom: 40px;
    }
    .section-title {
      font-size: 1.8em;
      color: #667eea;
      margin-bottom: 20px;
      padding-bottom: 10px;
      border-bottom: 3px solid #667eea;
    }
    .info-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }
    .info-card {
      background: #f8f9fa;
      padding: 20px;
      border-radius: 8px;
      border-left: 4px solid #667eea;
    }
    .info-card label {
      display: block;
      font-weight: 600;
      color: #666;
      margin-bottom: 5px;
      font-size: 0.9em;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .info-card value {
      display: block;
      font-size: 1.2em;
      color: #333;
      font-weight: 500;
    }
    .goals-list {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .goal-tag {
      background: #667eea;
      color: white;
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 0.9em;
    }
    .chat-item {
      background: #f8f9fa;
      border-left: 4px solid #667eea;
      padding: 20px;
      margin-bottom: 20px;
      border-radius: 8px;
    }
    .chat-item-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
      flex-wrap: wrap;
      gap: 10px;
    }
    .chat-date {
      color: #666;
      font-size: 0.9em;
    }
    .jlpt-badge {
      background: #667eea;
      color: white;
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 0.85em;
      font-weight: 600;
    }
    .chat-question {
      background: white;
      padding: 15px;
      border-radius: 8px;
      margin-bottom: 10px;
      border-left: 3px solid #667eea;
    }
    .chat-question strong {
      color: #667eea;
      display: block;
      margin-bottom: 5px;
    }
    .chat-answer {
      background: #f0f4ff;
      padding: 15px;
      border-radius: 8px;
      border-left: 3px solid #764ba2;
    }
    .chat-answer strong {
      color: #764ba2;
      display: block;
      margin-bottom: 5px;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-top: 30px;
    }
    .stat-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 25px;
      border-radius: 8px;
      text-align: center;
    }
    .stat-number {
      font-size: 2.5em;
      font-weight: bold;
      margin-bottom: 5px;
    }
    .stat-label {
      opacity: 0.9;
      font-size: 1em;
    }
    .empty-state {
      text-align: center;
      padding: 40px;
      color: #999;
    }
    .empty-state-icon {
      font-size: 4em;
      margin-bottom: 20px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    th {
      background: #667eea;
      color: white;
      font-weight: 600;
    }
    tr:hover {
      background: #f8f9fa;
    }
    .footer {
      background: #f8f9fa;
      padding: 20px;
      text-align: center;
      color: #666;
      font-size: 0.9em;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📚 SenpaiAI Learning Report</h1>
      <p>Your Japanese Learning Journey</p>
      <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">Exported on ${new Date().toLocaleString()}</p>
    </div>
    
    <div class="content">
      <!-- Profile Section -->
      <div class="section">
        <h2 class="section-title">👤 Profile Information</h2>
        <div class="info-grid">
          <div class="info-card">
            <label>Username</label>
            <value>${data.user_profile.username || 'N/A'}</value>
          </div>
          <div class="info-card">
            <label>Email</label>
            <value>${data.user_profile.email || 'N/A'}</value>
          </div>
          <div class="info-card">
            <label>Current JLPT Level</label>
            <value>${data.user_profile.current_jlpt_level || 'N/A'}</value>
          </div>
          <div class="info-card">
            <label>Member Since</label>
            <value>${data.user_profile.created_at ? new Date(data.user_profile.created_at).toLocaleDateString() : 'N/A'}</value>
          </div>
        </div>
        ${data.user_profile.learning_goals && data.user_profile.learning_goals.length > 0 ? `
        <div class="info-card" style="margin-top: 20px;">
          <label>Learning Goals</label>
          <div class="goals-list">
            ${data.user_profile.learning_goals.map((goal: string) => `<span class="goal-tag">${goal}</span>`).join('')}
          </div>
        </div>
        ` : ''}
      </div>

      <!-- Statistics -->
      <div class="section">
        <h2 class="section-title">📊 Statistics</h2>
        <div class="stats">
          <div class="stat-card">
            <div class="stat-number">${data.total_chat_messages || 0}</div>
            <div class="stat-label">Chat Messages</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">${data.total_learning_sessions || 0}</div>
            <div class="stat-label">Learning Sessions</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">${data.user_profile.learning_goals?.length || 0}</div>
            <div class="stat-label">Learning Goals</div>
          </div>
        </div>
      </div>

      <!-- Chat History -->
      <div class="section">
        <h2 class="section-title">💬 Chat History</h2>
        ${data.chat_history && data.chat_history.length > 0 ? data.chat_history.map((chat: any) => `
          <div class="chat-item">
            <div class="chat-item-header">
              <span class="chat-date">📅 ${chat.created_at ? new Date(chat.created_at).toLocaleString() : 'Unknown date'}</span>
              ${chat.jlpt_level ? `<span class="jlpt-badge">${chat.jlpt_level}</span>` : ''}
            </div>
            <div class="chat-question">
              <strong>❓ Question:</strong>
              ${chat.question}
            </div>
            <div class="chat-answer">
              <strong>💡 Answer:</strong>
              ${chat.answer}
            </div>
            ${chat.translation ? `
            <div style="margin-top: 10px; padding: 10px; background: #fff3cd; border-radius: 5px; border-left: 3px solid #ffc107;">
              <strong>🌐 Translation:</strong> ${chat.translation}
            </div>
            ` : ''}
            ${chat.grammar_points && chat.grammar_points.length > 0 ? `
            <div style="margin-top: 10px; padding: 10px; background: #d1ecf1; border-radius: 5px; border-left: 3px solid #17a2b8;">
              <strong>📚 Grammar Points:</strong>
              <ul style="margin-top: 5px; margin-left: 20px;">
                ${chat.grammar_points.map((gp: any) => `<li>${typeof gp === 'string' ? gp : JSON.stringify(gp)}</li>`).join('')}
              </ul>
            </div>
            ` : ''}
          </div>
        `).join('') : `
          <div class="empty-state">
            <div class="empty-state-icon">💬</div>
            <p>No chat history yet. Start chatting to see your conversations here!</p>
          </div>
        `}
      </div>

      <!-- Learning Sessions -->
      ${data.learning_sessions && data.learning_sessions.length > 0 ? `
      <div class="section">
        <h2 class="section-title">📖 Learning Sessions</h2>
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>Topic</th>
              <th>Level</th>
              <th>Duration</th>
              <th>Score</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            ${data.learning_sessions.map((session: any) => `
              <tr>
                <td>${session.session_type || 'N/A'}</td>
                <td>${session.topic || 'N/A'}</td>
                <td>${session.difficulty_level || 'N/A'}</td>
                <td>${session.duration_minutes ? session.duration_minutes + ' min' : 'N/A'}</td>
                <td>${session.questions_answered ? `${session.correct_answers || 0}/${session.questions_answered}` : 'N/A'}</td>
                <td>${session.created_at ? new Date(session.created_at).toLocaleDateString() : 'N/A'}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
      ` : ''}
    </div>

    <div class="footer">
      <p>Generated by SenpaiAI - Your Japanese Learning Assistant</p>
      <p style="margin-top: 5px;">© ${new Date().getFullYear()} SenpaiAI. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
      `
      
      // Create and download HTML file
      const dataBlob = new Blob([htmlContent], { type: 'text/html' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `senpai-ai-report-${new Date().toISOString().split('T')[0]}.html`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      toast.success('Learning report exported successfully!')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to export data')
    }
  }

  const handleResetProgress = async () => {
    if (!confirm('Are you sure you want to reset your progress? This will delete all your chat history and learning sessions. This action cannot be undone.')) {
      return
    }

    try {
      await authAPI.resetProgress()
      toast.success('Progress reset successfully!')
      // Refresh user data
      await refreshUser()
      // Optionally refresh chat history if on chat page
      queryClient.invalidateQueries(['chatHistory'])
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to reset progress')
    }
  }

  const handleDeleteAccount = async () => {
    if (!confirm('Are you sure you want to delete your account? This action cannot be undone and all your data will be permanently deleted.')) {
      return
    }

    if (!confirm('This is your last chance. Are you absolutely sure?')) {
      return
    }

    try {
      await authAPI.deleteAccount()
      toast.success('Account deleted successfully')
      // Logout and redirect to login
      logout()
      setTimeout(() => {
        window.location.href = '/login'
      }, 1000)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to delete account')
    }
  }

  // Show loading if user data is not loaded yet
  if (authLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3">
        <User className="h-8 w-8 text-primary-600" />
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Profile</h1>
          <p className="text-sm text-gray-600">
            Manage your account settings and learning preferences
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Form */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="card-header">
              <h2 className="card-title">Account Information</h2>
              <p className="card-description">
                Update your profile information and learning preferences
              </p>
            </div>
            <div className="card-content">
              <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={user?.email || ''}
                    disabled
                    className="input w-full bg-gray-50"
                  />
                  <p className="mt-1 text-xs text-gray-500">
                    Email cannot be changed
                  </p>
                </div>

                <div>
                  <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                    Username
                  </label>
                  <input
                    {...form.register('username', {
                      required: 'Username is required',
                      minLength: { value: 3, message: 'Username must be at least 3 characters' },
                      maxLength: { value: 20, message: 'Username must be less than 20 characters' },
                      pattern: {
                        value: /^[a-zA-Z0-9_]+$/,
                        message: 'Username can only contain letters, numbers, and underscores'
                      }
                    })}
                    type="text"
                    className="input w-full"
                    placeholder="Enter your username"
                  />
                  {form.formState.errors.username && (
                    <p className="mt-1 text-sm text-red-600">
                      {form.formState.errors.username.message}
                    </p>
                  )}
                </div>

                <div>
                  <label htmlFor="current_jlpt_level" className="block text-sm font-medium text-gray-700 mb-2">
                    Current JLPT Level
                  </label>
                  <select
                    {...form.register('current_jlpt_level', { required: 'JLPT level is required' })}
                    className="input w-full"
                  >
                    {JLPT_LEVELS.map((level) => (
                      <option key={level} value={level}>
                        {level} - {getJLPTDescription(level)}
                      </option>
                    ))}
                  </select>
                  {form.formState.errors.current_jlpt_level && (
                    <p className="mt-1 text-sm text-red-600">
                      {form.formState.errors.current_jlpt_level.message}
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Learning Goals
                  </label>
                  <div className="space-y-3">
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        value={newGoal}
                        onChange={(e) => setNewGoal(e.target.value)}
                        placeholder="Add a learning goal..."
                        className="input flex-1"
                        onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addGoal())}
                      />
                      <button
                        type="button"
                        onClick={addGoal}
                        className="btn btn-outline"
                        disabled={!newGoal.trim()}
                      >
                        Add
                      </button>
                    </div>
                    
                    <div className="space-y-2">
                      {form.watch('learning_goals').map((goal, index) => (
                        <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                          <span className="text-sm text-gray-700">{goal}</span>
                          <button
                            type="button"
                            onClick={() => removeGoal(index)}
                            className="text-red-500 hover:text-red-700"
                          >
                            ×
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={updateProfileMutation.isLoading}
                  className="btn btn-primary w-full"
                >
                  {updateProfileMutation.isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="mr-2 h-4 w-4" />
                      Save Changes
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>

        {/* Profile Stats */}
        <div className="space-y-6">
          {/* Account Info */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Account Information</h3>
            </div>
            <div className="card-content space-y-4">
              <div className="flex items-center space-x-3">
                <div className="h-12 w-12 rounded-full bg-primary-600 flex items-center justify-center">
                  <span className="text-lg font-medium text-white">
                    {user?.username?.charAt(0).toUpperCase()}
                  </span>
                </div>
                <div>
                  <p className="font-medium text-gray-900">{user?.username}</p>
                  <p className="text-sm text-gray-500">{user?.email}</p>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">Member since</span>
                  <span className="text-sm font-medium text-gray-900">
                    {user?.created_at ? formatDate(user.created_at) : 'N/A'}
                  </span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">Current Level</span>
                  <span className="text-sm font-medium text-gray-900">
                    {user?.current_jlpt_level}
                  </span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">Learning Goals</span>
                  <span className="text-sm font-medium text-gray-900">
                    {user?.learning_goals?.length || 0}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Learning Progress */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Learning Progress</h3>
            </div>
            <div className="card-content space-y-4">
              <div className="flex items-center space-x-3">
                <Trophy className="h-8 w-8 text-yellow-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">JLPT Level</p>
                  <p className="text-xs text-gray-500">
                    {user?.current_jlpt_level} - {getJLPTDescription(user?.current_jlpt_level || 'N5')}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <Target className="h-8 w-8 text-green-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Learning Goals</p>
                  <p className="text-xs text-gray-500">
                    {user?.learning_goals?.length || 0} goal{(user?.learning_goals?.length || 0) !== 1 ? 's' : ''} set
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <MessageCircle className="h-8 w-8 text-blue-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Chat Sessions</p>
                  <p className="text-xs text-gray-500">Track your conversations</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <BookOpen className="h-8 w-8 text-purple-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Study Materials</p>
                  <p className="text-xs text-gray-500">Access learning library</p>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">Quick Actions</h3>
            </div>
            <div className="card-content space-y-2">
              <button 
                onClick={handleExportData}
                className="w-full btn btn-outline btn-sm"
              >
                Export Learning Data
              </button>
              <button 
                onClick={handleResetProgress}
                className="w-full btn btn-outline btn-sm"
              >
                Reset Progress
              </button>
              <button 
                onClick={handleDeleteAccount}
                className="w-full btn btn-outline btn-sm text-red-600 hover:text-red-700"
              >
                Delete Account
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}


