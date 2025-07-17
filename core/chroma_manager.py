import chromadb
from config import PERSIST_DIRECTORY
import os

class ChromaManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
        print(f"Initializing ChromaDB with persistence at: {PERSIST_DIRECTORY}")
        
    def get_collection(self, name="resumes"):
        return self.client.get_or_create_collection(name=name)
    
    def ensure_persistence_directory(self):
        os.makedirs(PERSIST_DIRECTORY, exist_ok=True)