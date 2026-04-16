import streamlit as st
from PyPDF2 import PdfReader

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ------------------ HEADER ------------------
st.markdown("<h1 style='text-align: center;'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze your resume with AI insights</p>", unsafe_allow_html=True)

st.divider()

# ------------------ INPUT SECTION ------------------
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("🧾 Paste Job Description", height=200)

# ------------------ FUNCTIONS ------------------

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


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

    return list(set(found_skills))


def calculate_ats_score(skills):
    score = len(skills) * 10
    return min(score, 100)


# 🔥 NEW: JOB MATCH FUNCTION
def calculate_job_match(resume_skills, job_text):
    job_skills = extract_skills(job_text)

    if not job_skills:
        return 0, [], []

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    match_score = int((len(matched) / len(job_skills)) * 100)

    return match_score, matched, missing


def generate_suggestions(skills, missing_skills):
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

    # 🔥 Add missing job skills suggestions
    for skill in missing_skills:
        suggestions.append(f"Consider adding '{skill}' based on job description")

    return suggestions


# ------------------ MAIN ------------------

if uploaded_file is not None:

    st.success("✅ File uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)
    resume_skills = extract_skills(resume_text)
    ats_score = calculate_ats_score(resume_skills)

    # ------------------ DASHBOARD ------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 ATS Score")
        st.progress(ats_score / 100)
        st.metric(label="Score", value=f"{ats_score}/100")

    with col2:
        st.subheader("💡 Resume Skills")
        if resume_skills:
            for skill in resume_skills:
                st.markdown(
                    f"<span style='background-color:#d4edda; padding:6px; border-radius:8px; margin:5px; display:inline-block;'>{skill}</span>",
                    unsafe_allow_html=True
                )
        else:
            st.write("No skills detected")

    st.divider()

    # ------------------ JOB MATCHING ------------------
    if job_description:

        match_score, matched_skills, missing_skills = calculate_job_match(
            resume_skills, job_description
        )

        st.subheader("🎯 Job Match Analysis")

        col3, col4 = st.columns(2)

        with col3:
            st.metric("Match Score", f"{match_score}%")
            st.progress(match_score / 100)

        with col4:
            st.write("✅ Matched Skills:")
            for skill in matched_skills:
                st.success(skill)

            st.write("❌ Missing Skills:")
            for skill in missing_skills:
                st.error(skill)

    else:
        missing_skills = []

    st.divider()

    # ------------------ SUGGESTIONS ------------------
    suggestions = generate_suggestions(resume_skills, missing_skills)

    st.subheader("📌 Suggestions to Improve")

    if suggestions:
        for s in suggestions:
            st.warning(f"👉 {s}")
    else:
        st.success("Great! Your resume looks strong 💪")

    # ------------------ RESUME TEXT ------------------
    with st.expander("📄 View Extracted Resume Text"):
        st.write(resume_text)
