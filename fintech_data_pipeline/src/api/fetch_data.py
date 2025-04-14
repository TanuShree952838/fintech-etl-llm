# src/api/fetch_data.py

import pandas as pd
from openbb import obb
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from fintech_data_pipeline.src.database.models import DataEntry
from fintech_data_pipeline.src.database.db_connection import get_db_session
from fintech_data_pipeline.src.utils.helpers import init_router
from openbb_core.app.model.obbject import OBBject  # Make sure this import is correct


router = init_router("equity", "Equity")


@router.post("/fetch-data", summary="Fetch and Store Historical Equity Data")
def get_historical_data(symbol: str = Query("AAPL"), db: Session = Depends(get_db_session)):
    try:
        raw_data = obb.equity.price.historical(symbol=symbol, interval="1d", start_date="2024-01-01")

        # Check if OBBject and has results
        if isinstance(raw_data, OBBject) and isinstance(raw_data.results, list):
            df = pd.DataFrame(raw_data.results)

            if not df.empty:
                save_data_to_db(db, symbol, df)
                return {"message": f"Data for {symbol} saved successfully.", "rows": len(df)}
            else:
                return {"error": "No data found in response."}
        else:
            return {"error": "Failed to fetch valid data", "details": str(raw_data)}

    except Exception as e:
        return {"error": "Internal Server Error", "details": str(e)}


def save_data_to_db(session, symbol, data):
    # Rename columns if needed to match expected names
    if "date" not in data.columns:
        data.rename(columns={"datetime": "date"}, inplace=True)

    for _, row in data.iterrows():
        entry = DataEntry(
            symbol=symbol,
            date=row["date"],
            value=row["close"]
        )
        session.add(entry)
    session.commit()
