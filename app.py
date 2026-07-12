import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import load_data
from utils.metrics import compute_metrics

st.set_page_config(page_title="Caster Performance Dashboard", page_icon="🏭", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #071622 0%, #0b2545 100%);
        color: #f4f8ff;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .stMetric {
        background-color: rgba(7, 28, 48, 0.95);
        border: 1px solid #2d6cdf;
        border-radius: 10px;
        padding: 10px;
    }
    div[data-testid="stSidebar"] {
        background: #071622;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def get_filtered_data():
    df = load_data()
    return df


if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False

if st.sidebar.checkbox("Auto refresh", value=st.session_state.auto_refresh, key="auto_refresh"):
    try:
        from streamlit_autorefresh import st_autorefresh

        st_autorefresh(interval=30000, limit=100, key="caster_refresh")
    except Exception:
        st.sidebar.info("Auto refresh package is not available in the environment.")

st.sidebar.header("Filters")
df = get_filtered_data()

min_date = df["Timestamp"].dt.date.min()
max_date = df["Timestamp"].dt.date.max()

selected_dates = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = selected_dates
    end_date = selected_dates

shift_filter = st.sidebar.selectbox("Shift", ["All", *sorted(df["Shift"].unique())])
heat_filter = st.sidebar.selectbox("Heat Number", ["All", *sorted(df["Heat Number"].astype(str).unique())])

filtered_df = df.copy()
filtered_df = filtered_df[(filtered_df["Timestamp"].dt.date >= start_date) & (filtered_df["Timestamp"].dt.date <= end_date)]
if shift_filter != "All":
    filtered_df = filtered_df[filtered_df["Shift"] == shift_filter]
if heat_filter != "All":
    filtered_df = filtered_df[filtered_df["Heat Number"].astype(str) == heat_filter]

filtered_df = filtered_df.sort_values("Timestamp").reset_index(drop=True)

st.title("🏭 Caster Performance Dashboard")
st.caption("Industrial monitoring system for continuous casting performance, inspired by Siemens WinCC-style operations control.")

if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()

latest = filtered_df.iloc[-1]
current_day = filtered_df["Timestamp"].dt.date.max()
current_day_df = filtered_df[filtered_df["Timestamp"].dt.date == current_day]

metrics = compute_metrics(filtered_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Today's Production (Ton)", f"{current_day_df['Production'].sum():,.2f}")
col2.metric("Current Casting Speed (m/min)", f"{latest['Casting Speed']:.2f}")
col3.metric("Average Casting Speed", f"{metrics['avg_speed']:.2f}")
col4.metric("Mold Level", f"{latest['Mold Level']:.2f}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Downtime (min)", f"{latest['Downtime']:.1f}")
col6.metric("Availability (%)", f"{metrics['availability']:.1f}")
col7.metric("Productivity (Ton/hr)", f"{metrics['productivity']:.1f}")
col8.metric("Alarm Count", f"{int((filtered_df['Alarm'] != 'No Alarm').sum())}")

st.markdown("### Overview")
col_status, col_machine = st.columns([2, 1])
with col_status:
    st.metric("Machine Status", latest["Machine Status"])
with col_machine:
    st.metric("Current Shift", latest["Shift"])

st.markdown("### Trend Analysis")

# Aggregate data by hour for cleaner trends
hourly_df = filtered_df.set_index("Timestamp").resample("1H").agg({
    "Casting Speed": "mean",
    "Mold Level": "mean",
    "Temperature": "mean",
    "Water Flow": "mean",
    "Hydraulic Pressure": "mean",
}).reset_index()

trend_cols = st.columns(2)
with trend_cols[0]:
    fig_speed = px.line(hourly_df, x="Timestamp", y="Casting Speed", markers=True, title="Casting Speed (Hourly Avg)", 
                       line_shape="spline", color_discrete_sequence=["#00d4ff"])
    fig_speed.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
    fig_speed.update_traces(line=dict(width=2), marker=dict(size=5))
    st.plotly_chart(fig_speed, use_container_width=True)
    
with trend_cols[1]:
    mold_target = 74
    mold_upper = 76
    mold_lower = 72
    fig_mold = px.line(hourly_df, x="Timestamp", y="Mold Level", markers=True, title="Mold Level (with Control Limits)",
                      line_shape="spline", color_discrete_sequence=["#00ff88"])
    fig_mold.add_hline(y=mold_target, line_dash="dash", line_color="yellow", annotation_text="Target")
    fig_mold.add_hline(y=mold_upper, line_dash="dot", line_color="red", annotation_text="Upper Limit")
    fig_mold.add_hline(y=mold_lower, line_dash="dot", line_color="red", annotation_text="Lower Limit")
    fig_mold.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
    fig_mold.update_traces(line=dict(width=2), marker=dict(size=5))
    st.plotly_chart(fig_mold, use_container_width=True)

trend_cols2 = st.columns(2)
with trend_cols2[0]:
    temp_min = 1550
    temp_max = 1570
    fig_temp = px.line(hourly_df, x="Timestamp", y="Temperature", markers=True, title="Temperature (with Limits)",
                      line_shape="spline", color_discrete_sequence=["#ff4444"])
    fig_temp.add_hline(y=temp_max, line_dash="dot", line_color="orange", annotation_text="Max")
    fig_temp.add_hline(y=temp_min, line_dash="dot", line_color="orange", annotation_text="Min")
    fig_temp.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
    fig_temp.update_traces(line=dict(width=2), marker=dict(size=5))
    st.plotly_chart(fig_temp, use_container_width=True)

with trend_cols2[1]:
    fig_flow = px.line(hourly_df, x="Timestamp", y="Water Flow", markers=True, title="Water Flow (Hourly Avg)",
                      line_shape="spline", color_discrete_sequence=["#7b68ee"])
    fig_flow.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
    fig_flow.update_traces(line=dict(width=2), marker=dict(size=5))
    st.plotly_chart(fig_flow, use_container_width=True)

trend_cols3 = st.columns(2)
with trend_cols3[0]:
    fig_pressure = px.line(hourly_df, x="Timestamp", y="Hydraulic Pressure", markers=True, title="Hydraulic Pressure (Hourly Avg)",
                          line_shape="spline", color_discrete_sequence=["#ff1493"])
    fig_pressure.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
    fig_pressure.update_traces(line=dict(width=2), marker=dict(size=5))
    st.plotly_chart(fig_pressure, use_container_width=True)

with trend_cols3[1]:
    # Production by shift as bar chart
    prod_by_shift = filtered_df.groupby("Shift")["Production"].sum().reset_index().sort_values("Production", ascending=False)
    fig_prod_shift = px.bar(prod_by_shift, x="Shift", y="Production", title="Production by Shift", 
                           color="Shift", color_discrete_sequence=["#00d4ff", "#00ff88", "#ff9500"])
    fig_prod_shift.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig_prod_shift, use_container_width=True)

st.markdown("### System Performance Gauges")
gauge_cols = st.columns(3)

with gauge_cols[0]:
    fig_oee = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=metrics['oee'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "OEE (%)"},
        delta={'reference': 85, 'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "lightgreen"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}
    ))
    fig_oee.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=60, b=10), font=dict(size=14))
    st.plotly_chart(fig_oee, use_container_width=True)

with gauge_cols[1]:
    fig_avail = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=metrics['availability'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Availability (%)"},
        delta={'reference': 90, 'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 70], 'color': "lightgray"},
                {'range': [70, 90], 'color': "gray"},
                {'range': [90, 100], 'color': "lightgreen"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 95}}
    ))
    fig_avail.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=60, b=10), font=dict(size=14))
    st.plotly_chart(fig_avail, use_container_width=True)

with gauge_cols[2]:
    fig_yield = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=metrics['yield_pct'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Yield (%)"},
        delta={'reference': 95, 'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 80], 'color': "lightgray"},
                {'range': [80, 95], 'color': "gray"},
                {'range': [95, 100], 'color': "lightgreen"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 98}}
    ))
    fig_yield.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=60, b=10), font=dict(size=14))
    st.plotly_chart(fig_yield, use_container_width=True)
downtime_cols = st.columns(2)
with downtime_cols[0]:
    downtime_summary = filtered_df.groupby("Downtime Category")["Downtime"].sum().reset_index()
    fig_downtime_bar = px.bar(
        downtime_summary,
        x="Downtime Category",
        y="Downtime",
        color="Downtime Category",
        title="Downtime by Category",
    )
    fig_downtime_bar.update_layout(template="plotly_dark")
    st.plotly_chart(fig_downtime_bar, use_container_width=True)
with downtime_cols[1]:
    fig_downtime_pie = px.pie(
        downtime_summary,
        names="Downtime Category",
        values="Downtime",
        title="Downtime Distribution",
        hole=0.4,
    )
    fig_downtime_pie.update_layout(template="plotly_dark")
    st.plotly_chart(fig_downtime_pie, use_container_width=True)

st.markdown("### Alarm Analysis & Frequency")
alarm_cols = st.columns(2)
with alarm_cols[0]:
    active_alarms = filtered_df[filtered_df["Alarm"] != "No Alarm"][["Timestamp", "Alarm", "Alarm Severity"]]
    st.dataframe(active_alarms.tail(10), use_container_width=True, hide_index=True)
with alarm_cols[1]:
    alarm_freq = filtered_df[filtered_df["Alarm"] != "No Alarm"]["Alarm"].value_counts().reset_index()
    alarm_freq.columns = ["Alarm Name", "Count"]
    fig_alarm_freq = px.bar(alarm_freq, x="Count", y="Alarm Name", orientation="h", title="Alarm Frequency",
                           color_discrete_sequence=["#FF6B6B"])
    fig_alarm_freq.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
    st.plotly_chart(fig_alarm_freq, use_container_width=True)

st.markdown("### Machine Health")
health_cols = st.columns(3)
health_items = [
    ("PLC", latest["PLC_Status"]),
    ("Mold", latest["Mold_Status"]),
    ("Oscillation", latest["Oscillation_Status"]),
    ("Hydraulic System", latest["Hydraulic_Status"]),
    ("Water Cooling", latest["Water_Cooling_Status"]),
    ("Shear Machine", latest["Shear_Status"]),
    ("Roller Table", latest["Roller_Table_Status"]),
]
for idx, (name, status) in enumerate(health_items):
    color = "#2ecc71" if status == "Healthy" else "#e74c3c"
    with health_cols[idx % 3]:
        st.markdown(
            f"<div style='background:#071622;border:1px solid {color};border-radius:10px;padding:12px;margin-bottom:10px;'>"
            f"<strong>{name}</strong><br><span style='color:{color};'>{status}</span></div>",
            unsafe_allow_html=True,
        )

st.markdown("### Analytics")
analytics_cols = st.columns(2)
with analytics_cols[0]:
    st.metric("Average Casting Speed", f"{metrics['avg_speed']:.2f}")
    st.metric("Maximum Speed", f"{metrics['max_speed']:.2f}")
    st.metric("Minimum Speed", f"{metrics['min_speed']:.2f}")
    st.metric("Mold Level Stability", f"{metrics['mold_level_stability']:.2f}")
with analytics_cols[1]:
    st.metric("Availability", f"{metrics['availability']:.1f}%")
    st.metric("Productivity", f"{metrics['productivity']:.1f}")
    st.metric("OEE", f"{metrics['oee']:.1f}%")
    st.metric("Yield", f"{metrics['yield_pct']:.1f}%")

st.markdown("### Data Source")
with st.expander("Filtered dataset", expanded=True):
    st.dataframe(filtered_df.tail(15), use_container_width=True, hide_index=True)

st.sidebar.download_button(
    label="Download filtered data as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="caster_filtered_data.csv",
    mime="text/csv",
)

st.sidebar.caption(f"Records shown: {len(filtered_df)}")
