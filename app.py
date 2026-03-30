import streamlit as st
from PyPDF2 import PdfReader

# 🔹 Page Title
st.title("AI Resume Analyzer")
st.write("Upload your resume and get analysis")

# 🔹 Upload File
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# 🔹 Function: Extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
            
    return text

# 🔹 Function: Extract Skills
def extract_skills(text):
    skills_list = [
        "python", "java", "c++", "sql", "mysql",
        "html", "css", "javascript", "react",
        "machine learning", "deep learning",
        "data science", "pandas", "numpy",
        "git", "github", "docker", "aws"
    ]
    
    found_skills = []
    text = text.lower()
    
    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)
            
    return found_skills

# 🔹 Function: Calculate ATS Score
def calculate_ats_score(skills):
    score = len(skills) * 10
    
    if score > 100:
        score = 100
        
    return score

# 🔹 Function: Suggestions
def generate_suggestions(skills):
    suggestions = []
    
    if "python" not in skills:
        suggestions.append("Add Python skill")
    if "sql" not in skills:
        suggestions.append("Add SQL skill")
    if "machine learning" not in skills:
        suggestions.append("Add Machine Learning projects")
    if "react" not in skills:
        suggestions.append("Add React or frontend skills")
    if "git" not in skills:
        suggestions.append("Add Git/GitHub experience")
        
    return suggestions

# 🔹 Main Logic
if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # Extract text
    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("📄 Extracted Resume Text:")
    st.write(resume_text)

    # Extract skills
    skills = extract_skills(resume_text)

    st.subheader("💡 Detected Skills:")
    if skills:
        for skill in skills:
            st.write(f"✅ {skill}")
    else:
        st.write("No skills detected")

    # Calculate ATS score
    score = calculate_ats_score(skills)

    st.subheader("📊 ATS Score:")
    st.write(f"Your ATS Score is: {score}/100")

    # Suggestions
    suggestions = generate_suggestions(skills)

    st.subheader("📌 Suggestions to Improve:")
    if suggestions:
        for s in suggestions:
            st.write(f"👉 {s}")
    else:
        st.write("Great! Your resume looks strong 💪")