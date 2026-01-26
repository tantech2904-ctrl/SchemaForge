from pydantic import BaseModel
from typing import Dict, Any, Optional 

class InsertRequest(BaseModel):
    table: str
    data: Dict[str, Any]

class UpdateRequest(BaseModel):
    table: str
    data: Dict[str, Any]
    where: Dict[str, Any]

class DeleteRequest(BaseModel):
    table: str
    where: Dict[str, Any]

class SelectRequest(BaseModel):
    table: str
    columns: Optional[list[str]] = None   
    where: Optional[dict] = None       
    limit: int = 50
    offset: int = 0