import streamlit as st
import os
import pdfplumber
import docx
import re
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Section keywords
section_keywords = {
    "Skills": ["skills", "technical skills", "core competencies", "technical expertise", "key skills", "areas of expertise"],
    "Experience": ["experience", "professional experience", "work history", "employment", "internship", "career summary"],
    "Education": ["education", "academic qualifications", "qualifications", "academics", "academic background", "educational background"],
    "Projects": ["projects", "academic projects", "personal projects", "project work", "notable projects"]
}

# Job role keywords
job_roles = {
    "Data Analyst": ["excel", "power bi", "tableau", "data visualization", "data analysis", "sql", "business intelligence"],
    "Data Scientist": ["python", "machine learning", "data science", "regression", "modeling", "statistics", "numpy", "pandas"],
    "Software Engineer": ["java", "c++", "software development", "debugging", "algorithms", "system design"],
    "Web Developer": ["html", "css", "javascript", "react", "frontend", "backend", "node.js", "web development"],
    "Business Analyst": ["requirement gathering", "stakeholders", "business analysis", "process improvement", "gap analysis"],
    "Machine Learning Engineer": ["scikit-learn", "deep learning", "tensorflow", "neural networks", "ml", "model training"]
}

# Extract text from uploaded file
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

# Clean text
def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

# Extract specific sections
def extract_sections(text):
    lines = text.split('\n')
    current_section = None
    sections = {"Skills": [], "Experience": [], "Education": [], "Projects": []}

    for line in lines:
        line_lower = line.strip().lower()
        matched = False

        for section, keywords in section_keywords.items():
            for keyword in keywords:
                if keyword in line_lower:
                    current_section = section
                    matched = True
                    break
            if matched:
                break

        if current_section and not matched and line.strip():
            sections[current_section].append(clean_text(line))
    return sections

# Predict job role
def predict_role(text):
    text_lower = text.lower()
    role_scores = {}
    for role, keywords in job_roles.items():
        count = sum(1 for kw in keywords if kw in text_lower)
        role_scores[role] = count
    best_role = max(role_scores, key=role_scores.get)
    return best_role if role_scores[best_role] > 0 else "Unknown"

# Compare skills using cosine similarity
def compare_skills(jd_text, resume_skills):
    if not resume_skills or not jd_text.strip():
        return 0.0
    combined = [" ".join(resume_skills), jd_text]
    vectors = CountVectorizer().fit_transform(combined).toarray()
    return round(cosine_similarity([vectors[0]], [vectors[1]])[0][0] * 100, 2)

# Generate feedback based on match score
def get_feedback(score):
    if score > 80:
        return "Excellent Match 🎯"
    elif score > 60:
        return "Good Match 👍"
    elif score > 40:
        return "Average Fit 🧐"
    else:
        return "Low Match — Improve Your Skills 📉"

# Streamlit UI
st.set_page_config(page_title="AI Resume Classifier", layout="wide")
st.title("🤖 AI Resume Classifier & Matcher")

uploaded_resume = st.file_uploader("📤 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("📝 Paste the Job Description (JD)", height=300)

if uploaded_resume and jd_text:
    raw_text = extract_text(uploaded_resume)
    sections = extract_sections(raw_text)
    predicted_role = predict_role(raw_text)

    if predicted_role == "Unknown":
        st.error("❌ Could not identify a job role from the resume.")
    else:
        jd_lower = jd_text.lower()
        if predicted_role.lower() in jd_lower:
            st.success("✅ JD and Resume match!")

            score = compare_skills(jd_text, sections["Skills"])
            feedback = get_feedback(score)

            st.markdown(f"### 🏷️ Predicted Role: `{predicted_role}`")
            st.markdown(f"### 📊 Match Score: **{score}%**")
            st.markdown(f"### 💡 Feedback: *{feedback}*")
        else:
            st.error("🚫 JD and Resume do not align. Please search for another opportunity.")
else:
    st.info("Please upload a resume and paste a job description to continue.")
