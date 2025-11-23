import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useMutation } from 'react-query'
import { BookOpen, Loader2, Languages, Star, Lightbulb } from 'lucide-react'
import { analysisAPI } from '../services/api'
import { getJLPTColor } from '../utils/helpers'
import toast from 'react-hot-toast'

interface GrammarFormData {
  text: string
  includeTranslation: boolean
}

interface GrammarAnalysis {
  text: string
  jlpt_level: string
  grammar_points: Array<{
    pattern: string
    explanation: string
    example: string
  }>
  translation?: string
  difficulty_score: number
  suggestions: string[]
}

export default function Grammar() {
  const [analysis, setAnalysis] = useState<GrammarAnalysis | null>(null)
  
  const form = useForm<GrammarFormData>({
    defaultValues: {
      includeTranslation: false,
    }
  })

  const analyzeMutation = useMutation(
    (data: { text: string; includeTranslation: boolean }) =>
      analysisAPI.analyzeGrammar(data.text, data.includeTranslation).then(res => res.data),
    {
      onSuccess: (data) => {
        setAnalysis(data)
        toast.success('Grammar analysis completed!')
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Failed to analyze grammar')
      },
    }
  )

  const handleSubmit = (data: GrammarFormData) => {
    if (!data.text.trim()) return
    analyzeMutation.mutate(data)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3">
        <BookOpen className="h-8 w-8 text-primary-600" />
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Grammar Analysis</h1>
          <p className="text-sm text-gray-600">
            Analyze Japanese text for grammar patterns, JLPT level, and difficulty
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">Analyze Japanese Text</h2>
            <p className="card-description">
              Enter Japanese text to get detailed grammar analysis
            </p>
          </div>
          <div className="card-content">
            <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-4">
              <div>
                <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
                  Japanese Text
                </label>
                <textarea
                  {...form.register('text', { required: 'Text is required' })}
                  rows={6}
                  className="input w-full resize-none"
                  placeholder="Enter Japanese text to analyze..."
                  disabled={analyzeMutation.isLoading}
                />
                {form.formState.errors.text && (
                  <p className="mt-1 text-sm text-red-600">
                    {form.formState.errors.text.message}
                  </p>
                )}
              </div>

              <div className="flex items-center">
                <input
                  {...form.register('includeTranslation')}
                  type="checkbox"
                  id="includeTranslation"
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="includeTranslation" className="ml-2 block text-sm text-gray-700">
                  Include Vietnamese translation
                </label>
              </div>

              <button
                type="submit"
                disabled={analyzeMutation.isLoading || !form.watch('text')?.trim()}
                className="btn btn-primary w-full"
              >
                {analyzeMutation.isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <BookOpen className="mr-2 h-4 w-4" />
                    Analyze Grammar
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Analysis Results */}
        <div className="space-y-6">
          {analysis ? (
            <>
              {/* Basic Info */}
              <div className="card">
                <div className="card-header">
                  <h3 className="card-title">Analysis Results</h3>
                </div>
                <div className="card-content space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">JLPT Level:</span>
                    <span className={`jlpt-badge ${getJLPTColor(analysis.jlpt_level)}`}>
                      {analysis.jlpt_level}
                    </span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">Difficulty Score:</span>
                    <div className="flex items-center space-x-2">
                      <div className="flex">
                        {[...Array(10)].map((_, i) => (
                          <Star
                            key={i}
                            className={`h-4 w-4 ${
                              i < Math.round(analysis.difficulty_score)
                                ? 'text-yellow-400 fill-current'
                                : 'text-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                      <span className="text-sm text-gray-600">
                        {analysis.difficulty_score.toFixed(1)}/10
                      </span>
                    </div>
                  </div>

                  {analysis.translation && (
                    <div className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                      <div className="flex items-center space-x-2 mb-2">
                        <Languages className="h-4 w-4 text-blue-600" />
                        <span className="text-sm font-medium text-blue-800">Translation</span>
                      </div>
                      <p className="text-sm text-blue-900">{analysis.translation}</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Grammar Points */}
              {analysis.grammar_points.length > 0 && (
                <div className="card">
                  <div className="card-header">
                    <h3 className="card-title">Grammar Points</h3>
                  </div>
                  <div className="card-content">
                    <div className="space-y-4">
                      {analysis.grammar_points.map((point, index) => (
                        <div key={index} className="border border-gray-200 rounded-lg p-4">
                          <div className="flex items-start space-x-3">
                            <div className="flex-shrink-0">
                              <div className="h-6 w-6 rounded-full bg-primary-100 flex items-center justify-center">
                                <span className="text-xs font-medium text-primary-600">
                                  {index + 1}
                                </span>
                              </div>
                            </div>
                            <div className="flex-1">
                              <h4 className="text-sm font-medium text-gray-900 mb-1">
                                {point.pattern}
                              </h4>
                              <p className="text-sm text-gray-600 mb-2">
                                {point.explanation}
                              </p>
                              {point.example && (
                                <div className="p-2 bg-gray-50 rounded text-sm japanese-text">
                                  {point.example}
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Learning Suggestions */}
              {analysis.suggestions.length > 0 && (
                <div className="card">
                  <div className="card-header">
                    <h3 className="card-title">Learning Suggestions</h3>
                  </div>
                  <div className="card-content">
                    <div className="space-y-2">
                      {analysis.suggestions.map((suggestion, index) => (
                        <div key={index} className="flex items-start space-x-2">
                          <Lightbulb className="h-4 w-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                          <p className="text-sm text-gray-700">{suggestion}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="card">
              <div className="card-content">
                <div className="text-center py-8 text-gray-500">
                  <BookOpen className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                  <p className="text-lg font-medium">No analysis yet</p>
                  <p className="text-sm">Enter Japanese text to get started</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}


