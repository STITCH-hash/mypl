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
                    ColumnSchema(name="symbol", type="TEXT", description="股票代码"),
                    ColumnSchema(name="trade_date", type="TEXT", description="交易日期"),
                    ColumnSchema(name="open_price", type="REAL", description="开盘价"),
                    ColumnSchema(name="close_price", type="REAL", description="收盘价"),
                    ColumnSchema(name="high_price", type="REAL", description="最高价"),
                    ColumnSchema(name="low_price", type="REAL", description="最低价"),
                    ColumnSchema(name="volume", type="INTEGER", description="成交量"),
                    ColumnSchema(name="turnover", type="REAL", description="成交额"),
                    ColumnSchema(name="amplitude", type="REAL", description="振幅"),
                    ColumnSchema(name="change_pct", type="REAL", description="涨跌幅"),
                    ColumnSchema(name="change_amount", type="REAL", description="涨跌额"),
                    ColumnSchema(name="turnover_rate", type="REAL", description="换手率"),
                ],
            ),
            TableSchema(
                table_name="stock_quotes",
                description="最新行情快照表",
                columns=[
                    ColumnSchema(name="quote_id", type="INTEGER", description="行情快照 ID"),
                    ColumnSchema(name="stock_id", type="INTEGER", description="关联股票 ID"),
                    ColumnSchema(name="symbol", type="TEXT", description="股票代码"),
                    ColumnSchema(name="snapshot_date", type="TEXT", description="快照采集日期"),
                    ColumnSchema(name="latest_price", type="REAL", description="最新价"),
                    ColumnSchema(name="change_pct", type="REAL", description="涨跌幅"),
                    ColumnSchema(name="volume", type="INTEGER", description="成交量"),
                    ColumnSchema(name="turnover", type="REAL", description="成交额"),
                    ColumnSchema(name="turnover_rate", type="REAL", description="换手率"),
                    ColumnSchema(name="pe_dynamic", type="REAL", description="动态市盈率"),
                    ColumnSchema(name="pb_ratio", type="REAL", description="市净率"),
                    ColumnSchema(name="total_market_value", type="REAL", description="总市值"),
                    ColumnSchema(name="circulating_market_value", type="REAL", description="流通市值"),
                ],
            ),
        ],
    )
