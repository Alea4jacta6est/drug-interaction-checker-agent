import pandas as pd

def load_excel(path: str, sheet: str = None) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name=sheet) if sheet else pd.read_excel(path)