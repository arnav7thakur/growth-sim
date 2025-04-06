def compute_metrics(data: dict) -> dict:
    """
    Given parsed data (from CSV/JSON/XLSX), compute metrics like CAC, LTV, Retention, and Score.
    """
    # Example placeholders — use actual field keys from parsed data
    CAC = float(data.get("CAC", 0))
    LTV = float(data.get("LTV", 0))
    retention = float(data.get("Retention", 1.0))

    score = (LTV / CAC) * retention if CAC > 0 else 0

    return {
        "CAC": round(CAC, 2),
        "LTV": round(LTV, 2),
        "Retention": round(retention, 2),
        "Score": round(score, 2)
    }
