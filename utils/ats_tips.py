def generate_ats_tips(ats_score, resume_text):
    tips = []

    if ats_score < 40:
        tips.append("Add more role-specific technical keywords.")
        tips.append("Mention projects with clear responsibilities.")
        tips.append("Include a dedicated skills section.")

    if "project" not in resume_text:
        tips.append("Add a 'Projects' section with technologies used.")

    if "experience" not in resume_text:
        tips.append("Include internship or practical experience details.")

    word_count = len(resume_text.split())
    if word_count < 300:
        tips.append("Increase resume length with relevant technical content.")
    elif word_count > 1000:
        tips.append("Reduce resume length to keep it concise.")

    if not tips:
        tips.append("Your resume is well optimized for ATS systems.")

    return tips
