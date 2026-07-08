const apiBase = "http://127.0.0.1:8000";

const questionInput = document.querySelector("#questionInput");
const submitButton = document.querySelector("#submitButton");
const sqlOutput = document.querySelector("#sqlOutput");
const summaryOutput = document.querySelector("#summaryOutput");
const tableOutput = document.querySelector("#tableOutput");
const statusList = document.querySelector("#statusList");

let testCases = [];

async function loadTestCases() {
  try {
    const res = await fetch("../tests/text2sql_cases.json");
    const data = await res.json();
    testCases = data.cases || data;
  } catch (e) {
    console.warn("加载测试用例失败:", e);
    testCases = [];
  }
}
loadTestCases();

function findMockByQuestion(question) {
  const q = question.trim();

  for (const tc of testCases) {
    if (!tc.mock || !tc.question) continue;

    if (tc.question === q) {
      return tc.mock;
    }
  }

  return null;
}

function renderTable(columns, rows, charts) {
  if (!rows || !rows.length) {
    tableOutput.innerHTML = "<p>暂无结果</p>";
    const chartContainer = document.getElementById("chartContainer");
    if (chartContainer) {
      const instances = echarts.getInstanceByDom(chartContainer);
      if (instances) instances.dispose();
      chartContainer.innerHTML = "";
      chartContainer.style.display = "none";
    }
    return;
  }

  const thead = columns.map((col) => `<th>${col}</th>`).join("");
  const tbody = rows
    .map((row) => {
      const cells = columns.map((col) => `<td>${row[col] ?? ""}</td>`).join("");
      return `<tr>${cells}</tr>`;
    })
    .join("");
  tableOutput.innerHTML = `<table><thead><tr>${thead}</tr></thead><tbody>${tbody}</tbody></table>`;

  const chartContainer = document.getElementById("chartContainer");
  if (!chartContainer) return;

  const instances = echarts.getInstanceByDom(chartContainer);
  if (instances) instances.dispose();

  chartContainer.innerHTML = "";

  if (!charts || !charts.length) {
    chartContainer.style.display = "none";
    return;
  }

  chartContainer.style.display = "block";
  const totalHeight = charts.filter((c) => c.type !== "none").length * 316 + 16;
  chartContainer.style.height = totalHeight + "px";

  charts.forEach((config, index) => {
    if (config.type === "none") return;

    const wrapper = document.createElement("div");
    wrapper.id = `chart-wrapper-${index}`;
    wrapper.style.width = "100%";
    wrapper.style.height = "300px";
    wrapper.style.marginBottom = "16px";
    chartContainer.appendChild(wrapper);

    drawChart(rows, config, wrapper.id);
  });
}

function drawChart(data, chartConfig, containerId) {
  const chartDom = document.getElementById(containerId);
  if (!chartDom) return;
  if (typeof echarts === "undefined") {
    console.warn("ECharts 未加载");
    return;
  }

  chartDom.style.display = "block";

  let myChart = echarts.getInstanceByDom(chartDom);
  if (myChart) myChart.dispose();
  myChart = echarts.init(chartDom);

  const { type, xAxis, yAxis, title } = chartConfig;

  const xData = data.map((row) => row[xAxis] ?? "");
  const yData = data.map((row) => Number(row[yAxis]) || 0);

  const option = {
    title: {
      text: title || `${yAxis} 图表`,
      left: "center",
      textStyle: { fontSize: 16, fontWeight: "normal" },
    },
    tooltip: {
      trigger: "axis",
      formatter: function (params) {
        const p = params[0];
        return `<strong>${p.name}</strong><br/>${yAxis}：${p.value.toLocaleString()}`;
      },
    },
    grid: {
      left: "10%",
      right: "5%",
      bottom: "15%",
      top: "20%",
    },
    xAxis: {
      type: "category",
      data: xData,
      axisLabel: {
        rotate: xData.length > 6 ? 30 : 0,
        interval: 0,
        fontSize: 11,
      },
    },
    yAxis: {
      type: "value",
      name: yAxis,
      nameTextStyle: { fontSize: 12 },
      axisLabel: {
        formatter: function (value) {
          if (value >= 1000000000000) return value / 1000000000000 + "万亿";
          else if (value >= 100000000) return value / 100000000 + "亿";
          else if (value >= 10000) return value / 10000 + "万";
          else return value;
        },
      },
    },
    series: [
      {
        type: type === "line" ? "line" : "bar",
        data: yData,
        barWidth: type === "line" ? undefined : "45%",
        itemStyle: {
          color: "#409EFF",
          borderRadius: type === "line" ? undefined : [4, 4, 0, 0],
        },
        label: {
          show: true,
          position: "top",
          formatter: function (params) {
            return params.value.toLocaleString();
          },
          fontSize: 10,
        },
        smooth: type === "line",
      },
    ],
  };

  myChart.setOption(option);
}

async function submitQuestion() {
  const question = questionInput.value.trim();
  if (!question) return;

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
      signal: AbortSignal.timeout(3000),
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    sqlOutput.textContent = data.sql;
    summaryOutput.textContent = data.summary;
    renderTable(data.columns, data.rows, data.charts);
    setStatus(["后端接口：已连接", "数据来源：后端 API"]);
  } catch (error) {
    const mock = findMockByQuestion(question) || {
      sql: "未找到匹配的测试用例",
      columns: [],
      rows: [],
      summary: `未找到与 "${question}" 匹配的测试用例`,
    };

    sqlOutput.textContent = mock.sql;
    summaryOutput.textContent = mock.summary;
    renderTable(mock.columns, mock.rows, mock.charts);
    setStatus(["后端接口：未连接，使用本地 Mock", `错误：${error.message}`]);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "提交问题";
  }
}
submitButton.addEventListener("click", submitQuestion);
