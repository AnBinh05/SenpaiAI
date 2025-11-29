from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import time

from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.database import User, ChatHistory
from ..models.schemas import (
    ChatMessage, 
    ChatResponse, 
    ChatHistory as ChatHistorySchema,
    ErrorResponse
)
from ..services.llm_service import japanese_service
from ..services.vector_db import chroma_service

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Send a message and get AI response with RAG."""
    
    try:
        start_time = time.time()
        
        # Get relevant context using RAG
        context = chroma_service.get_relevant_context(
            message.message, 
            message.jlpt_level or current_user.current_jlpt_level
        )
        
        # Generate AI response
        response_data = await japanese_service.chat_response(
            question=message.message,
            context=context,
            jlpt_level=message.jlpt_level or current_user.current_jlpt_level
        )
        
        # Extract grammar points if the response contains Japanese
        grammar_points = None
        if any(ord(char) > 127 for char in response_data["answer"]):  # Contains non-ASCII (likely Japanese)
            grammar_analysis = await japanese_service.analyze_grammar(response_data["answer"])
            grammar_points = grammar_analysis.get("grammar_points", [])
        
        # Generate translation if requested
        translation = None
        if message.context and "translate" in message.context.lower():
            translation_result = await japanese_service.translate_text(
                text=response_data["answer"],
                source_lang="ja",
                target_lang="vi"
            )
            translation = translation_result["translated_text"]
        
        # Prepare sources from RAG
        sources = []
        if context:
            rag_results = chroma_service.search_documents(
                message.message, 
                n_results=3,
                filter_dict={"jlpt_level": message.jlpt_level or current_user.current_jlpt_level} if message.jlpt_level else None
            )
            sources = [
                {
                    "title": result["source"]["title"],
                    "url": result["source"]["source_url"],
                    "relevance": result["similarity_score"]
                }
                for result in rag_results
            ]
        
        # Save to chat history
        chat_entry = ChatHistory(
            user_id=current_user.id,
            question=message.message,
            answer=response_data["answer"],
            jlpt_level=response_data["jlpt_level"],
            grammar_points=grammar_points,
            translation=translation,
            sources=sources
        )
        
        db.add(chat_entry)
        db.commit()
        
        response_time = time.time() - start_time
        
        return ChatResponse(
            answer=response_data["answer"],
            jlpt_level=response_data["jlpt_level"],
            grammar_points=grammar_points,
            translation=translation,
            sources=sources,
            response_time=response_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )

@router.get("/history", response_model=List[ChatHistorySchema])
async def get_chat_history(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's chat history."""
    
    try:
        chat_history = db.query(ChatHistory)\
            .filter(ChatHistory.user_id == current_user.id)\
            .order_by(ChatHistory.created_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        # Convert sources relevance from float to string for validation
        result = []
        for chat in chat_history:
            chat_dict = {
                "id": chat.id,
                "question": chat.question,
                "answer": chat.answer,
                "jlpt_level": chat.jlpt_level,
                "grammar_points": chat.grammar_points,
                "translation": chat.translation,
                "created_at": chat.created_at,
            }
            
            # Convert sources if they exist
            if chat.sources:
                converted_sources = []
                for source in chat.sources:
                    if isinstance(source, dict):
                        converted_source = source.copy()
                        # Convert relevance from float to string if needed
                        if "relevance" in converted_source and isinstance(converted_source["relevance"], (int, float)):
                            converted_source["relevance"] = str(converted_source["relevance"])
                        converted_sources.append(converted_source)
                    else:
                        converted_sources.append(source)
                chat_dict["sources"] = converted_sources
            else:
                chat_dict["sources"] = None
            
            result.append(ChatHistorySchema(**chat_dict))
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving chat history: {str(e)}"
        )

@router.delete("/history/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_entry(
    chat_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a specific chat entry."""
    
    chat_entry = db.query(ChatHistory)\
        .filter(ChatHistory.id == chat_id)\
        .filter(ChatHistory.user_id == current_user.id)\
        .first()
    
    if not chat_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat entry not found"
        )
    
    db.delete(chat_entry)
    db.commit()
    
    return None

@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_chat_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear all chat history for current user."""
    
    db.query(ChatHistory)\
        .filter(ChatHistory.user_id == current_user.id)\
        .delete()
    
    db.commit()
    
    return None

@router.get("/search", response_model=List[ChatHistorySchema])
async def search_chat_history(
    query: str,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search through chat history."""
    
    # Simple text search in questions and answers
    chat_history = db.query(ChatHistory)\
        .filter(ChatHistory.user_id == current_user.id)\
        .filter(
            ChatHistory.question.ilike(f"%{query}%") |
            ChatHistory.answer.ilike(f"%{query}%")
        )\
        .order_by(ChatHistory.created_at.desc())\
        .limit(limit)\
        .all()
    
    return chat_history


