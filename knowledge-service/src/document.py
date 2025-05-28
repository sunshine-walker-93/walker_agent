from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    content: str
    metadata: Dict

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    
    class Config:
        orm_mode = True 