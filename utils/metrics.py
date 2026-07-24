import pandas as pd

def calculate_kpis(df_main, df_delays, monthly_target_mt=0):
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
    target_mt = monthly_target_mt
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
