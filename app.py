import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get instant AI-powered feedback 🔥")

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    else:
        text = file.read().decode("utf-8")
    return text

# -----------------------------
# SKILLS DATABASE
# -----------------------------
SKILLS_DB = [
    "python", "java", "c", "c++", "sql", "html", "css", "javascript",
    "react", "node", "machine learning", "deep learning", "ai",
    "excel", "power bi", "communication", "teamwork"
]

JOB_ROLES = {
    "python": "Python Developer",
    "java": "Java Developer",
    "sql": "Data Analyst",
    "machine learning": "ML Engineer",
    "excel": "Data Analyst",
    "html": "Frontend Developer",
    "react": "Frontend Developer"
}

LANGUAGES = ["english", "tamil", "hindi", "french", "german"]

# -----------------------------
# ANALYSIS FUNCTION
# -----------------------------
def analyze_resume(text, job_desc):

    text = text.lower()
    job_desc = job_desc.lower()

    # Skills
    matched_skills = [s for s in SKILLS_DB if s in text and s in job_desc]
    missing_skills = [s for s in SKILLS_DB if s in job_desc and s not in text]

    # Score calculation
    skill_score = len(matched_skills) / len(SKILLS_DB) * 50
    keyword_score = len(re.findall(r'\b\w+\b', text)) / 50
    experience_score = 20 if "intern" in text or "experience" in text or "project" in text else 10
    structure_score = 10
    language_score = 10 if any(lang in text for lang in LANGUAGES) else 5

    total = skill_score + keyword_score + experience_score + structure_score + language_score
    rating = round((total / 100) * 10, 1)

    ai_score = round(total, 1)

    # Job prediction
    predicted_role = "General Role"
    for key in JOB_ROLES:
        if key in text:
            predicted_role = JOB_ROLES[key]

    # Experience fit
    if "experience" in text or "intern" in text:
        exp_fit = "Highly Relevant ✅"
    else:
        exp_fit = "Low/No Experience Mentioned ⚠️"

    return {
        "rating": rating,
        "ai_score": ai_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "predicted_role": predicted_role,
        "experience_fit": exp_fit
    }

# -----------------------------
# UI
# -----------------------------
uploaded_file = st.file_uploader("📤 Upload Resume (PDF or TXT)", type=["pdf", "txt"])
job_desc = st.text_area("🧾 Paste Job Description Here")

if uploaded_file and job_desc:
    resume_text = extract_text(uploaded_file)

    result = analyze_resume(resume_text, job_desc)

    st.subheader("📊 AI Resume Report")

    st.metric("⭐ Rating (out of 10)", result["rating"])
    st.metric("🤖 AI Score (%)", result["ai_score"])

    st.write("🎯 Predicted Job Role:", result["predicted_role"])
    st.write("💼 Experience Fit:", result["experience_fit"])

    st.write("🧠 Matched Skills:", result["matched_skills"])
    st.write("❌ Missing Skills:", result["missing_skills"])

    # Progress bar
    st.progress(int(result["ai_score"]))
