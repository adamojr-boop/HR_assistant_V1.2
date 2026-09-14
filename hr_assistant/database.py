import chromadb
from hr_assistant.config import CHROMA_DIR

class Database:
    def __init__(self, collection_name="hr_resumes"):
        
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def get_collection(self):
        return self.collection