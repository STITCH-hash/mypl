from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import SchemaResponse, Text2SQLRequest, Text2SQLResponse
from app.services.schema_reader import get_mock_schema
from app.services.text2sql_service import run_mock_text2sql

app = FastAPI(
    title="Text2SQL Intelligent QA API",
    description="Minimal FastAPI skeleton for the Text2SQL course project.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "text2sql-api",
        "stage": "mock-skeleton",
    }


@app.get("/api/schema", response_model=SchemaResponse)
def read_schema(database: str = "stock_demo") -> SchemaResponse:
    return get_mock_schema(database=database)


@app.post("/api/text2sql/query", response_model=Text2SQLResponse)
def query_text2sql(request: Text2SQLRequest) -> Text2SQLResponse:
    return run_mock_text2sql(request)
