import pandas as pd
import plotly.express as px
import streamlit as st
from analytics import capacity_plan, headline_kpis, prepare_workforce

st.set_page_config(page_title="Fulfillment Workforce Analytics", page_icon="🏭", layout="wide")
st.title("🏭 Fulfillment Workforce Analytics")
st.caption("Productivity, attendance, backlog and capacity planning for shift operations.")

uploaded = st.sidebar.file_uploader("Upload workforce CSV", type="csv")
source = uploaded if uploaded else "data/workforce.csv"

try:
    df = prepare_workforce(pd.read_csv(source))
except Exception as exc:
    st.error(str(exc))
    st.stop()

shift = st.sidebar.multiselect("Shift", sorted(df["shift"].unique()))
process = st.sidebar.multiselect("Process", sorted(df["process"].unique()))
if shift:
    df = df[df["shift"].isin(shift)]
if process:
    df = df[df["process"].isin(process)]

kpi = headline_kpis(df)
cards = st.columns(5)
cards[0].metric("Units processed", f"{kpi['units_processed']:,}")
cards[1].metric("Units/labor hour", f"{kpi['uplh']:.1f}")
cards[2].metric("Plan attainment", f"{kpi['plan_attainment']:.1f}%")
cards[3].metric("Attendance", f"{kpi['attendance_rate']:.1f}%")
cards[4].metric("Backlog", f"{kpi['backlog']:,}")

left, right = st.columns(2)
by_process = df.groupby("process", as_index=False).agg(
    units_per_labor_hour=("units_per_labor_hour","mean"),
    plan_attainment=("plan_attainment","mean"),
    backlog_units=("backlog_units","sum"),
)
left.plotly_chart(px.bar(by_process, x="process", y="units_per_labor_hour",
                         color="plan_attainment", title="Productivity by process"), use_container_width=True)
by_shift = df.groupby("shift", as_index=False).agg(
    attendance_rate=("attendance_rate","mean"), plan_attainment=("plan_attainment","mean"))
right.plotly_chart(px.scatter(by_shift, x="attendance_rate", y="plan_attainment", text="shift",
                              size="plan_attainment", title="Shift attendance vs attainment"), use_container_width=True)

st.subheader("Capacity recommendation")
plan = capacity_plan(df)
st.dataframe(plan, use_container_width=True)
st.plotly_chart(px.bar(plan, x="process", y="additional_headcount", color="backlog_units",
                       title="Additional headcount required to clear backlog"), use_container_width=True)
st.download_button("Download capacity plan", plan.to_csv(index=False), "capacity_plan.csv", "text/csv")
