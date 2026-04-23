from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Document(BaseModel):
    id: str = Field(default_factory=lambda: f"doc_{uuid.uuid4().hex[:8]}")
    original_filename: str
    vault_path: str 
    ingested_at: datetime = Field(default_factory=datetime.utcnow)

class TagCreate(BaseModel):
    label: str
    source: str = Field(default="USER", pattern="^(USER|EGO)$")
    category: Optional[str] = "Geral"

class Tag(TagCreate):
    id: str = Field(default_factory=lambda: f"tag_{uuid.uuid4().hex[:8]}")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AnchorCreate(BaseModel):
    doc_id: str
    text_content: str
    page_number: Optional[int] = None

class Anchor(AnchorCreate):
    id: str = Field(default_factory=lambda: f"anc_{uuid.uuid4().hex[:8]}")
    tag_ids: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)