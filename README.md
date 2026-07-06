# 基于 Text2SQL 与 RAG 的大模型智能问答系统

本项目是小学期课程项目《基于 Text2SQL 的大模型智能问答系统实现》的工程仓库，并预留第二阶段《基于 RAG 的大模型智能问答系统实现》能力。系统目标是让用户用自然语言查询结构化数据库，并在后续通过 RAG 查询非结构化知识文档。

当前优先实现 Text2SQL 最小闭环：用户输入自然语言问题，后端拼接数据库 schema 和约束，调用大模型生成 SQL，进行 SQL 安全校验，执行查询并返回表格结果，再由大模型生成简要解释。

初始演示数据集选择股票相关数据。股票数据仅用于课程项目演示、数据库问答测试和字段概念解释，不用于真实投资建议。

## 文档目录

| 文档 | 说明 |
| --- | --- |
| [docs/TECHNICAL_ROUTE.md](docs/TECHNICAL_ROUTE.md) | 项目定位、技术路线、阶段规划、技术栈和模块划分 |
| [docs/DATASET_DESIGN.md](docs/DATASET_DESIGN.md) | 股票演示数据集表结构、示例问题和 RAG 知识库建议 |
| [docs/TASK_ASSIGNMENT.md](docs/TASK_ASSIGNMENT.md) | 4 人团队分工、交付物和协作节奏 |
| [docs/API_DESIGN.md](docs/API_DESIGN.md) | Text2SQL、Schema、RAG、Hybrid 和评估 API 初版设计 |
| [docs/CODEX_WORKFLOW.md](docs/CODEX_WORKFLOW.md) | 后续使用 Codex 协作时的 Git 与工程规范 |

## 初始开发目标

1. 搭建 FastAPI 后端基础结构。
2. 设计并初始化股票演示数据库。
3. 实现 schema 读取、prompt 构造、Text2SQL 调用和只读 SQL 执行。
4. 搭建 Vue 3 前端问答页面，展示生成 SQL、表格结果和摘要。
5. 建立测试问题集，记录 SQL 执行成功率和典型错误。

## 注意事项

- 初版仅允许执行 `SELECT` 查询，写操作能力作为后续受控扩展讨论。
- API Key、`.env`、缓存、虚拟环境、临时数据库文件不得提交到 Git。
- 股票相关回答必须带有课程演示和非投资建议边界。
