from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.auth import get_current_active_user
from ..models.database import User
from ..models.schemas import (
    GrammarAnalysisRequest,
    GrammarAnalysisResponse,
    TranslationRequest,
    TranslationResponse,
    ErrorResponse
)
from ..services.llm_service import japanese_service

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/grammar", response_model=GrammarAnalysisResponse)
async def analyze_grammar(
    request: GrammarAnalysisRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Analyze Japanese grammar in the given text."""
    
    try:
        # Perform grammar analysis
        analysis_result = await japanese_service.analyze_grammar(request.text)
        
        # Generate translation if requested
        translation = None
        if request.include_translation:
            translation_result = await japanese_service.translate_text(
                text=request.text,
                source_lang="ja",
                target_lang="vi"
            )
            translation = translation_result["translated_text"]
        
        # Generate learning suggestions based on analysis
        suggestions = await japanese_service.generate_learning_suggestions(
            user_level=current_user.current_jlpt_level,
            weak_areas=[point.get("pattern", "") for point in analysis_result.get("grammar_points", [])]
        )
        
        return GrammarAnalysisResponse(
            text=request.text,
            jlpt_level=analysis_result.get("jlpt_level", "N3"),
            grammar_points=analysis_result.get("grammar_points", []),
            translation=translation,
            difficulty_score=analysis_result.get("difficulty_score", 5.0),
            suggestions=suggestions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing grammar: {str(e)}"
        )

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(
    request: TranslationRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Translate text between Japanese and Vietnamese."""
    
    try:
        # Validate language codes
        valid_langs = ["ja", "vi"]
        if request.source_lang not in valid_langs or request.target_lang not in valid_langs:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid language code. Use 'ja' for Japanese or 'vi' for Vietnamese."
            )
        
        if request.source_lang == request.target_lang:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source and target languages must be different."
            )
        
        # Perform translation
        translation_result = await japanese_service.translate_text(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        return TranslationResponse(
            original_text=translation_result["original_text"],
            translated_text=translation_result["translated_text"],
            source_lang=translation_result["source_lang"],
            target_lang=translation_result["target_lang"],
            confidence=translation_result["confidence"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error translating text: {str(e)}"
        )

@router.post("/jlpt-level", response_model=dict)
async def predict_jlpt_level(
    text: str,
    current_user: User = Depends(get_current_active_user)
):
    """Predict JLPT level of Japanese text."""
    
    try:
        jlpt_level = await japanese_service.predict_jlpt_level(text)
        
        return {
            "text": text,
            "predicted_jlpt_level": jlpt_level,
            "user_current_level": current_user.current_jlpt_level,
            "is_appropriate": jlpt_level == current_user.current_jlpt_level
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error predicting JLPT level: {str(e)}"
        )

