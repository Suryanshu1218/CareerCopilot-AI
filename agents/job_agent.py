from utils.gemini_client import ask_gemini


class JobAgent:

    def recommend_jobs(self, resume_text, target_role):

        prompt = f"""
You are an experienced AI Career Coach.

A candidate wants to become a {target_role}.

Resume:
{resume_text}

Recommend the 5 most suitable job roles.

Return your answer in Markdown.

Rules:
- Maximum 250 words.
- Use a table.

Table columns:

| Job Role | Match Score | Salary (India) | Why Recommended |

Give realistic salaries in LPA.
"""

        return ask_gemini(prompt)