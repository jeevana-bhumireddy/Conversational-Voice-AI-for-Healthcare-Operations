import os
from gtts import gTTS
from pydub import AudioSegment
import json
import random
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetGenerator:
    def __init__(self, output_dir: str = "test_data"):
        """Initialize the dataset generator."""
        self.output_dir = output_dir
        self.sample_rate = 16000
        
        os.makedirs(output_dir, exist_ok=True)
        self.scenarios = {
            "appointment_scheduling": {
                "en": [
                    "I need to schedule a dental cleaning appointment for next week.",
                    "Can I book an appointment with Dr. Smith for a check-up?",
                    "I'd like to reschedule my appointment from tomorrow to next Monday.",
                    "What are your available slots for a physical examination?",
                    "I need to cancel my appointment scheduled for Friday."
                ],
                "es": [
                    "Necesito programar una cita para limpieza dental la próxima semana.",
                    "¿Puedo agendar una cita con el Dr. Smith para un chequeo?",
                    "Me gustaría reprogramar mi cita de mañana para el próximo lunes.",
                    "¿Cuáles son sus horarios disponibles para un examen físico?",
                    "Necesito cancelar mi cita programada para el viernes."
                ]
            },
            "insurance_coverage_inquiry": {
                "en": [
                    "Does my insurance cover dental implants?",
                    "I need to know if my plan covers physical therapy sessions.",
                    "What's my copay for specialist visits?",
                    "Is this medication covered under my current insurance?",
                    "Can you verify my insurance coverage for this procedure?"
                ],
                "es": [
                    "¿Mi seguro cubre implantes dentales?",
                    "Necesito saber si mi plan cubre sesiones de fisioterapia.",
                    "¿Cuál es mi copago para visitas al especialista?",
                    "¿Este medicamento está cubierto por mi seguro actual?",
                    "¿Puede verificar mi cobertura de seguro para este procedimiento?"
                ]
            },
            "prescription_refill": {
                "en": [
                    "I need a refill for my blood pressure medication.",
                    "Can you refill my prescription for antibiotics?",
                    "I'm running low on my diabetes medication, need a refill.",
                    "How do I request a refill for my maintenance medication?",
                    "My prescription is about to expire, can I get a refill?"
                ],
                "es": [
                    "Necesito un reabastecimiento de mi medicamento para la presión arterial.",
                    "¿Puede reabastecer mi receta de antibióticos?",
                    "Me estoy quedando sin mi medicamento para la diabetes, necesito un reabastecimiento.",
                    "¿Cómo solicito un reabastecimiento de mi medicamento de mantenimiento?",
                    "Mi receta está por vencer, ¿puedo obtener un reabastecimiento?"
                ]
            },
            "billing_inquiry": {
                "en": [
                    "I received a bill that seems incorrect, can you help?",
                    "What's the cost for a routine check-up?",
                    "Do you offer payment plans for medical procedures?",
                    "I need to understand my last medical bill.",
                    "Can you explain the charges for my recent visit?"
                ],
                "es": [
                    "Recibí una factura que parece incorrecta, ¿puede ayudarme?",
                    "¿Cuál es el costo de un chequeo de rutina?",
                    "¿Ofrecen planes de pago para procedimientos médicos?",
                    "Necesito entender mi última factura médica.",
                    "¿Puede explicar los cargos de mi visita reciente?"
                ]
            },
            "general_inquiry": {
                "en": [
                    "What are your office hours?",
                    "Do you accept walk-in patients?",
                    "What documents do I need to bring for my first visit?",
                    "How do I access my medical records online?",
                    "What's the best way to contact the doctor after hours?"
                ],
                "es": [
                    "¿Cuáles son sus horarios de atención?",
                    "¿Aceptan pacientes sin cita?",
                    "¿Qué documentos necesito traer para mi primera visita?",
                    "¿Cómo accedo a mis registros médicos en línea?",
                    "¿Cuál es la mejor manera de contactar al médico fuera de horario?"
                ]
            }
        }

    def generate_audio(self, text: str, language: str, filename: str) -> str:
        """
        Generate audio file from text using gTTS.
        
        Args:
            text (str): Text to convert to speech
            language (str): Language code (e.g., 'en', 'es')
            filename (str): Output filename
            
        Returns:
            str: Path to the generated audio file
        """
        try:
            tts = gTTS(text=text, lang=language, slow=False)
            
            output_path = os.path.join(self.output_dir, filename)
            tts.save(output_path)
            
            audio = AudioSegment.from_mp3(output_path)
            audio = audio.set_frame_rate(self.sample_rate)
            audio.export(output_path.replace('.mp3', '.wav'), format='wav')
            
            return output_path.replace('.mp3', '.wav')
            
        except Exception as e:
            logger.error(f"Error generating audio for {filename}: {str(e)}")
            raise

    def generate_dataset(self, samples_per_intent: int = 5) -> Dict:
        """
        Generate a complete dataset with audio files and metadata.
        
        Args:
            samples_per_intent (int): Number of samples to generate per intent
            
        Returns:
            Dict: Dataset metadata
        """
        dataset = {
            "metadata": {
                "total_samples": 0,
                "languages": ["en", "es"],
                "intents": list(self.scenarios.keys())
            },
            "samples": []
        }
        
        try:
            for intent, languages in self.scenarios.items():
                for lang, texts in languages.items():
                    selected_texts = random.sample(texts, min(samples_per_intent, len(texts)))
                    
                    for i, text in enumerate(selected_texts):
                        filename = f"{intent}_{lang}_{i+1}.wav"
                        audio_path = self.generate_audio(text, lang, filename)
                        
                        sample = {
                            "filename": filename,
                            "text": text,
                            "language": lang,
                            "intent": intent,
                            "path": audio_path
                        }
                        
                        dataset["samples"].append(sample)
                        dataset["metadata"]["total_samples"] += 1
                        
                        logger.info(f"Generated {filename}")
            
            metadata_path = os.path.join(self.output_dir, "dataset_metadata.json")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Dataset generation complete. Total samples: {dataset['metadata']['total_samples']}")
            return dataset
            
        except Exception as e:
            logger.error(f"Error generating dataset: {str(e)}")
            raise

if __name__ == "__main__":
    generator = DatasetGenerator()
    dataset = generator.generate_dataset(samples_per_intent=5)
    
    print(f"\nDataset generated successfully!")
    print(f"Total samples: {dataset['metadata']['total_samples']}")
    print(f"Output directory: {generator.output_dir}")
    print("\nYou can find the generated audio files and metadata in the test_data directory.") 