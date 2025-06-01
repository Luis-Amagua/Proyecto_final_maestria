import google.generativeai as genai
from typing import Optional, Dict, List
from .config import Config

class AIHandler:
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.chat_session = None
        self.last_used_chunks = []

    def start_session(self):
        """Inicia una nueva sesión de chat"""
        self.chat_session = self.model.start_chat(history=[])
        return self.chat_session

    def generate_analysis(self, text: str, is_long_document: bool = False) -> str:
        """Genera análisis del documento"""
        try:
            prompt = self._build_analysis_prompt(text, is_long_document)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error en generación de análisis: {str(e)}")

    def ask_question(self, question: str, context: str = None) -> str:
        """Responde preguntas sobre el documento"""
        try:
            if not self.chat_session:
                self.start_session()
            
            full_prompt = f"{context or ''}\n\nPregunta: {question}"
            response = self.chat_session.send_message(full_prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error en pregunta al modelo: {str(e)}")

    def _build_analysis_prompt(self, text: str, is_long_document: bool) -> str:
        """Construye el prompt según el tipo de documento"""
        base = "Como experto legal, analiza este documento identificando:"
        
        if is_long_document:
            return (
                f"{base}\n"
                "1. 2-3 problemas potenciales principales\n"
                "2. Recomendación clave\n"
                "3. Coherencia con normativas generales\n\n"
                "Contexto del documento:\n"
                f"{text[:3000]}\n\n"
                "Nota: Este es un resumen inicial para documentos largos."
            )
        
        return (
            f"{base}\n"
            "1. 3-5 aspectos clave\n"
            "2. Posibles riesgos\n"
            "3. Recomendaciones específicas\n"
            "4. Comparación con normativas relevantes\n\n"
            "Documento completo:\n"
            f"{text[:5000]}"
        )