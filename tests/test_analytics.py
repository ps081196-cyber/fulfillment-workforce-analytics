import pandas as pd
from analytics import capacity_plan, headline_kpis, prepare_workforce

def sample():
    return pd.DataFrame({
        "date":["2026-01-01"], "shift":["Morning"], "process":["Picking"],
        "scheduled_headcount":[10], "present_headcount":[9], "labor_hours":[72],
        "units_processed":[1440], "planned_units":[1600], "backlog_units":[320],
    })

def test_kpis():
    df = prepare_workforce(sample())
    kpi = headline_kpis(df)
    assert kpi["uplh"] == 20
    assert kpi["plan_attainment"] == 90
    assert kpi["attendance_rate"] == 90

def test_capacity_plan():
    plan = capacity_plan(prepare_workforce(sample()))
    assert plan.iloc[0]["additional_headcount"] == 2
