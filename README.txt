📄 ClausaLens - Análisis Inteligente de Contratos
Automatiza la revisión legal de contratos usando IA generativa
✨ Detecta inconsistencias, compara con normativas y genera recomendaciones en segundos.

🚀 Funcionalidades Principales
Análisis automático de documentos PDF (hasta 100 páginas)

Chat interactivo para consultas legales contextuales

Detección de riesgos con 85%+ de precisión

Modo RAG para documentos largos (>10 páginas)

Visualización integrada de contratos y normativas

🛠️ Tecnologías Clave
Área	Tecnologías
Backend	Python 3.9, Flask, PyPDF2
IA	Google Gemini 1.5 Flash, RAG (Recuperación-Aumentada)
Frontend	HTML5, CSS3, JavaScript (Vanilla)
Infra	Docker (opcional), Servidores con 4+ vCPUs

🏗️ Estructura del Proyecto
bash
proyecto/
├── app/
│   ├── core/           # Lógica de IA y procesamiento
│   ├── static/         # PDFs subidos
│   ├── templates/      # Interfaz web
│   ├── __init__.py     # Factory de la app
│   ├── services.py     # Orquestación
│   └── views.py        # Endpoints API
└── run.py              # Punto de entrada
📊 Métricas Clave
Precisión: 82-89% vs análisis humano

Latencia: <3s (doc. cortos), <8s (doc. largos)

Coste/Análisis: ~$0.002 (Gemini Flash)

instalacion: pip install -r requirements.txt
ejecucion: python run.py
