from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf_report(
    username,
    best_role,
    overall_score,
    readiness,
    skill_priority,
    roadmap
):
    filename = f"Career_Report_{username.replace(' ', '_')}.pdf"
    filepath = os.path.join(os.getcwd(), filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Career Analysis Report")
    y -= 30

    # Meta info
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Name: {username}")
    y -= 15
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%d %b %Y')}")
    y -= 30

    # Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Summary")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Best Career Match: {best_role}")
    y -= 15
    c.drawString(50, y, f"Overall Resume Strength: {overall_score}%")
    y -= 15
    c.drawString(50, y, f"Career Readiness Level: {readiness}")
    y -= 30

    # Skill Priority
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Skill Priority Ranking")
    y -= 20

    c.setFont("Helvetica", 11)
    for level, skills in skill_priority.items():
        c.drawString(50, y, f"{level}:")
        y -= 15
        if skills:
            for s in skills:
                c.drawString(70, y, f"- {s}")
                y -= 15
        else:
            c.drawString(70, y, "None")
            y -= 15
        y -= 5

    y -= 10

    # Learning Roadmap
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Learning Roadmap")
    y -= 20

    c.setFont("Helvetica", 11)
    for phase, skills in roadmap.items():
        c.drawString(50, y, phase)
        y -= 15
        if skills:
            for s in skills:
                c.drawString(70, y, f"- {s}")
                y -= 15
        else:
            c.drawString(70, y, "No skills in this phase")
            y -= 15
        y -= 5

    c.save()

    return filepath
