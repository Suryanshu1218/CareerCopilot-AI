from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

styles = getSampleStyleSheet()


def heading(text):
    return Paragraph(
        f"<b><font size=16>{text}</font></b>",
        styles["Heading2"],
    )


def subheading(text):
    return Paragraph(
        f"<b>{text}</b>",
        styles["Heading3"],
    )


def normal(text):
    return Paragraph(
        str(text),
        styles["BodyText"],
    )


def bullet(text):
    return Paragraph(
        f"• {text}",
        styles["BodyText"],
    )


def add_content(story, data):
    """
    Recursively formats dictionaries and lists.
    """

    # ---------------- STRING ----------------

    if isinstance(data, str):

        story.append(normal(data))
        story.append(Spacer(1, 6))
        return

    # ---------------- LIST ----------------

    if isinstance(data, list):

        for item in data:

            if isinstance(item, dict):

                story.append(Spacer(1, 4))

                add_content(story, item)

            else:

                story.append(bullet(item))

        story.append(Spacer(1, 8))
        return

    # ---------------- DICTIONARY ----------------

    if isinstance(data, dict):

        for key, value in data.items():

            story.append(subheading(key))

            if isinstance(value, (dict, list)):

                add_content(story, value)

            else:

                story.append(normal(value))

            story.append(Spacer(1, 8))


def create_pdf(results, filename="Career_Report.pdf"):

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            "<font size=24><b>CareerCopilot AI Report</b></font>",
            styles["Title"],
        )
    )

    story.append(
        Paragraph(
            "AI-Powered Career Analysis",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 20))

    sections = [

        ("Resume Analysis", results.get("resume", {})),

        ("Skill Gap Analysis", results.get("skills", {})),

        ("Learning Roadmap", results.get("roadmap", {})),

        ("Portfolio Projects", results.get("projects", {})),

        ("Interview Preparation", results.get("interview", {})),

        ("Resume Improvements", results.get("improvements", {})),

        ("Job Recommendations", results.get("jobs", {})),
    ]

    for title, content in sections:

        story.append(heading(title))

        add_content(story, content)

        story.append(Spacer(1, 20))

    doc.build(story)

    return filename