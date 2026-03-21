# 🚀 NSE MCP Server

⚡ Powered by `uv` + `pyproject.toml` for modern, fast, and reproducible Python environments

A powerful MCP (Model Context Protocol) server for accessing NSE (National Stock Exchange of India) data, financial insights, and advanced stock screening.

🔗 GitHub: https://github.com/JAY-MU-4098/nse-mcp-server
🔗 LinkedIn: https://www.linkedin.com/in/jay-gogra-108991237/
---

## 📌 Features

### 📊 Market Data
- Real-time stock price
- Symbol information
- Market status
- All NSE indices
- Index-specific data

### 📈 Options & F&O
- Option chain data
- Expiry dates
- F&O stock list

### 📉 Historical & Trading Insights
- Historical price data (multiple intervals)
- Delivery history
- Insider trading data
- Pledged shares data
- SAST disclosures

### 🔍 Screener Engine
- Custom query-based screener
- AND / OR logic support
- Operators: `gt`, `lt`, `eq`, `between`, `in`
- Predefined screeners:
  - Top Gainers
  - Top Losers
  - Undervalued Stocks
  - Growth Stocks
  - Top Mutual Funds

### 🏢 Financial Data
- Financial statements
- Balance sheet data
- ESG scores
- Company profile

### 📊 Analytics & Insights
- Analyst recommendations
- Earnings calendar
- Earnings forecast
- Holdings data

### 📰 Additional Data
- Stock news
- Insider activity
- Corporate actions

---

## 🧠 Why This Project?

Most NSE-related tools are:
- Not developer-friendly
- Limited in flexibility
- Not AI-ready

This project aims to provide:
- Clean MCP-based API abstraction
- AI-agent compatibility
- Extensible architecture
- Unified access to multiple data sources

---

## ⚙️ Installation (uv + pyproject.toml)

This project uses `uv` for ultra-fast dependency management.

### 1️⃣ Install uv

```bash
pip install uv
```

### 2️⃣ Clone the repository

```bash
git clone https://github.com/JAY-MU-4098/nse-mcp-server.git
cd nse-mcp-server
```

### 3️⃣ Create virtual environment
```bash
uv venv
source .venv/bin/activate   # Linux / Mac
# .venv\Scripts\activate    # Windows
```


### 4️⃣ Install dependencies
```bash
uv sync
```

### 🚀 Running the Server
```bash
# if you want it as api
python app/main.py
```

### 📁 Project Structure
```
nse-mcp-server/
│── app/
│   ├── main.py              # FastAPI entry point
│   ├── mcp_server.py       # MCP server logic
│   ├── tools.py            # Tool definitions
│   ├── utils/
│   │   ├── pnsea_lib.py
│   │   ├── pnsea_nse_client.py
│   │   ├── yfinance_lib.py
│   │   └── yfinance_screnner.py
│   └── test_mcp.py
│
│── pyproject.toml
│── uv.lock
│── README.md
```

### 🧠 MCP Usage

You can connect this server with MCP-compatible clients like:
- Claude Desktop
- Custom AI agents
- Automation tools
```bash
result = await client.call_tool("get_current_price", {"symbol": "RELIANCE"})

result = await client.call_tool(
    "run_screener",
    {
        "screener_type": "equity",
        "query_dict": {
            "and": [
                {"field": "pe", "op": "lt", "value": 8},
                {"field": "priceToBook", "op": "lt", "value": 3}
            ]
        },
        "index": "NIFTY"
    }
)
```

### 🔧 Claude Desktop MCP Config
- open claude desktop go to settings > developer > Edit Config JSON 
```
for web base usage 
{
  "mcpServers": {
    "nse-mcp-server": {
      "transport": "http",
      "url": "http://127.0.0.1:8001/mcp",
    }
  }
}

for local STDIO base usage
- Update 1 line in mcp_server.py 
    server.run(transport="http", host="0.0.0.0", port=8001) from to
    server.run()

{
  "mcpServers": {
    "nse-mcp-server": {
      "transport": "stdio",
      "command": "path/to/uv",
      "args": ["run", "path/to/app/mcp_server.py"]
    }
  }
}
```
- Restart Claude

### 🧩 Use Cases
- AI Trading Assistants
- Algo Trading Systems
- Stock Screeners
- Financial APIs
- Research Tools

