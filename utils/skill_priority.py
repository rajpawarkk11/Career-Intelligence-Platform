def prioritize_skills(all_skills, missing_skills):
    """
    Distribute missing skills into High / Medium / Low priority
    based on importance order.
    """

    high = []
    medium = []
    low = []

    for skill in all_skills:
        if skill in missing_skills:
            if len(high) < 3:
                high.append(skill)
            elif len(medium) < 3:
                medium.append(skill)
            else:
                low.append(skill)

    return {
        "High Priority": high,
        "Medium Priority": medium,
        "Low Priority": low
    }
