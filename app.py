

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_all_data
from utils.metrics import calculate_kpis
from utils.charts import create_gauge, create_pareto

st.set_page_config(page_title="Caster System OS", page_icon=" ", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #050e14; color: #e0e6ed; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
    .stTabs [data-baseweb="tab-list"] { background-color: #0a192f; border-bottom: 2px solid #1f4068; }
    .stTabs [data-baseweb="tab"] { color: #8892b0; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #64ffda !important; border-bottom-color: #64ffda !important; }
    div[data-testid="stMetricValue"] { color: #64ffda; }
    </style>
""", unsafe_allow_html=True)


data = load_all_data()
df_main = data.get("main", pd.DataFrame())
df_delays = data.get("delays", pd.DataFrame())

if df_main.empty:
    st.error("System Offline: No Main Production Data Found.")
    st.stop()


st.sidebar.markdown("### SCADA Control Panel")
date_min, date_max = df_main["Timestamp"].min().date(), df_main["Timestamp"].max().date()
date_range = st.sidebar.date_input("Operating Period", (date_min, date_max), min_value=date_min, max_value=date_max)


df_filtered = df_main.copy()
delay_filtered = df_delays.copy()

if len(date_range) == 2:
    df_filtered = df_filtered[(df_filtered["Timestamp"].dt.date >= date_range[0]) & (df_filtered["Timestamp"].dt.date <= date_range[1])]
    if not delay_filtered.empty:
        delay_filtered = delay_filtered[(delay_filtered['Date'].dt.date >= date_range[0]) & (delay_filtered['Date'].dt.date <= date_range[1])]


if 'Shift' in df_filtered.columns:
    valid_shifts = [s for s in df_filtered['Shift'].dropna().unique() if s != '']
    valid_shifts.sort()
    shift_sel = st.sidebar.selectbox("Shift Filter", ["All"] + valid_shifts)
    if shift_sel != "All":
        df_filtered = df_filtered[df_filtered["Shift"] == shift_sel]


kpis = calculate_kpis(df_filtered, delay_filtered, target_mt)


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("PLANT UPTIME", f"{kpis['availability']:.1f} %", delta_color="off")
col2.metric("TOTAL PROD (MT)", f"{kpis['total_prod']:,.2f}")
col3.metric("OEE %", f"{kpis['oee']:.1f} %")
col4.metric("TOTAL HEATS", f"{kpis['total_heats']}")
col5.metric("TOTAL DOWNTIME", f"{kpis['total_downtime']:,.0f} min")

st.markdown("---")


tab1, tab2, tab3, tab4 = st.tabs([" OEE & Speed", " Production & Temps", " Downtime & RCA", " PM & Chemistry"])

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
    
   
    rca_data = data.get('rca', pd.DataFrame())
    d3.metric("Root Cause Identifications", f"{len(rca_data)}")

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
    grid_data = data.get('grid', pd.DataFrame())
    if not grid_data.empty: 
        st.dataframe(grid_data.head(10), use_container_width=True)
    else: 
        st.info("Grid Gap data pending sync.")

   
    st.markdown("#### Chemical Composition Log (C%, Mn%, Si%, S%, P%)")
    chem_data = data.get('chem', pd.DataFrame())
    if not chem_data.empty: 
        st.dataframe(chem_data, use_container_width=True, hide_index=True)
    else: 
        st.info("Chemistry data pending sync.")

   
    st.markdown("#### SAP Preventative Maintenance (PM) Orders")
    pm_data = data.get('pm', pd.DataFrame())
    if not pm_data.empty: 
        display_cols = [c for c in ['Order', 'Basic start date', 'Description of Technical Object', 'System status', 'Equipment'] if c in pm_data.columns]
        st.dataframe(pm_data[display_cols] if display_cols else pm_data, use_container_width=True, hide_index=True)
    else: 
        st.info("PM SAP data pending sync.")
