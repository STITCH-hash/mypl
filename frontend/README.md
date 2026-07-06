# Frontend

当前前端是静态页面骨架，用于展示课程项目最小界面结构。后续可以替换为 Vue 3 + Element Plus + ECharts 工程。

## 页面区域

- 问答输入区
- SQL 展示区
- 查询结果展示区
- 系统状态/测试结果区域

## 使用方式

直接用浏览器打开 `frontend/index.html`。如果后端已启动，页面会请求 `http://127.0.0.1:8000/api/text2sql/query`；否则展示本地 mock 结果。
