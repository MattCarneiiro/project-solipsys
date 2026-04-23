import os
import sqlite3
import chromadb
from chromadb.utils import embedding_functions

class DualStorageEngine:
    def __init__(self, base_path: str = "./vault_data"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)
        
        # Cérebro Vetorial (ChromaDB)
        chroma_path = os.path.join(self.base_path, "vectors")
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.chroma_client.get_or_create_collection(
            name="semantic_anchors", 
            embedding_function=self.emb_fn
        )
        
        # Cérebro Lógico (SQLite)
        sqlite_path = os.path.join(self.base_path, "ontology.db")
        self.conn = sqlite3.connect(sqlite_path, check_same_thread=False)
        self._bootstrap_db()

    def _bootstrap_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                original_filename TEXT,
                vault_path TEXT,
                ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id TEXT PRIMARY KEY,
                label TEXT UNIQUE,
                source TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tag_relations (
                parent_id TEXT,
                child_id TEXT,
                relation_type TEXT,
                FOREIGN KEY(parent_id) REFERENCES tags(id),
                FOREIGN KEY(child_id) REFERENCES tags(id),
                PRIMARY KEY (parent_id, child_id)
            )
        ''')
        self.conn.commit()