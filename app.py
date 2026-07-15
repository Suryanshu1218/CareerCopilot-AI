import re
import streamlit as st

from agents.coordinator import CoordinatorAgent
from tools.resume_parser import extract_resume_text
from tools.learning_resources import get_learning_resources
from tools.progress_tool import load_progress, save_progress
from utils.pdf_generator import create_pdf


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CareerCopilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* ===========================================
GENERAL APP
=========================================== */

.stApp{
    background-color:#0B1120;
    color:#FFFFFF;
}

.block-container{
    max-width:1300px;
    padding-top:2rem;
    padding-bottom:2rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* Hide Streamlit Branding */
#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* ===========================================
HEADINGS
=========================================== */

h1{
    color:white;
    font-size:52px;
    font-weight:800;
    margin-bottom:5px;
}

h2{
    color:white;
    font-weight:700;
}

h3{
    color:white;
    font-weight:600;
}

h4{
    color:white;
}

label{
    color:white !important;
}

/* ===========================================
TEXT
=========================================== */

p{
    color:#B8C1CC;
    font-size:16px;
}

small{
    color:#94A3B8;
}

/* ===========================================
CUSTOM TITLES
=========================================== */

.hero-title{
    font-size:52px;
    font-weight:800;
    color:white;
    margin-bottom:8px;
}

.hero-subtitle{
    font-size:22px;
    color:#94A3B8;
    margin-bottom:30px;
}

.section-title{
    font-size:28px;
    font-weight:700;
    color:white;
}

.section-description{
    color:#94A3B8;
    font-size:16px;
    margin-bottom:20px;
}

/* ===========================================
SIDEBAR
=========================================== */

[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid #1F2937;
}

[data-testid="stSidebar"] *{
    color:white;
}

/* ===========================================
TEXT INPUTS
=========================================== */

textarea{
    background:#111827 !important;
    color:white !important;
    border-radius:14px !important;
    border:1px solid #334155 !important;
}

input{
    background:#111827 !important;
    color:white !important;
    border-radius:12px !important;
    border:1px solid #334155 !important;
}

/* ===========================================
FILE UPLOADER
=========================================== */

[data-testid="stFileUploader"]{
    border:2px dashed #2563EB;
    border-radius:16px;
    padding:18px;
    background:#111827;
}

/* ===========================================
BUTTONS
=========================================== */

.stButton>button{

    width:100%;

    background:#2563EB;

    color:white;

    border:none;

    border-radius:14px;

    padding:14px;

    font-size:17px;

    font-weight:700;

    transition:0.25s;
}

.stButton>button:hover{

    background:#1D4ED8;

    transform:translateY(-2px);

    box-shadow:0 10px 25px rgba(37,99,235,.35);
}

/* ===========================================
TABS
=========================================== */

button[data-baseweb="tab"]{

    color:#94A3B8;

    font-weight:600;

    font-size:15px;
}

button[data-baseweb="tab"][aria-selected="true"]{

    color:white;

    border-bottom:3px solid #2563EB;
}

/* ===========================================
EXPANDERS
=========================================== */

details{

    background:#111827;

    border-radius:14px;

    border:1px solid #1F2937;

    margin-bottom:12px;
}

summary{

    color:white;

    font-weight:600;
}

/* ===========================================
METRIC CARDS
=========================================== */

.metric-card{

    background:linear-gradient(145deg,#111827,#1F2937);

    border:1px solid rgba(255,255,255,.08);

    border-radius:18px;

    padding:24px;

    text-align:center;

    transition:0.25s;

    margin-bottom:18px;

    box-shadow:0 8px 20px rgba(0,0,0,.25);
}

.metric-card:hover{

    transform:translateY(-4px);

    border:1px solid #3B82F6;

    box-shadow:0 12px 28px rgba(59,130,246,.25);
}

.metric-title{

    color:#94A3B8;

    font-size:15px;

    margin-bottom:12px;
}

.metric-value{

    color:white;

    font-size:36px;

    font-weight:800;
}

.metric-subtitle{

    color:#60A5FA;

    font-size:14px;

    margin-top:8px;
}

/* ===========================================
DIVIDER
=========================================== */

hr{

    border-color:#1F2937;
}

/* ===========================================
SCROLLBAR
=========================================== */

::-webkit-scrollbar{

    width:10px;
}

::-webkit-scrollbar-track{

    background:#111827;
}

::-webkit-scrollbar-thumb{

    background:#374151;

    border-radius:10px;
}

::-webkit-scrollbar-thumb:hover{

    background:#4B5563;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🚀 CareerCopilot AI")

    st.caption("Version 2.0")

    st.divider()

    st.markdown("### Features")

    st.markdown("✔ Resume Analysis")
    st.markdown("✔ Skill Gap Detection")
    st.markdown("✔ Learning Roadmap")
    st.markdown("✔ Portfolio Builder")
    st.markdown("✔ Interview Coach")
    st.markdown("✔ Resume Optimizer")
    st.markdown("✔ Job Recommendations")

    st.divider()

    st.caption("Powered by Google Gemini 2.5 Flash") 

# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

st.markdown(
"""
<div style="
padding:35px;
border-radius:20px;
background:linear-gradient(135deg,#111827,#0F172A);
border:1px solid #1F2937;
margin-bottom:25px;
">

<h1 style="
margin-bottom:10px;
font-size:56px;
font-weight:800;
color:white;
">
🚀 CareerCopilot AI
</h1>

<p style="
font-size:22px;
color:#93C5FD;
font-weight:600;
margin-top:0px;
margin-bottom:18px;
">
AI-Powered Career Intelligence Platform
</p>

<p style="
font-size:18px;
line-height:1.8;
color:#CBD5E1;
max-width:900px;
">

Analyze your resume, discover skill gaps, generate personalized learning roadmaps,
build impressive portfolio projects, prepare for technical interviews, optimize your resume
for ATS systems, and explore tailored job opportunities—all powered by Google Gemini AI.

</p>

</div>
""",
unsafe_allow_html=True
)

# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
<div style="
background:#111827;
padding:20px;
border-radius:16px;
border:1px solid #1F2937;
height:170px;
">

<h3>📄 Resume Analysis</h3>

<p>
Receive a professional resume review with strengths, weaknesses,
ATS optimization tips and hiring readiness score.
</p>

</div>
""", unsafe_allow_html=True)

with col2:

    st.markdown("""
<div style="
background:#111827;
padding:20px;
border-radius:16px;
border:1px solid #1F2937;
height:170px;
">

<h3>🎯 Skill Gap Detection</h3>

<p>
Discover missing technical skills, recommended certifications,
learning priorities and technologies required for your dream role.
</p>

</div>
""", unsafe_allow_html=True)

with col3:

    st.markdown("""
<div style="
background:#111827;
padding:20px;
border-radius:16px;
border:1px solid #1F2937;
height:170px;
">

<h3>🛣️ Career Roadmap</h3>

<p>
Generate structured 30-Day, 60-Day and 90-Day learning plans
designed specifically for your target career.
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:

    st.markdown("""
<div style="
background:#111827;
padding:20px;
border-radius:16px;
border:1px solid #1F2937;
height:170px;
">

<h3>💼 Portfolio Projects</h3>

<p>
Receive practical project ideas with objectives,
technology stack, GitHub ideas and expected outcomes.
</p>

</div>
""", unsafe_allow_html=True)

with col5:

    st.markdown("""
<div style="
background:#111827;
padding:20px;
border-radius:16px;
border:1px solid #1F2937;
height:170px;
">

<h3>🎤 Interview Preparation</h3>

<p>
Practice technical, HR and behavioral interview questions
with expert interview tips and common mistakes to avoid.
</p>

</div>
""", unsafe_allow_html=True)

with col6:

    st.markdown("""
<div style="
background:#111827;
padding:20px;
border-radius:16px;
border:1px solid #1F2937;
height:170px;
">

<h3>💼 Job Recommendations</h3>

<p>
Explore AI-generated job recommendations based on
your resume, skills and target career path.
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.info(
    "💡 Upload your resume below, choose your target role, and let CareerCopilot AI generate your personalized career strategy in under a minute."
)
# --------------------------------------------------
# INPUTS
# --------------------------------------------------

with st.container(border=True):

    st.subheader("📄 Resume Details")

    resume_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    resume_text = st.text_area(
        "Or Paste Resume",
        height=220
    )

    target_role = st.text_input(
        "Target Job Role",
        placeholder="Example: AI Engineer"
    )

    analyze = st.button(
        "🚀 Analyze Resume",
        use_container_width=True
    )
if analyze:

    if resume_file is not None:
        resume_text = extract_resume_text(resume_file)

    if not resume_text.strip():
        st.error("Please upload or paste your resume.")
        st.stop()

    if not target_role.strip():
        st.error("Please enter a target job role.")
        st.stop()

    try:

        with st.spinner("🤖 AI Agents are analyzing your resume..."):

            coordinator = CoordinatorAgent()

            results = coordinator.run(
                resume_text=resume_text,
                target_role=target_role
            )

        st.success("✅ Analysis Complete!")

        resume = results["resume"]
        skills = results["skills"]
        roadmap = results["roadmap"]
        projects = results["projects"]
        interview = results["interview"]
        improvements = results["improvements"]
        jobs = results["jobs"]
        
        # --------------------------------------------------
        # Helper function
        # --------------------------------------------------

        def show_text_or_list(data, style="write"):
            """
            Displays either a string or a list cleanly.
            """

            if isinstance(data, list):
                for item in data:
                    if style == "success":
                        st.success(item)
                    elif style == "warning":
                        st.warning(item)
                    elif style == "info":
                        st.info(item)
                    else:
                        st.write("•", item)

            elif isinstance(data, str):
                st.write(data)
                
        def metric_card(title, value, subtitle=""):
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-subtitle">{subtitle}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        # --------------------------------------------------
        # CAREER DASHBOARD
        # --------------------------------------------------

        st.divider()

        st.markdown(
            """
        <div class="section-title">
        📊 Career Dashboard
        </div>

        <div class="section-description">
        A quick overview of your current career readiness based on your resume analysis.
        </div>
        """,
            unsafe_allow_html=True
        )

        # ---------------- Resume Score ----------------

        resume_score = resume.get("Readiness Score", "N/A")

        # ---------------- Skill Match ----------------

        try:
            score = int(str(resume_score).split("/")[0])
        except:
            score = 0

        skill_match = max(score - 5, 0)

        # ---------------- Skills To Learn ----------------

        missing_skills = skills.get("Missing Skills", "")

        if isinstance(missing_skills, str):
            skills_to_learn = max(
                6,
                missing_skills.count(".") + missing_skills.count(";")
            )
        else:
            skills_to_learn = len(missing_skills)

        # ---------------- Portfolio Projects ----------------

        project_count = len(
            projects.get("Portfolio Projects", [])
        )

        # ---------------- Interview Questions ----------------

        technical = len(
            interview.get("Technical Questions", [])
        )

        hr = len(
            interview.get("HR Questions", [])
        )

        behavioral = len(
            interview.get("Behavioral Questions", [])
        )

        question_count = technical + hr + behavioral

        # ---------------- Jobs ----------------

        job_count = len(
            jobs.get("Job Recommendations", [])
        )

        # ---------------- Dashboard ----------------

        col1, col2, col3 = st.columns(3)

        with col1:
            metric_card(
                "⭐ Resume Score",
                resume_score,
                "Career Readiness"
            )

        with col2:
            metric_card(
                "🎯 Skill Match",
                f"{skill_match}%",
                "Current Match"
            )

        with col3:
            metric_card(
                "📚 Skills To Learn",
                skills_to_learn,
                "Recommended"
            )

        col4, col5, col6 = st.columns(3)

        with col4:
            metric_card(
                "💼 Portfolio Projects",
                project_count,
                "Suggested"
            )

        with col5:
            metric_card(
                "🎤 Interview Questions",
                question_count,
                "Generated"
            )

        with col6:
            metric_card(
                "🏆 Job Matches",
                job_count,
                "Recommended"
            )
        # --------------------------------------------------
        # ANALYSIS TABS
        # --------------------------------------------------

        st.divider()

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📄 Resume",
            "🎯 Skills",
            "🗺️ Roadmap",
            "💼 Projects",
            "🎤 Interview",
            "✨ Improvements",
            "💼 Jobs"
        ])

        # --------------------------------------------------
        # TAB 1 : Resume Analysis
        # --------------------------------------------------

        with tab1:

            st.subheader("📝 Candidate Summary")
            st.write(resume.get("Candidate Summary", ""))

            st.subheader("🎓 Education Analysis")
            st.write(resume.get("Education Analysis", ""))

            st.subheader("💼 Experience Analysis")
            st.write(resume.get("Experience Analysis", ""))

            st.subheader("💻 Technical Skills Analysis")
            st.write(resume.get("Technical Skills Analysis", ""))

            st.subheader("🤝 Soft Skills Analysis")
            st.write(resume.get("Soft Skills Analysis", ""))

            st.subheader("✅ Strengths")

            for item in resume.get("Strengths", []):
                st.markdown(f"- {item}")
                
            st.subheader("⚠️ Weaknesses")

            for item in resume.get("Weaknesses", []):
                st.markdown(f"- {item}")

            st.subheader("🎯 Hiring Chances")
            st.markdown(f"- {resume.get('Hiring Chances', '')}")

            st.subheader("📊 Readiness Score")
            st.markdown(f"- {resume.get('Readiness Score', '')}")


        # --------------------------------------------------
        # TAB 2 : Skill Gap
        # --------------------------------------------------

        with tab2:

            st.subheader("✅ Existing Skills")
            st.write(skills.get("Existing Skills", ""))

            st.divider()

            st.subheader("❌ Missing Skills")
            st.write(skills.get("Missing Skills", ""))

            st.divider()

            st.subheader("🎯 Learning Priority")
            st.write(skills.get("Learning Priority", ""))

            st.divider()

            st.subheader("📜 Recommended Certifications")

            for cert in skills.get("Recommended Certifications", []):
                st.write("•", cert)

            st.divider()

            st.subheader("🛠 Recommended Tools")

            for tool in skills.get("Recommended Tools", []):
                st.write("•", tool)

            st.divider()

            st.subheader("⚙️ Recommended Technologies")

            for tech in skills.get("Recommended Technologies", []):
                st.write("•", tech)


            # --------------------------------------------------
            # TAB 3 : Learning Roadmap
            # --------------------------------------------------

            with tab3:

                st.header("🛣️ Personalized Learning Roadmap")

                st.write(
                    "Choose the roadmap that best matches your available learning time."
                )

                st.divider()

                # ==============================================
                # 30 DAY ROADMAP
                # ==============================================

                st.subheader("🗓️ 30-Day Roadmap")

                roadmap30 = roadmap.get("30-Day Roadmap", {})

                for week, plan in roadmap30.items():

                    with st.expander(f"📅 {week}", expanded=False):

                        # In case Gemini returns only a string
                        if isinstance(plan, str):

                            st.write(plan)

                        # In case Gemini returns structured JSON
                        elif isinstance(plan, dict):

                            st.markdown("### 📚 Topics")
                            st.write(plan.get("Topics", ""))

                            st.markdown("### 💻 Practice")
                            st.write(plan.get("Practice", ""))

                            st.markdown("### 🚀 Mini Project")
                            st.write(plan.get("Mini Project", ""))

                            st.markdown("### 🎯 Expected Outcome")
                            st.write(plan.get("Expected Outcome", ""))

                st.divider()

                # ==============================================
                # 60 DAY ROADMAP
                # ==============================================

                st.subheader("🗓️ 60-Day Roadmap")

                roadmap60 = roadmap.get("60-Day Roadmap", {})

                for week, plan in roadmap60.items():

                    with st.expander(f"📅 {week}"):

                        if isinstance(plan, str):

                            st.write(plan)

                        elif isinstance(plan, dict):

                            st.markdown("### 📚 Topics")
                            st.write(plan.get("Topics", ""))

                            st.markdown("### 💻 Practice")
                            st.write(plan.get("Practice", ""))

                            st.markdown("### 🚀 Mini Project")
                            st.write(plan.get("Mini Project", ""))

                            st.markdown("### 🎯 Expected Outcome")
                            st.write(plan.get("Expected Outcome", ""))

                # ==============================================
                # 90 DAY ROADMAP
                # ==============================================

                st.subheader("🗓️ 90-Day Roadmap")

                roadmap90 = roadmap.get("90-Day Roadmap", {})

                for month, plan in roadmap90.items():

                    with st.expander(f"📅 {month}"):

                        if isinstance(plan, str):

                            st.write(plan)

                        elif isinstance(plan, dict):

                            st.markdown("### 📚 Skills to Learn")
                            st.write(plan.get("Skills to learn", ""))

                            st.markdown("### 💼 Projects")
                            st.write(plan.get("Projects", ""))

                            st.markdown("### 📝 Practice")
                            st.write(plan.get("Practice", ""))

                            st.markdown("### 🎯 Expected Outcome")
                            st.write(
                                plan.get(
                                    "Expected Outcome",
                                    plan.get("Expected outcome", "")
                                )
                            )

        # --------------------------------------------------
        # TAB 4 : Projects
        # --------------------------------------------------

        with tab4:

            st.subheader("💼 Portfolio Projects")

            for project in projects.get("Portfolio Projects", []):

                with st.expander(project.get("Title", "Project")):

                    st.write("### 🎯 Objective")
                    st.write(project.get("Objective", ""))

                    st.write("### 💻 Tech Stack")
                    st.write(project.get("Tech Stack", ""))

                    st.write("### ⭐ Difficulty")
                    st.write(project.get("Difficulty", ""))

                    st.write("### ⏱ Estimated Time")
                    st.write(project.get("Estimated Time", ""))

                    st.write("### 📚 Skills Learned")
                    st.write(project.get("Skills Learned", ""))

                    st.write("### 🚀 GitHub Idea")
                    st.write(project.get("GitHub Idea", ""))


        # --------------------------------------------------
        # TAB 5 : Interview
        # --------------------------------------------------

        with tab5:

            st.subheader("💻 Technical Questions")

            for question in interview.get("Technical Questions", []):
                st.write("•", question)

            st.divider()

            st.subheader("👨‍💼 HR Questions")

            for question in interview.get("HR Questions", []):
                st.write("•", question)

            st.divider()

            st.subheader("🤝 Behavioral Questions")

            for question in interview.get("Behavioral Questions", []):
                st.write("•", question)

            st.divider()

            st.subheader("✅ Interview Tips")

            for tip in interview.get("Interview Tips", []):
                st.markdown(f"- {tip}")

            st.divider()

            st.subheader("❌ Common Mistakes")

            for mistake in interview.get("Common Mistakes", []):
                st.markdown(f"- {mistake}")


        # --------------------------------------------------
        # TAB 6 : Improvements
        # --------------------------------------------------

        with tab6:

            st.subheader("📝 Resume Improvements")

            for item in improvements.get("Resume Improvements", []):
                st.write("•", item)

            st.divider()

            st.subheader("🤖 ATS Suggestions")

            for item in improvements.get("ATS Suggestions", []):
                st.markdown(f"- {item}")

            st.divider()

            st.subheader("🔗 LinkedIn Improvements")

            for item in improvements.get("LinkedIn Improvements", []):
                st.write("•", item)

            st.divider()

            st.subheader("🌐 Portfolio Improvements")

            for item in improvements.get("Portfolio Improvements", []):
                st.write("•", item)


        # --------------------------------------------------
        # TAB 7 : Job Recommendations
        # --------------------------------------------------

        with tab7:

            st.subheader("💼 Recommended Jobs")

            for job in jobs.get("Job Recommendations", []):

                with st.expander(job.get("Job Title", "Job")):

                    st.write("### 💼 Job Title")
                    st.write(job.get("Job Title", ""))

                    st.write("### 📌 Why Recommended")
                    st.write(job.get("Why Recommended", ""))

                    st.write("### 💰 Salary Range")
                    st.write(job.get("Salary Range", ""))

                    st.write("### 📈 Experience Level")
                    st.write(job.get("Experience Level", ""))

                    st.write("### 🛠 Required Skills")

                    for skill in job.get("Required Skills", []):
                        st.write("•", skill)
                
        # --------------------------------------------------
        # LEARNING PROGRESS
        # --------------------------------------------------

        st.divider()

        st.subheader("📈 Learning Progress")

        progress = load_progress()
        resources = get_learning_resources()

        skills_to_learn = [
            "Python",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "Git & GitHub"
        ]

        for skill in skills_to_learn:

            checked = st.checkbox(
                skill,
                value=progress.get(skill, False),
                key=f"progress_{skill}"
            )

            progress[skill] = checked

            with st.expander(f"📚 Learn {skill}"):

                for resource in resources.get(skill, []):

                    st.markdown(f"### {resource['name']}")
                    st.write(resource["description"])

                    st.link_button(
                        "Open Resource",
                        resource["url"]
                    )

                    st.divider()

        save_progress(progress)
        
        # --------------------------------------------------
        # DOWNLOAD REPORT
        # --------------------------------------------------

        st.divider()

        st.subheader("📄 Download Career Report")

        try:

            pdf_file = create_pdf(results)

            with open(pdf_file, "rb") as file:

                st.download_button(
                    label="📥 Download PDF Report",
                    data=file,
                    file_name="Career_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        except Exception as e:

            st.warning(
                f"Unable to generate PDF report.\n\n{e}"
            )
            
    except Exception as e:

        st.error(f"❌ {e}")
        st.stop()
        