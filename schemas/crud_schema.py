from pydantic import BaseModel
from typing import Dict, Any

class CRUDPayload(BaseModel):
    data: Dict[str, Any]
