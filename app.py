import streamlit as st
from parser.resume_parser import extract_text_from_pdf
from analyzer.skill_extractor import load_skills, extract_skills
from analyzer.jd_matcher import match_resume_with_jd
from analyzer.ats_scorer import calculate_ats_score


def get_score_color(score):
    if score >= 75:
        return "#22c55e"
    elif score >= 50:
        return "#f59e0b"
    else:
        return "#ef4444"


st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    color: white;
}

header {
    display: none;
}

.block-container {
    max-width: 1450px !important;
    margin: 0 auto !important;
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #a78bfa;
    margin-bottom: 15px;
}

.metric-box {
    background: rgba(255, 255, 255, 0.10);
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
}

.metric-label {
    font-size: 15px;
    color: #cbd5e1;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
}

label, .stTextArea label, .stFileUploader label {
    color: white !important;
    font-weight: 600;
}

textarea {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 12px !important;
}

div[data-testid="stTextArea"] {
    background: rgba(255, 255, 255, 0.08);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

div[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.08);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

[data-testid="stFileUploader"] {
    color: black !important;
}

[data-testid="stFileUploader"] small {
    color: #374151 !important;
}

button, .stDownloadButton button {
    color: white !important;
    background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
}

button:hover {
    opacity: 0.88;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #8b5cf6, #3b82f6);
}

.skill-pill {
    display: inline-block;
    color: white;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 14px;
    margin: 4px 6px 4px 0;
    font-weight: 500;
}

.skill-pill-blue {
    background: linear-gradient(90deg, #7c3aed, #2563eb);
}

.skill-pill-green {
    background: linear-gradient(90deg, #22c55e, #16a34a);
}

.skill-pill-red {
    background: linear-gradient(90deg, #ef4444, #dc2626);
}

html, body, [class*="css"] {
    font-size: 17px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom:40px;">
    <h1 style="color:white; font-size:52px; margin-bottom:10px;">
        🚀 Welcome to AI Resume Analyzer
    </h1>
    <p style="color:#cbd5e1; font-size:20px; margin-bottom:0;">
        Upload your resume and compare it with job descriptions to improve your chances of getting hired.
    </p>
</div>
""", unsafe_allow_html=True)

outer1, top_left, top_right, outer2 = st.columns([0.4, 2.8, 2.8, 0.4])

with top_left:
    job_description = st.text_area("Paste Job Description", height=180)

with top_right:
    uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    skills_db = load_skills()
    skills = extract_skills(resume_text, skills_db)
    ats_score = calculate_ats_score(resume_text, skills)

    outer_left, main_left, main_right, outer_right = st.columns([0.4, 2.4, 1.2, 0.4])

    with main_left:
        st.markdown('<div class="section-title">Extracted Resume Text</div>', unsafe_allow_html=True)
        st.text_area("Resume Content", resume_text, height=420)

    with main_right:
        st.markdown('<div class="section-title">ATS Score</div>', unsafe_allow_html=True)
        st.progress(ats_score / 100)
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Score</div>
                <div class="metric-value">{ats_score}/100</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")
        st.markdown('<div class="section-title">Skills</div>', unsafe_allow_html=True)

        if skills:
            skill_html = "".join(
                [f'<span class="skill-pill skill-pill-blue">{skill.title()}</span>' for skill in skills]
            )
            st.markdown(skill_html, unsafe_allow_html=True)
        else:
            st.write("No skills detected")

    if job_description.strip():
        matched_skills, missing_skills, match_score = match_resume_with_jd(
            resume_text, job_description, skills_db
        )

        score_color = get_score_color(match_score)

        st.write("")
        st.markdown('<div class="section-title">Job Match Analysis</div>', unsafe_allow_html=True)

        spacer1, c1, c2, c3, spacer2 = st.columns([0.4, 1, 1, 1, 0.4])

        with c1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">Match Score</div>
                    <div class="metric-value" style="color:{score_color};">{match_score}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">Matched</div>
                    <div class="metric-value">{len(matched_skills)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-label">Missing</div>
                    <div class="metric-value">{len(missing_skills)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        _, progress_col, _ = st.columns([0.4, 3.2, 0.4])
        with progress_col:
            st.progress(match_score / 100)

        _, matched_col, _ = st.columns([0.4, 3.2, 0.4])
        with matched_col:
            st.markdown("### Matched Skills")
            if matched_skills:
                matched_html = "".join(
                    [f'<span class="skill-pill skill-pill-green">{skill.title()}</span>' for skill in matched_skills]
                )
                st.markdown(matched_html, unsafe_allow_html=True)
            else:
                st.write("None")

            st.markdown("### Missing Skills")
            if missing_skills:
                missing_html = "".join(
                    [f'<span class="skill-pill skill-pill-red">{skill.title()}</span>' for skill in missing_skills]
                )
                st.markdown(missing_html, unsafe_allow_html=True)
            else:
                st.write("None")

            report = f"""
AI RESUME ANALYSIS REPORT

ATS Score: {ats_score}/100
Match Score: {match_score}%

Detected Skills:
{', '.join(skills)}

Matched Skills:
{', '.join(matched_skills)}

Missing Skills:
{', '.join(missing_skills)}
"""

            st.download_button(
                label="📄 Download Report",
                data=report,
                file_name="resume_analysis.txt",
                mime="text/plain"
            )
    else:
        st.warning("Please paste a job description to see match analysis.")