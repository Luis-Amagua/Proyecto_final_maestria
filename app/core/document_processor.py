import PyPDF2
from pathlib import Path
from typing import Union, List
from .config import Config

class DocumentProcessor:
    @staticmethod
    def extract_text(filepath: Union[str, Path], max_pages: int = None) -> str:
        """Extrae texto de PDF con control de páginas"""
        try:
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages = reader.pages[:max_pages] if max_pages else reader.pages
                return "\n".join(page.extract_text() or '' for page in pages)
        except Exception as e:
            raise RuntimeError(f"Error procesando PDF: {str(e)}")

    @staticmethod
    def get_page_count(filepath: Union[str, Path]) -> int:
        """Obtiene número de páginas rápidamente"""
        try:
            with open(filepath, 'rb') as f:
                return len(PyPDF2.PdfReader(f).pages)
        except Exception as e:
            raise RuntimeError(f"Error contando páginas: {str(e)}")

    @staticmethod
    def split_into_chunks(text: str, chunk_size: int = None) -> List[str]:
        """Divide texto en chunks preservando párrafos"""
        chunk_size = chunk_size or Config.CHUNK_SIZE
        chunks = []
        current_chunk = ""
        
        for paragraph in text.split('\n\n'):
            if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
                chunks.append(current_chunk)
                current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks