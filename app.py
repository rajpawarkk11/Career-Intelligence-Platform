import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils.resume_parser import extract_text_from_pdf
from utils.skill_matcher import extract_skills
from utils.skill_priority import prioritize_skills
from utils.roadmap_generator import generate_roadmap
from utils.report_generator import generate_pdf_report
from utils.ats_scorer import calculate_ats_score
from utils.ats_tips import generate_ats_tips
from utils.adaptive_learning_plan import generate_adaptive_plan

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Career Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)

# ================= TITLE =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&display=swap');

.title-container { margin-top: 12px; margin-bottom: 24px; }

@keyframes glowMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 52px;
    font-weight: 800;
    background: linear-gradient(270deg,#2563eb,#06b6d4,#22c55e,#2563eb);
    background-size: 600% 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glowMove 6s ease infinite;
}

.sub-title {
    margin-top: 8px;
    font-size: 16px;
    color: #475569;
}
</style>

<div class="title-container">
    <div class="main-title">Career Intelligence Platform</div>
    <div class="sub-title">
        AI-Powered ATS • Multi-Domain Role Engine • Career Decision Dashboard
    </div>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🚀 Career Intelligence")
    st.caption("Enterprise Resume & ATS Analytics")
    username = st.text_input("👤 Your Name", "")
    st.divider()
    compare_mode = st.toggle("🔁 Enable Multi-Resume Comparison")

st.divider()

# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

    roles_df = pd.read_csv("data/job_roles.csv")
    results = []

    for _, row in roles_df.iterrows():
        role = row["role"]
        skills = row["skills"].split()

        matched = extract_skills(resume_text, skills)
        missing = list(set(skills) - set(matched))
        score = int((len(matched) / len(skills)) * 100)

        results.append({
            "role": role,
            "score": score,
            "matched": matched,
            "missing": missing,
            "skills": skills
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    best_role_data = results[0]
    best_role = best_role_data["role"]

    ats_score = calculate_ats_score(
        resume_text,
        best_role_data["matched"],
        len(best_role_data["skills"])
    )

    resume_strength = int(np.mean([r["score"] for r in results]))

    readiness = (
        "Beginner" if resume_strength <= 30 else
        "Intermediate" if resume_strength <= 60 else
        "Job Ready"
    )

    # ================= KPI ROW =================
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("ATS Score", f"{ats_score}/100")
    k2.metric("Resume Strength", f"{resume_strength}%")
    k3.metric("Best Role", best_role)
    k4.metric("Readiness", readiness)

    st.divider()

    # ================= TABS =================
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📊 Analysis", "🧾 ATS Insights", "🧠 Decision", "🔁 Compare", "📄 Report"]
    )

    # ---------- TAB 1: ANALYSIS (FIXED GRAPH) ----------
    with tab1:
        st.subheader("Top Matching Career Roles")

        top_roles = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )[:12]

        roles = [r["role"] for r in top_roles]
        scores = [r["score"] for r in top_roles]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(roles, scores)
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xlabel("Match Score (%)")
        ax.set_title("Top 12 Role Match Distribution")

        st.pyplot(fig)

    # ---------- TAB 2: ATS ----------
    with tab2:
        st.subheader("ATS Resume Insights")
        st.metric("ATS Score", f"{ats_score}/100")

        st.markdown("### Suggestions to Improve ATS")
        for tip in generate_ats_tips(ats_score, resume_text):
            st.write(f"• {tip}")

    # ---------- TAB 3: DECISION ----------
    with tab3:
        st.markdown(f"### Why **{best_role}** is recommended")

        if len(best_role_data["matched"]) >= 3:
            st.success("Strong overlap with required skills")
        if "project" in resume_text.lower():
            st.success("Hands-on project experience detected")
        if ats_score >= 40:
            st.success("Resume is ATS-friendly")

        st.divider()
        st.subheader("⏱️ Skill-Based Adaptive Learning Timeline")

        plan, total_days = generate_adaptive_plan(
            best_role,
            best_role_data["missing"]
        )

        if plan:
            for item in plan:
                st.write(f"• **{item['skill']}** → ~{item['days']} days")

            st.markdown(f"### Estimated Total Time: **~{total_days} days**")

    # ---------- TAB 4: COMPARE ----------
    with tab4:
        if compare_mode:
            files = st.file_uploader(
                "Upload 2–3 resumes (PDF)",
                type=["pdf"],
                accept_multiple_files=True
            )

            if files and len(files) >= 2:
                rows = []
                base_skills = best_role_data["skills"]

                for f in files[:3]:
                    text = extract_text_from_pdf(f)
                    matched = extract_skills(text, base_skills)
                    missing = list(set(base_skills) - set(matched))

                    ats = calculate_ats_score(text, matched, len(base_skills))
                    strength = int((len(matched) / len(base_skills)) * 100)

                    fit = "High Fit" if strength >= 70 else "Medium Fit" if strength >= 40 else "Low Fit"

                    rows.append({
                        "Resume": f.name,
                        "ATS Score": ats,
                        "Resume Strength (%)": strength,
                        "Matched Skills": len(matched),
                        "Missing Skills": len(missing),
                        "Fit Level": fit
                    })

                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True)
                st.bar_chart(df.set_index("Resume")[["ATS Score"]])

        else:
            st.info("Enable multi-resume comparison from sidebar")

    # ---------- TAB 5: REPORT ----------
    with tab5:
        skill_priority = prioritize_skills(
            best_role_data["skills"],
            best_role_data["missing"]
        )
        roadmap = generate_roadmap(skill_priority)

        if st.button("⬇️ Generate Career Report (PDF)"):
            pdf = generate_pdf_report(
                username,
                best_role,
                resume_strength,
                readiness,
                skill_priority,
                roadmap
            )
            with open(pdf, "rb") as f:
                st.download_button(
                    "Download PDF",
                    data=f,
                    file_name=pdf,
                    mime="application/pdf"
                )


st.caption("Career Intelligence Platform • Professional Modern AI Dashboard")







