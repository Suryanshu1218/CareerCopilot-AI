from utils.gemini_client import ask_gemini


class ResumeImprovementAgent:
    """
    AI Agent responsible for suggesting resume improvements.
    """

    def improve_resume(self, resume_text, target_role):

        prompt = f"""
You are an expert Resume Reviewer.

Review the following resume for the role of {target_role}.

Resume:
{resume_text}

Return your answer in Markdown.

Rules:
- Maximum 250 words.
- Use headings.
- Use bullet points.
- Keep the suggestions practical and specific.

Include:

# Resume Improvement Suggestions

- 5-8 specific improvements that would make the resume stronger.

# Missing Sections

Mention any important sections that are missing, such as:
- GitHub
- LinkedIn
- Portfolio
- Certifications
- Projects
- Achievements

# ATS Tips

Give 4-5 tips to improve the resume for Applicant Tracking Systems (ATS).

# Final Recommendation

Write 2-3 lines summarizing the overall advice.
"""

        return ask_gemini(prompt)