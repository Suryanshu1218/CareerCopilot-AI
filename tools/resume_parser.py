from pypdf import PdfReader


def extract_resume_text(uploaded_file):
    """
    Extract text from an uploaded PDF resume.
    """

    pdf = PdfReader(uploaded_file)

    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text