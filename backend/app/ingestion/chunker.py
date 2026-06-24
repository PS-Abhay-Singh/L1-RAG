import re


# All heading patterns ordered from most to least specific
_HEADING_PATTERNS = [
    re.compile(r"^\d+\.\d+\s+[A-Z]"),        # 1.1 Background
    re.compile(r"^\d+\s+[A-Z]"),              # 1 Introduction
    re.compile(r"^[IVX]+\.\s+[A-Z]"),         # I. Introduction
    re.compile(r"^[A-Z][A-Z\s]{4,}$"),        # ALL CAPS HEADING
    re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+){0,4}$"),  # Title Case Line (short)
]


def _is_heading(line: str) -> bool:
    line = line.strip()
    if not line or len(line) > 80:
        return False
    return any(p.match(line) for p in _HEADING_PATTERNS)


class SectionChunker:

    @staticmethod
    def chunk(text: str) -> list:
        lines = text.splitlines()

        sections = []
        current_section = "Introduction"
        current_content = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if _is_heading(stripped):
                if current_content:
                    sections.append({
                        "section": current_section,
                        "content": "\n".join(current_content)
                    })
                current_section = stripped
                current_content = []
            else:
                current_content.append(stripped)

        if current_content:
            sections.append({
                "section": current_section,
                "content": "\n".join(current_content)
            })

        # --- Fallback: no sections detected → paragraph-based chunking ---
        if len(sections) <= 1 and sections and len(sections[0]["content"]) > 500:
            return SectionChunker._paragraph_fallback(text)

        return sections

    @staticmethod
    def _paragraph_fallback(text: str) -> list:
        """
        Split by double newlines into paragraphs.
        Groups consecutive short paragraphs to avoid tiny chunks.
        Labels each chunk as Page-block N for BM25 to still work on content.
        """
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) > 80]

        sections = []
        buffer = []
        buffer_len = 0
        block_idx = 1

        for para in paragraphs:
            buffer.append(para)
            buffer_len += len(para)
            if buffer_len >= 800:
                sections.append({
                    "section": f"Block {block_idx}",
                    "content": "\n\n".join(buffer)
                })
                block_idx += 1
                buffer = []
                buffer_len = 0

        if buffer:
            sections.append({
                "section": f"Block {block_idx}",
                "content": "\n\n".join(buffer)
            })

        return sections if sections else [{"section": "Document", "content": text}]
