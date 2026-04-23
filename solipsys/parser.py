from pypdf import PdfReader
from typing import List
from .core import VaultClient

class SemanticParser:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def _sliding_window(self, text: str) -> List[str]:
        if not text: return []
        clean_text = " ".join(text.replace("\n", " ").split())
        chunks = []
        step = self.chunk_size - self.overlap
        
        for i in range(0, len(clean_text), step):
            chunks.append(clean_text[i:i + self.chunk_size])
        return chunks

    def process_and_ingest(self, client: VaultClient, filepath: str, macro_tag: str):
        print(f"[SOLIPSYS] Digerindo documento: {filepath}")
        doc = client.ingest_document(filepath)
        client.create_tag(label=macro_tag, source="EGO", category="Auto_Ingestion")
        
        try:
            reader = PdfReader(doc.vault_path)
            total_anchors = 0
            
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                if not text: continue
                
                chunks = self._sliding_window(text)
                for chunk in chunks:
                    client.create_anchor(
                        doc_id=doc.id,
                        text=chunk,
                        tags=[macro_tag],
                        page=page_num
                    )
                    total_anchors += 1
                    
            print(f"[SOLIPSYS] Sucesso. {total_anchors} âncoras geradas.")
            return doc.id
        except Exception as e:
            print(f"[SOLIPSYS] Falha crítica na digestão: {e}")
            raise