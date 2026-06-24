import re
import os


class MetadataExtractor:

    @staticmethod
    def extract(text: str, pdf_path: str = ""):
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        title = MetadataExtractor._extract_title(lines, pdf_path)
        abstract = MetadataExtractor._extract_abstract(text)
        sections = MetadataExtractor._extract_sections(text)

        return {"title": title, "abstract": abstract, "sections": sections}

    @staticmethod
    def _extract_title(lines: list, pdf_path: str) -> str:
        # Skip lines that look like metadata noise (DOIs, URLs, dates, page nums)
        noise = re.compile(
            r"(doi|arxiv|http|www|©|copyright|\d{4}|page\s*\d|proceedings|journal|conference|workshop|vol\.|issue)",
            re.IGNORECASE,
        )
        for line in lines[:15]:
            if len(line) > 10 and not noise.search(line):
                return line

        # Last resort: filename
        if pdf_path:
            return os.path.basename(pdf_path).replace(".pdf", "").replace("_", " ")
        return lines[0] if lines else "Unknown"

    @staticmethod
    def _extract_abstract(text: str) -> str:
        # Try explicit Abstract heading
        match = re.search(
            r"abstract[\s\.\-:]*(.*?)(?=\n\s*\n|\n\s*(?:\d+[\.\s]|[IVX]+[\.\s])?(?:introduction|background|related work|overview|motivation))",
            text,
            re.IGNORECASE | re.DOTALL,
        )
        if match:
            return match.group(1).strip()[:2000]

        # Try first substantial paragraph before any section heading
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) > 150]
        if paragraphs:
            return paragraphs[0][:2000]

        return ""

    @staticmethod
    def _extract_sections(text: str) -> list:
        patterns = [
            r"\n\d+\s+[A-Z][A-Za-z\s\-]+\n",          # 1 Introduction
            r"\n\d+\.\d*\s+[A-Z][A-Za-z\s\-]+\n",     # 1.1 Background
            r"\n[IVX]+\.\s+[A-Z][A-Za-z\s\-]+\n",     # I. Introduction
            r"\n[A-Z][A-Z\s]{4,}\n",                   # ALL CAPS HEADING
        ]
        sections = []
        for pattern in patterns:
            found = re.findall(pattern, text)
            sections.extend(found)
        return list(dict.fromkeys(sections))  # deduplicate preserving order
