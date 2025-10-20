import os
import json
import whisper
from langdetect import detect
from openai import OpenAI
from typing import Dict, Any
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceAIAgent:
    def __init__(self):
        """Initialize the Voice AI Agent with necessary models and configurations."""
        # Check if API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")
            
        self.whisper_model = whisper.load_model("base")
        self.openai_client = OpenAI(api_key=api_key)
        
        self.language_map = {
            'en': 'English',
            'es': 'Spanish',
            'ca': 'Catalan',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese'
        }

        self.intent_keywords = {
            "appointment_scheduling": ["cita", "agendar", "horario", "disponible", "appointment", "schedule"],
            "insurance_coverage_inquiry": ["seguro", "cobertura", "cubre", "insurance", "coverage"],
            "prescription_refill": ["receta", "medicamento", "reposición", "prescription", "refill"],
            "billing_inquiry": ["factura", "pago", "costo", "billing", "payment", "cost"],
            "general_inquiry": ["información", "pregunta", "duda", "information", "question"]
        }

    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file and detect language.
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            Dict containing transcript and detected language
        """
        try:
            # Transcribe audio
            result = self.whisper_model.transcribe(audio_path)
            transcript = result["text"]
            
            # Detect language
            detected_lang = detect(transcript)
            language_name = self.language_map.get(detected_lang, detected_lang)
            
            return {
                "transcript": transcript,
                "language": language_name
            }
        except Exception as e:
            logger.error(f"Error in transcription: {str(e)}")
            raise

    def classify_intent(self, transcript: str) -> Dict[str, Any]:
        """
        Classify the intent of the transcript.
        
        Args:
            transcript (str): The transcribed text
            
        Returns:
            Dict containing intent and confidence score
        """
        try:
            prompt = f"""
            Analyze the following healthcare-related message and classify its intent.
            Choose from: appointment_scheduling, insurance_coverage_inquiry, prescription_refill, billing_inquiry, general_inquiry
            
            Message: {transcript}
            
            Return a JSON with 'intent' and 'confidence_score' (0-1).
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a healthcare intent classification expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"Error in intent classification: {str(e)}")
            raise

    def generate_response(self, transcript: str, intent: str, language: str) -> str:
        """
        Generate an appropriate response based on the intent and language.
        
        Args:
            transcript (str): The original transcript
            intent (str): The classified intent
            language (str): The detected language
            
        Returns:
            str: Generated response
        """
        try:
            prompt = f"""
            Generate a professional healthcare response in {language} for the following:
            
            Original message: {transcript}
            Intent: {intent}
            
            The response should be helpful, concise, and maintain patient privacy.
            Return ONLY the response text without any prefixes or additional formatting.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional healthcare assistant. Return only the response text without any prefixes or additional formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            response_text = response.choices[0].message.content.strip()
            if response_text.lower().startswith("response:"):
                response_text = response_text[9:].strip()
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error in response generation: {str(e)}")
            raise

    def process_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Process audio file end-to-end and return structured response.
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            Dict containing all processing results
        """
        try:
            transcription_result = self.transcribe_audio(audio_path)
            intent_result = self.classify_intent(transcription_result["transcript"])
            
            response = self.generate_response(
                transcription_result["transcript"],
                intent_result["intent"],
                transcription_result["language"]
            )
            
            return {
                "transcript": transcription_result["transcript"],
                "language": transcription_result["language"],
                "intent": intent_result["intent"],
                "response": response,
                "confidence_score": intent_result["confidence_score"]
            }
            
        except Exception as e:
            logger.error(f"Error in processing audio: {str(e)}")
