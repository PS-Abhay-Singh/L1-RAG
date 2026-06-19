import re


class SectionChunker:

    @staticmethod
    def chunk(text: str):

        pattern = r"\n(\d+\s+[A-Z][A-Za-z\s\-]+)"

        matches = list(re.finditer(pattern, text))

        chunks = []

        # Abstract chunk
        if matches:
            abstract_text = text[:matches[0].start()].strip()

            chunks.append({
                "section": "Abstract",
                "content": abstract_text
            })

        # Sections
        for i in range(len(matches)):

            section_name = matches[i].group(1).strip()

            start = matches[i].end()

            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(text)

            content = text[start:end].strip()

            chunks.append({
                "section": section_name,
                "content": content
            })

        return chunks