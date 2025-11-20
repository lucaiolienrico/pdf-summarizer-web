const API_URL = 'http://localhost:8000';
const form = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const progress = document.getElementById('progress');
const resultsSection = document.getElementById('results');
const fileName = document.getElementById('file-name');
const textLength = document.getElementById('text-length');
const summaryBox = document.getElementById('summary');
const extractedText = document.getElementById('extracted-text');
const downloadBtn = document.getElementById('downloadPdfBtn');
const resetBtn = document.getElementById('reset-btn');

let lastSummary = '';
let lastFileName = 'documento.pdf';

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    resultsSection.classList.add('hidden');
    
    if (!fileInput.files.length) {
        alert('Seleziona un file PDF');
        return;
    }
    
    progress.classList.remove('hidden');
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    try {
        const response = await fetch(`${API_URL}/upload-pdf`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            alert('Errore: ' + (data.detail || 'Elaborazione fallita'));
        }
    } catch (error) {
        alert('Errore di connessione: ' + error.message + '\n\nAssicurati che il backend sia in esecuzione su http://localhost:8000');
    } finally {
        progress.classList.add('hidden');
    }
});

function displayResults(data) {
    fileName.textContent = data.filename;
    textLength.textContent = `${data.text_length.toLocaleString('it-IT')} caratteri`;
    summaryBox.textContent = data.summary;
    extractedText.textContent = data.extracted_text;
    
    lastSummary = data.summary;
    lastFileName = data.filename;
    
    resultsSection.classList.remove('hidden');
}

downloadBtn.addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_URL}/download-summary`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                summary: lastSummary,
                filename: lastFileName
            })
        });
        
        if (!response.ok) {
            throw new Error('Errore nel download');
        }
        
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'riassunto.pdf';
        document.body.appendChild(a);
        a.click();
        
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
    } catch (error) {
        alert('Errore nel download del PDF: ' + error.message);
    }
});

resetBtn.addEventListener('click', () => {
    form.reset();
    fileInput.value = '';
    resultsSection.classList.add('hidden');
    progress.classList.add('hidden');
});
