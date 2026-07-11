from utils.gemini_client import ask_gemini


class ResumeAgent:
    """
    AI Agent responsible for analyzing resumes.
    """

    def analyze_resume(self, resume_text, target_role):

        prompt = f"""
You are an expert Career Coach.

Analyze the resume for the role of {target_role}.

Resume:
{resume_text}

Return your answer in Markdown.

Rules:
- Maximum 250 words.
- Use headings.
- Use bullet points.
- Do NOT write long paragraphs.

Include:

# Candidate Summary
(4-5 lines)

# Strengths
- Bullet points

# Weaknesses
- Bullet points

# Readiness Score
Give a score out of 10 with one-line explanation.
"""
        return ask_gemini(prompt)