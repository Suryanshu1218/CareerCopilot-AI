from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue


def create_pdf(results):

    pdf = SimpleDocTemplate(
    "Career_Report.pdf",
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = darkblue

    heading_style = styles["Heading2"]
    heading_style.fontSize = 16
    heading_style.spaceAfter = 10
    heading_style.spaceBefore = 15

    body_style = styles["BodyText"]
    body_style.fontSize = 11
    body_style.leading = 18

    story = []

    # PDF Title
    story.append(Paragraph("CareerCopilot AI Report", title_style))
    story.append(Spacer(1, 20))

    sections = [
        ("Resume Analysis", results.get("resume")),
        ("Skill Gap Analysis", results.get("skills")),
        ("Learning Roadmap", results.get("roadmap")),
        ("Portfolio Projects", results.get("projects")),
        ("Interview Preparation", results.get("interview")),
        ("Resume Improvements", results.get("improvements"))
    ]

    for title, content in sections:

        story.append(Paragraph(title, heading_style))
        story.append(Spacer(1, 8))

        if not content:
            content = "No data available."

        clean_content = str(content)

        # Remove Markdown headings
        clean_content = clean_content.replace("# ", "")
        clean_content = clean_content.replace("## ", "")

        # Remove bold markers
        clean_content = clean_content.replace("**", "")

        # Convert bullets
        clean_content = clean_content.replace("* ", "• ")

        # New lines
        clean_content = clean_content.replace("\n", "<br/>")

        story.append(
          Paragraph(
             clean_content,
             body_style
          )
       )

        story.append(Spacer(1, 20))

    pdf.build(story)

    return "Career_Report.pdf"