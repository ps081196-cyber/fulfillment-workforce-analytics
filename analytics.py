"""Fulfillment workforce and capacity calculations."""
import math
import pandas as pd

REQUIRED = {
    "date", "shift", "process", "scheduled_headcount", "present_headcount",
    "labor_hours", "units_processed", "planned_units", "backlog_units",
}

def prepare_workforce(data: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    df = data.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    safe_hours = df["labor_hours"].replace(0, pd.NA)
    safe_plan = df["planned_units"].replace(0, pd.NA)
    safe_scheduled = df["scheduled_headcount"].replace(0, pd.NA)
    df["units_per_labor_hour"] = (df["units_processed"] / safe_hours).fillna(0)
    df["plan_attainment"] = (df["units_processed"] / safe_plan * 100).fillna(0)
    df["attendance_rate"] = (df["present_headcount"] / safe_scheduled * 100).fillna(0)
    return df

def headline_kpis(df: pd.DataFrame) -> dict:
    hours = df["labor_hours"].sum()
    return {
        "units_processed": int(df["units_processed"].sum()),
        "uplh": float(df["units_processed"].sum() / hours) if hours else 0,
        "plan_attainment": float(df["units_processed"].sum() / df["planned_units"].sum() * 100)
        if df["planned_units"].sum() else 0,
        "attendance_rate": float(df["present_headcount"].sum() / df["scheduled_headcount"].sum() * 100)
        if df["scheduled_headcount"].sum() else 0,
        "backlog": int(df["backlog_units"].sum()),
    }

def capacity_plan(df: pd.DataFrame, shift_hours: float = 8) -> pd.DataFrame:
    rows = []
    for process, group in df.groupby("process"):
        uplh = group["units_per_labor_hour"].replace(0, pd.NA).median()
        backlog = group["backlog_units"].sum()
        required = math.ceil(backlog / (uplh * shift_hours)) if pd.notna(uplh) and uplh > 0 else 0
        rows.append({"process": process, "backlog_units": int(backlog),
                     "median_uplh": round(float(uplh or 0), 1),
                     "additional_headcount": required})
    return pd.DataFrame(rows).sort_values("additional_headcount", ascending=False)
