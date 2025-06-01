from flask import Blueprint, render_template, request, jsonify, current_app
from pathlib import Path
from werkzeug.utils import secure_filename
import time
from app.services import AnalysisService
from app.core.config import Config

main = Blueprint('main', __name__)
service = AnalysisService()

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'pdf' in request.files:
        try:
            start_time = time.time()
            pdf = request.files['pdf']
            
            if not pdf.filename.lower().endswith('.pdf'):
                raise ValueError("Solo se aceptan archivos PDF")
            
            filename = secure_filename(pdf.filename)
            filepath = Config.UPLOAD_FOLDER / filename
            pdf.save(filepath)
            
            service.process_document(filepath)
            
            print(f"PDF cargado en {time.time() - start_time:.2f}s")
            
            return render_template(
                'index.html',
                contrato_file=filename,
                normativa_file="normativa.pdf",
                analysis=service.current_analysis,
                analysis_ready=service.analysis_ready,
                is_long_document=service.is_long_document,
                page_count=service.page_count,
                error=None
            )
            
        except Exception as e:
            return render_template('index.html', error=str(e))
    
    return render_template(
        'index.html',
        contrato_file=None,
        normativa_file="normativa.pdf",
        analysis=service.current_analysis if service.analysis_ready else None,
        analysis_ready=service.analysis_ready,
        is_long_document=getattr(service, 'is_long_document', False),
        page_count=getattr(service, 'page_count', 0),
        error=None
    )

@main.route('/ask', methods=['POST'])
def ask_gemini():
    try:
        question = request.form.get('question', '').strip()
        if not question:
            return jsonify({"response": "❌ Ingresa una pregunta", "error": True})
        
        context = service.get_context_for_question()
        response = service.ai.ask_question(question, context)
        
        return jsonify({"response": response, "error": False})
    
    except Exception as e:
        return jsonify({"response": f"⏳ Error: {str(e)}", "error": True})

@main.route('/check_analysis')
def check_analysis():
    return jsonify({
        'ready': service.analysis_ready,
        'analysis': service.current_analysis or '',
        'is_long_document': service.is_long_document,
        'page_count': service.page_count
    })