import sys
import os
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# Set path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'fintech_data_pipeline'))

from fintech_data_pipeline.src.api import fetch_data
from fintech_data_pipeline.src.api.fetch_data import save_data_to_db
from fintech_data_pipeline.src.insights.process_insights import generate_insights
from fintech_data_pipeline.src.database.db_connection import SessionLocal
from fintech_data_pipeline.src.api.fetch_data import router as equity_router

app = FastAPI()

# Setup scheduler to run daily
scheduler = BackgroundScheduler()

def fetch_and_process_data():
    session = SessionLocal()
    # Use OpenBB API directly instead of FastAPI route
    data = fetch_data.obb.equity.price.historical(
        symbol="AAPL", interval="1d", start_date="2024-01-01"
    )
    save_data_to_db(session, "AAPL", data)
    insights = generate_insights(data)
    print(f"[{datetime.now()}] Insights: {insights}")

scheduler.add_job(fetch_and_process_data, 'interval', hours=24)
scheduler.start()

@app.get("/")
def read_root():
    return {"message": "Fintech Data Pipeline is Running!"}

# Include equity router
app.include_router(equity_router)
