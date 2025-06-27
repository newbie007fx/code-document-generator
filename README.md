# 🧠 AI-Powered Code Documentation Generator

This tool automatically generates high-level documentation from your source code using large language models (LLMs). It supports multiple languages and can be deployed as a simple web interface using Streamlit.

## ✨ Features

- 📦 Upload a zipped codebase
- 📝 Add optional custom instructions to guide the generation
- 📘 Generates structured documentation with high-level logic summaries
- 🖼️ Auto-generates system diagrams using Mermaid, rendered as images
- 📥 Download the generated documentation as PDF

## 🛠️ Supported Languages

- Python (.py)
- Go (.go)
- JavaScript (.js)
- TypeScript (.ts)
- PHP (.php)

## 🚀 Getting Started

### Prerequisites

- Python 3.10+

### How to run


1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy environment variable config:
   ```bash
   cp env.example .env
   ```
2. Set environment variables in a `.env` file:
   ```env
   LLM_MODEL=your-model-id
   LLM_PROVIDER_URL=https://openrouter.ai/api/v1/chat/completions
   LLM_PROVIDER_API_KEY=your-api-key
   UPLOAD_DIR=/tmp/uploads
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## 📷 Example Output

![example](./screenshots/example_output.png)

