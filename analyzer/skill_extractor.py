def load_skills(filepath="data/skills_db.txt"):
    with open(filepath, "r") as file:
        skills = [line.strip().lower() for line in file if line.strip()]
    return skills


def extract_skills(text, skills_list):
    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))