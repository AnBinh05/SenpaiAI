from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.database import User, Document
from ..models.schemas import (
    Document as DocumentSchema,
    DocumentSearchRequest,
    DocumentSearchResponse,
    ErrorResponse
)
from ..services.vector_db import chroma_service

router = APIRouter(prefix="/library", tags=["library"])

@router.get("/documents", response_model=List[DocumentSchema])
async def get_documents(
    document_type: Optional[str] = None,
    jlpt_level: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get documents with optional filtering."""
    
    query = db.query(Document)
    
    if document_type:
        query = query.filter(Document.document_type == document_type)
    
    if jlpt_level:
        query = query.filter(Document.jlpt_level == jlpt_level)
    
    documents = query.order_by(Document.created_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()
    
    return documents

@router.get("/documents/{document_id}", response_model=DocumentSchema)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific document by ID."""
    
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document

@router.post("/search", response_model=DocumentSearchResponse)
async def search_documents(
    request: DocumentSearchRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search documents using semantic similarity."""
    
    try:
        # Prepare filter for ChromaDB
        filter_dict = {}
        if request.document_type:
            filter_dict["document_type"] = request.document_type
        if request.jlpt_level:
            filter_dict["jlpt_level"] = request.jlpt_level
        
        # Search using ChromaDB
        search_results = chroma_service.search_documents(
            query=request.query,
            n_results=request.limit,
            filter_dict=filter_dict if filter_dict else None
        )
        
        # Get document IDs from search results
        document_ids = []
        for result in search_results:
            # Extract document ID from metadata
            title = result["metadata"].get("title", "")
            if title:
                try:
                    doc_id = int(title.split("_")[0])
                    document_ids.append(doc_id)
                except (ValueError, IndexError):
                    continue
        
        # Get full document objects
        documents = []
        if document_ids:
            documents = db.query(Document)\
                .filter(Document.id.in_(document_ids))\
                .all()
        
        return DocumentSearchResponse(
            documents=documents,
            total_count=len(documents),
            query=request.query
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching documents: {str(e)}"
        )

@router.get("/categories")
async def get_document_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get available document categories and JLPT levels."""
    
    # Get unique document types
    document_types = db.query(Document.document_type)\
        .distinct()\
        .all()
    
    # Get unique JLPT levels
    jlpt_levels = db.query(Document.jlpt_level)\
        .filter(Document.jlpt_level.isnot(None))\
        .distinct()\
        .all()
    
    return {
        "document_types": [dt[0] for dt in document_types],
        "jlpt_levels": [jl[0] for jl in jlpt_levels],
        "jlpt_levels_ordered": ["N5", "N4", "N3", "N2", "N1"]
    }

@router.get("/stats")
async def get_library_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get library statistics."""
    
    # Count documents by type
    doc_type_counts = db.query(
        Document.document_type,
        db.func.count(Document.id)
    ).group_by(Document.document_type).all()
    
    # Count documents by JLPT level
    jlpt_counts = db.query(
        Document.jlpt_level,
        db.func.count(Document.id)
    ).group_by(Document.jlpt_level).all()
    
    # Total document count
    total_docs = db.query(Document).count()
    
    # ChromaDB stats
    chroma_stats = chroma_service.get_collection_stats()
    
    return {
        "total_documents": total_docs,
        "documents_by_type": {dt: count for dt, count in doc_type_counts},
        "documents_by_jlpt": {jlpt: count for jlpt, count in jlpt_counts if jlpt},
        "vector_db_stats": chroma_stats
    }

