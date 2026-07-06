# API 初版设计

本文档描述项目第一版接口形态，不要求立即全部实现。接口路径统一以 `/api` 开头，响应体建议统一返回 JSON。涉及股票数据的接口仅用于课程演示，不构成投资建议。

## 1. 通用约定

| 项目 | 约定 |
| --- | --- |
| 请求格式 | `application/json` |
| 响应格式 | `application/json` |
| 编码 | UTF-8 |
| 时间字段 | 日期使用 `YYYY-MM-DD`，时间使用 ISO 8601 字符串 |
| SQL 执行范围 | MVP 阶段只允许 `SELECT` 查询 |
| 错误响应 | 返回 `error_code`、`message` 和可选 `detail` |

通用错误响应示例：

```json
{
  "error_code": "SQL_NOT_SAFE",
  "message": "生成的 SQL 未通过安全校验",
  "detail": "Only SELECT statements are allowed."
}
```

## 2. Text2SQL API

### `POST /api/text2sql/query`

用于接收自然语言问题，生成 SQL，执行查询并返回结果。

请求体：

```json
{
  "question": "最近一个交易日成交量最高的10支股票是什么？",
  "database": "stock_demo"
}
```

响应体：

```json
{
  "question": "最近一个交易日成交量最高的10支股票是什么？",
  "sql": "SELECT s.symbol, s.stock_name, p.volume FROM daily_prices p JOIN stocks s ON p.stock_id = s.stock_id WHERE p.trade_date = (SELECT MAX(trade_date) FROM daily_prices) ORDER BY p.volume DESC LIMIT 10",
  "safe": true,
  "columns": ["symbol", "stock_name", "volume"],
  "rows": [
    {
      "symbol": "600000",
      "stock_name": "示例银行",
      "volume": 12345600
    }
  ],
  "summary": "最近一个交易日成交量最高的股票包括示例银行等。以上结果来自课程演示数据，不构成投资建议。"
}
```

建议处理流程：

1. 读取数据库 schema。
2. 构造 Text2SQL prompt。
3. 调用大模型生成 SQL。
4. 解析模型输出。
5. 执行 SQL 安全校验。
6. 执行 SQL。
7. 调用大模型生成结果摘要。
8. 返回 SQL、表格结果和摘要。

## 3. Schema API

### `GET /api/schema`

返回当前数据库表结构和字段说明，供前端展示或调试使用。

查询参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `database` | 否 | 数据库名称，默认 `stock_demo` |

响应体：

```json
{
  "database": "stock_demo",
  "tables": [
    {
      "table_name": "stocks",
      "description": "股票基础信息表",
      "columns": [
        {
          "name": "stock_id",
          "type": "INTEGER",
          "primary_key": true,
          "foreign_key": null,
          "description": "股票内部 ID"
        },
        {
          "name": "symbol",
          "type": "VARCHAR",
          "primary_key": false,
          "foreign_key": null,
          "description": "股票代码"
        }
      ]
    }
  ]
}
```

## 4. RAG API

### `POST /api/rag/query`

用于知识库问答，例如解释股票概念、估值指标、行情字段口径和系统使用说明。

请求体：

```json
{
  "question": "市盈率是什么意思？"
}
```

响应体：

```json
{
  "answer": "市盈率通常指股票价格与每股收益之间的比值，可用于观察市场对公司盈利能力的估值水平。单独使用市盈率不能判断股票是否便宜，还需要结合行业、增长、风险和数据口径等因素。以上为课程演示中的概念解释，不构成投资建议。",
  "sources": [
    {
      "doc_name": "financial_terms.md",
      "chunk": "市盈率是股票价格与每股收益的比值，常用于估值分析，但存在行业差异和周期性限制。"
    }
  ]
}
```

后续可扩展字段：

| 字段 | 说明 |
| --- | --- |
| `top_k` | 检索片段数量 |
| `category` | 文档分类过滤 |
| `conversation_id` | 多轮对话 ID |

## 5. Hybrid API

### `POST /api/hybrid/query`

用于同时调用 Text2SQL 和 RAG，适合既需要数据库结果又需要概念解释的问题。

请求体：

```json
{
  "question": "查询市盈率低于20的股票，并解释市盈率低可能代表什么。",
  "database": "stock_demo"
}
```

响应体：

```json
{
  "question": "查询市盈率低于20的股票，并解释市盈率低可能代表什么。",
  "route": "hybrid",
  "text2sql": {
    "sql": "SELECT s.symbol, s.stock_name, q.pe_dynamic FROM stock_quotes q JOIN stocks s ON q.stock_id = s.stock_id WHERE q.pe_dynamic < 20 ORDER BY q.pe_dynamic ASC LIMIT 20",
    "safe": true,
    "columns": ["symbol", "stock_name", "pe_dynamic"],
    "rows": []
  },
  "rag": {
    "answer": "市盈率较低可能表示估值较低，也可能反映市场对增长、盈利质量或风险的担忧，不能单独作为投资判断依据。",
    "sources": [
      {
        "doc_name": "financial_terms.md",
        "chunk": "市盈率需要结合行业、成长性、盈利稳定性和市场环境理解。"
      }
    ]
  },
  "summary": "数据库查询结果列出了市盈率低于 20 的股票；概念解释说明市盈率低并不必然代表值得投资。以上仅用于课程演示，不构成投资建议。"
}
```

初版路由规则建议：

| 问题类型 | 路由 |
| --- | --- |
| 包含排行、数量、最高、最低、平均、某日期等数据查询意图 | Text2SQL |
| 包含是什么意思、区别、为什么、如何理解等解释意图 | RAG |
| 同时包含查询结果和解释要求 | Hybrid |

## 6. Evaluation API

### `GET /api/evaluation/cases`

返回测试用例列表，供前端展示或后端批量执行。

响应体：

```json
{
  "cases": [
    {
      "case_id": "T2SQL-001",
      "type": "single_table",
      "question": "查询所有在上交所上市的股票。",
      "expected_behavior": "生成只查询 stocks 表的 SELECT SQL，并筛选 exchange 为 SSE 或上交所。"
    }
  ]
}
```

### `POST /api/evaluation/run`

执行测试用例并保存结果。

请求体：

```json
{
  "case_ids": ["T2SQL-001", "T2SQL-002"],
  "database": "stock_demo"
}
```

响应体：

```json
{
  "run_id": "eval-20260706-001",
  "total": 2,
  "success": 1,
  "failed": 1,
  "metrics": {
    "sql_execution_success_rate": 0.5,
    "sql_semantic_accuracy": 0.5,
    "average_latency_ms": 1320
  },
  "results": [
    {
      "case_id": "T2SQL-001",
      "question": "查询所有在上交所上市的股票。",
      "sql": "SELECT * FROM stocks WHERE exchange = 'SSE' LIMIT 100",
      "passed": true,
      "error": null
    }
  ]
}
```

## 7. 后续接口扩展

| 接口 | 用途 | 阶段 |
| --- | --- | --- |
| `POST /api/rag/documents` | 上传或导入知识库文档 | 阶段 3 |
| `GET /api/rag/documents` | 查看知识库文档列表 | 阶段 3 |
| `DELETE /api/rag/documents/{doc_id}` | 删除知识库文档 | 阶段 3 |
| `GET /api/logs/queries` | 查看历史问题、SQL 和错误日志 | 阶段 2 |
| `POST /api/charts/suggest` | 根据查询结果推荐图表类型 | 阶段 5 |
