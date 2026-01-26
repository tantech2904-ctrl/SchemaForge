from fastapi import FastAPI
from db.executor import execute_query
from routes.auth import router as auth_router
from routes.metadata import router as metadata_router
from routes.crud import router as crud_router


app = FastAPI(title="SchemaForge API")

app.include_router(auth_router)
app.include_router(metadata_router)
app.include_router(crud_router)

