import pandas as pd
import json
from io import StringIO, BytesIO

def load_and_parse(uploaded_file):
    """
    Accepts uploaded .csv, .xlsx, or .json file.
    Returns a pandas DataFrame or raises ValueError.
    """
    filename = uploaded_file.name.lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        elif filename.endswith(".json"):
            data = json.load(uploaded_file)
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unsupported file format. Please upload a .csv, .xlsx, or .json file.")
        
        # Clean column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        return df
    except Exception as e:
        raise ValueError(f"Failed to parse the file: {e}")
