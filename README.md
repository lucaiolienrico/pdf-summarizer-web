# 📄 PDF Summarizer - AI-Powered Web App

Web app completa per caricare file PDF, estrarre il testo e generare riassunti automatici con AI (OpenAI GPT).

## ✨ Caratteristiche Principali

✅ **Upload PDF intuitivo** - Carica facilmente file PDF tramite interfaccia responsiva
✅ **Estrazione testo affidabile** - Parsing PDF con libreria pypdf
✅ **Riassunto AI intelligente** - Riassunti generati da OpenAI GPT-4o-mini
✅ **Download PDF riassunto** - Scarica il riassunto in formato PDF
✅ **Design responsivo** - Interfaccia moderna e mobile-friendly
✅ **API RESTful completa** - Backend FastAPI con CORS abilitato

## 🛠️ Stack Tecnologico

### Backend
- **FastAPI 0.109.0** - Framework web moderno e veloce
- **Python 3.8+** - Linguaggio principale
- **PyPDF 4.1.1** - Estrazione testo affidabile da PDF
- **OpenAI API 1.14.0** - Integrazione modelli LLM
- **ReportLab 4.0.7** - Generazione PDF per download
- **Uvicorn 0.27.0** - Server ASGI

### Frontend
- **HTML5** - Struttura semantica
- **CSS3** - Styling responsivo con gradient
- **Vanilla JavaScript** - Gestione upload e API calls
- **No dependencies** - Nessuna libreria esterna richiesta

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.8+
- pip
- OpenAI API Key (gratuito con credit di prova)

### Passo 1: Clone il Repository

```bash
git clone https://github.com/lucaiolienrico/pdf-summarizer-web.git
cd pdf-summarizer-web
```

### Passo 2: Configura Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
```

### Passo 3: Configura OpenAI API Key

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key-here"

# macOS/Linux
export OPENAI_API_KEY="sk-your-api-key-here"
```

Ottieni la tua API key su: https://platform.openai.com/api-keys

### Passo 4: Avvia Backend

```bash
uvicorn main:app --reload
```

Il backend sarà disponibile su: `http://localhost:8000`

### Passo 5: Apri Frontend

Apri nel browser: `file:///path/to/frontend/index.html`

O usa un server locale (consigliato):
```bash
cd frontend
python -m http.server 3000
```

Quindi visita: `http://localhost:3000`

## 📁 Struttura Progetto

```
pdf-summarizer-web/
├── backend/
│   ├── main.py              # API FastAPI principale
│   └── requirements.txt      # Dipendenze Python
├── frontend/
│   ├── index.html           # Pagina web
│   ├── styles.css           # Stili CSS
│   └── app.js               # Logica JavaScript
├── README.md                # Questo file
├── LICENSE                  # MIT License
```

## 🔌 API Endpoints

### POST /upload-pdf
Carica un PDF e ottiene il riassunto

**Request:**
```bash
curl -X POST http://localhost:8000/upload-pdf \
  -F "file=@documento.pdf"
```

**Response:**
```json
{
  "filename": "documento.pdf",
  "text_length": 5000,
  "extracted_text": "...",
  "summary": "Riassunto generato dal modello AI",
  "error": null
}
```

### POST /download-summary
Genera e scarica il riassunto come PDF

**Request:**
```json
{
  "summary": "Testo del riassunto",
  "filename": "documento.pdf"
}
```

## 🔐 Sicurezza

- ✅ Validazione estensione file (.pdf)
- ✅ Limite dimensione file (5MB di default)
- ✅ Pulizia automatica file temporanei
- ✅ CORS abilitato per produzione
- ✅ Gestione errori robusta

## ⚙️ Configurazione Avanzata

Per modificare il limite di dimensione file, edita `backend/main.py`:

```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

Per usare modelli OpenAI diversi:

```python
model="gpt-4"  # oppure "gpt-3.5-turbo"
```

## 🐛 Troubleshooting

**Errore: "OPENAI_API_KEY not found"**
- Verifica di aver configurato la variabile di ambiente
- Riavvia il terminale/IDE dopo aver impostato la chiave

**Errore: "CORS error"**
- Assicurati che il backend sia in esecuzione su http://localhost:8000
- Verifica di usare l'URL corretto nel file app.js

**PDF non elaborato**
- Il PDF deve contenere testo estraibile (non scansionato)
- Massimo 5MB di dimensione

## 📦 Deployment

### Heroku
```bash
heroku create pdf-summarizer-web
git push heroku main
heroku config:set OPENAI_API_KEY="sk-..."
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Licenza

MIT License - Vedi [LICENSE](LICENSE) per dettagli

## 🤝 Contributi

Contributi sono benvenuti! Fork il repo e crea una pull request.

## 👨‍💻 Autore

**Lucaio Lienrico** - [GitHub](https://github.com/lucaiolienrico)

## 💡 Suggerimenti e Bug Report

Segnala problemi tramite GitHub Issues.

---

**Built with ❤️ using FastAPI + OpenAI + Vanilla JS**
