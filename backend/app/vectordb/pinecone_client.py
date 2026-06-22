from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

class LazyIndexWrapper:
    """Lazy wrapper for Pinecone index to defer initialization"""
    
    def __init__(self):
        self._index = None
        self._pc = None
    
    def _initialize(self):
        if self._index is None:
            api_key = os.getenv("PINECONE_API_KEY")
            if not api_key:
                raise ValueError("PINECONE_API_KEY environment variable not set")
            
            self._pc = Pinecone(api_key=api_key)
            index_name = os.getenv("PINECONE_INDEX_NAME")
            if not index_name:
                raise ValueError("PINECONE_INDEX_NAME environment variable not set")
            self._index = self._pc.Index(index_name)
    
    def __getattr__(self, name):
        self._initialize()
        return getattr(self._index, name)
    
    def query(self, *args, **kwargs):
        self._initialize()
        return self._index.query(*args, **kwargs)
    
    def upsert(self, *args, **kwargs):
        self._initialize()
        return self._index.upsert(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self._initialize()
        return self._index.delete(*args, **kwargs)

# Create the lazy index object
index = LazyIndexWrapper()
