from pydantic import BaseModel, Field


class ColumnSchema(BaseModel):
    name: str
    type: str
    description: str


class TableSchema(BaseModel):
    table_name: str
    description: str
    columns: list[ColumnSchema]


class SchemaResponse(BaseModel):
    database: str
    tables: list[TableSchema]


class Text2SQLRequest(BaseModel):
    question: str = Field(..., min_length=1, description="用户自然语言问题")
    database: str = Field(default="stock_demo", description="数据库名称")


class Text2SQLResponse(BaseModel):
    question: str
    sql: str
    safe: bool
    columns: list[str]
    rows: list[dict]
    summary: str
    mode: str = "mock"
