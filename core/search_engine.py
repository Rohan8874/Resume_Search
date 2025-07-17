import pandas as pd
from sentence_transformers import SentenceTransformer
from config import CSV_PATH, EMBEDDING_MODEL

class SearchEngine:
    def __init__(self, collection):
        self.collection = collection
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        
    def load_and_process_data(self):
        df = pd.read_csv(CSV_PATH)
        print("Available columns:", df.columns.tolist())
        
        ids = []
        documents = []
        embeddings = []
        metadatas = []
        
        for idx, row in df.iterrows():
            resume_text = row['Resume_str']
            if 'Skills' in df.columns:
                resume_text += " " + row['Skills']
            
            embedding = self.model.encode(resume_text)
            
            ids.append(str(row['ID']))
            documents.append(resume_text)
            embeddings.append(embedding.tolist())
            metadatas.append({"category": row['Category']})
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        
        print(f"Successfully stored {len(ids)} resumes in ChromaDB")
    
    def find_similar_resumes(self, query_text, n_results=5):
        query_embedding = self.model.encode(query_text).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        similar_resumes = []
        for i in range(len(results['ids'][0])):
            resume_id = results['ids'][0][i]
            distance = results['distances'][0][i]
            document = results['documents'][0][i]
            metadata = results['metadatas'][0][i]
            
            similar_resumes.append({
                'id': resume_id,
                'similarity': 1 - distance,
                'category': metadata['category'],
                'excerpt': document[:300] + "...",
                'full_text': document
            })
        
        return similar_resumes