class CitationAgent:

    @staticmethod
    def generate_sources(results):

        citations = []

        for match in results:

            citations.append({
                "source": match.metadata.get("paper_title", "Unknown"),
                "section": match.metadata.get("section", "Unknown"),
                "paper": match.metadata.get("paper_title", "Unknown")  # backwards compat
            })

        return citations


def verify_citation(results):
    return CitationAgent.generate_sources(results)