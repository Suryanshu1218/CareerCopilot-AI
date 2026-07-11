from utils.gemini_client import ask_gemini


class ProjectAgent:

    def recommend_projects(self, resume_text, target_role):

        prompt = f"""
Suggest 5 portfolio projects for becoming a {target_role}.

Resume:
{resume_text}

For each project include:

Project Name

Difficulty

Technologies

Description (2-3 lines)

Learning Outcome (2 bullets)

Rules:
- Maximum 300 words.
- No essays.
"""
        return ask_gemini(prompt)