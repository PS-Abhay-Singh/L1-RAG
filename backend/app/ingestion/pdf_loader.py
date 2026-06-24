from pypdf import PdfReader


class PDFLoader:

    @staticmethod
    def load(pdf_path: str) -> str:
        # Primary: pypdf
        text = PDFLoader._load_pypdf(pdf_path)
        if text and len(text.strip()) > 200:
            return text

        # Fallback: pdfplumber (handles 2-column, complex layouts)
        text = PDFLoader._load_pdfplumber(pdf_path)
        if text and len(text.strip()) > 200:
            return text

        return text or ""

    @staticmethod
    def _load_pypdf(pdf_path: str) -> str:
        try:
            reader = PdfReader(pdf_path)
            return "".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return ""

    @staticmethod
    def _load_pdfplumber(pdf_path: str) -> str:
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text(x_tolerance=3, y_tolerance=3)
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception:
            return ""
