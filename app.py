import streamlit as st
import re
import PyPDF2
import docx2txt

st.set_page_config(page_title="Resume Analyzer", layout="centered")

st.title("📄 Resume Analyzer")
st.write("Upload your resume (PDF or DOCX)")

def extract_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_docx(file):
    return docx2txt.process(file)

def clean(text):
    return re.sub(r'\s+', ' ', text).lower()

SKILLS = ["python", "java", "c", "c++", "html", "css", "javascript", "sql", "machine learning"]

def find_skills(text):
    return [s for s in SKILLS if s in text]

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "pdf":
        text = extract_pdf(uploaded_file)
    else:
        text = extract_docx(uploaded_file)

    text = clean(text)

    skills = find_skills(text)

    st.subheader("🧠 Detected Skills")
    st.write(skills)

    st.subheader("📄 Resume Text Preview")
    st.write(text[:1000])
