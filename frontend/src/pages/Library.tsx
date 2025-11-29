import { useState } from 'react'
import { useQuery, useQueryClient } from 'react-query'
import { useForm } from 'react-hook-form'
import { 
  Library as LibraryIcon, 
  Search, 
  Filter, 
  BookOpen, 
  Tag, 
  Calendar,
  ExternalLink,
  Loader2,
  Plus,
  X
} from 'lucide-react'
import { libraryAPI } from '../services/api'
import { getJLPTColor, formatDate } from '../utils/helpers'
import LoadingSpinner from '../components/LoadingSpinner'

interface Document {
  id: number
  title: string
  content: string
  document_type: string
  jlpt_level?: string
  tags: string[]
  source_url?: string
  created_at: string
}

interface SearchFormData {
  query: string
  document_type: string
  jlpt_level: string
}

interface DocumentFormData {
  title: string
  content: string
  document_type: string
  jlpt_level: string
  tags: string
  source_url: string
}

export default function Library() {
  const queryClient = useQueryClient()
  const [searchResults, setSearchResults] = useState<Document[]>([])
  const [isSearching, setIsSearching] = useState(false)
  const [showAddForm, setShowAddForm] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  const searchForm = useForm<SearchFormData>({
    defaultValues: {
      document_type: '',
      jlpt_level: '',
    }
  })

  const documentForm = useForm<DocumentFormData>({
    defaultValues: {
      title: '',
      content: '',
      document_type: '',
      jlpt_level: '',
      tags: '',
      source_url: '',
    }
  })

  const { data: documents, isLoading: isLoadingDocuments } = useQuery(
    ['documents'],
    () => libraryAPI.getDocuments().then(res => res.data),
    {
      refetchOnWindowFocus: false,
    }
  )

  const { data: categories } = useQuery(
    ['categories'],
    () => libraryAPI.getCategories().then(res => res.data),
    {
      refetchOnWindowFocus: false,
    }
  )

  const { data: stats } = useQuery(
    ['libraryStats'],
    () => libraryAPI.getStats().then(res => res.data),
    {
      refetchOnWindowFocus: false,
    }
  )

  const handleSearch = async (data: SearchFormData) => {
    if (!data.query.trim()) return
    
    setIsSearching(true)
    try {
      const response = await libraryAPI.searchDocuments(
        data.query,
        data.document_type || undefined,
        data.jlpt_level || undefined
      )
      setSearchResults(response.data.documents)
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setIsSearching(false)
    }
  }

  const clearSearch = () => {
    setSearchResults([])
    searchForm.reset()
  }

  const handleAddDocument = async (data: DocumentFormData) => {
    setIsSubmitting(true)
    try {
      const tagsArray = data.tags ? data.tags.split(',').map(t => t.trim()).filter(t => t) : []
      
      await libraryAPI.createDocument({
        title: data.title,
        content: data.content,
        document_type: data.document_type,
        jlpt_level: data.jlpt_level || undefined,
        tags: tagsArray,
        source_url: data.source_url || undefined,
      })
      
      // Refresh documents list and stats
      queryClient.invalidateQueries(['documents'])
      queryClient.invalidateQueries(['libraryStats'])
      queryClient.invalidateQueries(['categories'])
      
      // Reset form and close
      documentForm.reset()
      setShowAddForm(false)
      
      // Show success message
      alert('Document added successfully!')
    } catch (error: any) {
      console.error('Failed to create document:', error)
      const errorMessage = error.response?.data?.detail || 'Failed to create document. Please try again.'
      alert(errorMessage)
    } finally {
      setIsSubmitting(false)
    }
  }

  const displayDocuments = searchResults.length > 0 ? searchResults : documents || []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3">
        <LibraryIcon className="h-8 w-8 text-primary-600" />
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Learning Library</h1>
          <p className="text-sm text-gray-600">
            Browse and search Japanese learning materials
          </p>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="card">
            <div className="card-content">
              <div className="flex items-center">
                <BookOpen className="h-8 w-8 text-blue-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">Total Documents</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_documents}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="card-content">
              <div className="flex items-center">
                <Tag className="h-8 w-8 text-green-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">Document Types</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {Object.keys(stats.documents_by_type).length}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="card-content">
              <div className="flex items-center">
                <Calendar className="h-8 w-8 text-purple-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">JLPT Levels</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {Object.keys(stats.documents_by_jlpt).length}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="card">
            <div className="card-content">
              <div className="flex items-center">
                <Search className="h-8 w-8 text-orange-600" />
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">Vector Chunks</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stats.vector_db_stats?.total_documents || 0}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Add Document Button */}
      <div className="flex justify-end">
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="btn btn-primary"
        >
          <Plus className="mr-2 h-4 w-4" />
          Add New Document
        </button>
      </div>

      {/* Add Document Form */}
      {showAddForm && (
        <div className="card">
          <div className="card-header">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="card-title">Add New Document</h2>
                <p className="card-description">
                  Add a new learning material to the library
                </p>
              </div>
              <button
                onClick={() => {
                  setShowAddForm(false)
                  documentForm.reset()
                }}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          </div>
          <div className="card-content">
            <form onSubmit={documentForm.handleSubmit(handleAddDocument)} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="md:col-span-2">
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                    Title <span className="text-red-500">*</span>
                  </label>
                  <input
                    {...documentForm.register('title', { required: 'Title is required' })}
                    type="text"
                    className="input w-full"
                    placeholder="e.g., Basic Greetings - N5"
                  />
                  {documentForm.formState.errors.title && (
                    <p className="text-red-500 text-sm mt-1">{documentForm.formState.errors.title.message}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="document_type" className="block text-sm font-medium text-gray-700 mb-2">
                    Document Type <span className="text-red-500">*</span>
                  </label>
                  <select
                    {...documentForm.register('document_type', { required: 'Document type is required' })}
                    className="input w-full"
                  >
                    <option value="">Select type...</option>
                    <option value="vocabulary">Vocabulary</option>
                    <option value="grammar">Grammar</option>
                    <option value="lesson">Lesson</option>
                    <option value="culture">Culture</option>
                    <option value="example">Example</option>
                  </select>
                  {documentForm.formState.errors.document_type && (
                    <p className="text-red-500 text-sm mt-1">{documentForm.formState.errors.document_type.message}</p>
                  )}
                </div>

                <div>
                  <label htmlFor="jlpt_level" className="block text-sm font-medium text-gray-700 mb-2">
                    JLPT Level
                  </label>
                  <select
                    {...documentForm.register('jlpt_level')}
                    className="input w-full"
                  >
                    <option value="">Select level...</option>
                    <option value="N5">N5</option>
                    <option value="N4">N4</option>
                    <option value="N3">N3</option>
                    <option value="N2">N2</option>
                    <option value="N1">N1</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-2">
                    Tags (comma-separated)
                  </label>
                  <input
                    {...documentForm.register('tags')}
                    type="text"
                    className="input w-full"
                    placeholder="e.g., greetings, basic, polite"
                  />
                  <p className="text-xs text-gray-500 mt-1">Separate multiple tags with commas</p>
                </div>

                <div>
                  <label htmlFor="source_url" className="block text-sm font-medium text-gray-700 mb-2">
                    Source URL
                  </label>
                  <input
                    {...documentForm.register('source_url')}
                    type="url"
                    className="input w-full"
                    placeholder="https://example.com/..."
                  />
                </div>

                <div className="md:col-span-2">
                  <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
                    Content <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    {...documentForm.register('content', { required: 'Content is required' })}
                    rows={8}
                    className="input w-full"
                    placeholder="Enter the document content here..."
                  />
                  {documentForm.formState.errors.content && (
                    <p className="text-red-500 text-sm mt-1">{documentForm.formState.errors.content.message}</p>
                  )}
                </div>
              </div>

              <div className="flex space-x-2">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn btn-primary"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Adding...
                    </>
                  ) : (
                    <>
                      <Plus className="mr-2 h-4 w-4" />
                      Add Document
                    </>
                  )}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAddForm(false)
                    documentForm.reset()
                  }}
                  className="btn btn-outline"
                  disabled={isSubmitting}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Search Documents</h2>
          <p className="card-description">
            Find specific learning materials using semantic search
          </p>
        </div>
        <div className="card-content">
          <form onSubmit={searchForm.handleSubmit(handleSearch)} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
                  Search Query
                </label>
                <input
                  {...searchForm.register('query', { required: 'Search query is required' })}
                  type="text"
                  className="input w-full"
                  placeholder="Search for topics, grammar, vocabulary..."
                />
              </div>
              
              <div>
                <label htmlFor="document_type" className="block text-sm font-medium text-gray-700 mb-2">
                  Document Type
                </label>
                <select
                  {...searchForm.register('document_type')}
                  className="input w-full"
                >
                  <option value="">All Types</option>
                  {categories?.document_types.map((type: string) => (
                    <option key={type} value={type}>
                      {type.charAt(0).toUpperCase() + type.slice(1)}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label htmlFor="jlpt_level" className="block text-sm font-medium text-gray-700 mb-2">
                  JLPT Level
                </label>
                <select
                  {...searchForm.register('jlpt_level')}
                  className="input w-full"
                >
                  <option value="">All Levels</option>
                  {categories?.jlpt_levels_ordered.map((level: string) => (
                    <option key={level} value={level}>
                      {level}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="flex space-x-2">
              <button
                type="submit"
                disabled={isSearching || !searchForm.watch('query')?.trim()}
                className="btn btn-primary"
              >
                {isSearching ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="mr-2 h-4 w-4" />
                    Search
                  </>
                )}
              </button>
              
              {searchResults.length > 0 && (
                <button
                  type="button"
                  onClick={clearSearch}
                  className="btn btn-outline"
                >
                  Clear Search
                </button>
              )}
            </div>
          </form>
        </div>
      </div>

      {/* Documents List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">
            {searchResults.length > 0 ? 'Search Results' : 'All Documents'}
          </h2>
          <span className="text-sm text-gray-500">
            {displayDocuments.length} document{displayDocuments.length !== 1 ? 's' : ''}
          </span>
        </div>

        {isLoadingDocuments ? (
          <div className="flex justify-center py-8">
            <LoadingSpinner size="lg" />
          </div>
        ) : displayDocuments.length === 0 ? (
          <div className="card">
            <div className="card-content">
              <div className="text-center py-8 text-gray-500">
                <LibraryIcon className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <p className="text-lg font-medium">No documents found</p>
                <p className="text-sm">
                  {searchResults.length > 0 
                    ? 'Try adjusting your search criteria'
                    : 'No documents available yet'
                  }
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {displayDocuments.map((document: Document) => (
              <div key={document.id} className="card hover:shadow-lg transition-shadow">
                <div className="card-header">
                  <div className="flex items-start justify-between">
                    <h3 className="card-title text-lg">{document.title}</h3>
                    {document.source_url && (
                      <a
                        href={document.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-400 hover:text-gray-600"
                      >
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    )}
                  </div>
                  <p className="card-description">
                    {document.document_type.charAt(0).toUpperCase() + document.document_type.slice(1)}
                  </p>
                </div>
                
                <div className="card-content">
                  <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                    {document.content.substring(0, 150)}...
                  </p>
                  
                  <div className="space-y-2">
                    {document.jlpt_level && (
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-medium text-gray-500">Level:</span>
                        <span className={`jlpt-badge ${getJLPTColor(document.jlpt_level)}`}>
                          {document.jlpt_level}
                        </span>
                      </div>
                    )}
                    
                    <div className="flex items-center space-x-2">
                      <Calendar className="h-3 w-3 text-gray-400" />
                      <span className="text-xs text-gray-500">
                        {formatDate(document.created_at)}
                      </span>
                    </div>
                    
                    {document.tags.length > 0 && (
                      <div className="flex flex-wrap gap-1">
                        {document.tags.slice(0, 3).map((tag, index) => (
                          <span
                            key={index}
                            className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
                          >
                            {tag}
                          </span>
                        ))}
                        {document.tags.length > 3 && (
                          <span className="text-xs text-gray-500">
                            +{document.tags.length - 3} more
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}


