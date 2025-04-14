# Fintech ETL + LLM Pipeline

The task is to build an automated pipeline to fetch historical stock market data, process it, and store it in a PostgreSQL database. The challenge involves setting up a backend API, integrating with financial data sources, and deploying it on Railway.

# Deployed API
## Docs UI (Swagger):
https://fintech-etl-llm-production.up.railway.app/docs

## Base URL:
https://fintech-etl-llm-production.up.railway.app

# Features

1. Fetch historical stock data using a symbol (e.g., AAPL, MSFT, etc.)
2. Store clean and structured data in a PostgreSQL database
3. RESTful API built using FastAPI
4. Live deployment using Railway with automatic CI/CD from GitHub
5. Logs to track data fetch and DB commits
   
# Tech Stack

Backend: Python, FastAPI
Data: - OpenBB API
Database: PostgreSQL (hosted on Railway)
Deployment: Railway + Nixpacks

#  How It Works
1. Fetch stock data from OpenBB
2. Store data in Postgres
3. Send it to OpenRouter (free GPT-like LLM)
4. Save daily recommendations
   
# Use Case
Financial analysis, stock performance tracking, backtesting trading strategies, etc.
