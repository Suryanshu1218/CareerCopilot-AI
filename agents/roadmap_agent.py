from utils.gemini_client import ask_gemini


class RoadmapAgent:

    def generate_roadmap(self, resume_text, target_role):

        prompt = f"""
Create a concise 90-day roadmap for becoming a {target_role}.

Resume:
{resume_text}

Return in Markdown.

Rules:
- Maximum 350 words.
- No long paragraphs.

Use this structure:

# Month 1
Skills
Resources
Milestone

# Month 2
Skills
Resources
Milestone

# Month 3
Skills
Resources
Milestone
"""
        return ask_gemini(prompt)