# 系统设计说明书

## 1. 文档目的

本文档描述系统总体架构、模块划分、接口设计、数据设计和部署运行方式。当前版本以课程项目初始框架为主，后续随代码实现补充详细类图、流程图和截图。

## 2. 总体架构

```text
浏览器前端
  ↓ HTTP/JSON
FastAPI 后端
  ↓
Text2SQL 服务层
  ├── AkShare 数据采集脚本
  ├── Schema 读取模块
  ├── Prompt 构造模块
  ├── LLMClient 预留模块
  ├── SQL 安全校验模块
  └── SQL 执行模块
  ↓
股票演示数据库 SQLite

第二阶段：
RAG 文档管理 → 文档切分 → 向量库 Chroma → 检索增强回答
```

## 3. 目录设计

| 目录 | 说明 |
| --- | --- |
| `backend/` | FastAPI 后端服务 |
| `backend/app/db/` | 数据库初始化脚本和连接代码预留 |
| `backend/app/scripts/` | AkShare 数据采集脚本预留 |
| `backend/app/services/` | schema 读取、SQL 安全校验、Text2SQL 业务服务 |
| `frontend/` | 前端页面骨架 |
| `docs/` | 课程文档和技术文档 |
| `tests/` | 测试用例和后续自动化测试 |

## 4. 后端模块设计

| 模块 | 文件位置 | 职责 |
| --- | --- | --- |
| API 入口 | `backend/app/main.py` | 注册 FastAPI 应用和基础接口 |
| 请求/响应模型 | `backend/app/models.py` | 定义 schema 和 Text2SQL 响应结构 |
| Schema 读取 | `backend/app/services/schema_reader.py` | 当前返回 mock schema，后续读取真实数据库 |
| SQL 安全校验 | `backend/app/services/sql_safety.py` | 当前只允许单条 `SELECT`，后续扩展表字段校验 |
| Text2SQL 服务 | `backend/app/services/text2sql_service.py` | 当前返回 mock SQL 和 mock 数据，后续接入 LLM |
| 数据库脚本 | `backend/app/db/init_stock_demo.sql` | 预留股票演示库建表脚本 |
| 数据采集脚本 | `backend/app/scripts/sync_akshare_data.py` | 后续采集 AkShare 数据并写入 SQLite |

## 5. 前端模块设计

当前前端为静态页面，后续可迁移到 Vue 3。

| 区域 | 说明 |
| --- | --- |
| 问答输入区 | 输入自然语言问题并提交 |
| SQL 展示区 | 展示后端返回的 SQL |
| 查询结果展示区 | 展示摘要和表格结果 |
| 系统状态/测试结果区域 | 展示后端连接状态、SQL 安全状态和测试入口提示 |

## 6. API 设计

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/health` | 返回服务状态 |
| GET | `/api/schema` | 返回当前数据库 schema |
| POST | `/api/text2sql/query` | 接收自然语言问题并返回 SQL、结果和摘要 |

详细请求和响应结构见 `docs/API_DESIGN.md`。

## 7. 数据库设计

初始数据库采用股票演示数据方向。第一阶段使用 AkShare 作为数据来源，但运行时 Text2SQL 只查询本地 SQLite。当前核心表为：

- `stocks`：股票基础信息。
- `daily_prices`：最近 1 年历史日行情数据。
- `stock_quotes`：一次最新行情快照，包含最新价、市盈率、市净率、市值等字段。

后续可扩展 `sectors`、`stock_sector_map`、`market_news`、`financial_indicators` 和 `watchlists`。详细设计见 `docs/DATASET_DESIGN.md`。

## 8. Text2SQL 处理流程

1. 先通过 AkShare 数据采集脚本生成或更新 SQLite 演示库。
2. 前端提交自然语言问题。
3. 后端读取 SQLite 数据库 schema。
4. 构造包含 schema 和安全约束的 prompt。
5. 调用大模型生成 SQL。
6. 执行 SQL 安全校验。
7. 查询 SQLite 并获得结果。
8. 返回 SQL、表格数据和自然语言总结。

当前代码只实现 mock 版本，流程位置已经预留。

## 9. 安全设计

- MVP 阶段只允许 `SELECT` 查询。
- 禁止 `INSERT`、`UPDATE`、`DELETE`、`DROP`、`ALTER`、`TRUNCATE`、`CREATE` 等危险语句。
- 禁止提交 API Key、`.env`、虚拟环境、缓存、日志和临时数据库文件。
- 后续补充表名字段名白名单校验、自动 `LIMIT`、错误日志和审计记录。

## 10. 部署与运行设计

开发阶段采用本地运行：

- 后端：`uvicorn app.main:app --reload`
- 前端：直接打开静态页面，后续改为 Vue 开发服务器
- 数据库：SQLite 本地文件，后续可切换 MySQL

## 11. 后续待补充

- 真实 LLMClient 设计。
- 数据库连接配置和迁移策略。
- RAG 文档处理与向量库设计。
- 测试指标统计方式。
- 最终系统截图和运行环境说明。
