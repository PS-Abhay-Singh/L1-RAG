import re


class MetadataExtractor:

    @staticmethod
    def extract(text: str):

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        title = lines[0] if lines else ""

        abstract = ""

        abstract_match = re.search(
            r"abstract(.*?)(?:1\s+introduction|introduction)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if abstract_match:
            abstract = abstract_match.group(1).strip()

        sections = re.findall(
            r"\n\d+\s+[A-Z][A-Za-z\s\-]+\n",
            text
        )

        return {
            "title": title,
            "abstract": abstract,
            "sections": sections
        }