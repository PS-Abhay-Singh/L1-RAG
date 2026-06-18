# backend/app/embeddings/embedding_generator.py

import ollama


class EmbeddingGenerator:

    @staticmethod
    def generate(text: str):

        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=text
        )

        return response["embedding"]