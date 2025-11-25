from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import time
import json

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
    print(f"📨 New chat message from user {current_user.id}: '{message.message[:50]}...'")
    
    try:
        start_time = time.time()
        
        # Disable RAG completely for speed - only use for very specific keywords
        # RAG is too slow for 5s target response time
        use_rag = False  # Disabled for speed
        context = None
        
        # Only use RAG for very specific grammar explanations (optional, slower)
        if message.context and "grammar" in message.context.lower() and len(message.message.split()) > 5:
            try:
                context = chroma_service.get_relevant_context(
                    message.message, 
                    message.jlpt_level or current_user.current_jlpt_level
                )
                if context and len(context.strip()) >= 50:
                    use_rag = True
                else:
                    context = None
            except Exception as e:
                print(f"RAG error (continuing without context): {e}")
                context = None
        
        # Generate AI response
        print(f"🚀 Starting AI response generation...")
        try:
            response_data = await japanese_service.chat_response(
                question=message.message,
                context=context,
                jlpt_level=message.jlpt_level or current_user.current_jlpt_level
            )
            
            if not response_data or "answer" not in response_data:
                raise Exception("Invalid response from AI service")
                
            print(f"✅ AI response generated successfully")
        except Exception as e:
            print(f"❌ Error generating AI response: {e}")
            # Create a fallback response
            response_data = {
                "answer": f"Xin lỗi, không thể tạo phản hồi: {str(e)}",
                "jlpt_level": message.jlpt_level or current_user.current_jlpt_level or "N5",
                "response_time": time.time() - start_time
            }
        
        # Only extract grammar points if explicitly requested (skip for speed)
        grammar_points = None
        if message.context and ("grammar" in message.context.lower() or "ngữ pháp" in message.context.lower()):
            if any(ord(char) > 127 for char in response_data["answer"]):  # Contains non-ASCII (likely Japanese)
                try:
                    grammar_analysis = await japanese_service.analyze_grammar(response_data["answer"])
                    raw_grammar_points = grammar_analysis.get("grammar_points", [])
                    # Ensure grammar_points is a list of dicts
                    if isinstance(raw_grammar_points, list):
                        grammar_points = [
                            item if isinstance(item, dict) else {"pattern": "Unknown", "explanation": str(item), "example": ""}
                            for item in raw_grammar_points
                        ]
                    elif isinstance(raw_grammar_points, dict):
                        grammar_points = [raw_grammar_points]
                    else:
                        grammar_points = None
                except Exception as e:
                    print(f"Grammar analysis error: {e}")
                    grammar_points = None
        
        # Generate translation only if explicitly requested
        translation = None
        if message.context and "translate" in message.context.lower():
            try:
                translation_result = await japanese_service.translate_text(
                    text=response_data["answer"],
                    source_lang="ja",
                    target_lang="vi"
                )
                translation = translation_result["translated_text"]
            except Exception as e:
                print(f"Translation error: {e}")
        
        # Prepare sources from RAG only if context was used
        sources = []
        if context and use_rag:
            try:
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
            except Exception as e:
                print(f"Source extraction error: {e}")
        
        # Save to chat history (always save, even if there was an error)
        try:
            chat_entry = ChatHistory(
                user_id=current_user.id,
                question=message.message,
                answer=response_data["answer"],
                jlpt_level=response_data.get("jlpt_level") or message.jlpt_level or current_user.current_jlpt_level or "N5",
                grammar_points=grammar_points,
                translation=translation,
                sources=sources
            )
            
            db.add(chat_entry)
            db.commit()
            db.refresh(chat_entry)
            print(f"✅ Chat message saved: ID={chat_entry.id}, Question='{message.message[:50]}...'")
        except Exception as e:
            print(f"❌ Error saving chat history: {e}")
            import traceback
            traceback.print_exc()
            # Continue even if save fails
        
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
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error processing chat message: {e}")
        print(f"📋 Traceback:\n{error_trace}")
        
        # Return a more user-friendly error message
        error_detail = str(e)
        if "Ollama" in error_detail or "model" in error_detail.lower():
            error_detail = "AI service is temporarily unavailable. Please try again later."
        elif "timeout" in error_detail.lower():
            error_detail = "Request timed out. Please try again with a shorter message."
        elif "connection" in error_detail.lower() or "refused" in error_detail.lower():
            error_detail = "Cannot connect to AI service. Please check if Ollama is running."
        
        # Try to save error message to chat history
        try:
            error_chat_entry = ChatHistory(
                user_id=current_user.id,
                question=message.message,
                answer=f"Xin lỗi, có lỗi xảy ra: {error_detail}. Vui lòng thử lại sau.",
                jlpt_level=message.jlpt_level or current_user.current_jlpt_level or "N5",
                grammar_points=None,
                translation=None,
                sources=None
            )
            db.add(error_chat_entry)
            db.commit()
            db.refresh(error_chat_entry)
            print(f"✅ Error message saved to chat history: ID={error_chat_entry.id}")
        except Exception as save_error:
            print(f"❌ Error saving error message to chat history: {save_error}")
        
        # Try to return a basic response instead of raising exception
        # This ensures the frontend always gets a response
        try:
            return ChatResponse(
                answer=f"Xin lỗi, có lỗi xảy ra: {error_detail}. Vui lòng thử lại sau.",
                jlpt_level=message.jlpt_level or current_user.current_jlpt_level or "N5",
                grammar_points=None,
                translation=None,
                sources=None,
                response_time=time.time() - start_time if 'start_time' in locals() else 0.0
            )
        except:
            # If even creating response fails, raise exception
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_detail
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
        import traceback
        chat_history = db.query(ChatHistory)\
            .filter(ChatHistory.user_id == current_user.id)\
            .order_by(ChatHistory.created_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        # Convert to list of dicts to help with serialization
        result = []
        for entry in chat_history:
            try:
                # Ensure JSON fields are properly handled
                # Handle grammar_points - might be string, list, or None
                grammar_points = None
                if entry.grammar_points is not None:
                    if isinstance(entry.grammar_points, str):
                        # Try to parse string as JSON
                        try:
                            parsed = json.loads(entry.grammar_points)
                            if isinstance(parsed, list):
                                grammar_points = parsed
                            elif isinstance(parsed, dict):
                                grammar_points = [parsed]
                            else:
                                grammar_points = None
                        except (json.JSONDecodeError, ValueError):
                            # If parsing fails, skip grammar_points
                            grammar_points = None
                    elif isinstance(entry.grammar_points, list):
                        # Validate that all items are dicts
                        grammar_points = []
                        for item in entry.grammar_points:
                            if isinstance(item, dict):
                                grammar_points.append(item)
                            elif isinstance(item, str):
                                # Try to parse string items
                                try:
                                    parsed = json.loads(item)
                                    if isinstance(parsed, dict):
                                        grammar_points.append(parsed)
                                except:
                                    pass
                    elif isinstance(entry.grammar_points, dict):
                        grammar_points = [entry.grammar_points]
                
                # Handle sources - might be string, list, or None
                sources = None
                if entry.sources is not None:
                    if isinstance(entry.sources, str):
                        try:
                            parsed = json.loads(entry.sources)
                            if isinstance(parsed, list):
                                sources = parsed
                            elif isinstance(parsed, dict):
                                sources = [parsed]
                        except (json.JSONDecodeError, ValueError):
                            sources = None
                    elif isinstance(entry.sources, list):
                        sources = entry.sources
                    elif isinstance(entry.sources, dict):
                        sources = [entry.sources]
                
                result.append(ChatHistorySchema(
                    id=entry.id,
                    question=entry.question,
                    answer=entry.answer,
                    jlpt_level=entry.jlpt_level,
                    grammar_points=grammar_points,
                    translation=entry.translation,
                    sources=sources,
                    created_at=entry.created_at
                ))
            except Exception as e:
                print(f"Error serializing chat entry {entry.id}: {e}")
                print(traceback.format_exc())
                # Skip problematic entries
                continue
        
        print(f"✅ Returning {len(result)} messages to frontend")
        return result
    except Exception as e:
        import traceback
        print(f"Error in get_chat_history: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching chat history: {str(e)}"
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


