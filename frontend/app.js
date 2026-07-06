const apiBase = "http://127.0.0.1:8000";

const questionInput = document.querySelector("#questionInput");
const submitButton = document.querySelector("#submitButton");
const sqlOutput = document.querySelector("#sqlOutput");
const summaryOutput = document.querySelector("#summaryOutput");
const tableOutput = document.querySelector("#tableOutput");
const statusList = document.querySelector("#statusList");

const fallbackResponse = {
  sql: "SELECT s.symbol, s.stock_name, p.volume FROM daily_prices p JOIN stocks s ON p.stock_id = s.stock_id ORDER BY p.volume DESC LIMIT 10",
  columns: ["symbol", "stock_name", "volume"],
  rows: [
    { symbol: "600000", stock_name: "示例银行", volume: 12800000 },
    { symbol: "000001", stock_name: "示例科技", volume: 8600000 },
  ],
  summary: "后端接口不可用时展示的本地 mock 结果；股票数据仅用于课程演示，不构成投资建议。",
};

function renderTable(columns, rows) {
  if (!rows.length) {
    tableOutput.innerHTML = "<p>暂无结果</p>";
    return;
  }

  const thead = columns.map((column) => `<th>${column}</th>`).join("");
  const tbody = rows
    .map((row) => {
      const cells = columns.map((column) => `<td>${row[column] ?? ""}</td>`).join("");
      return `<tr>${cells}</tr>`;
    })
    .join("");

  tableOutput.innerHTML = `<table><thead><tr>${thead}</tr></thead><tbody>${tbody}</tbody></table>`;
}

function setStatus(items) {
  statusList.innerHTML = items.map((item) => `<li>${item}</li>`).join("");
}

async function submitQuestion() {
  const question = questionInput.value.trim();
  if (!question) {
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "查询中...";
  sqlOutput.textContent = "正在请求后端接口...";
  summaryOutput.textContent = "等待查询结果...";
  tableOutput.innerHTML = "";

  try {
    const response = await fetch(`${apiBase}/api/text2sql/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, database: "stock_demo" }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    sqlOutput.textContent = data.sql;
    summaryOutput.textContent = data.summary;
    renderTable(data.columns, data.rows);
    setStatus(["后端接口：已连接", `SQL 安全校验：${data.safe ? "通过" : "未通过"}`, "当前模式：mock"]);
  } catch (error) {
    sqlOutput.textContent = fallbackResponse.sql;
    summaryOutput.textContent = fallbackResponse.summary;
    renderTable(fallbackResponse.columns, fallbackResponse.rows);
    setStatus(["后端接口：未连接，已使用本地 mock", "SQL 安全校验：前端 mock 展示", `错误信息：${error.message}`]);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "提交问题";
  }
}

submitButton.addEventListener("click", submitQuestion);
