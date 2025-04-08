import pandas as pd
import json

def parse_upload_file(uploaded_file):
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


def extract_metrics(df):
    """
    Extracts and normalizes metric names and values from a DataFrame.
    Returns a dictionary of standardized metrics like {'CAC': 120, 'LTV': 450}.
    """
    synonym_map = {
        "customer_acquisition_cost": "CAC",
        "cac": "CAC",
        "ltv": "LTV",
        "customer_lifetime_value": "LTV",
        "churn": "Churn Rate",
        "churn_rate": "Churn Rate",
        "retention_rate": "Retention Rate",
        "arpu": "ARPU",
        "mrr": "MRR",
        "arr": "ARR",
        "conversion_rate": "Conversion Rate",
        "revenue_per_customer": "Revenue per Customer",
        "avg_revenue_per_customer": "Revenue per Customer",
    }

    metrics = {}

    for col in df.columns:
        normalized = col.strip().lower().replace(" ", "_")
        if normalized in synonym_map:
            kpi_name = synonym_map[normalized]
            value = df[col].values[0]
            if pd.notna(value):
                try:
                    metrics[kpi_name] = float(value)
                except ValueError:
                    continue  # skip non-numeric values
        else:
            print(f"⚠️ Unknown metric '{col}' – will be ignored for now.")

    return metrics
