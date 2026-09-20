# Fulfillment Workforce Analytics

A Streamlit workforce-planning dashboard for fulfillment-center operations. It evaluates hourly productivity, labor utilization, backlog, attendance and staffing gaps, then recommends where capacity should be added.

## KPIs

- Units per labor hour
- Plan attainment
- Labor utilization
- Attendance rate
- Backlog by process
- Required versus scheduled headcount
- Shift and process performance

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The project includes realistic synthetic sample data and supports CSV uploads.

## Required columns

`date, shift, process, scheduled_headcount, present_headcount, labor_hours, units_processed, planned_units, backlog_units`

## Testing

```bash
pytest
```

## Technology

Python · pandas · Streamlit · Plotly · pytest

## Business use

Operations leaders can use the dashboard during shift reviews to find capacity constraints, compare process performance and estimate the additional headcount required to clear backlog.
