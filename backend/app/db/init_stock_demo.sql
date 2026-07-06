-- 股票演示数据库初始化脚本。
-- 第一阶段使用 AkShare 采集数据，写入 stocks、daily_prices、stock_quotes 三张核心表。

CREATE TABLE IF NOT EXISTS stocks (
    stock_id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL UNIQUE,
    stock_name TEXT NOT NULL,
    exchange TEXT NOT NULL,
    industry TEXT,
    list_date TEXT,
    market TEXT
);

CREATE TABLE IF NOT EXISTS daily_prices (
    price_id INTEGER PRIMARY KEY,
    stock_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    trade_date TEXT NOT NULL,
    open_price REAL,
    close_price REAL,
    high_price REAL,
    low_price REAL,
    volume INTEGER,
    turnover REAL,
    amplitude REAL,
    change_pct REAL,
    change_amount REAL,
    turnover_rate REAL,
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
);

CREATE TABLE IF NOT EXISTS stock_quotes (
    quote_id INTEGER PRIMARY KEY,
    stock_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    snapshot_date TEXT NOT NULL,
    latest_price REAL,
    change_pct REAL,
    volume INTEGER,
    turnover REAL,
    turnover_rate REAL,
    pe_dynamic REAL,
    pb_ratio REAL,
    total_market_value REAL,
    circulating_market_value REAL,
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_stocks_symbol ON stocks(symbol);
CREATE UNIQUE INDEX IF NOT EXISTS idx_daily_prices_symbol_date ON daily_prices(symbol, trade_date);
CREATE UNIQUE INDEX IF NOT EXISTS idx_stock_quotes_symbol_date ON stock_quotes(symbol, snapshot_date);
