-- 股票演示数据库初始化脚本预留文件。
-- 后续阶段将在这里创建 stocks、daily_prices、financial_indicators 等表。

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
    trade_date TEXT NOT NULL,
    open_price REAL,
    close_price REAL,
    high_price REAL,
    low_price REAL,
    volume INTEGER,
    turnover REAL,
    change_pct REAL,
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
);

CREATE TABLE IF NOT EXISTS financial_indicators (
    indicator_id INTEGER PRIMARY KEY,
    stock_id INTEGER NOT NULL,
    report_period TEXT NOT NULL,
    pe_ratio REAL,
    pb_ratio REAL,
    roe REAL,
    revenue REAL,
    net_profit REAL,
    gross_margin REAL,
    debt_ratio REAL,
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
);
