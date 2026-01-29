def generate_roadmap(skill_priority):
    """
    Generate phase-wise roadmap from prioritized skills.
    """

    roadmap = {
        "Phase 1 — Foundations": skill_priority.get("High Priority", []),
        "Phase 2 — Core Skills": skill_priority.get("Medium Priority", []),
        "Phase 3 — Tools & Frameworks": skill_priority.get("Low Priority", [])
    }

    return roadmap
