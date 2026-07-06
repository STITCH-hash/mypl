# Backend

后端使用 FastAPI 搭建最小可运行骨架。当前接口返回 mock 数据，重点是确定项目结构和 API 形态，后续再通过 AkShare 采集股票数据写入 SQLite，并接入真实数据库查询与大模型。

## 启动方式

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

后续实现 AkShare 数据采集时，再额外安装：

```bash
pip install -r requirements-data.txt
```

## 当前接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/api/health` | 健康检查 |
| GET | `/api/schema` | 返回股票演示库 mock schema |
| POST | `/api/text2sql/query` | 返回 mock SQL、mock 查询结果和摘要 |

## 后续接入点

- `app/db/init_stock_demo.sql`：数据库初始化脚本。
- `app/scripts/sync_akshare_data.py`：后续 AkShare 数据采集脚本位置。
- `app/services/schema_reader.py`：后续改为读取真实数据库 schema。
- `app/services/sql_safety.py`：后续增强 SQL 安全校验。
- `app/services/text2sql_service.py`：后续接入真实 `LLMClient`。
