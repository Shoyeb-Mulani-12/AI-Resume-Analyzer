import streamlit as st
from PyPDF2 import PdfReader

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 15px;
}

.card {
    background: #161b22;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

.skill {
    display: inline-block;
    padding: 8px 14px;
    margin: 6px;
    border-radius: 20px;
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    font-weight: 600;
    font-size: 14px;
}

.section-title {
    font-size: 22px;
    margin-bottom: 10px;
    font-weight: 600;
}

.profile {
    text-align: center;
    padding: 20px;
}

.profile-name {
    font-size: 18px;
    font-weight: bold;
}

.profile-role {
    color: gray;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown('<p class="main-title">🚀 AI Resume Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Smart Resume Insights powered by AI</p>', unsafe_allow_html=True)

# ✅ UPDATED BRANDING
st.markdown("""
<p style='text-align:center; font-size:14px; color:gray;'>
Developed by <b>Shoyeb Hamid Mulani</b> | MCA Graduate | AI Enthusiast 🚀
</p>
""", unsafe_allow_html=True)

st.divider()

# ------------------ INPUT ------------------
col1, col2 = st.columns([2,1])

with col1:
    uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])
    job_description = st.text_area("🧾 Paste Job Description", height=180)

# ------------------ PROFILE CARD ------------------
with col2:
    st.markdown('<div class="card profile">', unsafe_allow_html=True)

    st.markdown("### 👤 Developer")

    st.markdown('<p class="profile-name">Shoyeb Hamid Mulani</p>', unsafe_allow_html=True)
    st.markdown('<p class="profile-role">AI Developer | MCA Graduate</p>', unsafe_allow_html=True)

    st.markdown("📧 Email: shoyebmulani4521@gmail.com")

    st.markdown("""
🔗 [GitHub](https://github.com/Shoyeb-Mulani-12)  
💼 [LinkedIn](https://linkedin.com/in/shoyeb-mulani)
""")

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ FUNCTIONS ------------------

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def extract_skills(text):
    skills_list = [
        "python", "java", "c++", "sql", "mysql",
        "html", "css", "javascript", "react",
        "machine learning", "deep learning",
        "data science", "pandas", "numpy",
        "git", "github", "docker", "aws"
    ]

    text = text.lower()
    return list(set([skill for skill in skills_list if skill in text]))


def calculate_ats_score(skills):
    return min(len(skills) * 10, 100)


def calculate_job_match(resume_skills, job_text):
    job_skills = extract_skills(job_text)

    if not job_skills:
        return 0, [], []

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = int((len(matched) / len(job_skills)) * 100)
    return score, matched, missing


def generate_suggestions(skills, missing):
    suggestions = []

    if "python" not in skills:
        suggestions.append("Add Python skill")
    if "sql" not in skills:
        suggestions.append("Add SQL skill")
    if "machine learning" not in skills:
        suggestions.append("Add ML projects")

    for skill in missing:
        suggestions.append(f"Add {skill} (based on job description)")

    return suggestions

# ------------------ MAIN ------------------

if uploaded_file:

    text = extract_text_from_pdf(uploaded_file)
    skills = extract_skills(text)
    ats_score = calculate_ats_score(skills)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-title">📊 ATS Score</p>', unsafe_allow_html=True)
        st.progress(ats_score / 100)
        st.metric("Score", f"{ats_score}/100")

    with col2:
        st.markdown('<p class="section-title">💡 Skills</p>', unsafe_allow_html=True)

        if skills:
            for skill in skills:
                st.markdown(f'<span class="skill">{skill}</span>', unsafe_allow_html=True)
        else:
            st.write("No skills detected")

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    if job_description:
        match, matched, missing = calculate_job_match(skills, job_description)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('<p class="section-title">🎯 Job Match</p>', unsafe_allow_html=True)
        st.metric("Match Score", f"{match}%")
        st.progress(match / 100)

        col3, col4 = st.columns(2)

        with col3:
            st.write("✅ Matched Skills")
            for s in matched:
                st.success(s)

        with col4:
            st.write("❌ Missing Skills")
            for s in missing:
                st.error(s)

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        missing = []

    st.divider()

    suggestions = generate_suggestions(skills, missing)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<p class="section-title">📌 Suggestions</p>', unsafe_allow_html=True)

    if suggestions:
        for s in suggestions:
            st.warning(s)
    else:
        st.success("Resume looks strong!")

    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("📄 Resume Text"):
        st.write(text)

# ------------------ FOOTER ------------------
st.markdown("---")

st.markdown("""
<div style='text-align:center; color:gray; font-size:13px;'>
🚀 AI Resume Analyzer <br>
Developed by <b>Shoyeb Hamid Mulani</b><br>
📩 Contact: shoyebmulani4521@gmail.com
</div>
""", unsafe_allow_html=True)
