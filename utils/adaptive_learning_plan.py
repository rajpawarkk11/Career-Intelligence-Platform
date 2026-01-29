def generate_adaptive_plan(role, missing_skills):
    """
    Generates a realistic, industry-aligned learning timeline
    for a fresher to become job-ready in missing skills.
    """

    # REALISTIC time estimates (days) for fresher-level job readiness
    skill_time_map = {
        "python": 15,
        "numpy": 6,
        "pandas": 8,
        "statistics": 10,
        "sql": 10,
        "machine": 18,
        "learning": 18,
        "deep": 20,
        "tensorflow": 12,
        "pytorch": 12,
        "excel": 4,
        "powerbi": 7,
        "oop": 8,
        "structures": 15,
        "algorithms": 18,
        "java": 12,
        "c++": 15
    }

    plan = []
    total_days = 0

    for skill in missing_skills:
        days = skill_time_map.get(skill.lower(), 7)  # fallback realistic default
        plan.append({
            "skill": skill,
            "days": days
        })
        total_days += days

    return plan, total_days
