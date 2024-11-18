from openai import OpenAI

class EmbeddingModel:
    def __init__(self):
        self.client = OpenAI()
    
    def embed_query(self, text):
        """Convert text to embedding vector."""
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
