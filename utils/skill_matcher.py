def extract_skills(resume_text, skill_list):
    found_skills = set()
    resume_text = resume_text.lower()

    for skill in skill_list:
        if skill.lower() in resume_text:
            found_skills.add(skill)

    return list(found_skills)

