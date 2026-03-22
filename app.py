import streamlit as st
from parser.resume_parser import extract_text_from_pdf
from analyzer.skill_extractor import load_skills, extract_skills
from analyzer.jd_matcher import match_resume_with_jd
from analyzer.ats_scorer import calculate_ats_score

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("AI Resume Analyzer")

job_description = st.text_area("Paste Job Description", height=150)
uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=300)

    skills_db = load_skills()
    skills = extract_skills(resume_text, skills_db)

    st.subheader("Detected Skills")
    if skills:
        st.write(", ".join([skill.title() for skill in skills]))
    else:
        st.write("No skills detected")

    ats_score = calculate_ats_score(resume_text, skills)

    st.subheader("ATS Score")
    st.progress(ats_score / 100)
    st.write(f"{ats_score}/100")

    if job_description.strip():
        matched_skills, missing_skills, match_score = match_resume_with_jd(
            resume_text, job_description, skills_db
        )

        st.subheader("Job Match Analysis")

        st.write("Match Score")
        st.progress(match_score / 100)
        st.write(f"{match_score}% match")

        st.write("Matched Skills:")
        if matched_skills:
            st.write(", ".join([skill.title() for skill in matched_skills]))
        else:
            st.write("None")

        st.write("Missing Skills:")
        if missing_skills:
            st.write(", ".join([skill.title() for skill in missing_skills]))
        else:
            st.write("None")
    else:
        st.warning("Please paste a job description to see match analysis.")