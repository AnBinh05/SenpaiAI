from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.database import User, Document
from ..models.schemas import (
    Document as DocumentSchema,
    DocumentCreate,
    DocumentUpdate,
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
        seen_ids = set()  # Avoid duplicates
        
        for result in search_results:
            # Try to get document ID from metadata first (new format)
            doc_id = result["metadata"].get("document_id")
            if doc_id:
                try:
                    doc_id_int = int(doc_id)
                    if doc_id_int not in seen_ids:
                        document_ids.append(doc_id_int)
                        seen_ids.add(doc_id_int)
                    continue
                except (ValueError, TypeError):
                    pass
            
            # Fallback: Extract from ChromaDB doc_id (format: "document_id_chunk_index")
            doc_id_str = result.get("doc_id", "")
            if doc_id_str:
                try:
                    doc_id_int = int(doc_id_str.split("_")[0])
                    if doc_id_int not in seen_ids:
                        document_ids.append(doc_id_int)
                        seen_ids.add(doc_id_int)
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

@router.post("/documents", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
async def create_document(
    document_data: DocumentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new document."""
    
    try:
        # Create document in database
        new_document = Document(
            title=document_data.title,
            content=document_data.content,
            document_type=document_data.document_type,
            jlpt_level=document_data.jlpt_level,
            tags=document_data.tags,
            source_url=document_data.source_url
        )
        
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        
        # Add to ChromaDB vector store
        try:
            doc_data = [{
                "id": str(new_document.id),
                "title": new_document.title,
                "content": new_document.content,
                "document_type": new_document.document_type,
                "jlpt_level": new_document.jlpt_level or "",
                "tags": new_document.tags,
                "source_url": new_document.source_url or ""
            }]
            chroma_service.add_documents(doc_data)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Warning: Failed to add document to vector store: {e}")
        
        return new_document
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating document: {str(e)}"
        )

@router.put("/documents/{document_id}", response_model=DocumentSchema)
async def update_document(
    document_id: int,
    document_data: DocumentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an existing document."""
    
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    try:
        # Update fields
        if document_data.title is not None:
            document.title = document_data.title
        if document_data.content is not None:
            document.content = document_data.content
        if document_data.document_type is not None:
            document.document_type = document_data.document_type
        if document_data.jlpt_level is not None:
            document.jlpt_level = document_data.jlpt_level
        if document_data.tags is not None:
            document.tags = document_data.tags
        if document_data.source_url is not None:
            document.source_url = document_data.source_url
        
        db.commit()
        db.refresh(document)
        
        # Update ChromaDB (delete old and add new)
        try:
            chroma_service.delete_document(str(document_id))
            doc_data = [{
                "id": str(document.id),
                "title": document.title,
                "content": document.content,
                "document_type": document.document_type,
                "jlpt_level": document.jlpt_level or "",
                "tags": document.tags,
                "source_url": document.source_url or ""
            }]
            chroma_service.add_documents(doc_data)
        except Exception as e:
            print(f"Warning: Failed to update document in vector store: {e}")
        
        return document
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating document: {str(e)}"
        )

@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    try:
        # Delete from ChromaDB first
        try:
            chroma_service.delete_document(str(document_id))
        except Exception as e:
            print(f"Warning: Failed to delete document from vector store: {e}")
        
        # Delete from database
        db.delete(document)
        db.commit()
        
        return None
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting document: {str(e)}"
        )

@router.get("/stats")
async def get_library_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get library statistics."""
    
    try:
        # Count documents by type
        from sqlalchemy import func as sql_func  # Ensure func is imported
        doc_type_counts = db.query(
            Document.document_type,
            sql_func.count(Document.id)
        ).group_by(Document.document_type).all()
        
        # Count documents by JLPT level
        jlpt_counts = db.query(
            Document.jlpt_level,
            sql_func.count(Document.id)
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting library stats: {str(e)}"
        )


