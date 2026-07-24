import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

@st.cache_data(show_spinner=False)
def load_all_data():
    current_dir = Path.cwd()
    possible_dirs = [current_dir / "data", current_dir, Path(__file__).resolve().parents[1] / "data", Path(__file__).resolve().parents[1]]
    
    def find_file(pattern, dirs):
        for d in dirs:
            if d.exists() and d.is_dir():
                matches = list(d.glob(pattern))
                if matches: return matches[0]
        return None

   
    bops_file = find_file("*BOPS*.xlsx", possible_dirs) or find_file("*log*sheet*.xlsx", possible_dirs)
    csp_delay = find_file("*CSP DELAY*.xlsx", possible_dirs)
    elec_delay = find_file("*Electrical Delay*.xlsx", possible_dirs)
    chem_file = find_file("*Chemistry*.xlsx", possible_dirs)
    pm_file = find_file("*PM*.xlsx", possible_dirs) or find_file("*PM*.XLSX", possible_dirs)
    target_file = find_file("*MBP*.xlsx", possible_dirs) or find_file("*target*.xlsx", possible_dirs)
    rca_file = find_file("*RCA*.xlsx", possible_dirs)
    grid_file = find_file("*Grid*.xlsx", possible_dirs) or find_file("*Gap*.xlsx", possible_dirs)

    if not bops_file:
        st.error(" Could not find BOPS/Log Sheet file. Please ensure files are in the /data folder.")
        return {k: pd.DataFrame() for k in ["main", "delays", "targets", "pm", "chem", "rca", "grid"]}

 
    df_bops = pd.DataFrame()
    try:
        xls = pd.ExcelFile(bops_file)
        sheets = [pd.read_excel(bops_file, sheet_name=s, skiprows=0) for s in xls.sheet_names]
        df_bops = pd.concat(sheets, ignore_index=True)
        
   
        if len(df_bops.columns) >= 16: 
            df_bops = df_bops.rename(columns={
                df_bops.columns[1]: 'DATE',           # Column B
                df_bops.columns[2]: 'Shift',          # Column C
                df_bops.columns[5]: 'Sequence Number',# Column F
                df_bops.columns[9]: 'Heat Number',    # Column J
                df_bops.columns[10]: 'Lifting Temp',  # Column K
                df_bops.columns[15]: 'Tundish Temp',  # Column P
                df_bops.columns[16]: 'Casting Speed', # Column Q
                df_bops.columns[17]: 'Casting Time',  # Column R
                df_bops.columns[26]: 'Production'     # Column AA (DISCHARGE (MT))
            })

       
        if 'DATE' in df_bops.columns:
            
            df_bops = df_bops.dropna(subset=['DATE'])
           
            df_bops['Timestamp'] = pd.to_datetime(df_bops['DATE'], errors='coerce')
            
            df_bops = df_bops.dropna(subset=['Timestamp']).reset_index(drop=True)

      
        if 'Shift' in df_bops.columns:
            df_bops['Shift'] = df_bops['Shift'].astype(str).str.strip().str.upper()
            df_bops['Shift'] = df_bops['Shift'].replace(['NAN', 'NONE', ''], np.nan)

       
        for col in ['Casting Speed', 'Production', 'Tundish Temp', 'Lifting Temp', 'Casting Time']:
            if col in df_bops.columns:
                
                df_bops[col] = df_bops[col].astype(str).str.replace('-', '0', regex=False)
                df_bops[col] = pd.to_numeric(df_bops[col], errors='coerce').fillna(0)
            else:
                df_bops[col] = 0.0

    except Exception as e:
        st.error(f"Error reading BOPS: {e}")

   
    df_delays = pd.DataFrame()
    delay_list = []
    for f in [csp_delay, elec_delay]:
        if f:
            try:
                xls = pd.ExcelFile(f)
                for sheet in xls.sheet_names:
                    temp_df = pd.read_excel(f, sheet_name=sheet)
                    delay_col = next((c for c in temp_df.columns if 'DELAY' in str(c).upper() and 'MIN' in str(c).upper()), None)
                    date_col = next((c for c in temp_df.columns if 'DATE' in str(c).upper()), None)
                    
                    if date_col and delay_col:
                        temp_df = temp_df.rename(columns={delay_col: 'Delay (mins)', date_col: 'Date'})
                        temp_df['Agency'] = temp_df.get('Agency', 'Unknown')
                        temp_df['Reason'] = temp_df.get('Reason', 'Unknown')
                        temp_df['Type'] = 'Electrical' if 'elect' in str(f).lower() else temp_df.get('Type', 'Mechanical/Process')
                        delay_list.append(temp_df[['Date', 'Delay (mins)', 'Agency', 'Reason', 'Type']])
            except Exception:
                pass
            
    if delay_list:
        df_delays = pd.concat(delay_list, ignore_index=True)
        df_delays['Date'] = pd.to_datetime(df_delays['Date'], errors='coerce')
        df_delays['Delay (mins)'] = pd.to_numeric(df_delays['Delay (mins)'], errors='coerce').fillna(0)
        df_delays = df_delays.drop_duplicates(subset=['Date', 'Delay (mins)', 'Reason', 'Agency'])

   
    df_targets = pd.DataFrame(columns=['MONTH', 'TARGET', 'ACTUAL'])
    if target_file:
        try:
            temp_targets = pd.read_excel(target_file)
            if not temp_targets.empty and 'MONTH' not in [str(c).upper() for c in temp_targets.columns]:
                first_row_vals = [str(x).upper() for x in temp_targets.iloc[0].values]
                if 'MONTH' in first_row_vals:
                    temp_targets.columns = temp_targets.iloc[0]
                    temp_targets = temp_targets[1:].reset_index(drop=True)
            temp_targets.columns = [str(c).upper().strip() for c in temp_targets.columns]
            df_targets = temp_targets
        except Exception:
            pass

    return {
        "main": df_bops.sort_values('Timestamp').reset_index(drop=True) if not df_bops.empty else df_bops,
        "delays": df_delays,
        "targets": df_targets,
        "pm": pd.read_excel(pm_file) if pm_file else pd.DataFrame(),
        "chem": pd.read_excel(chem_file) if chem_file else pd.DataFrame(),
        "rca": pd.read_excel(rca_file) if rca_file else pd.DataFrame(),
        "grid": pd.read_excel(grid_file) if grid_file else pd.DataFrame() 
    }


