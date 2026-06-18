from pypdf import PdfReader


class PDFLoader:

    @staticmethod
    def load(pdf_path: str) -> str:

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text