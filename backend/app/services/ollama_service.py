from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict, List, Any, Optional
import time
import json
import re
import ollama
from ..core.config import settings

class OllamaJapaneseLearningService:
    def __init__(self):
        # Initialize Ollama LLM
        self.llm = OllamaLLM(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0.7,
            num_predict=1000,
        )
        
        # Initialize Ollama embeddings (using a smaller model for embeddings)
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",  # Lightweight embedding model
            base_url=settings.ollama_base_url
        )
        
        # Initialize prompts
        self._setup_prompts()

    def _setup_prompts(self):
        """Setup all the prompt templates."""
        
        # Chat prompt for general Q&A
        self.chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are SenpaiAI, a helpful Japanese learning assistant. 
            You provide accurate, educational responses about Japanese language, culture, and grammar.
            Always include relevant examples and explanations suitable for the user's JLPT level.
            If asked about grammar, provide detailed explanations with usage patterns.
            If asked for translations, provide both literal and natural translations.
            Use polite, encouraging language and include cultural context when relevant.
            Respond in a helpful and educational manner."""),
            HumanMessage(content="{question}")
        ])
        
        # Grammar analysis prompt
        self.grammar_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a Japanese grammar expert. Analyze the given Japanese text and provide:
            1. JLPT level assessment (N5-N1)
            2. Grammar points with explanations
            3. Difficulty score (0-10)
            4. Learning suggestions
            
            Format your response as JSON with these fields:
            - jlpt_level: string
            - grammar_points: array of objects with 'pattern', 'explanation', 'example'
            - difficulty_score: number
            - suggestions: array of strings"""),
            HumanMessage(content="Analyze this Japanese text: {text}")
        ])
        
        # Translation prompt
        self.translation_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a professional Japanese-Vietnamese translator.
            Provide accurate, natural translations while preserving the original meaning and tone.
            For Japanese to Vietnamese: Provide both literal and natural translations.
            For Vietnamese to Japanese: Provide natural Japanese that sounds native.
            Include pronunciation guides (romaji) for Japanese text when helpful."""),
            HumanMessage(content="Translate this {source_lang} text to {target_lang}: {text}")
        ])
        
        # JLPT level prediction prompt
        self.jlpt_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a JLPT level assessment expert. 
            Analyze Japanese text and determine the appropriate JLPT level (N5, N4, N3, N2, N1).
            Consider vocabulary difficulty, grammar complexity, and kanji usage.
            Respond with just the JLPT level (e.g., "N3")."""),
            HumanMessage(content="What JLPT level is this text: {text}")
        ])

    async def chat_response(
        self, 
        question: str, 
        context: Optional[str] = None,
        jlpt_level: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a chat response with RAG context."""
        start_time = time.time()
        
        try:
            # Prepare the question with context
            if context:
                enhanced_question = f"Context: {context}\n\nQuestion: {question}"
            else:
                enhanced_question = question
            
            # Add JLPT level context if provided
            if jlpt_level:
                enhanced_question = f"User's JLPT level: {jlpt_level}\n\n{enhanced_question}"
            
            # Generate response using Ollama
            response = self.llm.invoke(enhanced_question)
            
            answer = response.strip()
            
            # Predict JLPT level of the response
            jlpt_prediction = await self.predict_jlpt_level(answer)
            
            response_time = time.time() - start_time
            
            return {
                "answer": answer,
                "jlpt_level": jlpt_prediction,
                "response_time": response_time
            }
            
        except Exception as e:
            return {
                "answer": f"I apologize, but I encountered an error: {str(e)}",
                "jlpt_level": None,
                "response_time": time.time() - start_time
            }

    async def analyze_grammar(self, text: str) -> Dict[str, Any]:
        """Analyze Japanese grammar in the given text."""
        try:
            prompt = f"Analyze this Japanese text: {text}"
            response = self.llm.invoke(prompt)
            
            # Try to parse JSON response
            try:
                # Extract JSON from response if it's wrapped in text
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    result = json.loads(response)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "jlpt_level": "N3",
                    "grammar_points": [{"pattern": "Unknown", "explanation": response, "example": ""}],
                    "difficulty_score": 5.0,
                    "suggestions": ["Review basic grammar patterns"]
                }
            
            return result
            
        except Exception as e:
            return {
                "jlpt_level": "N3",
                "grammar_points": [],
                "difficulty_score": 5.0,
                "suggestions": [f"Error in analysis: {str(e)}"]
            }

    async def translate_text(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str
    ) -> Dict[str, Any]:
        """Translate text between Japanese and Vietnamese."""
        try:
            prompt = f"Translate this {source_lang} text to {target_lang}: {text}"
            response = self.llm.invoke(prompt)
            
            translated_text = response.strip()
            
            return {
                "original_text": text,
                "translated_text": translated_text,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "confidence": 0.9  # Placeholder confidence score
            }
            
        except Exception as e:
            return {
                "original_text": text,
                "translated_text": f"Translation error: {str(e)}",
                "source_lang": source_lang,
                "target_lang": target_lang,
                "confidence": 0.0
            }

    async def predict_jlpt_level(self, text: str) -> str:
        """Predict the JLPT level of Japanese text."""
        try:
            prompt = f"What JLPT level is this text: {text}"
            response = self.llm.invoke(prompt)
            
            level = response.strip()
            
            # Validate JLPT level format
            if re.match(r'^N[1-5]$', level):
                return level
            else:
                return "N3"  # Default fallback
                
        except Exception as e:
            return "N3"  # Default fallback

    async def generate_learning_suggestions(
        self, 
        user_level: str, 
        weak_areas: List[str]
    ) -> List[str]:
        """Generate personalized learning suggestions."""
        try:
            prompt = f"""Based on the user's JLPT level ({user_level}) and weak areas ({', '.join(weak_areas)}), 
            provide 5 specific learning suggestions. Focus on practical, actionable advice."""
            
            response = self.llm.invoke(prompt)
            
            # Split into individual suggestions
            suggestions = [s.strip() for s in response.split('\n') if s.strip()]
            return suggestions[:5]  # Limit to 5 suggestions
            
        except Exception as e:
            return [f"Error generating suggestions: {str(e)}"]

    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = ollama.list()
            return True
        except Exception:
            return False

    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models."""
        try:
            response = ollama.list()
            return [model['name'] for model in response['models']]
        except Exception:
            return []

# Global instance
ollama_service = OllamaJapaneseLearningService()

