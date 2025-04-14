import pandas as pd
from openbb import obb
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from fintech_data_pipeline.src.database.models import DataEntry
from fintech_data_pipeline.src.database.db_connection import get_db_session
from fintech_data_pipeline.src.utils.helpers import init_router
from openbb_core.app.model.obbject import OBBject
from loguru import logger

router = init_router("equity", "Equity")


@router.post("/fetch-data", summary="Fetch and Store Historical Equity Data")
def get_historical_data(symbol: str = Query("AAPL"), db: Session = Depends(get_db_session)):
    try:
        logger.info(f"Starting to fetch historical data for symbol: {symbol}")

        raw_data = obb.equity.price.historical(symbol=symbol, interval="1d", start_date="2024-01-01")

        # Check if OBBject and has results
        if isinstance(raw_data, OBBject) and isinstance(raw_data.results, list):
            df = pd.DataFrame(raw_data.results)

            if "date" not in df.columns:
                df.rename(columns={"datetime": "date"}, inplace=True)
            if not df.empty:
                logger.info(f"Data fetched successfully for {symbol}. Number of rows: {len(df)}")
                save_data_to_db(db, symbol, df)
                logger.info(f"Data for {symbol} saved successfully to database.")
                return {"message": f"Data for {symbol} saved successfully.", "rows": len(df)}
            else:
                logger.warning(f"No data found in response for symbol: {symbol}")
                return {"error": "No data found in response."}
        else:
            logger.error(f"Failed to fetch valid data for symbol: {symbol}. Raw response: {str(raw_data)}")
            return {"error": "Failed to fetch valid data", "details": str(raw_data)}

    except Exception as e:
        logger.exception(f"Error occurred while fetching or processing data for symbol: {symbol}")
        return {"error": "Internal Server Error", "details": str(e)}


def save_data_to_db(session, symbol, data):
    try:
        logger.info(f"Saving data for symbol {symbol} to the database.")

        # Assuming 'date' is at index 0 and 'close' is at index 4 in the transposed DataFrame
        date_series = data.loc[data.index == 'date', 0:].values.flatten().tolist()
        close_series = data.loc[data.index == 'close', 0:].values.flatten().tolist()

        # Assuming all other rows have the same number of entries as 'date'
        num_entries = len(date_series)

        logger.info(f"Extracted {num_entries} data points for symbol {symbol}.")

        for i in range(num_entries):
            entry_date_str = date_series[i]
            close_value = close_series[i]

            # Convert date string to a date object (assuming 'YYYY-MM-DD' format)
            try:
                entry_date = pd.to_datetime(entry_date_str).date()
            except ValueError as e:
                logger.error(f"Error converting date string '{entry_date_str}' to date object: {e}")
                continue  # Skip this entry if date conversion fails

            entry = DataEntry(
                symbol=symbol,
                date=entry_date,
                value=close_value
            )
            session.add(entry)

        session.commit()
        logger.info(f"Successfully committed {num_entries} rows of data for symbol {symbol} to the database.")

    except Exception as e:
        logger.exception(f"Failed to save data for symbol {symbol} to the database: {e}")
        raise