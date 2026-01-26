from pydantic import BaseModel
from typing import List

class TableListResponse(BaseModel):
    tables: List[str]

class ColumnInfo(BaseModel):
    Field: str
    Type: str
    Null: str
    Key: str
    Default: str | None
    Extra: str

class ColumnsResponse(BaseModel):
    columns: list[ColumnInfo]
