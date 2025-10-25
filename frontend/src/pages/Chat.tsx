import { useState, useRef, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Send, Bot, User, Loader2, Trash2, Search } from 'lucide-react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { chatAPI } from '../services/api'
import { useAuth } from '../services/auth'
import { formatRelativeTime, getJLPTColor } from '../utils/helpers'
import toast from 'react-hot-toast'
import LoadingSpinner from '../components/LoadingSpinner'

interface ChatMessage {
  id: number
  question: string
  answer: string
  jlpt_level?: string
  grammar_points?: any[]
  translation?: string
  sources?: any[]
  created_at: string
}

interface MessageFormData {
  message: string
}

export default function Chat() {
  const [searchQuery, setSearchQuery] = useState('')
  const { user } = useAuth()
  const queryClient = useQueryClient()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const form = useForm<MessageFormData>()

  const { data: chatHistory, isLoading: isLoadingHistory } = useQuery(
    ['chatHistory'],
    () => chatAPI.getHistory().then(res => res.data),
    {
      refetchOnWindowFocus: false,
    }
  )

  const sendMessageMutation = useMutation(
    (data: { message: string; context?: string; jlpt_level?: string }) =>
      chatAPI.sendMessage(data.message, data.context, data.jlpt_level).then(res => res.data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['chatHistory'])
        form.reset()
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Failed to send message')
      },
    }
  )

  const deleteMessageMutation = useMutation(
    (chatId: number) => chatAPI.deleteEntry(chatId),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['chatHistory'])
        toast.success('Message deleted')
      },
      onError: () => {
        toast.error('Failed to delete message')
      },
    }
  )

  const clearHistoryMutation = useMutation(
    () => chatAPI.clearHistory(),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['chatHistory'])
        toast.success('Chat history cleared')
      },
      onError: () => {
        toast.error('Failed to clear history')
      },
    }
  )

  const filteredHistory = chatHistory?.filter((message: ChatMessage) =>
    message.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    message.answer.toLowerCase().includes(searchQuery.toLowerCase())
  ) || []

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatHistory])

  const handleSubmit = (data: MessageFormData) => {
    if (!data.message.trim()) return
    
    sendMessageMutation.mutate({
      message: data.message,
      jlpt_level: user?.current_jlpt_level,
    })
  }

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Chat with SenpaiAI</h1>
          <p className="text-sm text-gray-600">
            Ask questions about Japanese language, grammar, or culture
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search chat history..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={() => clearHistoryMutation.mutate()}
            className="btn btn-outline btn-sm"
            disabled={clearHistoryMutation.isLoading}
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto border border-gray-200 rounded-lg bg-white p-4 space-y-4">
        {isLoadingHistory ? (
          <div className="flex justify-center py-8">
            <LoadingSpinner size="lg" />
          </div>
        ) : filteredHistory.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-gray-500">
            <Bot className="h-12 w-12 mb-4" />
            <p className="text-lg font-medium">No messages yet</p>
            <p className="text-sm">Start a conversation by asking a question below</p>
          </div>
        ) : (
          filteredHistory.map((message: ChatMessage) => (
            <div key={message.id} className="space-y-3">
              {/* User Question */}
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center">
                    <User className="h-4 w-4 text-white" />
                  </div>
                </div>
                <div className="flex-1">
                  <div className="bg-gray-100 rounded-lg p-3">
                    <p className="text-sm text-gray-900">{message.question}</p>
                  </div>
                  <p className="mt-1 text-xs text-gray-500">
                    {formatRelativeTime(message.created_at)}
                  </p>
                </div>
                <button
                  onClick={() => deleteMessageMutation.mutate(message.id)}
                  className="text-gray-400 hover:text-red-500"
                  disabled={deleteMessageMutation.isLoading}
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>

              {/* AI Response */}
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 rounded-full bg-secondary-600 flex items-center justify-center">
                    <Bot className="h-4 w-4 text-white" />
                  </div>
                </div>
                <div className="flex-1 space-y-2">
                  <div className="bg-white border border-gray-200 rounded-lg p-3">
                    <p className="text-sm text-gray-900 japanese-text">{message.answer}</p>
                    
                    {message.jlpt_level && (
                      <div className="mt-2">
                        <span className={`jlpt-badge ${getJLPTColor(message.jlpt_level)}`}>
                          {message.jlpt_level}
                        </span>
                      </div>
                    )}
                    
                    {message.translation && (
                      <div className="mt-2 p-2 bg-blue-50 rounded border-l-4 border-blue-400">
                        <p className="text-xs text-blue-800 font-medium">Translation:</p>
                        <p className="text-sm text-blue-900">{message.translation}</p>
                      </div>
                    )}
                    
                    {message.grammar_points && message.grammar_points.length > 0 && (
                      <div className="mt-2">
                        <p className="text-xs font-medium text-gray-700 mb-1">Grammar Points:</p>
                        <div className="space-y-1">
                          {message.grammar_points.map((point, index) => (
                            <div key={index} className="text-xs text-gray-600">
                              <span className="font-medium">{point.pattern}:</span> {point.explanation}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-2">
                        <p className="text-xs font-medium text-gray-700 mb-1">Sources:</p>
                        <div className="space-y-1">
                          {message.sources.map((source, index) => (
                            <div key={index} className="text-xs text-blue-600">
                              {source.title}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  <p className="text-xs text-gray-500">
                    {formatRelativeTime(message.created_at)}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div className="mt-4">
        <form onSubmit={form.handleSubmit(handleSubmit)} className="flex space-x-2">
          <input
            {...form.register('message', { required: 'Message is required' })}
            type="text"
            placeholder="Ask a question about Japanese..."
            className="flex-1 input"
            disabled={sendMessageMutation.isLoading}
          />
          <button
            type="submit"
            disabled={sendMessageMutation.isLoading || !form.watch('message')?.trim()}
            className="btn btn-primary"
          >
            {sendMessageMutation.isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </button>
        </form>
        {form.formState.errors.message && (
          <p className="mt-1 text-sm text-red-600">
            {form.formState.errors.message.message}
          </p>
        )}
      </div>
    </div>
  )
}

