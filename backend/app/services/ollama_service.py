from typing import Dict, List, Any, Optional
import time
import json
import re
import ollama
from ..core.config import settings

class OllamaJapaneseLearningService:
    def __init__(self):
        # Store Ollama configuration
        self.base_url = settings.ollama_base_url
        self.embedding_model = "nomic-embed-text"
        
        # Try to find and set a working model
        self.model = self._get_working_model(settings.ollama_model)
        
        # Initialize prompts
        self._setup_prompts()
    
    def _get_working_model(self, preferred_model: str) -> str:
        """Get a working model, fallback to available models if preferred not found."""
        try:
            available_models = self.get_available_models()
            
            # Check if preferred model is available
            if preferred_model in available_models:
                return preferred_model
            
            # Try common fallback models
            fallback_models = [
                "llama2",
                "llama2:7b",
                "llama2:13b",
                "mistral",
                "mistral:7b",
                "gemma:7b",
                "gemma:2b",
                "gemma3:270m",  # Smaller Gemma model
                "phi",
                "phi:2"
            ]
            
            for fallback in fallback_models:
                if fallback in available_models:
                    print(f"⚠️  Warning: Model '{preferred_model}' not found. Using fallback: '{fallback}'")
                    return fallback
            
            # If no models found, return preferred (will error later with better message)
            if not available_models:
                print(f"⚠️  Warning: No Ollama models found. Please install a model with: ollama pull {preferred_model}")
            else:
                print(f"⚠️  Warning: Model '{preferred_model}' not found. Available models: {', '.join(available_models)}")
                print(f"⚠️  Using first available model: {available_models[0]}")
                return available_models[0]
            
            return preferred_model
            
        except Exception as e:
            print(f"⚠️  Warning: Could not check available models: {e}")
            return preferred_model

    def _setup_prompts(self):
        """Setup all the prompt templates."""
        # Prompts are now built directly in methods
        pass
    
    def _call_ollama(self, prompt: str, system_prompt: str = None, timeout: int = 8) -> str:
        """Call Ollama API directly with optimized settings."""
        try:
            # Check if Ollama is running
            try:
                ollama.list()
            except Exception as check_error:
                raise Exception(f"Ollama is not running or not accessible. Please start Ollama first. Error: {str(check_error)}")
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Optimize for speed: limit tokens significantly for 5s response time
            options = {
                "temperature": 0.7,  # Balanced creativity
                "num_predict": 120,  # Very short responses for speed (target: 5s)
                "top_p": 0.9,
                "top_k": 20,  # Reduced for faster generation
            }
            
            print(f"🤖 Calling Ollama with model: {self.model}")
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options=options
            )
            
            if not response or 'message' not in response or 'content' not in response['message']:
                raise Exception("Invalid response from Ollama API")
            
            return response['message']['content']
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Ollama chat error: {error_msg}")
            
            # Fallback to generate if chat fails
            try:
                print(f"🔄 Trying fallback generate method...")
                response = ollama.generate(
                    model=self.model,
                    prompt=f"{system_prompt}\n\n{prompt}" if system_prompt else prompt,
                    options={
                        "temperature": 0.7,
                        "num_predict": 120,  # Very short for speed
                    }
                )
                if not response or 'response' not in response:
                    raise Exception("Invalid response from Ollama generate API")
                return response['response']
            except Exception as fallback_error:
                # More descriptive error message
                if "model" in error_msg.lower() or "not found" in error_msg.lower():
                    raise Exception(f"Model '{self.model}' not found. Please install it with: ollama pull {self.model}")
                elif "connection" in error_msg.lower() or "refused" in error_msg.lower():
                    raise Exception(f"Cannot connect to Ollama at {self.base_url}. Please make sure Ollama is running.")
                else:
                    raise Exception(f"Ollama API error: {str(e)}. Fallback also failed: {str(fallback_error)}")

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
            
            # Generate response using Ollama with optimized, shorter prompt for speed
            system_prompt = """Bạn là SenpaiAI, trợ lý học tiếng Nhật. 
            QUAN TRỌNG: Luôn trả lời bằng TIẾNG VIỆT, trừ khi người dùng yêu cầu cụ thể bằng ngôn ngữ khác.
            - Nếu câu hỏi bằng tiếng Việt → trả lời bằng tiếng Việt
            - Nếu câu hỏi bằng tiếng Nhật → giải thích bằng tiếng Việt, có thể kèm tiếng Nhật
            - Giữ câu trả lời ngắn gọn, dễ hiểu (1-3 câu)
            - Sử dụng ngôn ngữ thân thiện, khuyến khích học tập"""
            
            print(f"💬 Generating response for: '{question[:50]}...'")
            answer = self._call_ollama(enhanced_question, system_prompt).strip()
            
            if not answer or len(answer) == 0:
                raise Exception("Received empty response from Ollama")
            
            print(f"✅ Got response: '{answer[:50]}...'")
            
            # Skip JLPT prediction completely for speed - always use user's level
            jlpt_prediction = jlpt_level or "N3"  # Always use user's level, no prediction
            
            response_time = time.time() - start_time
            print(f"⏱️  Response time: {response_time:.2f}s")
            
            return {
                "answer": answer,
                "jlpt_level": jlpt_prediction,
                "response_time": response_time
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error in chat_response: {error_msg}")
            response_time = time.time() - start_time
            
            # Return error message that will be saved to chat history
            return {
                "answer": f"Xin lỗi, có lỗi xảy ra khi tạo phản hồi: {error_msg}",
                "jlpt_level": jlpt_level or "N3",
                "response_time": response_time
            }

    async def analyze_grammar(self, text: str) -> Dict[str, Any]:
        """Analyze Japanese grammar in the given text."""
        try:
            system_prompt = """You are a Japanese grammar expert. Analyze the given Japanese text and provide:
            1. JLPT level assessment (N5-N1)
            2. Grammar points with explanations
            3. Difficulty score (0-10)
            4. Learning suggestions
            
            Format your response as JSON with these fields:
            - jlpt_level: string
            - grammar_points: array of objects with 'pattern', 'explanation', 'example'
            - difficulty_score: number
            - suggestions: array of strings"""
            
            prompt = f"Analyze this Japanese text: {text}"
            response = self._call_ollama(prompt, system_prompt)
            
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
            system_prompt = """You are a professional Japanese-Vietnamese translator.
            Provide accurate, natural translations while preserving the original meaning and tone.
            For Japanese to Vietnamese: Provide both literal and natural translations.
            For Vietnamese to Japanese: Provide natural Japanese that sounds native.
            Include pronunciation guides (romaji) for Japanese text when helpful."""
            
            prompt = f"Translate this {source_lang} text to {target_lang}: {text}"
            response = self._call_ollama(prompt, system_prompt)
            
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
        """Predict the JLPT level of Japanese text (optimized for speed)."""
        try:
            # Use a simpler, faster prompt
            system_prompt = """Respond with only the JLPT level: N5, N4, N3, N2, or N1."""
            
            # Limit text length for faster processing
            text_sample = text[:200] if len(text) > 200 else text
            prompt = f"JLPT level of: {text_sample}"
            
            response = self._call_ollama(prompt, system_prompt)
            
            level = response.strip()
            
            # Extract JLPT level from response (handle various formats)
            match = re.search(r'N[1-5]', level)
            if match:
                return match.group()
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
            
            response = self._call_ollama(prompt)
            
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
            if 'models' in response and response['models']:
                return [model['name'] for model in response['models']]
            return []
        except Exception as e:
            print(f"Error getting available models: {e}")
            return []

# Global instance
ollama_service = OllamaJapaneseLearningService()




