import { useState, useRef, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { Send, Bot, User, Loader2, Trash2, Search, BookOpen } from 'lucide-react'
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

  const { data: chatHistory, isLoading: isLoadingHistory, refetch: refetchHistory, error: historyError } = useQuery(
    ['chatHistory'],
    () => {
      // Check if user is logged in
      const token = localStorage.getItem('access_token')
      if (!token) {
        throw new Error('Bạn chưa đăng nhập. Vui lòng đăng nhập để xem lịch sử chat.')
      }
      
      return chatAPI.getHistory().then(res => {
        // Ensure we return an array
        if (!res.data) {
          console.warn('⚠️ No data in response, returning empty array')
          return []
        }
        
        if (!Array.isArray(res.data)) {
          console.warn('⚠️ Response data is not an array:', typeof res.data, res.data)
          return []
        }
        
        return res.data
      }).catch(error => {
        console.error('❌ Error loading chat history:', error)
        console.error('❌ Error response:', error.response)
        console.error('❌ Error data:', error.response?.data)
        
        // Handle specific error cases
        if (error.response?.status === 401 || error.response?.status === 403) {
          // Authentication error - clear token and redirect
          localStorage.removeItem('access_token')
          window.location.href = '/login'
          throw new Error('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.')
        }
        
        // Create a more descriptive error
        const errorMessage = error.response?.data?.detail || 
                            error.message || 
                            (error.code === 'ERR_NETWORK' || !error.response 
                              ? 'Lỗi kết nối. Vui lòng kiểm tra backend đang chạy.' 
                              : 'Lỗi không xác định')
        
        const enhancedError = new Error(errorMessage)
        ;(enhancedError as any).response = error.response
        ;(enhancedError as any).code = error.code
        throw enhancedError
      })
    },
    {
      refetchOnWindowFocus: true, // Refetch when window gains focus
      refetchInterval: false, // Don't auto-refetch
      retry: (failureCount, error: any) => {
        // Don't retry on auth errors
        if (error?.response?.status === 401 || error?.response?.status === 403) {
          return false
        }
        // Retry once for other errors
        return failureCount < 1
      },
      enabled: !!localStorage.getItem('access_token'), // Only run if user is logged in
    }
  )

  const sendMessageMutation = useMutation(
    (data: { message: string; context?: string; jlpt_level?: string }) =>
      chatAPI.sendMessage(data.message, data.context, data.jlpt_level).then(res => res.data),
    {
      onMutate: async (newMessage) => {
        // Cancel any outgoing refetches (so they don't overwrite our optimistic update)
        await queryClient.cancelQueries(['chatHistory'])

        // Snapshot the previous value
        const previousHistory = queryClient.getQueryData(['chatHistory'])

        // Optimistically update to the new value
        const optimisticMessage: ChatMessage = {
          id: Date.now(), // Temporary ID
          question: newMessage.message,
          answer: 'AI is thinking...', // Clearer placeholder
          created_at: new Date().toISOString(),
        }

        queryClient.setQueryData(['chatHistory'], (old: ChatMessage[] = []) => [
          optimisticMessage,
          ...old,
        ])
        
        // Scroll to bottom to show new message
        setTimeout(() => {
          messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
        }, 100)

        // Return a context object with the snapshotted value
        return { previousHistory }
      },
      onSuccess: (data, variables, context) => {
        // Force refetch to get the real data from server (including the saved message)
        queryClient.invalidateQueries(['chatHistory'])
        // Refetch immediately
        queryClient.refetchQueries(['chatHistory'])
        form.reset()
        // Scroll to bottom after response
        setTimeout(() => {
          messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
        }, 200)
        // Don't show success toast - response is visible in chat
        console.log('✅ Message sent successfully, chat history refreshed')
      },
      onError: (error: any, variables, context) => {
        // If the mutation fails, use the context returned from onMutate to roll back
        if (context?.previousHistory) {
          queryClient.setQueryData(['chatHistory'], context.previousHistory)
        }
        
        const errorMessage = error.response?.data?.detail || error.message || 'Failed to send message'
        toast.error(errorMessage)
        console.error('Chat error:', error)
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

  // Ensure chatHistory is always an array and filter it
  const filteredHistory = (Array.isArray(chatHistory) ? chatHistory : [])
    .filter((message: ChatMessage) => {
      // Only filter out completely invalid messages
      if (!message || typeof message !== 'object') {
        console.warn('⚠️ Invalid message format (not an object):', message)
        return false
      }
      
      // Log warning but don't filter if question or answer is missing
      if (!message.question) {
        console.warn('⚠️ Message missing question:', message.id, message)
      }
      if (!message.answer) {
        console.warn('⚠️ Message missing answer:', message.id, message)
      }
      
      const query = searchQuery.toLowerCase().trim()
      // If search query is empty, show all messages
      if (query === '') {
        return true
      }
      
      // Filter based on search query
      const questionMatch = message.question?.toLowerCase().includes(query) || false
      const answerMatch = message.answer?.toLowerCase().includes(query) || false
      return questionMatch || answerMatch
    })
  
  useEffect(() => {
    // Scroll to bottom when chat history changes or when sending message
    setTimeout(() => {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }, [chatHistory, sendMessageMutation.isLoading, isLoadingHistory])

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
              placeholder="Tìm kiếm lịch sử chat..."
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
      <div className="flex-1 overflow-y-auto border border-gray-200 rounded-lg bg-white p-4 space-y-4 min-h-0">
        {/* Loading state */}
        {isLoadingHistory && (
          <div className="flex justify-center py-8">
            <LoadingSpinner size="lg" />
          </div>
        )}
        
        {/* Error state */}
        {!isLoadingHistory && historyError && (
          <div className="flex flex-col items-center justify-center py-12 text-red-500">
            <Bot className="h-12 w-12 mb-4" />
            <p className="text-lg font-medium">Lỗi khi tải lịch sử chat</p>
            <p className="text-sm">
              {(() => {
                if (historyError instanceof Error) {
                  const error = historyError as any
                  // Check for network error
                  if (error.message?.includes('Network') || error.code === 'ERR_NETWORK' || !error.response) {
                    return 'Lỗi kết nối. Vui lòng kiểm tra backend đang chạy.'
                  }
                  // Check for authentication error
                  if (error.response?.status === 401) {
                    return 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.'
                  }
                  // Check for server error
                  if (error.response?.status >= 500) {
                    return 'Lỗi server. Vui lòng thử lại sau.'
                  }
                  // Return API error message
                  return error.response?.data?.detail || error.message || 'Lỗi không xác định'
                }
                return 'Lỗi không xác định'
              })()}
            </p>
            <button
              onClick={() => refetchHistory()}
              className="mt-4 btn btn-primary btn-sm"
            >
              Thử lại
            </button>
          </div>
        )}
        
        {/* Empty state */}
        {!isLoadingHistory && !historyError && filteredHistory.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-gray-500">
            <Bot className="h-12 w-12 mb-4" />
            <p className="text-lg font-medium">
              {chatHistory && chatHistory.length > 0 
                ? `Không tìm thấy tin nhắn phù hợp với "${searchQuery}"` 
                : 'Chưa có tin nhắn nào'}
            </p>
            <p className="text-sm">
              {chatHistory && chatHistory.length > 0
                ? `Thử tìm kiếm với từ khóa khác. Tổng số tin nhắn: ${chatHistory.length}`
                : 'Bắt đầu cuộc trò chuyện bằng cách đặt câu hỏi bên dưới'}
            </p>
          </div>
        )}
        
        {/* Messages */}
        {!isLoadingHistory && !historyError && Array.isArray(filteredHistory) && filteredHistory.length > 0 && (
          <>
            {filteredHistory.map((message: ChatMessage, index: number) => {
              try {
                // Simple version first to test
                const safeFormatTime = (date: string) => {
                  try {
                    return formatRelativeTime(date)
                  } catch (e) {
                    return 'Unknown time'
                  }
                }
                
                const safeGetColor = (level?: string) => {
                  try {
                    return level ? getJLPTColor(level) : 'jlpt-n3'
                  } catch (e) {
                    return 'jlpt-n3'
                  }
                }
                
                return (
            <div key={`message-${message.id}`} className="space-y-3 mb-4 p-2" style={{ minHeight: '50px', border: '1px solid #ccc' }}>
              {/* User Question */}
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center">
                    <User className="h-4 w-4 text-white" />
                  </div>
                </div>
                <div className="flex-1">
                  <div className="bg-gray-100 rounded-lg p-3">
                    <p className="text-sm text-gray-900">{message.question || 'No question'}</p>
                  </div>
                  <p className="mt-1 text-xs text-gray-500">
                    {safeFormatTime(message.created_at)}
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
                    {message.answer === 'AI is thinking...' || message.answer === '...' ? (
                      <div className="flex items-center space-x-2 py-2">
                        <Loader2 className="h-4 w-4 animate-spin text-primary-600" />
                        <p className="text-sm text-gray-600 italic">AI đang suy nghĩ...</p>
                      </div>
                    ) : (
                      <p className="text-sm text-gray-900 japanese-text whitespace-pre-wrap">{message.answer || 'No answer'}</p>
                    )}
                    
                    {message.jlpt_level && (
                      <div className="mt-2">
                        <span className={`jlpt-badge ${safeGetColor(message.jlpt_level)}`}>
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
                    
                    {message.grammar_points && (
                      <div className="mt-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
                        <p className="text-xs font-semibold text-gray-800 mb-2 flex items-center">
                          <BookOpen className="h-3 w-3 mr-1" />
                          Grammar Points
                        </p>
                        <div className="space-y-2">
                          {Array.isArray(message.grammar_points) && message.grammar_points.length > 0 ? (
                            message.grammar_points.map((point, idx) => {
                              // Handle both object and string formats
                              if (typeof point === 'string') {
                                return (
                                  <div key={idx} className="text-xs text-gray-700 bg-white p-2 rounded border-l-2 border-primary-400">
                                    {point}
                                  </div>
                                )
                              }
                              
                              // Handle object format
                              const pattern = point?.pattern || point?.grammar || 'Unknown'
                              const explanation = point?.explanation || point?.description || ''
                              const example = point?.example || ''
                              
                              return (
                                <div key={idx} className="bg-white border border-gray-200 rounded p-2">
                                  <div className="flex items-start space-x-2">
                                    <div className="flex-shrink-0">
                                      <div className="h-5 w-5 rounded-full bg-primary-100 flex items-center justify-center">
                                        <span className="text-xs font-medium text-primary-600">
                                          {idx + 1}
                                        </span>
                                      </div>
                                    </div>
                                    <div className="flex-1 min-w-0">
                                      <h5 className="text-xs font-semibold text-gray-900 mb-0.5 japanese-text">
                                        {pattern}
                                      </h5>
                                      {explanation && (
                                        <p className="text-xs text-gray-600 mb-1">
                                          {explanation}
                                        </p>
                                      )}
                                      {example && (
                                        <div className="mt-1 p-1.5 bg-gray-50 rounded text-xs japanese-text text-gray-700 border-l-2 border-gray-300">
                                          {example}
                                        </div>
                                      )}
                                    </div>
                                  </div>
                                </div>
                              )
                            })
                          ) : typeof message.grammar_points === 'object' ? (
                            // Handle case where grammar_points is a single object instead of array
                            <div className="bg-white border border-gray-200 rounded p-2">
                              <div className="text-xs text-gray-700">
                                <span className="font-semibold">{message.grammar_points.pattern || 'Grammar Point'}:</span>{' '}
                                {message.grammar_points.explanation || JSON.stringify(message.grammar_points)}
                              </div>
                            </div>
                          ) : null}
                        </div>
                      </div>
                    )}
                    
                    {message.sources && Array.isArray(message.sources) && message.sources.length > 0 && (
                      <div className="mt-2">
                        <p className="text-xs font-medium text-gray-700 mb-1">Sources:</p>
                        <div className="space-y-1">
                          {message.sources.map((source, idx) => (
                            <div key={idx} className="text-xs text-blue-600">
                              {source?.title || 'Unknown source'}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                  <p className="text-xs text-gray-500">
                    {safeFormatTime(message.created_at)}
                  </p>
                </div>
              </div>
            </div>
                )
              } catch (error) {
                console.error('❌ Error rendering message:', message.id, error)
                return (
                  <div key={`error-${message.id}`} className="p-2 bg-red-100 border border-red-300 rounded">
                    Error rendering message {message.id}: {String(error)}
                  </div>
                )
              }
            })}
          </>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div className="mt-4">
        <form onSubmit={form.handleSubmit(handleSubmit)} className="flex space-x-2">
          <input
            {...form.register('message', { required: 'Vui lòng nhập câu hỏi' })}
            type="text"
            placeholder="Đặt câu hỏi về tiếng Nhật..."
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


