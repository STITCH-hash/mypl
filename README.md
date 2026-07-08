# 基于 Text2SQL 与 RAG 的大模型智能问答系统

本项目是小学期课程项目《基于 Text2SQL 的大模型智能问答系统实现》的工程仓库，并预留第二阶段《基于 RAG 的大模型智能问答系统实现》能力。系统目标是让用户使用自然语言查询结构化数据库，后续再通过 RAG 查询非结构化知识文档。

当前阶段目标是“框架规范 + 最小可运行 + 符合课程文档要求”。项目先实现 Text2SQL 最小闭环的接口骨架，暂时使用 mock schema、mock SQL 和 mock 查询结果，后续通过 AkShare 采集股票数据写入 SQLite，再接入真实大模型、数据库查询和评估流程。

初始演示数据集选择股票相关数据。第一阶段计划采集约 30 支 A 股的基础信息、最近 1 年日行情和最新行情快照，形成 `stocks`、`daily_prices`、`stock_quotes` 三张核心表。股票数据仅用于课程项目演示、数据库问答测试和字段概念解释，不用于真实投资建议。

## 当前技术路线

```text
用户自然语言问题
→ 后端读取数据库 schema
→ 构造 prompt
→ 调用大模型生成 SQL
→ SQL 安全校验
→ 执行 SQL
→ 返回表格结果与自然语言总结
```

MVP 阶段只允许 `SELECT` 查询。RAG、Agent、多轮复杂推理和真实行情接入都放到后续阶段。

数据使用路线：

```text
AkShare
→ Python 采集脚本
→ 清洗字段并写入 SQLite
→ Text2SQL 查询 SQLite
→ 前端展示结果
```

数据更新策略：

```text
第一阶段：手动运行采集脚本，保证演示数据可复现
第二阶段：每天 18:00 定时运行采集脚本，更新 SQLite
不采用：用户每次提问时实时请求 AkShare
```

## 目录结构

```text
.
├── backend/                    # FastAPI 后端最小骨架
│   ├── app/
│   │   ├── db/                 # 数据库初始化脚本预留位置
│   │   ├── scripts/            # AkShare 数据采集脚本预留位置
│   │   ├── services/           # schema 读取、SQL 安全校验、Text2SQL 服务
│   │   └── main.py             # API 入口
│   ├── README.md
│   ├── requirements-data.txt   # AkShare 数据采集可选依赖
│   └── requirements.txt
├── frontend/                   # 前端基础页面框架
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── docs/                       # 课程文档与技术文档
├── tests/                      # 测试用例与后续自动化测试
│   └── text2sql_cases.json
└── README.md
```

## 如何启动后端

进入后端目录：

```bash
cd backend
```

创建并激活虚拟环境后安装依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

启动 FastAPI 服务：

```bash
uvicorn app.main:app --reload
```

启动后可访问：

- `GET http://127.0.0.1:8000/api/health`
- `GET http://127.0.0.1:8000/api/schema`
- `POST http://127.0.0.1:8000/api/text2sql/query`

## 如何查看前端

当前前端是轻量静态页面。可以直接用浏览器打开：

```text
frontend/index.html
```

由于浏览器 CORS 策略限制，直接用 file:// 协议打开时无法加载 tests/text2sql_cases.json。
推荐使用 VS Code Live Server：右键 index.html → "Open with Live Server" 打开。

如果后端已启动，前端会优先调用后端接口；如果接口不可用，前端自动从 tests/text2sql_cases.json 加载 mock 数据。

## 后端接口格式

{
  "sql": "SELECT ...",
  "columns": ["股票名称", "成交量"],
  "rows": [{ "股票名称": "示例银行", "成交量": 66570000 }],
  "summary": "查询结果摘要",
  "charts": [
    { "type": "bar", "xAxis": "股票名称", "yAxis": "成交量", "title": "成交量 TOP 5" }
  ]
}

若 charts 为空数组或不传，则不显示图表。type 支持 bar（柱状图）和 line（折线图）。

## 文档目录

| 文档 | 说明 |
| --- | --- |
| [docs/REQUIREMENTS_SPECIFICATION.md](docs/REQUIREMENTS_SPECIFICATION.md) | 需求规格说明书骨架 |
| [docs/SYSTEM_DESIGN_SPECIFICATION.md](docs/SYSTEM_DESIGN_SPECIFICATION.md) | 系统设计说明书骨架 |
| [docs/TEST_REPORT.md](docs/TEST_REPORT.md) | 测试报告骨架 |
| [docs/TASK_ASSIGNMENT.md](docs/TASK_ASSIGNMENT.md) | 小组分工说明 |
| [docs/TECHNICAL_ROUTE.md](docs/TECHNICAL_ROUTE.md) | 项目定位、技术路线、阶段规划、技术栈和模块划分 |
| [docs/DATASET_DESIGN.md](docs/DATASET_DESIGN.md) | 股票演示数据集表结构、示例问题和 RAG 知识库建议 |
| [docs/API_DESIGN.md](docs/API_DESIGN.md) | Text2SQL、Schema、RAG、Hybrid 和评估 API 初版设计 |
| [docs/AI_AGENT_COLLABORATION.md](docs/AI_AGENT_COLLABORATION.md) | 后续使用 AI 写作工具或 Agent 协作时的 Git 与工程规范 |

## 当前完成状态

- 已建立 `backend/`、`frontend/`、`docs/`、`tests/` 基础结构。
- 后端已提供 FastAPI mock 接口：健康检查、schema 查询、Text2SQL 查询。
- 后端已预留数据库初始化脚本、AkShare 数据采集脚本位置、schema 读取模块、SQL 安全校验模块。
- 前端已提供问答输入区、SQL 展示区、查询结果展示区、系统状态/测试结果区域，已接入ECharts。
- `tests/text2sql_cases.json` 已提供第一批股票相关自然语言测试问题(含 mock 数据和图表配置)。
- 课程要求文档已建立骨架，便于后续补充截图、测试结果和设计细节。

## 后续开发计划

1. 完成 SQLite 股票演示库建表：`stocks`、`daily_prices`、`stock_quotes`。
2. 编写 AkShare 数据采集脚本，采集约 30 支 A 股、最近 1 年日行情和一次最新行情快照。
3. 增加每天 18:00 的定时同步任务，用于更新 SQLite 演示库。
4. 将 `/api/schema` 从 mock 数据切换为真实数据库 introspection。
5. 接入统一 `LLMClient`，替换 mock SQL 生成逻辑。
6. 完善 SQL 安全校验，限制只读查询并自动补充 `LIMIT`。
7. 前端接入真实 API 状态、错误提示和表格/图表展示。
8. 基于 `tests/text2sql_cases.json` 记录执行成功率和错误类型。

## 注意事项

- 不提交 API Key、`.env`、虚拟环境、缓存、临时数据库文件。
- 不在当前阶段引入复杂 Agent 框架。
- 不在当前阶段实现复杂 RAG，只保留文档和接口方向。
- 股票相关回答必须说明课程演示边界，不构成投资建议。