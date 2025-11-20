from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from pypdf import PdfReader
import openai
import os
import tempfile
from io import BytesIO
import json

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@app.get("/")
async def read_root():
    return {"message": "PDF Summarizer API - Upload PDF at /upload-pdf"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Carica un PDF, estrae il testo e genera un riassunto con OpenAI
    """
    try:
        # Validazione estensione
        if not file.filename.endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Il file deve essere un PDF. Estensione non valida."
            )
        
        # Lettura del file
        contents = await file.read()
        
        # Validazione dimensione
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File troppo grande. Massimo {MAX_FILE_SIZE / (1024*1024):.0f}MB."
            )
        
        # Crea file temporaneo
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp.write(contents)
        tmp.close()
        
        try:
            # Estrae testo dal PDF
            reader = PdfReader(tmp.name)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
            
            text = text.strip()
            
            if not text:
                raise HTTPException(
                    status_code=400,
                    detail="Impossibile estrarre testo dal PDF. Verifica che il PDF contenga testo."
                )
            
            # Limita il testo a 4000 caratteri per l'API
            text_for_summary = text[:4000] if len(text) > 4000 else text
            
            # Genera riassunto con OpenAI
            if not openai.api_key:
                raise HTTPException(
                    status_code=500,
                    detail="API key OpenAI non configurata. Imposta OPENAI_API_KEY."
                )
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"Fornisci un riassunto breve e conciso del seguente testo:\n\n{text_for_summary}"
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            
            return {
                "filename": file.filename,
                "text_length": len(text),
                "extracted_text": text[:500] + "..." if len(text) > 500 else text,
                "summary": summary,
                "error": None
            }
        
        finally:
            # Pulizia file temporaneo
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore nell'elaborazione: {str(e)}"
        )

@app.post("/download-summary")
async def download_summary(request: dict):
    """
    Crea un PDF con il riassunto e lo scarica
    """
    try:
        summary = request.get("summary", "")
        filename = request.get("filename", "documento.pdf")
        
        if not summary:
            raise HTTPException(
                status_code=400,
                detail="Riassunto vuoto"
            )
        
        # Crea PDF in memoria
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Titolo
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, height - 50, "RIASSUNTO PDF")
        
        # Nome file originale
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, height - 70, f"Documento: {filename}")
        
        # Testo riassunto
        pdf.setFont("Helvetica", 11)
        y = height - 100
        margin = 50
        max_width = width - 2 * margin
        
        lines = simpleSplit(summary, "Helvetica", 11, max_width)
        for line in lines:
            if y < 50:  # Nuova pagina se necessario
                pdf.showPage()
                y = height - 50
            pdf.drawString(margin, y, line)
            y -= 15
        
        pdf.save()
        buffer.seek(0)
        
        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=riassunto.pdf"}
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore nel download: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
