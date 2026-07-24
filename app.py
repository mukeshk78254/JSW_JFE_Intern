# # # # import pandas as pd
# # # # import plotly.express as px
# # # # import plotly.graph_objects as go
# # # # import streamlit as st

# # # # from utils.data_loader import load_data
# # # # from utils.metrics import compute_metrics

# # # # st.set_page_config(page_title="Caster Performance Dashboard", page_icon="🏭", layout="wide")

# # # # st.markdown(
# # # #     """
# # # #     <style>
# # # #     .stApp {
# # # #         background: linear-gradient(135deg, #071622 0%, #0b2545 100%);
# # # #         color: #f4f8ff;
# # # #     }
# # # #     .block-container {
# # # #         padding-top: 1.5rem;
# # # #         padding-bottom: 2rem;
# # # #     }
# # # #     .stMetric {
# # # #         background-color: rgba(7, 28, 48, 0.95);
# # # #         border: 1px solid #2d6cdf;
# # # #         border-radius: 10px;
# # # #         padding: 10px;
# # # #     }
# # # #     div[data-testid="stSidebar"] {
# # # #         background: #071622;
# # # #     }
# # # #     </style>
# # # #     """,
# # # #     unsafe_allow_html=True,
# # # # )


# # # # @st.cache_data(show_spinner=False)
# # # # def get_filtered_data():
# # # #     df = load_data()
# # # #     return df


# # # # if "auto_refresh" not in st.session_state:
# # # #     st.session_state.auto_refresh = False

# # # # if st.sidebar.checkbox("Auto refresh", value=st.session_state.auto_refresh, key="auto_refresh"):
# # # #     try:
# # # #         from streamlit_autorefresh import st_autorefresh

# # # #         st_autorefresh(interval=30000, limit=100, key="caster_refresh")
# # # #     except Exception:
# # # #         st.sidebar.info("Auto refresh package is not available in the environment.")

# # # # st.sidebar.header("Filters")
# # # # df = get_filtered_data()

# # # # min_date = df["Timestamp"].dt.date.min()
# # # # max_date = df["Timestamp"].dt.date.max()

# # # # selected_dates = st.sidebar.date_input(
# # # #     "Date range",
# # # #     value=(min_date, max_date),
# # # #     min_value=min_date,
# # # #     max_value=max_date,
# # # # )

# # # # if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
# # # #     start_date, end_date = selected_dates
# # # # else:
# # # #     start_date = selected_dates
# # # #     end_date = selected_dates

# # # # shift_filter = st.sidebar.selectbox("Shift", ["All", *sorted(df["Shift"].unique())])
# # # # heat_filter = st.sidebar.selectbox("Heat Number", ["All", *sorted(df["Heat Number"].astype(str).unique())])

# # # # filtered_df = df.copy()
# # # # filtered_df = filtered_df[(filtered_df["Timestamp"].dt.date >= start_date) & (filtered_df["Timestamp"].dt.date <= end_date)]
# # # # if shift_filter != "All":
# # # #     filtered_df = filtered_df[filtered_df["Shift"] == shift_filter]
# # # # if heat_filter != "All":
# # # #     filtered_df = filtered_df[filtered_df["Heat Number"].astype(str) == heat_filter]

# # # # filtered_df = filtered_df.sort_values("Timestamp").reset_index(drop=True)

# # # # st.title("🏭 Caster Performance Dashboard")
# # # # st.caption("Industrial monitoring system for continuous casting performance, inspired by Siemens WinCC-style operations control.")

# # # # if filtered_df.empty:
# # # #     st.warning("No records match the selected filters.")
# # # #     st.stop()

# # # # latest = filtered_df.iloc[-1]
# # # # current_day = filtered_df["Timestamp"].dt.date.max()
# # # # current_day_df = filtered_df[filtered_df["Timestamp"].dt.date == current_day]

# # # # metrics = compute_metrics(filtered_df)

# # # # col1, col2, col3, col4 = st.columns(4)
# # # # col1.metric("Today's Production (Ton)", f"{current_day_df['Production'].sum():,.2f}")
# # # # col2.metric("Current Casting Speed (m/min)", f"{latest['Casting Speed']:.2f}")
# # # # col3.metric("Average Casting Speed", f"{metrics['avg_speed']:.2f}")
# # # # col4.metric("Mold Level", f"{latest['Mold Level']:.2f}")

# # # # col5, col6, col7, col8 = st.columns(4)
# # # # col5.metric("Downtime (min)", f"{latest['Downtime']:.1f}")
# # # # col6.metric("Availability (%)", f"{metrics['availability']:.1f}")
# # # # col7.metric("Productivity (Ton/hr)", f"{metrics['productivity']:.1f}")
# # # # col8.metric("Alarm Count", f"{int((filtered_df['Alarm'] != 'No Alarm').sum())}")

# # # # st.markdown("### Overview")
# # # # col_status, col_machine = st.columns([2, 1])
# # # # with col_status:
# # # #     st.metric("Machine Status", latest["Machine Status"])
# # # # with col_machine:
# # # #     st.metric("Current Shift", latest["Shift"])

# # # # st.markdown("### Trend Analysis")

# # # # # Aggregate data by hour for cleaner trends
# # # # hourly_df = filtered_df.set_index("Timestamp").resample("1H").agg({
# # # #     "Casting Speed": "mean",
# # # #     "Mold Level": "mean",
# # # #     "Temperature": "mean",
# # # #     "Water Flow": "mean",
# # # #     "Hydraulic Pressure": "mean",
# # # # }).reset_index()

# # # # trend_cols = st.columns(2)
# # # # with trend_cols[0]:
# # # #     fig_speed = px.line(hourly_df, x="Timestamp", y="Casting Speed", markers=True, title="Casting Speed (Hourly Avg)", 
# # # #                        line_shape="spline", color_discrete_sequence=["#00d4ff"])
# # # #     fig_speed.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
# # # #     fig_speed.update_traces(line=dict(width=2), marker=dict(size=5))
# # # #     st.plotly_chart(fig_speed, use_container_width=True)
    
# # # # with trend_cols[1]:
# # # #     mold_target = 74
# # # #     mold_upper = 76
# # # #     mold_lower = 72
# # # #     fig_mold = px.line(hourly_df, x="Timestamp", y="Mold Level", markers=True, title="Mold Level (with Control Limits)",
# # # #                       line_shape="spline", color_discrete_sequence=["#00ff88"])
# # # #     fig_mold.add_hline(y=mold_target, line_dash="dash", line_color="yellow", annotation_text="Target")
# # # #     fig_mold.add_hline(y=mold_upper, line_dash="dot", line_color="red", annotation_text="Upper Limit")
# # # #     fig_mold.add_hline(y=mold_lower, line_dash="dot", line_color="red", annotation_text="Lower Limit")
# # # #     fig_mold.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
# # # #     fig_mold.update_traces(line=dict(width=2), marker=dict(size=5))
# # # #     st.plotly_chart(fig_mold, use_container_width=True)

# # # # trend_cols2 = st.columns(2)
# # # # with trend_cols2[0]:
# # # #     temp_min = 1550
# # # #     temp_max = 1570
# # # #     fig_temp = px.line(hourly_df, x="Timestamp", y="Temperature", markers=True, title="Temperature (with Limits)",
# # # #                       line_shape="spline", color_discrete_sequence=["#ff4444"])
# # # #     fig_temp.add_hline(y=temp_max, line_dash="dot", line_color="orange", annotation_text="Max")
# # # #     fig_temp.add_hline(y=temp_min, line_dash="dot", line_color="orange", annotation_text="Min")
# # # #     fig_temp.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
# # # #     fig_temp.update_traces(line=dict(width=2), marker=dict(size=5))
# # # #     st.plotly_chart(fig_temp, use_container_width=True)

# # # # with trend_cols2[1]:
# # # #     fig_flow = px.line(hourly_df, x="Timestamp", y="Water Flow", markers=True, title="Water Flow (Hourly Avg)",
# # # #                       line_shape="spline", color_discrete_sequence=["#7b68ee"])
# # # #     fig_flow.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
# # # #     fig_flow.update_traces(line=dict(width=2), marker=dict(size=5))
# # # #     st.plotly_chart(fig_flow, use_container_width=True)

# # # # trend_cols3 = st.columns(2)
# # # # with trend_cols3[0]:
# # # #     fig_pressure = px.line(hourly_df, x="Timestamp", y="Hydraulic Pressure", markers=True, title="Hydraulic Pressure (Hourly Avg)",
# # # #                           line_shape="spline", color_discrete_sequence=["#ff1493"])
# # # #     fig_pressure.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
# # # #     fig_pressure.update_traces(line=dict(width=2), marker=dict(size=5))
# # # #     st.plotly_chart(fig_pressure, use_container_width=True)

# # # # with trend_cols3[1]:
# # # #     # Production by shift as bar chart
# # # #     prod_by_shift = filtered_df.groupby("Shift")["Production"].sum().reset_index().sort_values("Production", ascending=False)
# # # #     fig_prod_shift = px.bar(prod_by_shift, x="Shift", y="Production", title="Production by Shift", 
# # # #                            color="Shift", color_discrete_sequence=["#00d4ff", "#00ff88", "#ff9500"])
# # # #     fig_prod_shift.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
# # # #     st.plotly_chart(fig_prod_shift, use_container_width=True)

# # # # st.markdown("### System Performance Gauges")
# # # # gauge_cols = st.columns(3)

# # # # with gauge_cols[0]:
# # # #     fig_oee = go.Figure(go.Indicator(
# # # #         mode="gauge+number+delta",
# # # #         value=metrics['oee'],
# # # #         domain={'x': [0, 1], 'y': [0, 1]},
# # # #         title={'text': "OEE (%)"},
# # # #         delta={'reference': 85, 'suffix': "%"},
# # # #         gauge={
# # # #             'axis': {'range': [0, 100]},
# # # #             'bar': {'color': "darkblue"},
# # # #             'steps': [
# # # #                 {'range': [0, 50], 'color': "lightgray"},
# # # #                 {'range': [50, 80], 'color': "gray"},
# # # #                 {'range': [80, 100], 'color': "lightgreen"}],
# # # #             'threshold': {
# # # #                 'line': {'color': "red", 'width': 4},
# # # #                 'thickness': 0.75,
# # # #                 'value': 90}}
# # # #     ))
# # # #     fig_oee.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=60, b=10), font=dict(size=14))
# # # #     st.plotly_chart(fig_oee, use_container_width=True)

# # # # with gauge_cols[1]:
# # # #     fig_avail = go.Figure(go.Indicator(
# # # #         mode="gauge+number+delta",
# # # #         value=metrics['availability'],
# # # #         domain={'x': [0, 1], 'y': [0, 1]},
# # # #         title={'text': "Availability (%)"},
# # # #         delta={'reference': 90, 'suffix': "%"},
# # # #         gauge={
# # # #             'axis': {'range': [0, 100]},
# # # #             'bar': {'color': "darkblue"},
# # # #             'steps': [
# # # #                 {'range': [0, 70], 'color': "lightgray"},
# # # #                 {'range': [70, 90], 'color': "gray"},
# # # #                 {'range': [90, 100], 'color': "lightgreen"}],
# # # #             'threshold': {
# # # #                 'line': {'color': "red", 'width': 4},
# # # #                 'thickness': 0.75,
# # # #                 'value': 95}}
# # # #     ))
# # # #     fig_avail.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=60, b=10), font=dict(size=14))
# # # #     st.plotly_chart(fig_avail, use_container_width=True)

# # # # with gauge_cols[2]:
# # # #     fig_yield = go.Figure(go.Indicator(
# # # #         mode="gauge+number+delta",
# # # #         value=metrics['yield_pct'],
# # # #         domain={'x': [0, 1], 'y': [0, 1]},
# # # #         title={'text': "Yield (%)"},
# # # #         delta={'reference': 95, 'suffix': "%"},
# # # #         gauge={
# # # #             'axis': {'range': [0, 100]},
# # # #             'bar': {'color': "darkblue"},
# # # #             'steps': [
# # # #                 {'range': [0, 80], 'color': "lightgray"},
# # # #                 {'range': [80, 95], 'color': "gray"},
# # # #                 {'range': [95, 100], 'color': "lightgreen"}],
# # # #             'threshold': {
# # # #                 'line': {'color': "red", 'width': 4},
# # # #                 'thickness': 0.75,
# # # #                 'value': 98}}
# # # #     ))
# # # #     fig_yield.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=60, b=10), font=dict(size=14))
# # # #     st.plotly_chart(fig_yield, use_container_width=True)
# # # # downtime_cols = st.columns(2)
# # # # with downtime_cols[0]:
# # # #     downtime_summary = filtered_df.groupby("Downtime Category")["Downtime"].sum().reset_index()
# # # #     fig_downtime_bar = px.bar(
# # # #         downtime_summary,
# # # #         x="Downtime Category",
# # # #         y="Downtime",
# # # #         color="Downtime Category",
# # # #         title="Downtime by Category",
# # # #     )
# # # #     fig_downtime_bar.update_layout(template="plotly_dark")
# # # #     st.plotly_chart(fig_downtime_bar, use_container_width=True)
# # # # with downtime_cols[1]:
# # # #     fig_downtime_pie = px.pie(
# # # #         downtime_summary,
# # # #         names="Downtime Category",
# # # #         values="Downtime",
# # # #         title="Downtime Distribution",
# # # #         hole=0.4,
# # # #     )
# # # #     fig_downtime_pie.update_layout(template="plotly_dark")
# # # #     st.plotly_chart(fig_downtime_pie, use_container_width=True)

# # # # st.markdown("### Alarm Analysis & Frequency")
# # # # alarm_cols = st.columns(2)
# # # # with alarm_cols[0]:
# # # #     active_alarms = filtered_df[filtered_df["Alarm"] != "No Alarm"][["Timestamp", "Alarm", "Alarm Severity"]]
# # # #     st.dataframe(active_alarms.tail(10), use_container_width=True, hide_index=True)
# # # # with alarm_cols[1]:
# # # #     alarm_freq = filtered_df[filtered_df["Alarm"] != "No Alarm"]["Alarm"].value_counts().reset_index()
# # # #     alarm_freq.columns = ["Alarm Name", "Count"]
# # # #     fig_alarm_freq = px.bar(alarm_freq, x="Count", y="Alarm Name", orientation="h", title="Alarm Frequency",
# # # #                            color_discrete_sequence=["#FF6B6B"])
# # # #     fig_alarm_freq.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
# # # #     st.plotly_chart(fig_alarm_freq, use_container_width=True)

# # # # st.markdown("### Machine Health")
# # # # health_cols = st.columns(3)
# # # # health_items = [
# # # #     ("PLC", latest["PLC_Status"]),
# # # #     ("Mold", latest["Mold_Status"]),
# # # #     ("Oscillation", latest["Oscillation_Status"]),
# # # #     ("Hydraulic System", latest["Hydraulic_Status"]),
# # # #     ("Water Cooling", latest["Water_Cooling_Status"]),
# # # #     ("Shear Machine", latest["Shear_Status"]),
# # # #     ("Roller Table", latest["Roller_Table_Status"]),
# # # # ]
# # # # for idx, (name, status) in enumerate(health_items):
# # # #     color = "#2ecc71" if status == "Healthy" else "#e74c3c"
# # # #     with health_cols[idx % 3]:
# # # #         st.markdown(
# # # #             f"<div style='background:#071622;border:1px solid {color};border-radius:10px;padding:12px;margin-bottom:10px;'>"
# # # #             f"<strong>{name}</strong><br><span style='color:{color};'>{status}</span></div>",
# # # #             unsafe_allow_html=True,
# # # #         )

# # # # st.markdown("### Analytics")
# # # # analytics_cols = st.columns(2)
# # # # with analytics_cols[0]:
# # # #     st.metric("Average Casting Speed", f"{metrics['avg_speed']:.2f}")
# # # #     st.metric("Maximum Speed", f"{metrics['max_speed']:.2f}")
# # # #     st.metric("Minimum Speed", f"{metrics['min_speed']:.2f}")
# # # #     st.metric("Mold Level Stability", f"{metrics['mold_level_stability']:.2f}")
# # # # with analytics_cols[1]:
# # # #     st.metric("Availability", f"{metrics['availability']:.1f}%")
# # # #     st.metric("Productivity", f"{metrics['productivity']:.1f}")
# # # #     st.metric("OEE", f"{metrics['oee']:.1f}%")
# # # #     st.metric("Yield", f"{metrics['yield_pct']:.1f}%")

# # # # st.markdown("### Data Source")
# # # # with st.expander("Filtered dataset", expanded=True):
# # # #     st.dataframe(filtered_df.tail(15), use_container_width=True, hide_index=True)

# # # # st.sidebar.download_button(
# # # #     label="Download filtered data as CSV",
# # # #     data=filtered_df.to_csv(index=False).encode("utf-8"),
# # # #     file_name="caster_filtered_data.csv",
# # # #     mime="text/csv",
# # # # )

# # # # st.sidebar.caption(f"Records shown: {len(filtered_df)}")





# # # import pandas as pd
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # import streamlit as st
# # # from utils.data_loader import load_data
# # # from utils.metrics import compute_metrics

# # # # 1. Page Configuration
# # # st.set_page_config(page_title="Caster Performance Dashboard", page_icon="🏭", layout="wide")
# # # st.markdown(
# # #     """
# # #     <style>
# # #     .stApp { background: linear-gradient(135deg, #071622 0%, #0b2545 100%); color: #f4f8ff; }
# # #     .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
# # #     .stMetric { background-color: rgba(7, 28, 48, 0.95); border: 1px solid #2d6cdf; border-radius: 10px; padding: 10px; }
# # #     div[data-testid="stSidebar"] { background: #071622; }
# # #     </style>
# # #     """,
# # #     unsafe_allow_html=True,
# # # )

# # # # 2. Data Loading & Caching
# # # @st.cache_data(show_spinner=False)
# # # def get_filtered_data():
# # #     df = load_data()
# # #     return df

# # # # 3. Sidebar Configuration
# # # st.sidebar.header("Filters")
# # # df = get_filtered_data()

# # # if df.empty:
# # #     st.error("Real data files could not be loaded. Ensure 'BOPS_Alarm.xlsx' and delay files exist in the root directory.")
# # #     st.stop()

# # # min_date = df["Timestamp"].dt.date.min()
# # # max_date = df["Timestamp"].dt.date.max()
# # # selected_dates = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# # # if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
# # #     start_date, end_date = selected_dates
# # # else:
# # #     start_date = selected_dates
# # #     end_date = selected_dates

# # # shift_filter = st.sidebar.selectbox("Shift", ["All", *sorted(df["Shift"].astype(str).unique())])
# # # heat_filter = st.sidebar.selectbox("Heat Number", ["All", *sorted(df["Heat Number"].astype(str).unique())])

# # # # Apply Filters
# # # filtered_df = df.copy()
# # # filtered_df = filtered_df[(filtered_df["Timestamp"].dt.date >= start_date) & (filtered_df["Timestamp"].dt.date <= end_date)]

# # # if shift_filter != "All":
# # #     filtered_df = filtered_df[filtered_df["Shift"] == shift_filter]
# # # if heat_filter != "All":
# # #     filtered_df = filtered_df[filtered_df["Heat Number"].astype(str) == heat_filter]

# # # filtered_df = filtered_df.sort_values("Timestamp").reset_index(drop=True)

# # # # 4. Main Dashboard Header
# # # st.title("🏭 Caster Performance Dashboard (Live Data)")

# # # if filtered_df.empty:
# # #     st.warning("No records match the selected filters.")
# # #     st.stop()

# # # latest = filtered_df.iloc[-1]
# # # current_day = filtered_df["Timestamp"].dt.date.max()
# # # current_day_df = filtered_df[filtered_df["Timestamp"].dt.date == current_day]
# # # metrics = compute_metrics(filtered_df)

# # # # 5. Top Metrics Row
# # # col1, col2, col3, col4 = st.columns(4)
# # # col1.metric("Today's Production (Ton)", f"{current_day_df['Production'].sum():,.2f}")
# # # col2.metric("Current Casting Speed (m/min)", f"{latest['Casting Speed']:.2f}")
# # # col3.metric("Average Casting Speed", f"{metrics['avg_speed']:.2f}")
# # # col4.metric("Downtime (min)", f"{latest['Downtime']:.1f}")

# # # st.markdown("### Overview")
# # # col_status, col_machine = st.columns([2, 1])
# # # with col_status:
# # #     st.metric("Machine Status", latest["Machine Status"])
# # # with col_machine:
# # #     st.metric("Current Shift", latest["Shift"])

# # # # 6. Trend Analysis Charts
# # # st.markdown("### Trend Analysis")
# # # # Group data by Day for clean line charts
# # # trend_df = filtered_df.set_index("Timestamp").resample("1D").agg({
# # #     "Casting Speed": "mean",
# # #     "Temperature": "mean"
# # # }).dropna().reset_index()

# # # trend_cols = st.columns(2)
# # # with trend_cols[0]:
# # #     fig_speed = px.line(trend_df, x="Timestamp", y="Casting Speed", markers=True, title="Casting Speed (Daily Avg)",
# # #                         line_shape="spline", color_discrete_sequence=["#00d4ff"])
# # #     fig_speed.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
# # #     st.plotly_chart(fig_speed, use_container_width=True) 

# # # with trend_cols[1]:
# # #     fig_temp = px.line(trend_df, x="Timestamp", y="Temperature", markers=True, title="Tundish Temperature (Daily Avg)",
# # #                       line_shape="spline", color_discrete_sequence=["#ff4444"])
# # #     fig_temp.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), hovermode="x unified")
# # #     st.plotly_chart(fig_temp, use_container_width=True)

# # # # 7. Production and Downtime Bar Charts
# # # st.markdown("### Production & Downtime")
# # # trend_cols3 = st.columns(2)
# # # with trend_cols3[0]:
# # #     prod_by_shift = filtered_df.groupby("Shift")["Production"].sum().reset_index().sort_values("Production", ascending=False)
# # #     fig_prod_shift = px.bar(prod_by_shift, x="Shift", y="Production", title="Production by Shift",
# # #                             color="Shift", color_discrete_sequence=["#00d4ff", "#00ff88", "#ff9500"])
# # #     fig_prod_shift.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
# # #     st.plotly_chart(fig_prod_shift, use_container_width=True)

# # # with trend_cols3[1]:
# # #     downtime_summary = filtered_df.groupby("Downtime Category")["Downtime"].sum().reset_index()
# # #     downtime_summary = downtime_summary[downtime_summary["Downtime"] > 0]
# # #     if not downtime_summary.empty:
# # #         fig_downtime_bar = px.bar(downtime_summary, x="Downtime Category", y="Downtime", color="Downtime Category", title="Downtime by Category")
# # #         fig_downtime_bar.update_layout(template="plotly_dark", showlegend=False)
# # #         st.plotly_chart(fig_downtime_bar, use_container_width=True)
# # #     else:
# # #         st.info("No recorded downtime in this timeframe.")

# # # # 8. Performance Gauges
# # # st.markdown("### System Performance Gauges")
# # # gauge_cols = st.columns(3)
# # # with gauge_cols[0]:
# # #     fig_oee = go.Figure(go.Indicator(
# # #         mode="gauge+number+delta", value=metrics['oee'], title={'text': "OEE (%)"},
# # #         gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
# # #     ))
# # #     fig_oee.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=60, b=10), font=dict(size=14))
# # #     st.plotly_chart(fig_oee, use_container_width=True)

# # # with gauge_cols[1]:
# # #     fig_avail = go.Figure(go.Indicator(
# # #         mode="gauge+number+delta", value=metrics['availability'], title={'text': "Availability (%)"},
# # #         gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
# # #     ))
# # #     fig_avail.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=60, b=10), font=dict(size=14))
# # #     st.plotly_chart(fig_avail, use_container_width=True)

# # # with gauge_cols[2]:
# # #     fig_yield = go.Figure(go.Indicator(
# # #         mode="gauge+number+delta", value=metrics['yield_pct'], title={'text': "Yield (%)"},
# # #         gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
# # #     ))
# # #     fig_yield.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=60, b=10), font=dict(size=14))
# # #     st.plotly_chart(fig_yield, use_container_width=True)

# # # # 9. KPI Footers
# # # st.markdown("### Analytics")
# # # analytics_cols = st.columns(2)
# # # with analytics_cols[0]:
# # #     st.metric("Average Casting Speed", f"{metrics['avg_speed']:.2f}")
# # #     st.metric("Maximum Speed", f"{metrics['max_speed']:.2f}")
# # #     st.metric("Minimum Speed", f"{metrics['min_speed']:.2f}")
# # # with analytics_cols[1]:
# # #     st.metric("Availability", f"{metrics['availability']:.1f}%")
# # #     st.metric("Productivity", f"{metrics['productivity']:.1f}")
# # #     st.metric("OEE", f"{metrics['oee']:.1f}%")

# # # # 10. Raw Data Table & Download
# # # st.markdown("### Data Source")
# # # with st.expander("Filtered dataset", expanded=True):
# # #     st.dataframe(filtered_df.tail(15), use_container_width=True, hide_index=True)

# # # st.sidebar.download_button(
# # #     label="Download filtered data as CSV",
# # #     data=filtered_df.to_csv(index=False).encode("utf-8"),
# # #     file_name="caster_filtered_real_data.csv",
# # #     mime="text/csv",
# # # )
# # # st.sidebar.caption(f"Records shown: {len(filtered_df)}")


# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # from utils.data_loader import load_all_data
# # from utils.metrics import calculate_kpis
# # from utils.charts import create_gauge, create_pareto, create_trend

# # st.set_page_config(page_title="Caster System OS", page_icon="⚙️", layout="wide")
# # st.markdown("""
# #     <style>
# #     .stApp { background: #050e14; color: #e0e6ed; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
# #     .stTabs [data-baseweb="tab-list"] { background-color: #0a192f; border-bottom: 2px solid #1f4068; }
# #     .stTabs [data-baseweb="tab"] { color: #8892b0; font-weight: bold; }
# #     .stTabs [aria-selected="true"] { color: #64ffda !important; border-bottom-color: #64ffda !important; }
# #     div[data-testid="stMetricValue"] { color: #64ffda; }
# #     </style>
# # """, unsafe_allow_html=True)

# # # 1. Load Data
# # data_dict = load_all_data()
# # df_main = data_dict["main"]
# # df_delays = data_dict["delays"]

# # # 2. Sidebar Filters
# # st.sidebar.markdown("### SCADA System Control")
# # if df_main.empty:
# #     st.stop()

# # date_min, date_max = df_main["Timestamp"].min().date(), df_main["Timestamp"].max().date()
# # date_range = st.sidebar.date_input("Operating Period", (date_min, date_max), min_value=date_min, max_value=date_max)

# # df_filtered = df_main.copy()
# # if len(date_range) == 2:
# #     df_filtered = df_filtered[(df_filtered["Timestamp"].dt.date >= date_range[0]) & (df_filtered["Timestamp"].dt.date <= date_range[1])]

# # # Safeguard shift filter in case 'Shift' column is mostly null
# # if 'Shift' in df_filtered.columns and not df_filtered['Shift'].isna().all():
# #     shift_sel = st.sidebar.selectbox("Shift Selector", ["All", *df_filtered['Shift'].dropna().astype(str).unique()])
# #     if shift_sel != "All":
# #         df_filtered = df_filtered[df_filtered["Shift"] == shift_sel]

# # # 3. Calculate KPIs
# # kpis = calculate_kpis(df_filtered)

# # # 4. Top WinCC Style Header
# # col_a, col_b, col_c, col_d = st.columns(4)
# # col_a.metric("SYSTEM STATUS", "RUNNING" if kpis['downtime'] == 0 else "FAULT/STOPPED", delta_color="off")
# # col_b.metric("PRODUCTION (MT)", f"{kpis['total_prod']:,.2f}")
# # col_c.metric("CASTING SPEED", f"{kpis['avg_speed']:.2f} m/min")
# # col_d.metric("DOWNTIME", f"{kpis['downtime']:.0f} min")

# # st.markdown("---")

# # # 5. Application Tabs
# # tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview & OEE", "📈 Production & Heats", "⚠️ Delays & Pareto", "🛠️ Health & PM"])

# # with tab1:
# #     st.markdown("### Overall Equipment Effectiveness (OEE)")
# #     g1, g2, g3, g4 = st.columns(4)
# #     with g1: st.plotly_chart(create_gauge(kpis['oee'], "OEE", 85), use_container_width=True)
# #     with g2: st.plotly_chart(create_gauge(kpis['availability'], "Availability", 90), use_container_width=True)
# #     with g3: st.plotly_chart(create_gauge(kpis['performance'], "Performance", 95), use_container_width=True)
# #     with g4: st.plotly_chart(create_gauge(kpis['utilization'], "Utilization", 80), use_container_width=True)
    
# #     st.markdown("### Daily Speed Trend")
# #     if not df_filtered.empty and 'Casting Speed' in df_filtered.columns:
# #         trend_data = df_filtered.groupby(df_filtered['Timestamp'].dt.date)['Casting Speed'].mean().reset_index()
# #         st.plotly_chart(create_trend(trend_data, 'Timestamp', 'Casting Speed', "Average Casting Speed (m/min)", "#64ffda"), use_container_width=True)

# # with tab2:
# #     st.markdown("### Heat & Shift Analysis")
# #     c1, c2 = st.columns(2)
# #     with c1:
# #         if 'Shift' in df_filtered.columns:
# #             shift_prod = df_filtered.groupby('Shift')['Production'].sum().reset_index()
# #             fig_shift = px.bar(shift_prod, x='Shift', y='Production', title="Production by Shift", color='Shift', color_discrete_sequence=["#112240", "#233554", "#64ffda"])
# #             fig_shift.update_layout(template="plotly_dark")
# #             st.plotly_chart(fig_shift, use_container_width=True)
# #     with c2:
# #         if 'Casting Time' in df_filtered.columns:
# #             heat_time = df_filtered.groupby('Timestamp')['Casting Time'].sum().reset_index()
# #             st.plotly_chart(create_trend(heat_time, 'Timestamp', 'Casting Time', "Casting Time per Day (mins)", "#ff9500"), use_container_width=True)

# # with tab3:
# #     st.markdown("### RCA & Downtime Analysis")
# #     if not df_delays.empty:
# #         filtered_delays = df_delays[(df_delays['Date'].dt.date >= date_range[0]) & (df_delays['Date'].dt.date <= date_range[1])]
# #         st.plotly_chart(create_pareto(filtered_delays), use_container_width=True)
        
# #         c3, c4 = st.columns(2)
# #         with c3:
# #             st.markdown("#### Electrical vs Mechanical")
# #             pie_data = filtered_delays.groupby('Category')['Delay (mins)'].sum().reset_index()
# #             fig_pie = px.pie(pie_data, names='Category', values='Delay (mins)', hole=0.5, color_discrete_sequence=px.colors.sequential.Agalmati)
# #             fig_pie.update_layout(template="plotly_dark")
# #             st.plotly_chart(fig_pie, use_container_width=True)
# #         with c4:
# #             st.markdown("#### Delay Log")
# #             st.dataframe(filtered_delays.sort_values('Delay (mins)', ascending=False), use_container_width=True, hide_index=True)
# #     else:
# #         st.info("No delay data available.")

# # with tab4:
# #     st.markdown("### Machine Health & Analysis (Grid Gap / PM / Chem)")
# #     st.info("🔌 System Integration Pending: PM SAP, RCA, and Product Chemistry databases are queued for synchronization.")
    
# #     if not data_dict['grid'].empty:
# #         st.markdown("#### Grid Gap Readings")
# #         st.dataframe(data_dict['grid'].head(10), use_container_width=True)



# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from utils.data_loader import load_all_data
# from utils.metrics import calculate_kpis
# from utils.charts import create_gauge, create_pareto

# st.set_page_config(page_title="Caster System OS", page_icon="⚙️", layout="wide")
# st.markdown("""
#     <style>
#     .stApp { background: #050e14; color: #e0e6ed; }
#     .stTabs [data-baseweb="tab-list"] { background-color: #0a192f; border-bottom: 2px solid #1f4068; }
#     .stTabs [data-baseweb="tab"] { color: #8892b0; font-weight: bold; }
#     .stTabs [aria-selected="true"] { color: #64ffda !important; border-bottom-color: #64ffda !important; }
#     div[data-testid="stMetricValue"] { color: #64ffda; }
#     </style>
# """, unsafe_allow_html=True)

# # 1. Load Data
# data = load_all_data()
# df_main = data["main"]
# df_delays = data["delays"]

# if df_main.empty:
#     st.error("System Offline: No Main Production Data Found.")
#     st.stop()

# # 2. Sidebar Filters
# st.sidebar.markdown("### SCADA Control Panel")
# date_min, date_max = df_main["Timestamp"].min().date(), df_main["Timestamp"].max().date()
# date_range = st.sidebar.date_input("Operating Period", (date_min, date_max), min_value=date_min, max_value=date_max)
# target_mt = st.sidebar.number_input("Monthly Target (MT)", value=50000)

# df_filtered = df_main.copy()
# delay_filtered = df_delays.copy()

# if len(date_range) == 2:
#     df_filtered = df_filtered[(df_filtered["Timestamp"].dt.date >= date_range[0]) & (df_filtered["Timestamp"].dt.date <= date_range[1])]
#     if not delay_filtered.empty:
#         delay_filtered = delay_filtered[(delay_filtered['Date'].dt.date >= date_range[0]) & (delay_filtered['Date'].dt.date <= date_range[1])]

# if 'Shift' in df_filtered.columns and not df_filtered['Shift'].isna().all():
#     shift_sel = st.sidebar.selectbox("Shift Filter", ["All", *df_filtered['Shift'].dropna().astype(str).unique()])
#     if shift_sel != "All":
#         df_filtered = df_filtered[df_filtered["Shift"] == shift_sel]

# # 3. Calculate KPIs
# kpis = calculate_kpis(df_filtered, delay_filtered, monthly_target_mt=target_mt)

# # 4. Top WinCC Status Header
# col1, col2, col3, col4, col5 = st.columns(5)
# col1.metric("STATUS", "RUNNING" if kpis['total_downtime'] == 0 else "STOPPED", delta_color="off")
# col2.metric("TOTAL PROD (MT)", f"{kpis['total_prod']:,.2f}")
# col3.metric("OEE %", f"{kpis['oee']:.1f}%")
# col4.metric("TOTAL HEATS", f"{kpis['total_heats']}")
# col5.metric("TOTAL DOWNTIME", f"{kpis['total_downtime']:.0f} min")

# st.markdown("---")

# # 5. Application Tabs
# tab1, tab2, tab3, tab4 = st.tabs(["📊 OEE & Speed", "📈 Production & Temps", "⚠️ Downtime & RCA", "🛠️ PM & Chemistry"])

# with tab1:
#     st.markdown("### Equipment Effectiveness")
#     g1, g2, g3, g4 = st.columns(4)
#     with g1: st.plotly_chart(create_gauge(kpis['oee'], "OEE", 85), use_container_width=True)
#     with g2: st.plotly_chart(create_gauge(kpis['availability'], "Availability", 90), use_container_width=True)
#     with g3: st.plotly_chart(create_gauge(kpis['performance'], "Performance", 95), use_container_width=True)
#     with g4: st.plotly_chart(create_gauge(kpis['utilization'], "Utilization", 80), use_container_width=True)

#     st.markdown("### Speed Analytics")
#     s1, s2, s3, s4 = st.columns(4)
#     s1.metric("Avg Casting Speed", f"{kpis['avg_speed']:.2f} m/min")
#     s2.metric("Max Casting Speed", f"{kpis['max_speed']:.2f} m/min")
#     s3.metric("Min Casting Speed", f"{kpis['min_speed']:.2f} m/min")
#     s4.metric("Total Casting Time", f"{kpis['casting_time']:,.0f} mins")

# with tab2:
#     st.markdown("### Production Achievement & Targets")
#     p1, p2, p3 = st.columns(3)
#     p1.metric("Target vs Actual", f"{kpis['achievement_pct']:.1f} %")
#     p2.metric("Average Production", f"{kpis['avg_prod']:.2f} MT/Heat")
#     p3.metric("Total Sequences", f"{kpis['total_seq']}")

#     st.markdown("### Thermal Dynamics")
#     t1, t2 = st.columns(2)
#     t1.metric("Avg Tundish Temp", f"{kpis['avg_tun_temp']:.1f} °C")
#     t2.metric("Avg Lifting Temp", f"{kpis['avg_lift_temp']:.1f} °C")

# with tab3:
#     st.markdown("### Downtime & Delay Breakdown")
#     d1, d2, d3 = st.columns(3)
#     d1.metric("Avg Downtime", f"{kpis['avg_downtime']:.1f} min/incident")
#     d2.metric("Electrical Delay Count", f"{kpis['electrical_count']}")
#     d3.metric("Root Cause Identifications", f"{len(data['rca'])}")

#     if not delay_filtered.empty:
#         c1, c2 = st.columns(2)
#         with c1:
#             st.plotly_chart(create_pareto(delay_filtered, group_col='Agency'), use_container_width=True)
#         with c2:
#             st.plotly_chart(create_pareto(delay_filtered, group_col='Reason'), use_container_width=True)
        
#         st.markdown("#### Detailed Delay Log (Type / Agency / Reason)")
#         st.dataframe(delay_filtered.sort_values('Delay (mins)', ascending=False), use_container_width=True, hide_index=True)

# with tab4:
#     st.markdown("### Machine Health, PMs, & Chemistry")
    
#     st.markdown("#### Grid Gap Measurements")
#     if not data['grid'].empty: st.dataframe(data['grid'].head(10), use_container_width=True)
#     else: st.info("Grid Gap data pending sync.")

#     st.markdown("#### Chemical Composition (C, Mn, Si, P, S, Cr, Ni, Mo)")
#     if not data['chem'].empty: st.dataframe(data['chem'], use_container_width=True)
#     else: st.info("Chemistry data pending sync.")

#     st.markdown("#### PM Orders & Status")
#     if not data['pm'].empty: st.dataframe(data['pm'], use_container_width=True)
#     else: st.info("PM SAP data pending sync.")



import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_all_data
from utils.metrics import calculate_kpis
from utils.charts import create_gauge, create_pareto

st.set_page_config(page_title="Caster System OS", page_icon="⚙️", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #050e14; color: #e0e6ed; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
    .stTabs [data-baseweb="tab-list"] { background-color: #0a192f; border-bottom: 2px solid #1f4068; }
    .stTabs [data-baseweb="tab"] { color: #8892b0; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #64ffda !important; border-bottom-color: #64ffda !important; }
    div[data-testid="stMetricValue"] { color: #64ffda; }
    </style>
""", unsafe_allow_html=True)

# 1. Load Data
data = load_all_data()
df_main = data["main"]
df_delays = data["delays"]

if df_main.empty:
    st.error("System Offline: No Main Production Data Found.")
    st.stop()

# 2. Sidebar Filters
st.sidebar.markdown("### SCADA Control Panel")
date_min, date_max = df_main["Timestamp"].min().date(), df_main["Timestamp"].max().date()
date_range = st.sidebar.date_input("Operating Period", (date_min, date_max), min_value=date_min, max_value=date_max)
target_mt = st.sidebar.number_input("Monthly Target (MT)", value=50000)

df_filtered = df_main.copy()
delay_filtered = df_delays.copy()

if len(date_range) == 2:
    df_filtered = df_filtered[(df_filtered["Timestamp"].dt.date >= date_range[0]) & (df_filtered["Timestamp"].dt.date <= date_range[1])]
    if not delay_filtered.empty:
        delay_filtered = delay_filtered[(delay_filtered['Date'].dt.date >= date_range[0]) & (delay_filtered['Date'].dt.date <= date_range[1])]

# Clean Shift Filter Dropdown (Removes NaNs and formats correctly)
if 'Shift' in df_filtered.columns:
    valid_shifts = [s for s in df_filtered['Shift'].dropna().unique() if s != '']
    valid_shifts.sort()
    shift_sel = st.sidebar.selectbox("Shift Filter", ["All"] + valid_shifts)
    if shift_sel != "All":
        df_filtered = df_filtered[df_filtered["Shift"] == shift_sel]

# 3. Calculate KPIs
kpis = calculate_kpis(df_filtered, delay_filtered, monthly_target_mt=target_mt)

# 4. Top WinCC Status Header
col1, col2, col3, col4, col5 = st.columns(5)
# Swapped the confusing RUNNING/STOPPED for a logical UPTIME metric
col1.metric("PLANT UPTIME", f"{kpis['availability']:.1f} %", delta_color="off")
col2.metric("TOTAL PROD (MT)", f"{kpis['total_prod']:,.2f}")
col3.metric("OEE %", f"{kpis['oee']:.1f} %")
col4.metric("TOTAL HEATS", f"{kpis['total_heats']}")
col5.metric("TOTAL DOWNTIME", f"{kpis['total_downtime']:,.0f} min")

st.markdown("---")

# 5. Application Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 OEE & Speed", "📈 Production & Temps", "⚠️ Downtime & RCA", "🛠️ PM & Chemistry"])

with tab1:
    st.markdown("### Equipment Effectiveness")
    g1, g2, g3, g4 = st.columns(4)
    with g1: st.plotly_chart(create_gauge(kpis['oee'], "OEE", 85), use_container_width=True)
    with g2: st.plotly_chart(create_gauge(kpis['availability'], "Availability", 90), use_container_width=True)
    with g3: st.plotly_chart(create_gauge(kpis['performance'], "Performance", 95), use_container_width=True)
    with g4: st.plotly_chart(create_gauge(kpis['utilization'], "Utilization", 80), use_container_width=True)

    st.markdown("### Speed Analytics")
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Avg Casting Speed", f"{kpis['avg_speed']:.2f} m/min")
    s2.metric("Max Casting Speed", f"{kpis['max_speed']:.2f} m/min")
    s3.metric("Min Casting Speed", f"{kpis['min_speed']:.2f} m/min")
    s4.metric("Total Casting Time", f"{kpis['casting_time']:,.0f} mins")

with tab2:
    st.markdown("### Production Achievement & Targets")
    p1, p2, p3 = st.columns(3)
    p1.metric("Target vs Actual", f"{kpis['achievement_pct']:.1f} %")
    p2.metric("Average Production", f"{kpis['avg_prod']:.2f} MT/Heat")
    p3.metric("Total Sequences", f"{kpis['total_seq']}")

    st.markdown("### Thermal Dynamics")
    t1, t2 = st.columns(2)
    t1.metric("Avg Tundish Temp", f"{kpis['avg_tun_temp']:.1f} °C")
    t2.metric("Avg Lifting Temp", f"{kpis['avg_lift_temp']:.1f} °C")

with tab3:
    st.markdown("### Downtime & Delay Breakdown")
    d1, d2, d3 = st.columns(3)
    d1.metric("Avg Downtime per Incident", f"{kpis['avg_downtime']:.1f} min")
    d2.metric("Electrical Delay Count", f"{kpis['electrical_count']}")
    d3.metric("Root Cause Identifications", f"{len(data['rca'])}")

    if not delay_filtered.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(create_pareto(delay_filtered, group_col='Agency'), use_container_width=True)
        with c2:
            st.plotly_chart(create_pareto(delay_filtered, group_col='Reason'), use_container_width=True)
        
        st.markdown("#### Detailed Delay Log (Type / Agency / Reason)")
        st.dataframe(delay_filtered.sort_values('Delay (mins)', ascending=False), use_container_width=True, hide_index=True)
    else:
        st.success("No downtime recorded for this period.")

with tab4:
    st.markdown("### Machine Health, PMs, & Chemistry")
    
    st.markdown("#### Grid Gap Measurements")
    if not data['grid'].empty: st.dataframe(data['grid'].head(10), use_container_width=True)
    else: st.info("Grid Gap data pending sync.")

    st.markdown("#### Chemical Composition")
    if not data['chem'].empty: st.dataframe(data['chem'], use_container_width=True)
    else: st.info("Chemistry data pending sync.")

    st.markdown("#### PM Orders & Status")
    if not data['pm'].empty: st.dataframe(data['pm'], use_container_width=True)
    else: st.info("PM SAP data pending sync.")
