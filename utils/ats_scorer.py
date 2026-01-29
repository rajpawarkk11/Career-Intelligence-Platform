def calculate_ats_score(resume_text, matched_skills, total_skills):
    # Skill match score (60%)
    skill_score = (len(matched_skills) / total_skills) * 60 if total_skills else 0

    # Keyword density score (25%)
    keywords = ["experience", "project", "skills", "education", "certification"]
    keyword_hits = sum(1 for k in keywords if k in resume_text)
    keyword_score = (keyword_hits / len(keywords)) * 25

    # Resume length score (15%)
    word_count = len(resume_text.split())
    if 300 <= word_count <= 800:
        length_score = 15
    elif 200 <= word_count < 300 or 800 < word_count <= 1000:
        length_score = 10
    else:
        length_score = 5

    total_score = skill_score + keyword_score + length_score
    return int(total_score)
