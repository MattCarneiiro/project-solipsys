import os
import shutil
from typing import List, Dict, Any, Optional
from .schemas import Tag, Document, Anchor
from .storage import DualStorageEngine

class VaultClient:
    def __init__(self, base_path: str = "./vault_data"):
        self.db = DualStorageEngine(base_path)
        self.pdf_vault_dir = os.path.join(base_path, "pdfs")
        os.makedirs(self.pdf_vault_dir, exist_ok=True)

    def ingest_document(self, filepath: str) -> Document:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo ausente: {filepath}")
            
        original_name = os.path.basename(filepath)
        doc = Document(original_filename=original_name, vault_path="")
        
        safe_filename = f"{doc.id}.pdf"
        vault_dest = os.path.join(self.pdf_vault_dir, safe_filename)
        
        shutil.copy(filepath, vault_dest)
        doc.vault_path = vault_dest
        
        cursor = self.db.conn.cursor()
        cursor.execute(
            "INSERT INTO documents (id, original_filename, vault_path) VALUES (?, ?, ?)",
            (doc.id, doc.original_filename, doc.vault_path)
        )
        self.db.conn.commit()
        return doc

    def create_tag(self, label: str, source: str = "USER", category: str = "Geral") -> Tag:
        tag = Tag(label=label, source=source, category=category)
        cursor = self.db.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tags (id, label, source, category) VALUES (?, ?, ?, ?)",
                (tag.id, tag.label, tag.source, tag.category)
            )
            self.db.conn.commit()
        except Exception:
            cursor.execute("SELECT id, label, source, category FROM tags WHERE label=?", (label,))
            row = cursor.fetchone()
            tag = Tag(id=row[0], label=row[1], source=row[2], category=row[3])
        return tag

    def link_tags(self, parent_label: str, child_label: str, relation_type: str = "is_child_of"):
        parent = self.create_tag(parent_label)
        child = self.create_tag(child_label)
        cursor = self.db.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO tag_relations (parent_id, child_id, relation_type) VALUES (?, ?, ?)",
                (parent.id, child.id, relation_type)
            )
            self.db.conn.commit()
        except:
            pass

    def create_anchor(self, doc_id: str, text: str, tags: List[str], page: Optional[int] = None) -> Anchor:
        tag_objects = [self.create_tag(t) for t in tags]
        tag_ids = [t.id for t in tag_objects]
        tag_labels = [t.label for t in tag_objects]
        
        anchor = Anchor(doc_id=doc_id, text_content=text, page_number=page, tag_ids=tag_ids)
        
        self.db.collection.add(
            documents=[anchor.text_content],
            metadatas=[{
                "doc_id": anchor.doc_id, 
                "page": anchor.page_number or 0,
                "tags": ",".join(tag_labels)
            }],
            ids=[anchor.id]
        )
        return anchor

    def search_semantic(self, query: str, n_results: int = 3, threshold: float = 1.5) -> List[Dict[str, Any]]:
        results = self.db.collection.query(query_texts=[query], n_results=n_results)
        
        formatted_results = []
        if not results['documents']: return formatted_results
        
        for i in range(len(results['documents'][0])):
            distance = results['distances'][0][i]
            if distance < threshold:
                formatted_results.append({
                    "anchor_id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": distance
                })
        return formatted_results