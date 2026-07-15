from utils.gemini_client import ask_gemini


class CareerMasterAgent:

    def analyze(self, resume_text: str, target_role: str):

        prompt = f"""
You are an expert AI Career Coach, Resume Reviewer, Interview Coach, and Career Mentor.

Analyze the following resume for the target role and return a detailed career report.

Target Role:
{target_role}

Resume:
{resume_text}

IMPORTANT RULES

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT wrap the response inside ```json.
- Do NOT include explanations outside JSON.
- Every field must contain useful and detailed information.
- Keep the response balanced: informative but not excessively long.

Return EXACTLY this JSON structure:

Return EXACTLY this JSON structure:

{{
    "resume": {{
        "Candidate Summary": "",
        "Education Analysis": "",
        "Experience Analysis": "",
        "Technical Skills Analysis": "",
        "Soft Skills Analysis": "",
        "Strengths": [],
        "Weaknesses": [],
        "Hiring Chances": "",
        "Readiness Score": "",
        "Score Explanation": ""
    }},

    "skills": {{
        "Existing Skills": "",
        "Missing Skills": "",
        "Learning Priority": "",
        "Recommended Certifications": [],
        "Recommended Tools": [],
        "Recommended Technologies": []
    }},

    "roadmap": {{
        "30-Day Roadmap": {{
            "Week 1": "",
            "Week 2": "",
            "Week 3": "",
            "Week 4": ""
        }},

        "60-Day Roadmap": {{
            "Week 1-2": "",
            "Week 3-4": "",
            "Week 5-6": "",
            "Week 7-8": ""
        }},

        "90-Day Roadmap": {{
            "Month 1": "",
            "Month 2": "",
            "Month 3": ""
        }}
    }},

    "projects": {{
        "Portfolio Projects": [
            {{
                "Title": "",
                "Objective": "",
                "Tech Stack": "",
                "Difficulty": "",
                "Estimated Time": "",
                "Skills Learned": "",
                "GitHub Idea": ""
            }}
        ]
    }},

    "interview": {{
        "Technical Questions": [],
        "HR Questions": [],
        "Behavioral Questions": [],
        "Interview Tips": [],
        "Common Mistakes": []
    }},

    "improvements": {{
        "Resume Improvements": [],
        "ATS Suggestions": [],
        "LinkedIn Improvements": [],
        "Portfolio Improvements": []
    }},

    "jobs": {{
        "Job Recommendations": [
            {{
                "Job Title": "",
                "Why Recommended": "",
                "Salary Range": "",
                "Experience Level": "",
                "Required Skills": []
            }}
        ]
    }}
}}

CONTENT REQUIREMENTS

Resume
- Candidate Summary should be 8-10 sentences.
- Education Analysis should explain how the education matches the target role.
- Experience Analysis should evaluate projects, internships, and work experience.
- Technical Skills Analysis should discuss current technical strengths and weaknesses.
- Soft Skills Analysis should evaluate communication, teamwork, leadership, and problem solving.
- Give 6-8 strengths.
- Give 6-8 weaknesses.
- Hiring Chances should explain employability in detail.
Readiness Score:
- Return ONLY the numeric score in the format:
15/100

Score Explanation:
- Write 2–3 sentences explaining the score.

Skills
For the "Existing Skills" field:
- Write 2-3 well-structured paragraphs.
- Explain what technical skills the candidate already possesses.
- Mention strengths and current proficiency.
- Do NOT return a list.

For the "Missing Skills" field:
- Write 2-3 paragraphs.
- Explain which important skills are missing for the target role.
- Explain why each category of missing skills matters.
- Do NOT return a list.

For the "Learning Priority" field:
- Write 2-3 paragraphs.
- Explain the ideal learning sequence.
- Mention what should be learned first, second and third.
- Give reasons for the order.
- Do NOT return a list.

- Return 8-12 detailed action items in logical order.
- Recommend 5-8 certifications.
- Recommend commonly used AI tools.
- Recommend technologies required for the target role.

ROADMAP REQUIREMENTS

Generate THREE completely separate learning plans.

Do NOT continue one roadmap into another.

Instead create:

1. 30-Day Roadmap
- Beginner friendly
- Covers only the first 30 days
- Weekly milestones
- Weekly goals
- Weekly tasks

2. 60-Day Roadmap
Imagine the learner has exactly 60 days available.

Create a fresh roadmap from Day 1.

Do NOT continue the 30-day roadmap.

Include:

- Week 1-2
- Week 3-4
- Week 5-6
- Week 7-8

Each section should contain:

• Topics
• Practice
• Mini Project
• Expected Outcome

3. 90-Day Roadmap

Imagine the learner has 90 days available.

Create another completely independent roadmap starting from Day 1.

Do NOT continue the 60-day roadmap.

Include:

Month 1
Month 2
Month 3

Each month should include:

• Skills to learn
• Projects
• Practice
• Expected outcome

Every roadmap should be self-contained.

Each roadmap should contain weekly milestones, learning goals, and practical tasks.

Projects
Recommend 5 portfolio projects.

For EACH project include:
- Title
- Objective
- Tech Stack
- Difficulty
- Estimated Time
- Skills Learned
- GitHub Project Idea

Interview
Generate:
- 10 Technical Questions
- 10 HR Questions
- 5 Behavioral Questions
- 10 Interview Tips
- 10 Common Mistakes

Improvements
Provide:
- 10 Resume Improvements
- 8 ATS Suggestions
- 8 LinkedIn Improvements
- 8 Portfolio Improvements

Jobs
Recommend 10 suitable jobs.

For EACH job include:
- Job Title
- Why Recommended
- Salary Range (estimated)
- Experience Level
- Required Skills

Return ONLY valid JSON.
"""

        return ask_gemini(
            prompt,
            expect_json=True
        )