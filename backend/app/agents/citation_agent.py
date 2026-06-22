class CitationAgent:

    @staticmethod
    def generate_sources(results):

        citations = []

        for match in results:

            citations.append({
                "paper": match.metadata["paper_title"],
                "section": match.metadata["section"]
            })

        return citations


def verify_citation(results):
    return CitationAgent.generate_sources(results)