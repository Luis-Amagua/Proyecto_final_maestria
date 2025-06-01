import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuración de archivos
    BASE_DIR = Path(__file__).resolve().parent.parent
    UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Configuración de AI
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    MODEL_NAME = 'gemini-1.5-flash-latest'
    
    # Configuración de procesamiento
    SHORT_DOC_PAGES = 10  # Límite para considerar documento corto
    CHUNK_SIZE = 2000     # Tamaño de chunks para RAG
    
    @classmethod
    def init_app(cls, app):
        app.config['UPLOAD_FOLDER'] = cls.UPLOAD_FOLDER
        app.config['MAX_CONTENT_LENGTH'] = cls.MAX_CONTENT_LENGTH
        # Crear directorio de uploads si no existe
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)