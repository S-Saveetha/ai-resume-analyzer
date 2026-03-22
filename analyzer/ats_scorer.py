def calculate_ats_score(resume_text, extracted_skills):
    score = 0
    text = resume_text.lower()

    if "education" in text:
        score += 15
    if "skills" in text or "skill" in text:
        score += 15
    if "project" in text or "projects" in text:
        score += 20
    if "experience" in text:
        score += 20
    if len(extracted_skills) >= 5:
        score += 15
    if len(resume_text.split()) >= 150:
        score += 15

    return min(score, 100)