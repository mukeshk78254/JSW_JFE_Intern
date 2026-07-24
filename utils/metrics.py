# # # # def compute_metrics(df):
# # # #     if df.empty:
# # # #         return {
# # # #             "avg_speed": 0.0,
# # # #             "max_speed": 0.0,
# # # #             "min_speed": 0.0,
# # # #             "mold_level_stability": 0.0,
# # # #             "availability": 0.0,
# # # #             "productivity": 0.0,
# # # #             "oee": 0.0,
# # # #             "yield_pct": 0.0,
# # # #         }

# # # #     runtime_minutes = max(len(df) * 10, 1)
# # # #     total_downtime = df["Downtime"].sum()
# # # #     availability = max(0.0, 100.0 * (1 - total_downtime / runtime_minutes))

# # # #     avg_speed = df["Casting Speed"].mean()
# # # #     max_speed = df["Casting Speed"].max()
# # # #     min_speed = df["Casting Speed"].min()
# # # #     mold_level_stability = max(0.0, 100.0 - (df["Mold Level"].std() * 12.5))

# # # #     productivity = df["Production"].sum() / (runtime_minutes / 60.0)
# # # #     target_speed = 1.6
# # # #     target_output_per_hour = 220.0

# # # #     performance = min(100.0, (avg_speed / target_speed) * 100.0)
# # # #     quality = min(100.0, max(0.0, 100.0 - (total_downtime / runtime_minutes) * 100.0))
# # # #     oee = availability * (performance / 100.0) * (quality / 100.0) * 100.0
# # # #     yield_pct = min(100.0, (df["Production"].sum() / ((runtime_minutes / 60.0) * target_output_per_hour)) * 100.0)

# # # #     return {
# # # #         "avg_speed": avg_speed,
# # # #         "max_speed": max_speed,
# # # #         "min_speed": min_speed,
# # # #         "mold_level_stability": mold_level_stability,
# # # #         "availability": availability,
# # # #         "productivity": productivity,
# # # #         "oee": oee,
# # # #         "yield_pct": yield_pct,
# # # #     }


# # # def compute_metrics(df):
# # #     if df.empty:
# # #         return {
# # #             "avg_speed": 0.0,
# # #             "max_speed": 0.0,
# # #             "min_speed": 0.0,
# # #             "availability": 0.0,
# # #             "productivity": 0.0,
# # #             "oee": 0.0,
# # #             "yield_pct": 0.0,
# # #         }
    
# # #     # Use real Casting Time from the Excel sheet
# # #     if "Casting Time" in df.columns and df["Casting Time"].sum() > 0:
# # #         runtime_minutes = df["Casting Time"].sum()
# # #     else:
# # #         runtime_minutes = max(len(df) * 10, 1)
        
# # #     total_downtime = df["Downtime"].sum()
# # #     total_time = runtime_minutes + total_downtime
    
# # #     # Calculate Availability
# # #     availability = max(0.0, 100.0 * (1 - total_downtime / max(total_time, 1)))
    
# # #     # Calculate Speed Metrics
# # #     avg_speed = df["Casting Speed"].mean()
# # #     max_speed = df["Casting Speed"].max()
# # #     min_speed = df["Casting Speed"].min()
    
# # #     productivity = df["Production"].sum() / max((runtime_minutes / 60.0), 1)
    
# # #     # Operational Targets
# # #     target_speed = 5.0
# # #     target_output_per_hour = 220.0
    
# # #     performance = min(100.0, (avg_speed / target_speed) * 100.0) if target_speed else 0.0
# # #     quality = min(100.0, max(0.0, 100.0 - (total_downtime / max(total_time, 1)) * 100.0))
    
# # #     # OEE & Yield Math
# # #     oee = (availability / 100.0) * (performance / 100.0) * (quality / 100.0) * 100.0
# # #     yield_pct = min(100.0, (df["Production"].sum() / max(((runtime_minutes / 60.0) * target_output_per_hour), 1)) * 100.0)
    
# # #     return {
# # #         "avg_speed": avg_speed,
# # #         "max_speed": max_speed,
# # #         "min_speed": min_speed,
# # #         "availability": availability,
# # #         "productivity": productivity,
# # #         "oee": oee,
# # #         "yield_pct": yield_pct,
# # #     }


# # def calculate_kpis(df):
# #     if df.empty:
# #         return {"oee": 0, "availability": 0, "performance": 0, "quality": 0, "utilization": 0, "total_prod": 0, "avg_speed": 0, "downtime": 0}

# #     # Time Metrics (Assumes daily aggregation for calendar time)
# #     calendar_mins = len(df) * 24 * 60
# #     downtime_mins = df['Downtime'].sum() if 'Downtime' in df.columns else 0
# #     casting_mins = df['Casting Time'].sum() if 'Casting Time' in df.columns else (calendar_mins - downtime_mins)
    
# #     # 1. Availability = Operating Time / Planned Production Time
# #     planned_time = calendar_mins 
# #     operating_time = planned_time - downtime_mins
# #     availability = max(0.0, (operating_time / planned_time) * 100) if planned_time > 0 else 0

# #     # 2. Performance = (Total Parts / Operating Time) / Ideal Run Rate
# #     target_speed = 5.0 # m/min target
# #     avg_speed = df['Casting Speed'].mean() if 'Casting Speed' in df.columns else 0
# #     performance = min(100.0, (avg_speed / target_speed) * 100) if target_speed > 0 else 0

# #     # 3. Quality (Assumed 98% yield baseline if no scrap data available yet)
# #     quality = 98.5 

# #     # 4. OEE = Availability x Performance x Quality
# #     oee = (availability / 100) * (performance / 100) * (quality / 100) * 100

# #     # 5. Utilization
# #     utilization = (casting_mins / calendar_mins) * 100 if calendar_mins > 0 else 0

# #     total_prod = df['Production'].sum() if 'Production' in df.columns else 0

# #     return {
# #         "oee": oee,
# #         "availability": availability,
# #         "performance": performance,
# #         "quality": quality,
# #         "utilization": utilization,
# #         "total_prod": total_prod,
# #         "avg_speed": avg_speed,
# #         "downtime": downtime_mins
# #     }


# import pandas as pd

# def calculate_kpis(df_main, df_delays, monthly_target_mt=50000):
#     if df_main.empty:
#         return {
#             "total_prod": 0, "avg_prod": 0, "avg_speed": 0, "max_speed": 0, "min_speed": 0,
#             "casting_time": 0, "total_heats": 0, "total_seq": 0, "avg_tun_temp": 0, "avg_lift_temp": 0,
#             "total_downtime": 0, "avg_downtime": 0, "electrical_count": 0,
#             "oee": 0, "availability": 0, "performance": 0, "quality": 0, "utilization": 0,
#             "monthly_target": monthly_target_mt, "achievement_pct": 0
#         }

#     # Production & Speeds
#     total_prod = df_main['Production'].sum()
#     avg_prod = df_main['Production'].mean()
#     speeds = df_main[df_main['Casting Speed'] > 0]['Casting Speed']
#     avg_speed = speeds.mean() if not speeds.empty else 0
#     max_speed = speeds.max() if not speeds.empty else 0
#     min_speed = speeds.min() if not speeds.empty else 0
    
#     # Times & Counts
#     casting_time = df_main['Casting Time'].sum()
#     total_heats = df_main['Heat Number'].nunique() if 'Heat Number' in df_main.columns else len(df_main)
#     total_seq = df_main['Sequence Number'].nunique() if 'Sequence Number' in df_main.columns else 1

#     # Temperatures
#     tuns = df_main[df_main['Tundish Temp'] > 0]['Tundish Temp']
#     lifts = df_main[df_main['Lifting Temp'] > 0]['Lifting Temp'] if 'Lifting Temp' in df_main.columns else pd.Series()
#     avg_tun_temp = tuns.mean() if not tuns.empty else 0
#     avg_lift_temp = lifts.mean() if not lifts.empty else 0

#     # Delays
#     total_downtime = df_delays['Delay (mins)'].sum() if not df_delays.empty else 0
#     avg_downtime = df_delays['Delay (mins)'].mean() if not df_delays.empty else 0
#     elec_delays = df_delays[df_delays['Type'] == 'Electrical'] if not df_delays.empty else pd.DataFrame()
#     electrical_count = len(elec_delays)

#     # OEE Variables
#     calendar_mins = len(df_main) * 24 * 60 # Assuming df_main represents daily records
#     planned_time = calendar_mins
#     operating_time = planned_time - total_downtime
    
#     availability = max(0.0, (operating_time / planned_time) * 100) if planned_time > 0 else 0
    
#     target_speed = 5.0 # baseline target
#     performance = min(100.0, (avg_speed / target_speed) * 100) if target_speed > 0 else 0
    
#     quality = 98.5 # baseline yield
#     oee = (availability / 100) * (performance / 100) * (quality / 100) * 100
#     utilization = (casting_time / calendar_mins) * 100 if calendar_mins > 0 else 0

#     # Targets
#     achievement_pct = (total_prod / monthly_target_mt) * 100 if monthly_target_mt > 0 else 0

#     return {
#         "total_prod": total_prod, "avg_prod": avg_prod, 
#         "avg_speed": avg_speed, "max_speed": max_speed, "min_speed": min_speed,
#         "casting_time": casting_time, "total_heats": total_heats, "total_seq": total_seq,
#         "avg_tun_temp": avg_tun_temp, "avg_lift_temp": avg_lift_temp,
#         "total_downtime": total_downtime, "avg_downtime": avg_downtime, "electrical_count": electrical_count,
#         "oee": oee, "availability": availability, "performance": performance, 
#         "quality": quality, "utilization": utilization,
#         "monthly_target": monthly_target_mt, "achievement_pct": achievement_pct
#     # }

#     import pandas as pd

# def calculate_kpis(df_main, df_delays, monthly_target_mt=50000):
#     if df_main.empty:
#         return {
#             "total_prod": 0, "avg_prod": 0, "avg_speed": 0, "max_speed": 0, "min_speed": 0,
#             "casting_time": 0, "total_heats": 0, "total_seq": 0, "avg_tun_temp": 0, "avg_lift_temp": 0,
#             "total_downtime": 0, "avg_downtime": 0, "electrical_count": 0,
#             "oee": 0, "availability": 0, "performance": 0, "quality": 0, "utilization": 0,
#             "monthly_target": monthly_target_mt, "achievement_pct": 0
#         }

#     # Production & Speeds
#     total_prod = df_main['Production'].sum()
#     avg_prod = df_main['Production'].mean()
    
#     # Filter out absolute 0s for realistic averages
#     speeds = df_main[df_main['Casting Speed'] > 0.1]['Casting Speed'] 
#     avg_speed = speeds.mean() if not speeds.empty else 0
#     max_speed = speeds.max() if not speeds.empty else 0
#     min_speed = speeds.min() if not speeds.empty else 0
    
#     # Times & Counts
#     casting_time = df_main['Casting Time'].sum()
#     total_heats = df_main['Heat Number'].nunique() if 'Heat Number' in df_main.columns else len(df_main)
#     total_seq = df_main['Sequence Number'].nunique() if 'Sequence Number' in df_main.columns else 1

#     # Temperatures
#     tuns = df_main[df_main['Tundish Temp'] > 0]['Tundish Temp']
#     lifts = df_main[df_main['Lifting Temp'] > 0]['Lifting Temp'] if 'Lifting Temp' in df_main.columns else pd.Series()
#     avg_tun_temp = tuns.mean() if not tuns.empty else 0
#     avg_lift_temp = lifts.mean() if not lifts.empty else 0

#     # Delays
#     total_downtime = df_delays['Delay (mins)'].sum() if not df_delays.empty else 0
    
#     # Fix avg downtime calculation (avoid div by zero)
#     incidents = len(df_delays[df_delays['Delay (mins)'] > 0])
#     avg_downtime = (total_downtime / incidents) if incidents > 0 else 0
    
#     elec_delays = df_delays[df_delays['Type'] == 'Electrical'] if not df_delays.empty else pd.DataFrame()
#     electrical_count = len(elec_delays)

#     # OEE Variables
#     # If casting_time exists, calculate calendar time based on rows. Otherwise approximate.
#     total_rows = len(df_main)
#     planned_time = (total_rows * 24 * 60) if total_rows > 0 else (30 * 24 * 60)
#     operating_time = max(0, planned_time - total_downtime)
    
#     availability = max(0.0, (operating_time / planned_time) * 100) if planned_time > 0 else 0
    
#     # Target Speed baseline (adjust if your plant standard is different than 5.0m/min)
#     target_speed = 5.0 
#     # Fallback: if no speed data exists but production exists, assume 80% performance
#     if avg_speed == 0 and total_prod > 0:
#         performance = 80.0 
#     else:
#         performance = min(100.0, (avg_speed / target_speed) * 100) if target_speed > 0 else 0
    
#     quality = 98.5 # standard yield baseline
#     oee = (availability / 100) * (performance / 100) * (quality / 100) * 100
#     utilization = (casting_time / planned_time) * 100 if planned_time > 0 else 0

#     achievement_pct = (total_prod / monthly_target_mt) * 100 if monthly_target_mt > 0 else 0

#     return {
#         "total_prod": total_prod, "avg_prod": avg_prod, 
#         "avg_speed": avg_speed, "max_speed": max_speed, "min_speed": min_speed,
#         "casting_time": casting_time, "total_heats": total_heats, "total_seq": total_seq,
#         "avg_tun_temp": avg_tun_temp, "avg_lift_temp": avg_lift_temp,
#         "total_downtime": total_downtime, "avg_downtime": avg_downtime, "electrical_count": electrical_count,
#         "oee": oee, "availability": availability, "performance": performance, 
#         "quality": quality, "utilization": utilization,
#         "monthly_target": monthly_target_mt, "achievement_pct": achievement_pct
#     }


import pandas as pd

# def calculate_kpis(df_main, df_delays, df_targets):
def calculate_kpis(df_production, df_delays, monthly_target_mt=0):
    if df_main.empty:
        return {
            "total_prod": 0, "avg_prod": 0, "avg_speed": 0, "max_speed": 0, "min_speed": 0,
            "casting_time": 0, "total_heats": 0, "total_seq": 0, "avg_tun_temp": 0, "avg_lift_temp": 0,
            "total_downtime": 0, "avg_downtime": 0, "electrical_count": 0,
            "oee": 0, "availability": 0, "performance": 0, "utilization": 0, "achievement_pct": 0
        }

    total_prod = df_main['Production'].sum()
    avg_prod = df_main['Production'].mean()
    
    speeds = df_main[df_main['Casting Speed'] > 0.1]['Casting Speed'] 
    avg_speed = speeds.mean() if not speeds.empty else 0
    max_speed = speeds.max() if not speeds.empty else 0
    min_speed = speeds.min() if not speeds.empty else 0
    
    casting_time = df_main['Casting Time'].sum()
    total_heats = df_main['Heat Number'].nunique() if 'Heat Number' in df_main.columns else len(df_main)
    total_seq = df_main['Sequence Number'].nunique() if 'Sequence Number' in df_main.columns else 1

    tuns = df_main[df_main['Tundish Temp'] > 0]['Tundish Temp']
    lifts = df_main[df_main['Lifting Temp'] > 0]['Lifting Temp']
    avg_tun_temp = tuns.mean() if not tuns.empty else 0
    avg_lift_temp = lifts.mean() if not lifts.empty else 0

    total_downtime = df_delays['Delay (mins)'].sum() if not df_delays.empty else 0
    incidents = len(df_delays[df_delays['Delay (mins)'] > 0])
    avg_downtime = (total_downtime / incidents) if incidents > 0 else 0
    electrical_count = len(df_delays[df_delays['Type'] == 'Electrical']) if not df_delays.empty else 0

    # OEE Logic
    total_rows = len(df_main)
    planned_time = (total_rows * 24 * 60) if total_rows > 0 else (30 * 24 * 60)
    operating_time = max(0, planned_time - total_downtime)
    
    availability = max(0.0, (operating_time / planned_time) * 100) if planned_time > 0 else 0
    
    target_speed = 5.0 # baseline
    performance = 80.0 if avg_speed == 0 and total_prod > 0 else min(100.0, (avg_speed / target_speed) * 100) if target_speed > 0 else 0
    
    quality = 98.5 # yield baseline
    oee = (availability / 100) * (performance / 100) * (quality / 100) * 100
    utilization = (casting_time / planned_time) * 100 if planned_time > 0 else 0

    # Monthly Target Achievement
    target_mt = df_targets['TARGET'].sum() if not df_targets.empty and 'TARGET' in df_targets.columns else 0
    achievement_pct = (total_prod / target_mt) * 100 if target_mt > 0 else 0

    return {
        "total_prod": total_prod, "avg_prod": avg_prod, 
        "avg_speed": avg_speed, "max_speed": max_speed, "min_speed": min_speed,
        "casting_time": casting_time, "total_heats": total_heats, "total_seq": total_seq,
        "avg_tun_temp": avg_tun_temp, "avg_lift_temp": avg_lift_temp,
        "total_downtime": total_downtime, "avg_downtime": avg_downtime, "electrical_count": electrical_count,
        "oee": oee, "availability": availability, "performance": performance, 
        "utilization": utilization, "achievement_pct": achievement_pct
    }
