import streamlit as st
from services.code_reader import CodeReader
from services.doc_generator import DocGenerator
from utils.mermaid_image import render_mermaid_as_image
from utils.file_utils import cleanup_folder
from utils.pdf_generator import generate_pdf_from_markdown
import os
from typing import List, Tuple
from datetime import datetime
from dotenv import load_dotenv
import re

load_dotenv(override=True)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", '/tmp/uploads')
LLM_PROVIDER_URL = os.getenv("LLM_PROVIDER_URL", 'https://openrouter.ai/api/v1/chat/completions')
LLM_MODEL = os.getenv("LLM_MODEL", 'mistralai/mistral-small-3.2-24b-instruct-2506:free')
LLM_PROVIDER_API_KEY = os.getenv("LLM_PROVIDER_API_KEY", '')

reader = CodeReader(extract_path=UPLOAD_DIR)
generator = DocGenerator(LLM_PROVIDER_URL, LLM_MODEL, LLM_PROVIDER_API_KEY)

st.set_page_config(page_title="AI Service Doc Generator", layout="wide")

page = st.sidebar.selectbox("Navigate", ["Home", "Generate Document"])

if page == "Home":
    st.title("📘 AI-Powered Code Documentation Generator")
    st.markdown("""
    Welcome to your intelligent documentation assistant!

    This tool helps developers automatically generate high-level, human-readable documentation from their source code.

    ### 💡 Key Features:
    - 🗃️ Supports popular programming languages: `.py`, `.go`, `.js`, `.ts`, `.php`
    - ⚙️ Generates structured documentation and system diagrams
    - ✏️ Accepts custom instructions to refine document results
    - 📥 Download the result in PDF format

    👉 Go to the **Generate Document** page to get started.
    """)

elif page == "Generate Document":
    st.title("🛠️ Code to Documentation Generator")
    st.markdown("""
    This tool converts your source code into readable, high-level documentation with optional Mermaid diagrams.

    ✅ **Supported file types**: `.py`, `.go`, `.js`, `.ts`, `.php`  
    📦 Upload a ZIP file containing your project code.
    ✏️ Optionally add extra instructions to improve the result.
    """)

    st.subheader("📂 Upload Code Archive")
    uploaded_file = st.file_uploader("Upload a zipped service codebase", type="zip")

    st.subheader("📝 Add Custom Instructions (Optional)")
    additional_prompt = st.text_area("Add additional instructions or context for the documentation")

    code_chunks: List[Tuple[str, str]]
    if uploaded_file:
        with st.spinner("Extracting and reading code..."):
            cleanup_folder(UPLOAD_DIR)
            zip_path = os.path.join(UPLOAD_DIR, "code.zip")
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            reader.extract_zip(zip_path)
            code_chunks = reader.read_code_files()
            st.success(f"{len(code_chunks)} source files loaded.")

        if code_chunks:
            st.subheader("⚙️ Generate")
            if st.button("Generate Documentation"):
                with st.spinner("Generating documentation..."):
                    try:
                        doc_text = generator.generate_summary_and_diagram(
                            code_chunks, additional_instruction=additional_prompt
                        )
                        pattern = r"```mermaid(.*?)```"
                        match = re.search(pattern, doc_text, re.DOTALL)
                        if match:
                            mermaid_code = match.group(1).strip()
                            image_url = render_mermaid_as_image(mermaid_code)
                            doc_text = re.sub(pattern, f"![Diagram]({image_url})", doc_text, flags=re.DOTALL)
                        st.session_state["doc_text"] = doc_text
                    except Exception as e:
                        print(e)
                        st.warning("unexpected issue happen. please try again later.")
        else:
            st.warning("No code files found in the uploaded zip.")

    if "doc_text" in st.session_state:
        st.subheader("📘 Generated Documentation")
        st.markdown(st.session_state["doc_text"].encode().decode("unicode_escape"))

        doc_content = st.session_state["doc_text"]
        doc_bytes = doc_content.encode("utf-8")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_bytes = generate_pdf_from_markdown(doc_content)
        st.download_button(
            label="📥 Download as PDF",
            data=pdf_bytes,
            file_name=f"documentation_{timestamp}.pdf",
            mime="application/pdf"
        )
