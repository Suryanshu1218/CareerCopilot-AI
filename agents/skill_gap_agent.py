from utils.gemini_client import ask_gemini


class SkillGapAgent:

    def analyze_skill_gap(self, resume_text, target_role):

        prompt = f"""
You are an AI Career Coach.

Compare this resume with the requirements of a {target_role}.

Resume:
{resume_text}

Return ONLY:

# Existing Skills
- bullets

# Missing Skills
- bullets

# Learning Priority
1.
2.
3.
4.
5.

# Suggestions
Maximum 5 bullet points.

Rules:
- Maximum 250 words.
- No long paragraphs.
"""
        return ask_gemini(prompt)