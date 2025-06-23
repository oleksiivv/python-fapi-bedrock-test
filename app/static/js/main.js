// static/js/main.js
const uploadSection = document.getElementById('uploadSection');
const fileInput = document.getElementById('imageFile');
const fileInfo = document.getElementById('fileInfo');
const analyzeButton = document.getElementById('analyzeButton');
const resultSection = document.getElementById('resultSection');
const resultContent = document.getElementById('resultContent');
const resultMeta = document.getElementById('resultMeta');

// Drag and drop functionality
uploadSection.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadSection.classList.add('dragover');
});

uploadSection.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadSection.classList.remove('dragover');
});

uploadSection.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadSection.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        updateFileInfo(files[0]);
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        updateFileInfo(e.target.files[0]);
    }
});

function updateFileInfo(file) {
    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
    fileInfo.innerHTML = `
        <strong>Selected:</strong> ${file.name}<br>
        <strong>Size:</strong> ${fileSizeMB} MB<br>
        <strong>Type:</strong> ${file.type}
    `;
    fileInfo.style.display = 'block';
}

async function analyzeImage() {
    const file = fileInput.files[0];
    const prompt = document.getElementById('customPrompt').value.trim();

    if (!file) {
        alert('Please select an image file');
        return;
    }

    // Show loading state
    analyzeButton.disabled = true;
    analyzeButton.innerHTML = '<div class="spinner"></div>Analyzing...';
    resultSection.style.display = 'block';
    resultContent.innerHTML = '<div class="loading"><div class="spinner"></div>Analyzing your image...</div>';

    try {
        const formData = new FormData();
        formData.append('file', file);
        if (prompt) {
            formData.append('prompt', prompt);
        }

        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        // Display results
        resultMeta.textContent = `Analysis completed at ${new Date().toLocaleString()}`;
        resultContent.innerHTML = result.analysis || 'No analysis result returned.';

    } catch (error) {
        console.error('Error analyzing image:', error);
        resultContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    } finally {
        // Reset button
        analyzeButton.disabled = false;
        analyzeButton.innerHTML = '🚀 Analyze Image';
    }
}