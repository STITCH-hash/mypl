# Frontend

当前前端是静态页面骨架，用于展示课程项目最小界面结构。后续可以替换为 Vue 3 + Element Plus工程。
已接入ECharts

## 页面区域

- 问答输入区
- SQL 展示区
- 查询结果展示区
- 系统状态/测试结果区域

## 数据流

1. 用户输入问题，点击提交
2. 前端请求后端 API：`POST /api/text2sql/query`
3. 后端返回 JSON，包含：
   - `sql`: 生成的 SQL 语句
   - `columns`: 表格列名（中文）
   - `rows`: 表格数据
   - `summary`: 结果摘要
   - `charts`: 图表配置数组（每个图表包含 `type`、`xAxis`、`yAxis`、`title`）
4. 前端渲染表格和图表

## 本地 Mock

后端未启动时，前端自动从 `tests/text2sql_cases.json` 加载测试数据，按 `question` 字段匹配对应的 mock 数据。

## 使用方式

直接用浏览器打开 `frontend/index.html`，如遇 CORS 问题，建议使用 Live Server 启动。
如果后端已启动，页面会请求 `http://127.0.0.1:8000/api/text2sql/query`；否则展示本地 mock 结果。