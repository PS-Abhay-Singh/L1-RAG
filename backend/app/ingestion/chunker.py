import re


class SectionChunker:

    @staticmethod
    def chunk(text: str):

        lines = text.splitlines()

        sections = []

        current_section = "Abstract"
        current_content = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if re.match(r"^\d+\s+[A-Z]", line):

                sections.append({
                    "section": current_section,
                    "content": "\n".join(current_content)
                })

                current_section = line
                current_content = []

            else:

                current_content.append(line)

        sections.append({
            "section": current_section,
            "content": "\n".join(current_content)
        })

        return sections