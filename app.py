import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Load API key from backend .env file
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="DevGuard | AI Code Auditor",
    page_icon="⚡",
    layout="wide"
)

# Application Header
st.title("⚡ DevGuard — Enterprise AI Code Reviewer")
st.caption("Automated Code Quality, Security Audit & Optimization Engine")

# Fetch API key securely from .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Backend Error: `GEMINI_API_KEY` not found in `.env` file.")
    st.stop()

st.divider()

# Main Inputs & Settings
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("⚙️ Audit Settings")
    language = st.selectbox("Select Target Language", ["Python", "JavaScript", "C++", "Java", "C", "Go", "Rust"])
    
    st.write("---")
    st.subheader("🎯 Review Scope")
    focus_bugs = st.checkbox("🐛 Bugs & Logic Flaws", value=True)
    focus_perf = st.checkbox("🚀 Performance & Complexity", value=True)
    focus_sec = st.checkbox("🔒 Security Vulnerabilities", value=True)
    focus_refactor = st.checkbox("✨ Refactored Code", value=True)

with col2:
    st.subheader("📄 Code Input")
    uploaded_file = st.file_uploader("Upload Source Code File", type=["py", "js", "cpp", "java", "c", "go", "rs", "txt"])
    
    if uploaded_file is not None:
        user_code = uploaded_file.read().decode("utf-8")
        st.success(f"📂 Loaded file: **{uploaded_file.name}**")
    else:
        user_code = st.text_area("Or paste code snippet directly:", height=250, placeholder="Paste your code here...")

# System Prompt Configuration
sections = []
if focus_bugs:
    sections.append("1. 🐛 **Bugs & Logic Failures**: Detail syntax errors, unhandled edge cases, and runtime issues.")
if focus_perf:
    sections.append("2. 🚀 **Performance & Best Practices**: Analyze time/space complexity and suggest optimizations.")
if focus_sec:
    sections.append("3. 🔒 **Security Audit**: Highlight vulnerabilities (e.g., SQL injection, memory leaks, unsafe inputs).")
if focus_refactor:
    sections.append("4. ✨ **Refactored Code Block**: Provide clean, production-ready refactored code.")

sections_text = "\n".join(sections)

SYSTEM_PROMPT = f"""You are a Principal Software Engineer and Code Auditor.
Perform a strict code review on the given snippet. Provide structured, executive-ready feedback covering:

{sections_text}
"""

st.write("---")

# Execution Button
if st.button("⚡ Run Full Audit", type="primary", use_container_width=True):
    if not user_code.strip():
        st.warning("Please provide code input via text box or file upload before auditing.")
    else:
        try:
            with st.spinner("Analyzing code architecture and vulnerabilities..."):
                client = genai.Client(api_key=api_key)
                
                full_prompt = f"{SYSTEM_PROMPT}\n\nLanguage: {language}\nCode:\n```{language}\n{user_code}\n```"
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=full_prompt
                )
                
                st.divider()
                st.subheader("📋 Executive Audit Report")
                st.markdown(response.text)
                
                st.download_button(
                    label="📥 Download Audit Report (.md)",
                    data=response.text,
                    file_name=f"audit_report_{language.lower()}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
        except Exception as e:
            st.error(f"Execution Error: {e}")