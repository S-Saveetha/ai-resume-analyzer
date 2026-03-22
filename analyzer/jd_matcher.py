from analyzer.skill_extractor import extract_skills

def match_resume_with_jd(resume_text, jd_text, skills_db):
    resume_skills = extract_skills(resume_text, skills_db)
    jd_skills = extract_skills(jd_text, skills_db)

    matched_skills = [skill for skill in jd_skills if skill in resume_skills]
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

    match_score = 0
    if len(jd_skills) > 0:
        match_score = round((len(matched_skills) / len(jd_skills)) * 100, 2)

    return matched_skills, missing_skills, match_score