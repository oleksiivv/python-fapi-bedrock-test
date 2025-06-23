# app/views/html_views.py
from app.config.settings import settings


class HTMLViews:
    """HTML views and templates for the application"""

    @staticmethod
    def get_main_page() -> str:
        """Get the main HTML page"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{settings.APP_NAME}</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}

                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    padding: 20px;
                }}

                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}

                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}

                .header h1 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    font-weight: 300;
                }}

                .header p {{
                    font-size: 1.1em;
                    opacity: 0.9;
                }}

                .content {{
                    padding: 40px;
                }}

                .upload-section {{
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 30px;
                    margin-bottom: 30px;
                    border: 2px dashed #dee2e6;
                    transition: all 0.3s ease;
                }}

                .upload-section:hover {{
                    border-color: #667eea;
                    background: #f0f4ff;
                }}

                .upload-section.dragover {{
                    border-color: #667eea;
                    background: #e3f2fd;
                    transform: scale(1.02);
                }}

                .file-input-wrapper {{
                    position: relative;
                    display: inline-block;
                    cursor: pointer;
                    width: 100%;
                }}

                .file-input {{
                    position: absolute;
                    opacity: 0;
                    width: 100%;
                    height: 100%;
                    cursor: pointer;
                }}

                .file-input-button {{
                    display: inline-block;
                    padding: 12px 24px;
                    background: #667eea;
                    color: white;
                    border-radius: 25px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-weight: 500;
                }}

                .file-input-button:hover {{
                    background: #5a67d8;
                    transform: translateY(-2px);
                }}

                .file-info {{
                    margin: 15px 0;
                    padding: 10px;
                    background: #e8f5e8;
                    border-radius: 5px;
                    display: none;
                }}

                .prompt-section {{
                    margin: 20px 0;
                }}

                .prompt-input {{
                    width: 100%;
                    height: 100px;
                    padding: 15px;
                    border: 2px solid #dee2e6;
                    border-radius: 8px;
                    font-family: inherit;
                    font-size: 14px;
                    resize: vertical;
                    transition: border-color 0.3s ease;
                }}

                .prompt-input:focus {{
                    outline: none;
                    border-color: #667eea;
                }}

                .analyze-button {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 30px;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 500;
                    transition: all 0.3s ease;
                    width: 100%;
                    margin-top: 20px;
                }}

                .analyze-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }}

                .analyze-button:disabled {{
                    opacity: 0.6;
                    cursor: not-allowed;
                    transform: none;
                }}

                .result-section {{
                    margin-top: 30px;
                    padding: 25px;
                    background: #f8f9fa;
                    border-radius: 10px;
                    display: none;
                }}

                .result-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #dee2e6;
                }}

                .result-title {{
                    font-size: 1.4em;
                    color: #667eea;
                    font-weight: 500;
                }}

                .result-meta {{
                    font-size: 0.9em;
                    color: #6c757d;
                }}

                .result-content {{
                    line-height: 1.8;
                    color: #333;
                    white-space: pre-wrap;
                }}

                .loading {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}

                .spinner {{
                    width: 20px;
                    height: 20px;
                    border: 2px solid #f3f3f3;
                    border-top: 2px solid #667eea;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin-right: 10px;
                }}

                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}

                .error {{
                    color: #dc3545;
                    background: #f8d7da;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 10px 0;
                }}

                .success {{
                    color: #155724;
                    background: #d4edda;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 10px 0;
                }}

                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #6c757d;
                    font-size: 0.9em;
                }}

                @media (max-width: 768px) {{
                    .container {{
                        margin: 10px;
                        border-radius: 10px;
                    }}

                    .header h1 {{
                        font-size: 2em;
                    }}

                    .content {{
                        padding: 20px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🖼️ {settings.APP_NAME}</h1>
                    <p>Upload an image to get AI-powered analysis using Amazon Bedrock</p>
                </div>

                <div class="content">
                    <div class="upload-section" id="uploadSection">
                        <div style="text-align: center; margin-bottom: 20px;">
                            <h3>📤 Upload Your Image</h3>
                            <p style="color: #6c757d; margin-top: 10px;">
                                Drag and drop an image here, or click to select
                            </p>
                        </div>

                        <div class="file-input-wrapper">
                            <input type="file" id="imageFile" class="file-input" accept="image/*" />
                            <div class="file-input-button" style="text-align: center; width: 100%;">
                                Choose Image File
                            </div>
                        </div>

                        <div id="fileInfo" class="file-info"></div>

                        <div class="prompt-section">
                            <label for="customPrompt" style="display: block; margin-bottom: 8px; font-weight: 500;">
                                🎯 Analysis Prompt (Optional)
                            </label>
                            <textarea 
                                id="customPrompt" 
                                class="prompt-input"
                                placeholder="Enter custom analysis instructions... (e.g., 'Describe the colors and emotions in this image', 'What objects can you identify?', 'Analyze the composition and lighting')"
                            >{settings.DEFAULT_ANALYSIS_PROMPT}</textarea>
                        </div>

                        <button id="analyzeButton" class="analyze-button" onclick="analyzeImage()">
                            🚀 Analyze Image
                        </button>
                    </div>

                    <div id="resultSection" class="result-section">
                        <div class="result-header">
                            <div class="result-title">📊 Analysis Results</div>
                            <div id="resultMeta" class="result-meta"></div>
                        </div>
                        <div id="resultContent" class="result-content"></div>
                    </div>
                </div>

                <div class="footer">
                    <p>Powered by Amazon Bedrock & Claude AI | Max file size: {settings.max_file_size_mb}MB</p>
                </div>
            </div>

            <script>
                const uploadSection = document.getElementById('uploadSection');
                const fileInput = document.getElementById('imageFile');
                const fileInfo = document.getElementById('fileInfo');
                const analyzeButton = document.getElementById('analyzeButton');
                const resultSection = document.getElementById('resultSection');
                const resultContent = document.getElementById('resultContent');
                const resultMeta = document.getElementById('resultMeta');

                // Drag and drop functionality
                uploadSection.addEventListener('dragover', (e) => {{
                    e.preventDefault();
                    uploadSection.classList.add('dragover');
                }});

                uploadSection.addEventListener('dragleave', (e) => {{
                    e.preventDefault();
                    uploadSection.classList.remove('dragover');
                }});

                uploadSection.addEventListener('drop', (e) => {{
                    e.preventDefault();
                    uploadSection.classList.remove('dragover');

                    const files = e.dataTransfer.files;
                    if (files.length > 0) {{
                        fileInput.files = files;
                        updateFileInfo(files[0]);
                    }}
                }});

                // File input change
                fileInput.addEventListener('change', (e) => {{
                    if (e.target.files.length > 0) {{
                        updateFileInfo(e.target.files[0]);
                    }}
                }});

                function updateFileInfo(file) {{
                    const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
                    fileInfo.innerHTML = `
                        <strong>Selected:</strong> ${{file.name}}<br>
                        <strong>Size:</strong> ${{fileSizeMB}} MB<br>
                        <strong>Type:</strong> ${{file.type}}
                    `;
                    fileInfo.style.display = 'block';
                }}

                async function analyzeImage() {{
                    const file = fileInput.files[0];
                    const prompt = document.getElementById('customPrompt').value.trim();

                    if (!file) {{
                        alert('Please select an image file');
                        return;
                    }}

                    // Show loading state
                    analyzeButton.disabled = true;
                    analyzeButton.innerHTML = '<div class="spinner"></div>Analyzing...';
                    resultSection.style.display = 'block';
                    resultContent.innerHTML = '<div class="loading"><div class="spinner"></div>Analyzing your image...</div>';

                    try {{
                        const formData = new FormData();
                        formData.append('file', file);
                        if (prompt) {{
                            formData.append('prompt', prompt);
                        }}

                        const response = await fetch('/api/analyze', {{
                            method: 'POST',
                            body: formData
                        }});

                        if (!response.ok) {{
                            const errorData = await response.json();
                            throw new Error(errorData.detail || `HTTP error! status: ${{response.status}}`);
                        }}

                        const result = await response.json();
    """