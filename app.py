from tools.learning_resources import get_learning_resources
from utils.pdf_generator import create_pdf
from tools.progress_tool import load_progress, save_progress
import streamlit as st

from agents.coordinator import CoordinatorAgent
from tools.resume_parser import extract_resume_text

# Configure the page
st.set_page_config(
    page_title="CareerCopilot AI",
    page_icon="🚀",
    layout="wide"
)

# Sidebar
with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

    st.title("CareerCopilot AI")

    st.caption("Your Personal AI Career Coach")

    st.markdown("---")

    st.subheader("✨ Features")

    st.success("Resume Analysis")

    st.success("Skill Gap Detection")

    st.success("Learning Roadmap")

    st.success("Portfolio Projects")

    st.success("Interview Preparation")

    st.success("Resume Improvements")

    st.success("Job Recommendations")

    st.markdown("---")

    st.info("Powered by Google Gemini 2.5 Flash")

# Main Title
st.title("🚀 CareerCopilot AI")
st.markdown("""
### Your Personal AI Career Coach

Upload your resume, choose your dream role, and receive:

- 📄 Resume Analysis
- 🎯 Skill Gap Detection
- 📚 Personalized Learning Roadmap
- 💼 Portfolio Project Ideas
- 🎤 Interview Preparation
- ✨ Resume Improvement Suggestions
- 🔍 Job Recommendations

Everything is powered by Google Gemini AI.
""")

st.info(
    "💡 Tip: Upload your latest resume and choose your target role to get the most accurate career recommendations."
)

st.divider()

# Upload Resume
resume_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

# Paste Resume
resume_text = st.text_area(
    "Or Paste Your Resume",
    height=200
)

# Target Role
target_role = st.text_input(
    "Target Job Role",
    placeholder="Example: AI Engineer"
)

# Analyze Button
analyze_button = st.button("Analyze Resume")

if analyze_button:

    # Extract PDF text if uploaded
    if resume_file is not None:
        resume_text = extract_resume_text(resume_file)

    # Validation
    if not resume_text.strip():
        st.error("Please upload or paste your resume.")
        st.stop()

    if not target_role.strip():
        st.error("Please enter a target job role.")
        st.stop()

    try:
        with st.spinner("🤖 CareerCopilot AI is analyzing your resume... Please wait..."):

            coordinator = CoordinatorAgent()

            results = coordinator.run(
                resume_text,
                target_role
            )

        st.success("✅ Resume analyzed successfully!")

        # -------------------------------
        # Dashboard Calculations
        # -------------------------------
        import re

        st.subheader("📊 Career Dashboard")

        # ---------------- Resume Score ----------------
        resume_score = "N/A"

        match = re.search(r'(\d+)\s*/\s*10', results.get("resume", ""))

        if match:
           resume_score = f"{match.group(1)}/10"

        # ---------------- Missing Skills ----------------
        skills_text = results.get("skills", "")

        missing_skills = 0

        if "Missing Skills" in skills_text:
           section = skills_text.split("Missing Skills")[-1]
           missing_skills = section.count("-") + section.count("•")

        # ---------------- Projects ----------------
        projects_text = results.get("projects", "")

        project_count = (
           projects_text.count("Difficulty")
    +      projects_text.count("Project")
        )

        if project_count == 0:
          project_count = 5

        # ---------------- Interview Questions ----------------
        interview_text = results.get("interview", "")

        question_count = interview_text.count("?")

        if question_count == 0:
          question_count = (
             interview_text.count("-")
             + interview_text.count("•")
          )

        # ---------------- Dashboard ----------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
          st.metric("Resume Score", resume_score)

        with col2:
          st.metric("Missing Skills", missing_skills)

        with col3:
          st.metric("Projects", project_count)
 
        with col4:
          st.metric("Interview Questions", question_count)

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📄 Resume Analysis",
        "🎯 Skill Gap",
        "🗺️ Roadmap",
        "💼 Projects",
        "🎤 Interview",
        "✨ Improvements",
        "💼 Job Recommendations"
        ])

        with tab1:
            st.markdown(results.get("resume", "No resume analysis available."))

        with tab2:
            st.markdown(results.get("skills", "No skill gap analysis available."))

        with tab3:
            st.markdown(results.get("roadmap", "No roadmap available."))

        with tab4:
            st.markdown(results.get("projects", "No project suggestions available."))

        with tab5:
            st.markdown(results.get("interview", "No interview preparation available."))

        with tab6:
            st.markdown(results.get("improvements", "No suggestions available."))

        with tab7:
           st.markdown(
              results.get(
                "jobs",
                "No job recommendations available."
              )
            )

        st.divider()

        st.subheader("📈 Learning Progress")

        progress = load_progress()
        resources = get_learning_resources()
        
        skills = [
            "Python",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "Git & GitHub"
        ]

        for skill in skills:

            checked = st.checkbox(
                skill,
                value=progress.get(skill, False)
            )

            progress[skill] = checked

            with st.expander(f"📚 Learn {skill}"):

              for resource in resources.get(skill, []):

                st.markdown(f"### 📘 {resource['name']}")
                st.write(resource["description"])
                st.link_button("Open Resource", resource["url"])
                st.divider()

        # Save progress
        save_progress(progress)

        # Generate PDF
        pdf_file = create_pdf(results)

        # Download Button
        with open(pdf_file, "rb") as file:
            st.download_button(
                label="📄 Download Career Report",
                data=file,
                file_name="Career_Report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")