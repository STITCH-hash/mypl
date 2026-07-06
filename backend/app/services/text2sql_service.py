from app.models import Text2SQLRequest, Text2SQLResponse
from app.services.sql_safety import is_safe_select


def build_mock_sql(question: str) -> str:
    """Return simple mock SQL so frontend and API integration can proceed."""
    if "市盈率" in question or "pe" in question.lower():
        return (
            "SELECT s.symbol, s.stock_name, q.pe_dynamic "
            "FROM stock_quotes q "
            "JOIN stocks s ON q.stock_id = s.stock_id "
            "WHERE q.pe_dynamic < 20 "
            "ORDER BY q.pe_dynamic ASC "
            "LIMIT 10"
        )

    if "成交量" in question or "volume" in question.lower():
        return (
            "SELECT s.symbol, s.stock_name, p.volume "
            "FROM daily_prices p "
            "JOIN stocks s ON p.stock_id = s.stock_id "
            "ORDER BY p.volume DESC "
            "LIMIT 10"
        )

    return (
        "SELECT symbol, stock_name, exchange, industry "
        "FROM stocks "
        "LIMIT 10"
    )


def run_mock_text2sql(request: Text2SQLRequest) -> Text2SQLResponse:
    sql = build_mock_sql(request.question)
    safe = is_safe_select(sql)

    if "pe_dynamic" in sql:
        columns = ["symbol", "stock_name", "pe_dynamic"]
        rows = [
            {"symbol": "600000", "stock_name": "示例银行", "pe_dynamic": 8.6},
            {"symbol": "000001", "stock_name": "示例科技", "pe_dynamic": 18.4},
        ]
    elif "volume" in sql:
        columns = ["symbol", "stock_name", "volume"]
        rows = [
            {"symbol": "600000", "stock_name": "示例银行", "volume": 12800000},
            {"symbol": "000001", "stock_name": "示例科技", "volume": 8600000},
        ]
    else:
        columns = ["symbol", "stock_name", "exchange", "industry"]
        rows = [
            {"symbol": "600000", "stock_name": "示例银行", "exchange": "SSE", "industry": "金融"},
            {"symbol": "000001", "stock_name": "示例科技", "exchange": "SZSE", "industry": "软件服务"},
        ]

    return Text2SQLResponse(
        question=request.question,
        sql=sql,
        safe=safe,
        columns=columns,
        rows=rows,
        summary="当前为 mock 查询结果，用于验证接口结构和前端展示；股票数据仅用于课程演示，不构成投资建议。",
    )
