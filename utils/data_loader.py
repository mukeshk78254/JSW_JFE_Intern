from pathlib import Path

import pandas as pd
import numpy as np

from data.generate_data import generate_dataset


def load_data() -> pd.DataFrame:
    data_path = Path(__file__).resolve().parents[1] / "data" / "Caster_Performance_Dummy_Dataset.csv"
    if not data_path.exists():
        generate_dataset(data_path)
    
    df = pd.read_csv(data_path)
    
    # Map columns from your dataset to app's expected columns
    column_mapping = {
        'Heat_Number': 'Heat Number',
        'Casting_Speed_m_min': 'Casting Speed',
        'Mold_Level_mm': 'Mold Level',
        'Downtime_min': 'Downtime',
        'Production_Ton': 'Production',
        'Steel_Temperature_C': 'Temperature',
        'Water_Flow_L_min': 'Water Flow',
        'Hydraulic_Pressure_bar': 'Hydraulic Pressure',
        'Alarm_Name': 'Alarm',
        'Alarm_Severity': 'Alarm Severity',
        'Downtime_Reason': 'Downtime Category',
        'Machine_Status': 'Machine Status',
        'PLC_Status': 'PLC_Status',
    }
    
    # Rename columns
    df = df.rename(columns=column_mapping)
    
    # Parse Timestamp
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Fill NaN/missing values with safe defaults
    df['Alarm'] = df['Alarm'].fillna('No Alarm').replace({np.nan: 'No Alarm'})
    df['Alarm Severity'] = df['Alarm Severity'].fillna('None').replace({np.nan: 'None'})
    df['Downtime Category'] = df['Downtime Category'].fillna('None').replace({np.nan: 'None'})
    
    # Ensure numeric columns are properly typed
    df['Casting Speed'] = pd.to_numeric(df['Casting Speed'], errors='coerce').fillna(0)
    df['Mold Level'] = pd.to_numeric(df['Mold Level'], errors='coerce').fillna(0)
    df['Downtime'] = pd.to_numeric(df['Downtime'], errors='coerce').fillna(0)
    df['Production'] = pd.to_numeric(df['Production'], errors='coerce').fillna(0)
    df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce').fillna(0)
    df['Water Flow'] = pd.to_numeric(df['Water Flow'], errors='coerce').fillna(0)
    df['Hydraulic Pressure'] = pd.to_numeric(df['Hydraulic Pressure'], errors='coerce').fillna(0)
    
    # Set default status columns if missing
    status_cols = ['Mold_Status', 'Oscillation_Status', 'Hydraulic_Status', 'Water_Cooling_Status', 'Shear_Status', 'Roller_Table_Status']
    for col in status_cols:
        if col not in df.columns:
            df[col] = 'Healthy'
        else:
            df[col] = df[col].fillna('Healthy')
    
    df = df.sort_values("Timestamp").reset_index(drop=True)
    return df
