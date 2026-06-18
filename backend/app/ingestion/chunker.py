# Split extracted text into chunks for embedding
import re


class SectionChunker:

    @staticmethod
    def chunk(text: str):

        pattern = r"(\n\d+\s+[A-Z][A-Za-z\s\-]+\n)"

        parts = re.split(pattern, text)

        chunks = []

        current_section = "Unknown"

        for part in parts:

            part = part.strip()

            if not part:
                continue

            if re.match(r"^\d+\s+", part):

                current_section = part

            else:

                chunks.append(
                    {
                        "section": current_section,
                        "content": part
                    }
                )

        return chunks