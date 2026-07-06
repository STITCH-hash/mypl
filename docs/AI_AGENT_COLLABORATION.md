# AI 写作与 Agent 合作规范

本文档用于约定后续使用 AI 写作工具、编程助手或 Agent 参与开发时的基本流程。目标是让每次修改都可追踪、可验证、可回滚，避免把密钥、缓存或临时文件提交到仓库。

## 1. 修改前检查

每次开始任务前，先查看 Git 状态：

```bash
git status --short --branch
```

如果工作区已有未提交内容，要先判断这些修改是否与当前任务相关。不要随意覆盖或还原他人的改动。

## 2. 使用功能分支

不要直接在 `main` 上乱改。每个任务创建一个语义清楚的分支，例如：

```bash
git checkout -b feat/text2sql-query-api
git checkout -b docs/update-api-design
git checkout -b fix/sql-safety-check
```

分支名建议包含类型和主题，方便团队成员从名称判断修改范围。

## 3. 一次任务只做一类修改

一次任务尽量只处理一个目标，例如只做后端接口、只做前端页面、只更新文档或只修复某个 bug。不要把大范围重构、格式化、功能开发和文档改动混在一个提交里。

## 4. 修改后做验证

修改后运行能运行的测试或至少做静态检查。示例：

```bash
pytest
npm run lint
npm run build
```

如果当前项目还没有测试命令，也要至少运行相关服务或检查 Markdown、JSON、Python 语法等基础问题。无法运行的检查需要在提交或 PR 说明中写清楚原因。

## 5. 不提交密钥

API Key、数据库密码、私有 Token、`.env` 文件和任何密钥都不能提交到 Git。需要配置示例时，只提交 `.env.example`，并使用占位值。

## 6. 不提交临时文件

不要提交虚拟环境、缓存、构建产物、数据库临时文件和日志文件，例如：

- `.venv/`
- `venv/`
- `node_modules/`
- `__pycache__/`
- `.pytest_cache/`
- `*.db`
- `*.sqlite`
- `*.log`

提交前使用 `git status` 和 `git diff --stat` 检查是否混入无关文件。

## 7. 提交信息要清楚

提交信息使用简洁的英文前缀和明确描述，例如：

```bash
git commit -m "docs: add technical route and team plan"
git commit -m "feat: add text2sql query api"
git commit -m "fix: block unsafe sql statements"
```

常用前缀包括 `feat`、`fix`、`docs`、`test`、`refactor`、`chore`。

## 8. Push 前展示修改摘要

Push 前建议执行：

```bash
git status
git diff --stat HEAD
```

如果是首次提交或还没有 `HEAD`，可以使用：

```bash
git diff --stat --cached
```

确认只包含当前任务相关文件后再 push。

## 9. 优先使用 PR

如果仓库支持 PR，优先开 PR，而不是直接合入 `main`。PR 描述建议包含：

- 本次修改内容。
- 已完成的验证。
- 已知限制或后续任务。
- 是否涉及配置、数据库或 API 变更。

团队成员 review 后再合并，有利于减少接口不一致和重复实现。
