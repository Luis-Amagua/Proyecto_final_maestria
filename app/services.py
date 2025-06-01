from threading import Thread
from pathlib import Path
from typing import Union, List, Optional
from app.core.document_processor import DocumentProcessor
from app.core.ai_handler import AIHandler
from app.core.config import Config

class AnalysisService:
    def __init__(self):
        self.ai = AIHandler()
        self.processor = DocumentProcessor()
        self.current_analysis = None
        self.current_file = None
        self.is_long_document = False
        self.page_count = 0
        self.analysis_ready = False

    def process_document(self, filepath: Union[str, Path]):
        """Procesa el documento y prepara el análisis"""
        self.current_file = str(filepath)
        self.page_count = self.processor.get_page_count(filepath)
        self.is_long_document = self.page_count > Config.SHORT_DOC_PAGES
        
        # Ejecutar en segundo plano
        Thread(target=self._background_analysis, args=(filepath,)).start()

    def _background_analysis(self, filepath):
        """Ejecuta el análisis en segundo plano"""
        try:
            text = self.processor.extract_text(
                filepath,
                max_pages=None if not self.is_long_document else Config.SHORT_DOC_PAGES
            )
            
            self.current_analysis = self.ai.generate_analysis(
                text,
                is_long_document=self.is_long_document
            )
            self.analysis_ready = True
        except Exception as e:
            self.current_analysis = f"Error en análisis: {str(e)}"
            self.analysis_ready = True

    def get_context_for_question(self) -> str:
        """Prepara contexto para preguntas"""
        if not self.current_file:
            return "No hay documento cargado"
            
        try:
            text = self.processor.extract_text(
                self.current_file,
                max_pages=3  # Solo primeras páginas para contexto
            )
            return (
                f"Documento actual: {Path(self.current_file).name}\n"
                f"Páginas: {self.page_count}\n"
                f"Modo: {'RAG (documento largo)' if self.is_long_document else 'Completo'}\n"
                f"Texto relevante:\n{text[:2000]}"
            )
        except Exception:
            return f"Documento: {Path(self.current_file).name} (error extrayendo texto)"