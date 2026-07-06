from app.models import ColumnSchema, SchemaResponse, TableSchema


def get_mock_schema(database: str = "stock_demo") -> SchemaResponse:
    """Return a stable mock schema until the real database is connected."""
    return SchemaResponse(
        database=database,
        tables=[
            TableSchema(
                table_name="stocks",
                description="股票基础信息表",
                columns=[
                    ColumnSchema(name="stock_id", type="INTEGER", description="股票内部 ID"),
                    ColumnSchema(name="symbol", type="TEXT", description="股票代码"),
                    ColumnSchema(name="stock_name", type="TEXT", description="股票名称"),
                    ColumnSchema(name="exchange", type="TEXT", description="交易所"),
                    ColumnSchema(name="industry", type="TEXT", description="所属行业"),
                    ColumnSchema(name="market", type="TEXT", description="市场类型"),
                ],
            ),
            TableSchema(
                table_name="daily_prices",
                description="日行情表",
                columns=[
                    ColumnSchema(name="price_id", type="INTEGER", description="行情记录 ID"),
                    ColumnSchema(name="stock_id", type="INTEGER", description="关联股票 ID"),
                    ColumnSchema(name="trade_date", type="TEXT", description="交易日期"),
                    ColumnSchema(name="close_price", type="REAL", description="收盘价"),
                    ColumnSchema(name="volume", type="INTEGER", description="成交量"),
                    ColumnSchema(name="change_pct", type="REAL", description="涨跌幅"),
                ],
            ),
            TableSchema(
                table_name="financial_indicators",
                description="财务指标表",
                columns=[
                    ColumnSchema(name="indicator_id", type="INTEGER", description="指标记录 ID"),
                    ColumnSchema(name="stock_id", type="INTEGER", description="关联股票 ID"),
                    ColumnSchema(name="report_period", type="TEXT", description="报告期"),
                    ColumnSchema(name="pe_ratio", type="REAL", description="市盈率"),
                    ColumnSchema(name="roe", type="REAL", description="净资产收益率"),
                    ColumnSchema(name="debt_ratio", type="REAL", description="资产负债率"),
                ],
            ),
        ],
    )
