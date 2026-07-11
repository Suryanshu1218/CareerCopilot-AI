from utils.gemini_client import ask_gemini


class InterviewAgent:

    def generate_interview_questions(self, resume_text, target_role):

        prompt = f"""
Generate interview preparation for a {target_role}.

Resume:
{resume_text}

Return:

# Technical Questions
5 questions

# HR Questions
5 questions

# Interview Tips
5 bullets

# Common Mistakes
5 bullets

Rules:
- Maximum 300 words.
- Use bullet points.
"""
        return ask_gemini(prompt)