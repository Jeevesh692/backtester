import pandas as pd

def load_prices(path: str) -> pd.DataFrame:
    # 1. Read the CSV
    df = pd.read_csv(path)
    
    # 2. Check that all five required columns are present
    required_columns = {"time", "open", "high", "low", "close"}
    missing_columns = required_columns - set(df.columns)
    
    if missing_columns:
        # Sort the missing names for a clean, predictable error message
        missing_str = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing_str}")
        
    # 3. Convert 'time' to datetimes
    df["time"] = pd.to_datetime(df["time"])
    
    # 4. Sort by 'time' and reset the index
    df = df.sort_values(by="time").reset_index(drop=True)
    
    return df
