# # # # # # # from pathlib import Path

# # # # # # # import pandas as pd
# # # # # # # import numpy as np

# # # # # # # from data.generate_data import generate_dataset


# # # # # # # def load_data() -> pd.DataFrame:
# # # # # # #     data_path = Path(__file__).resolve().parents[1] / "data" / "Caster_Performance_Dummy_Dataset.csv"
# # # # # # #     if not data_path.exists():
# # # # # # #         generate_dataset(data_path)
    
# # # # # # #     df = pd.read_csv(data_path)
    
# # # # # # #     # Map columns from your dataset to app's expected columns
# # # # # # #     column_mapping = {
# # # # # # #         'Heat_Number': 'Heat Number',
# # # # # # #         'Casting_Speed_m_min': 'Casting Speed',
# # # # # # #         'Mold_Level_mm': 'Mold Level',
# # # # # # #         'Downtime_min': 'Downtime',
# # # # # # #         'Production_Ton': 'Production',
# # # # # # #         'Steel_Temperature_C': 'Temperature',
# # # # # # #         'Water_Flow_L_min': 'Water Flow',
# # # # # # #         'Hydraulic_Pressure_bar': 'Hydraulic Pressure',
# # # # # # #         'Alarm_Name': 'Alarm',
# # # # # # #         'Alarm_Severity': 'Alarm Severity',
# # # # # # #         'Downtime_Reason': 'Downtime Category',
# # # # # # #         'Machine_Status': 'Machine Status',
# # # # # # #         'PLC_Status': 'PLC_Status',
# # # # # # #     }
    
# # # # # # #     # Rename columns
# # # # # # #     df = df.rename(columns=column_mapping)
    
# # # # # # #     # Parse Timestamp
# # # # # # #     if 'Timestamp' in df.columns:
# # # # # # #         df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
# # # # # # #     # Fill NaN/missing values with safe defaults
# # # # # # #     df['Alarm'] = df['Alarm'].fillna('No Alarm').replace({np.nan: 'No Alarm'})
# # # # # # #     df['Alarm Severity'] = df['Alarm Severity'].fillna('None').replace({np.nan: 'None'})
# # # # # # #     df['Downtime Category'] = df['Downtime Category'].fillna('None').replace({np.nan: 'None'})
    
# # # # # # #     # Ensure numeric columns are properly typed
# # # # # # #     df['Casting Speed'] = pd.to_numeric(df['Casting Speed'], errors='coerce').fillna(0)
# # # # # # #     df['Mold Level'] = pd.to_numeric(df['Mold Level'], errors='coerce').fillna(0)
# # # # # # #     df['Downtime'] = pd.to_numeric(df['Downtime'], errors='coerce').fillna(0)
# # # # # # #     df['Production'] = pd.to_numeric(df['Production'], errors='coerce').fillna(0)
# # # # # # #     df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce').fillna(0)
# # # # # # #     df['Water Flow'] = pd.to_numeric(df['Water Flow'], errors='coerce').fillna(0)
# # # # # # #     df['Hydraulic Pressure'] = pd.to_numeric(df['Hydraulic Pressure'], errors='coerce').fillna(0)
    
# # # # # # #     # Set default status columns if missing
# # # # # # #     status_cols = ['Mold_Status', 'Oscillation_Status', 'Hydraulic_Status', 'Water_Cooling_Status', 'Shear_Status', 'Roller_Table_Status']
# # # # # # #     for col in status_cols:
# # # # # # #         if col not in df.columns:
# # # # # # #             df[col] = 'Healthy'
# # # # # # #         else:
# # # # # # #             df[col] = df[col].fillna('Healthy')
    
# # # # # # #     df = df.sort_values("Timestamp").reset_index(drop=True)
# # # # # # #     return df


# # # # # # import os
# # # # # # from pathlib import Path
# # # # # # import pandas as pd
# # # # # # import numpy as np
# # # # # # import streamlit as st

# # # # # # def load_data() -> pd.DataFrame:
# # # # # #     # 1. Dynamically find the project root (goes up one level from the 'utils' folder)
# # # # # #     project_root = Path(__file__).resolve().parents[1]
    
# # # # # #     # 2. Check multiple locations just in case (Root folder, Data folder, and Current Working Directory)
# # # # # #     possible_paths = [project_root, project_root / "data", Path.cwd()]
    
# # # # # #     base_path = None
# # # # # #     bops_file = None
    
# # # # # #     for p in possible_paths:
# # # # # #         if (p / "BOPS Alarm.xlsx").exists():
# # # # # #             bops_file = p / "BOPS_Alarm.xlsx"
# # # # # #             base_path = p
# # # # # #             break
            
# # # # # #     if not bops_file:
# # # # # #         st.error(f"❌ Could not find 'BOPS_Alarm.xlsx'. Please ensure the file is placed in one of these folders: {', '.join([str(p) for p in possible_paths])}")
# # # # # #         return pd.DataFrame()

# # # # # #     delay_files = [
# # # # # #         base_path / "CSP DELAY REPORT OF DT-19.10.2024_.xlsx",
# # # # # #         base_path / "Electrical Delay.xlsx"
# # # # # #     ]
    
# # # # # #     # 3. Load BOPS Data
# # # # # #     all_bops = []
# # # # # #     try:
# # # # # #         xls = pd.ExcelFile(bops_file)
# # # # # #         for sheet in xls.sheet_names:
# # # # # #             df_sheet = pd.read_excel(bops_file, sheet_name=sheet)
# # # # # #             all_bops.append(df_sheet)
# # # # # #     except Exception as e:
# # # # # #         st.error(f"Error reading BOPS file: {e}")
# # # # # #         return pd.DataFrame()
            
# # # # # #     if all_bops:
# # # # # #         df = pd.concat(all_bops, ignore_index=True)
# # # # # #     else:
# # # # # #         return pd.DataFrame()
        
# # # # # #     # Drop empty dates and convert to Timestamp
# # # # # #     df = df.dropna(subset=['DATE'])
# # # # # #     df['Timestamp'] = pd.to_datetime(df['DATE'], errors='coerce')
# # # # # #     df = df.dropna(subset=['Timestamp']) # Remove any rows where date conversion failed
    
# # # # # #     # Map real column headers
# # # # # #     col_mapping = {
# # # # # #         'SHIFT': 'Shift',
# # # # # #         'HEAT NO': 'Heat Number',
# # # # # #         'ACTUAL CASTING SPEED (m/min)': 'Casting Speed',
# # # # # #         'DISCHARGE (MT)': 'Production',
# # # # # #         'TUNDISH TEMPERATURE': 'Temperature',
# # # # # #         'CASTING TIME': 'Casting Time'
# # # # # #     }
# # # # # #     df = df.rename(columns=col_mapping)
    
# # # # # #     # 4. Load Delay Data
# # # # # #     delay_dfs = []
# # # # # #     for f in delay_files:
# # # # # #         if f.exists():
# # # # # #             try:
# # # # # #                 xls_d = pd.ExcelFile(f)
# # # # # #                 for sheet in xls_d.sheet_names:
# # # # # #                     df_d = pd.read_excel(f, sheet_name=sheet)
# # # # # #                     if 'Date' in df_d.columns and 'Delay (mins)' in df_d.columns:
# # # # # #                         if 'Reason' in df_d.columns:
# # # # # #                             df_d['Category'] = df_d['Reason']
# # # # # #                         elif 'Agency' in df_d.columns:
# # # # # #                             df_d['Category'] = df_d['Agency']
# # # # # #                         else:
# # # # # #                             df_d['Category'] = 'Unknown'
# # # # # #                         delay_dfs.append(df_d[['Date', 'Delay (mins)', 'Category']])
# # # # # #             except Exception:
# # # # # #                 pass # Skip files that are open or corrupted
                    
# # # # # #     if delay_dfs:
# # # # # #         all_delays = pd.concat(delay_dfs, ignore_index=True)
# # # # # #         all_delays['Date'] = pd.to_datetime(all_delays['Date'], errors='coerce')
# # # # # #         all_delays = all_delays.dropna(subset=['Date'])
# # # # # #         all_delays['Delay (mins)'] = pd.to_numeric(all_delays['Delay (mins)'], errors='coerce').fillna(0)
        
# # # # # #         # Aggregate delays by Date
# # # # # #         delay_summary = all_delays.groupby('Date').agg({
# # # # # #             'Delay (mins)': 'sum', 
# # # # # #             'Category': lambda x: ', '.join([str(i) for i in x.unique() if str(i) != 'nan'])
# # # # # #         }).reset_index()
        
# # # # # #         # Merge delays into BOPS
# # # # # #         df = pd.merge(df, delay_summary, left_on='Timestamp', right_on='Date', how='left')
# # # # # #         df['Downtime'] = df['Delay (mins)'].fillna(0.0)
# # # # # #         df['Downtime Category'] = df['Category'].replace('', 'None').fillna('None')
# # # # # #     else:
# # # # # #         df['Downtime'] = 0.0
# # # # # #         df['Downtime Category'] = 'None'
        
# # # # # #     df['Machine Status'] = np.where(df['Downtime'] > 0, 'Stopped', 'Running')
    
# # # # # #     # Ensure numerics
# # # # # #     for col in ['Casting Speed', 'Production', 'Temperature', 'Casting Time']:
# # # # # #         if col in df.columns:
# # # # # #             df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
# # # # # #     df['Alarm'] = 'No Alarm'
# # # # # #     df['Alarm Severity'] = 'None'
    
# # # # # #     # Basic Machine Health flags
# # # # # #     status_cols = ['PLC_Status', 'Mold_Status', 'Oscillation_Status', 'Hydraulic_Status', 'Water_Cooling_Status', 'Shear_Status', 'Roller_Table_Status']
# # # # # #     for col in status_cols:
# # # # # #         df[col] = 'Healthy'
        
# # # # # #     df = df.sort_values('Timestamp').reset_index(drop=True)
# # # # # #     return df



# # # # # import pandas as pd
# # # # # import numpy as np
# # # # # from pathlib import Path
# # # # # import streamlit as st

# # # # # @st.cache_data(show_spinner=False)
# # # # # def load_all_data():
# # # # #     # 1. Define all possible folders to search
# # # # #     current_dir = Path.cwd()
# # # # #     data_dir = current_dir / "data"
# # # # #     script_dir = Path(__file__).resolve().parents[1]
# # # # #     script_data_dir = script_dir / "data"
    
# # # # #     possible_dirs = [data_dir, current_dir, script_data_dir, script_dir]
    
# # # # #     # Helper function to find files flexibly (ignoring exact spaces, underscores, or " (1)" suffixes)
# # # # #     def find_file(pattern, dirs):
# # # # #         for d in dirs:
# # # # #             if d.exists() and d.is_dir():
# # # # #                 matches = list(d.glob(pattern))
# # # # #                 if matches:
# # # # #                     return matches[0]
# # # # #         return None

# # # # #     # 2. Locate files
# # # # #     bops_file = find_file("BOPS*Alarm*.xlsx", possible_dirs)
# # # # #     csp_delay = find_file("CSP DELAY*.xlsx", possible_dirs)
# # # # #     elec_delay = find_file("Electrical Delay*.xlsx", possible_dirs)
# # # # #     grid_file = find_file("Grid Gap*.xlsx", possible_dirs)

# # # # #     if not bops_file:
# # # # #         st.error(f"❌ Could not find BOPS Alarm file. Searched in: {[str(p) for p in possible_dirs]}")
# # # # #         return {"main": pd.DataFrame(), "delays": pd.DataFrame(), "grid": pd.DataFrame(), "pm": pd.DataFrame(), "rca": pd.DataFrame(), "chem": pd.DataFrame()}

# # # # #     delay_files = [f for f in [csp_delay, elec_delay] if f is not None]

# # # # #     # 3. Load BOPS (Production)
# # # # #     df_bops = pd.DataFrame()
# # # # #     try:
# # # # #         xls = pd.ExcelFile(bops_file)
# # # # #         sheets = [pd.read_excel(bops_file, sheet_name=s) for s in xls.sheet_names]
# # # # #         df_bops = pd.concat(sheets, ignore_index=True).dropna(subset=['DATE'])
# # # # #         df_bops['Timestamp'] = pd.to_datetime(df_bops['DATE'], errors='coerce')
# # # # #         df_bops = df_bops.rename(columns={
# # # # #             'SHIFT': 'Shift', 'HEAT NO': 'Heat Number', 'GRADE': 'Grade',
# # # # #             'ACTUAL CASTING SPEED (m/min)': 'Casting Speed', 
# # # # #             'DISCHARGE (MT)': 'Production', 'TUNDISH TEMPERATURE': 'Temperature',
# # # # #             'CASTING TIME': 'Casting Time'
# # # # #         })
# # # # #         for col in ['Casting Speed', 'Production', 'Temperature', 'Casting Time']:
# # # # #             df_bops[col] = pd.to_numeric(df_bops[col], errors='coerce').fillna(0)
# # # # #     except Exception as e:
# # # # #         st.error(f"Error reading {bops_file.name}: {e}")

# # # # #     # 4. Load Delays (CSP & Electrical)
# # # # #     df_delays = pd.DataFrame()
# # # # #     delay_list = []
# # # # #     for f in delay_files:
# # # # #         try:
# # # # #             xls = pd.ExcelFile(f)
# # # # #             for sheet in xls.sheet_names:
# # # # #                 temp_df = pd.read_excel(f, sheet_name=sheet)
# # # # #                 if 'Date' in temp_df.columns and 'Delay (mins)' in temp_df.columns:
# # # # #                     temp_df['Category'] = temp_df.get('Agency', temp_df.get('Reason', 'Unknown'))
# # # # #                     delay_list.append(temp_df[['Date', 'Delay (mins)', 'Category']])
# # # # #         except Exception:
# # # # #             pass
            
# # # # #     if delay_list:
# # # # #         df_delays = pd.concat(delay_list, ignore_index=True)
# # # # #         df_delays['Date'] = pd.to_datetime(df_delays['Date'], errors='coerce')
# # # # #         df_delays['Delay (mins)'] = pd.to_numeric(df_delays['Delay (mins)'], errors='coerce').fillna(0)

# # # # #     # 5. Load Grid Gap
# # # # #     df_grid = pd.DataFrame()
# # # # #     if grid_file:
# # # # #         try:
# # # # #             df_grid = pd.read_excel(grid_file, sheet_name="Grid Gap ")
# # # # #         except Exception:
# # # # #             pass

# # # # #     # 6. Placeholders for PM, RCA, Chemistry
# # # # #     df_pm = pd.DataFrame()
# # # # #     df_rca = pd.DataFrame()
# # # # #     df_chem = pd.DataFrame()

# # # # #     # 7. Merge Production and Delays for the Main View
# # # # #     df_main = df_bops.copy()
# # # # #     if not df_main.empty and not df_delays.empty:
# # # # #         delay_summary = df_delays.groupby('Date').agg({
# # # # #             'Delay (mins)': 'sum', 
# # # # #             'Category': lambda x: ', '.join([str(i) for i in x.unique() if str(i) != 'nan'])
# # # # #         }).reset_index()
# # # # #         df_main = pd.merge(df_main, delay_summary, left_on='Timestamp', right_on='Date', how='left')
# # # # #         df_main['Downtime'] = df_main['Delay (mins)'].fillna(0.0)
# # # # #         df_main['Downtime Category'] = df_main['Category'].fillna('None')
# # # # #     elif not df_main.empty:
# # # # #         df_main['Downtime'] = 0.0
# # # # #         df_main['Downtime Category'] = 'None'

# # # # #     if not df_main.empty:
# # # # #         df_main['Machine Status'] = np.where(df_main['Downtime'] > 0, 'Stopped', 'Running')

# # # # #     return {
# # # # #         "main": df_main.sort_values('Timestamp').reset_index(drop=True) if not df_main.empty else df_main,
# # # # #         "delays": df_delays,
# # # # #         "grid": df_grid,
# # # # #         "pm": df_pm,
# # # # #         "rca": df_rca,
# # # # #         "chem": df_chem
# # # # #     }

# # # # import pandas as pd
# # # # import numpy as np
# # # # from pathlib import Path
# # # # import streamlit as st

# # # # @st.cache_data(show_spinner=False)
# # # # def load_all_data():
# # # #     current_dir = Path.cwd()
# # # #     possible_dirs = [current_dir / "data", current_dir, Path(__file__).resolve().parents[1] / "data", Path(__file__).resolve().parents[1]]
    
# # # #     def find_file(pattern, dirs):
# # # #         for d in dirs:
# # # #             if d.exists() and d.is_dir():
# # # #                 matches = list(d.glob(pattern))
# # # #                 if matches: return matches[0]
# # # #         return None

# # # #     # 1. Locate files
# # # #     bops_file = find_file("BOPS*Alarm*.xlsx", possible_dirs)
# # # #     csp_delay = find_file("CSP DELAY*.xlsx", possible_dirs)
# # # #     elec_delay = find_file("Electrical Delay*.xlsx", possible_dirs)
# # # #     grid_file = find_file("Grid Gap*.xlsx", possible_dirs)
# # # #     chem_file = find_file("*Chem*.xlsx", possible_dirs)
# # # #     pm_file = find_file("*PM*.xlsx", possible_dirs)

# # # #     if not bops_file:
# # # #         st.error(f"❌ Could not find BOPS Alarm file. Checked: {[str(p) for p in possible_dirs]}")
# # # #         return {k: pd.DataFrame() for k in ["main", "delays", "grid", "pm", "chem", "rca"]}

# # # #     # 2. Load BOPS (Production)
# # # #     df_bops = pd.DataFrame()
# # # #     try:
# # # #         xls = pd.ExcelFile(bops_file)
# # # #         sheets = [pd.read_excel(bops_file, sheet_name=s) for s in xls.sheet_names]
# # # #         df_bops = pd.concat(sheets, ignore_index=True).dropna(subset=['DATE'])
# # # #         df_bops['Timestamp'] = pd.to_datetime(df_bops['DATE'], errors='coerce')
        
# # # #         # Standardize columns based on requested KPIs
# # # #         rename_map = {
# # # #             'SHIFT': 'Shift', 'HEAT NO': 'Heat Number', 'SEQ NO': 'Sequence Number',
# # # #             'GRADE': 'Grade', 'ACTUAL CASTING SPEED (m/min)': 'Casting Speed', 
# # # #             'DISCHARGE (MT)': 'Production', 'TUNDISH TEMPERATURE': 'Tundish Temp',
# # # #             'LIFTING TEMPERATURE': 'Lifting Temp', 'CASTING TIME': 'Casting Time'
# # # #         }
# # # #         df_bops = df_bops.rename(columns=lambda x: rename_map.get(x.strip().upper(), x) if isinstance(x, str) else x)
        
# # # #         # Ensure numeric types
# # # #         numeric_cols = ['Casting Speed', 'Production', 'Tundish Temp', 'Lifting Temp', 'Casting Time']
# # # #         for col in numeric_cols:
# # # #             if col not in df_bops.columns: df_bops[col] = 0.0
# # # #             df_bops[col] = pd.to_numeric(df_bops[col], errors='coerce').fillna(0)
# # # #     except Exception as e:
# # # #         st.error(f"Error reading BOPS: {e}")

# # # #     # 3. Load Delays
# # # #     df_delays = pd.DataFrame()
# # # #     delay_list = []
# # # #     for f in [csp_delay, elec_delay]:
# # # #         if f:
# # # #             try:
# # # #                 xls = pd.ExcelFile(f)
# # # #                 for sheet in xls.sheet_names:
# # # #                     temp_df = pd.read_excel(f, sheet_name=sheet)
# # # #                     if 'Date' in temp_df.columns and 'Delay (mins)' in temp_df.columns:
# # # #                         temp_df['Agency'] = temp_df.get('Agency', 'Unknown')
# # # #                         temp_df['Reason'] = temp_df.get('Reason', 'Unknown')
# # # #                         temp_df['Type'] = 'Electrical' if 'elect' in str(f).lower() else temp_df.get('Type', 'Mechanical/Process')
# # # #                         delay_list.append(temp_df[['Date', 'Delay (mins)', 'Agency', 'Reason', 'Type']])
# # # #             except Exception:
# # # #                 pass
            
# # # #     if delay_list:
# # # #         df_delays = pd.concat(delay_list, ignore_index=True)
# # # #         df_delays['Date'] = pd.to_datetime(df_delays['Date'], errors='coerce')
# # # #         df_delays['Delay (mins)'] = pd.to_numeric(df_delays['Delay (mins)'], errors='coerce').fillna(0)

# # # #     # 4. Load Grid Gap & Placeholders
# # # #     df_grid = pd.read_excel(grid_file, sheet_name=0) if grid_file else pd.DataFrame()
# # # #     df_chem = pd.read_excel(chem_file, sheet_name=0) if chem_file else pd.DataFrame(columns=['Date', 'Heat Number', 'C', 'Mn', 'Si', 'P', 'S', 'Cr', 'Ni', 'Mo'])
# # # #     df_pm = pd.read_excel(pm_file, sheet_name=0) if pm_file else pd.DataFrame(columns=['Date', 'PM Order', 'Status'])
# # # #     df_rca = pd.DataFrame(columns=['Date', 'Root Cause Count']) # Placeholder if separate RCA file exists

# # # #     return {
# # # #         "main": df_bops.sort_values('Timestamp').reset_index(drop=True) if not df_bops.empty else df_bops,
# # # #         "delays": df_delays,
# # # #         "grid": df_grid,
# # # #         "pm": df_pm,
# # # #         "chem": df_chem,
# # # #         "rca": df_rca
# # # #     }
# # # import pandas as pd
# # # import numpy as np
# # # from pathlib import Path
# # # import streamlit as st

# # # @st.cache_data(show_spinner=False)
# # # def load_all_data():
# # #     current_dir = Path.cwd()
# # #     possible_dirs = [current_dir / "data", current_dir, Path(__file__).resolve().parents[1] / "data", Path(__file__).resolve().parents[1]]
    
# # #     def find_file(pattern, dirs):
# # #         for d in dirs:
# # #             if d.exists() and d.is_dir():
# # #                 matches = list(d.glob(pattern))
# # #                 if matches: return matches[0]
# # #         return None

# # #     # Locate files
# # #     bops_file = find_file("BOPS*Alarm*.xlsx", possible_dirs)
# # #     csp_delay = find_file("CSP DELAY*.xlsx", possible_dirs)
# # #     elec_delay = find_file("Electrical Delay*.xlsx", possible_dirs)
# # #     grid_file = find_file("Grid Gap*.xlsx", possible_dirs)
# # #     chem_file = find_file("*Chem*.xlsx", possible_dirs)
# # #     pm_file = find_file("*PM*.xlsx", possible_dirs)

# # #     if not bops_file:
# # #         st.error("❌ Could not find BOPS Alarm file. Please ensure it is in the data folder.")
# # #         return {k: pd.DataFrame() for k in ["main", "delays", "grid", "pm", "chem", "rca"]}

# # #     # --- 1. Load BOPS (Production) ---
# # #     df_bops = pd.DataFrame()
# # #     try:
# # #         xls = pd.ExcelFile(bops_file)
# # #         sheets = [pd.read_excel(bops_file, sheet_name=s) for s in xls.sheet_names]
# # #         df_bops = pd.concat(sheets, ignore_index=True).dropna(subset=['DATE'])
# # #         df_bops['Timestamp'] = pd.to_datetime(df_bops['DATE'], errors='coerce')
        
# # #         # FUZZY COLUMN MATCHER - Finds the column even if there are spaces or name changes
# # #         def get_col(keyword):
# # #             for col in df_bops.columns:
# # #                 if keyword.upper() in str(col).upper():
# # #                     return col
# # #             return None

# # #         rename_map = {}
# # #         if get_col('SHIFT'): rename_map[get_col('SHIFT')] = 'Shift'
# # #         if get_col('HEAT'): rename_map[get_col('HEAT')] = 'Heat Number'
# # #         if get_col('SEQ'): rename_map[get_col('SEQ')] = 'Sequence Number'
# # #         if get_col('SPEED'): rename_map[get_col('SPEED')] = 'Casting Speed'
# # #         if get_col('DISCHARGE'): rename_map[get_col('DISCHARGE')] = 'Production'
# # #         if get_col('TUNDISH'): rename_map[get_col('TUNDISH')] = 'Tundish Temp'
# # #         if get_col('LIFTING'): rename_map[get_col('LIFTING')] = 'Lifting Temp'
# # #         if get_col('CASTING TIME'): rename_map[get_col('CASTING TIME')] = 'Casting Time'

# # #         df_bops = df_bops.rename(columns=rename_map)
        
# # #         # Clean Shift Column (fixes "botha", spaces, and NaN issues)
# # #         if 'Shift' in df_bops.columns:
# # #             df_bops['Shift'] = df_bops['Shift'].astype(str).str.strip().str.upper()
# # #             df_bops['Shift'] = df_bops['Shift'].replace(['NAN', 'NONE', ''], np.nan)

# # #         # Force Numeric Types safely
# # #         numeric_cols = ['Casting Speed', 'Production', 'Tundish Temp', 'Lifting Temp', 'Casting Time']
# # #         for col in numeric_cols:
# # #             if col not in df_bops.columns: 
# # #                 df_bops[col] = 0.0
# # #             else:
# # #                 # Convert anything that isn't a number to NaN, then fill with 0
# # #                 df_bops[col] = pd.to_numeric(df_bops[col], errors='coerce').fillna(0)

# # #     except Exception as e:
# # #         st.error(f"Error reading BOPS: {e}")

# # #     # --- 2. Load Delays ---
# # #     df_delays = pd.DataFrame()
# # #     delay_list = []
# # #     for f in [csp_delay, elec_delay]:
# # #         if f:
# # #             try:
# # #                 xls = pd.ExcelFile(f)
# # #                 for sheet in xls.sheet_names:
# # #                     temp_df = pd.read_excel(f, sheet_name=sheet)
                    
# # #                     # Fuzzy match Delay columns
# # #                     delay_col = None
# # #                     for col in temp_df.columns:
# # #                         if 'DELAY' in str(col).upper() and 'MIN' in str(col).upper():
# # #                             delay_col = col
# # #                             break
                    
# # #                     if 'Date' in temp_df.columns and delay_col:
# # #                         temp_df = temp_df.rename(columns={delay_col: 'Delay (mins)'})
# # #                         temp_df['Agency'] = temp_df.get('Agency', 'Unknown')
# # #                         temp_df['Reason'] = temp_df.get('Reason', 'Unknown')
# # #                         temp_df['Type'] = 'Electrical' if 'elect' in str(f).lower() else temp_df.get('Type', 'Mechanical/Process')
# # #                         delay_list.append(temp_df[['Date', 'Delay (mins)', 'Agency', 'Reason', 'Type']])
# # #             except Exception:
# # #                 pass
            
# # #     if delay_list:
# # #         df_delays = pd.concat(delay_list, ignore_index=True)
# # #         df_delays['Date'] = pd.to_datetime(df_delays['Date'], errors='coerce')
# # #         df_delays['Delay (mins)'] = pd.to_numeric(df_delays['Delay (mins)'], errors='coerce').fillna(0)
# # #         # CRITICAL FIX: Drop duplicates to prevent massive 194k minute inflation
# # #         df_delays = df_delays.drop_duplicates(subset=['Date', 'Delay (mins)', 'Reason', 'Agency'])

# # #     # --- 3. Load Grids & Placeholders ---
# # #     df_grid = pd.read_excel(grid_file, sheet_name=0) if grid_file else pd.DataFrame()
# # #     df_chem = pd.read_excel(chem_file, sheet_name=0) if chem_file else pd.DataFrame(columns=['Date', 'Heat Number', 'C', 'Mn', 'Si', 'P', 'S', 'Cr', 'Ni', 'Mo'])
# # #     df_pm = pd.read_excel(pm_file, sheet_name=0) if pm_file else pd.DataFrame(columns=['Date', 'PM Order', 'Status'])
# # #     df_rca = pd.DataFrame(columns=['Date', 'Root Cause Count'])

# # #     return {
# # #         "main": df_bops.sort_values('Timestamp').reset_index(drop=True) if not df_bops.empty else df_bops,
# # #         "delays": df_delays,
# # #         "grid": df_grid,
# # #         "pm": df_pm,
# # #         "chem": df_chem,
# # #         "rca": df_rca
# # #     }
# # # import pandas as pd
# # # import numpy as np
# # # from pathlib import Path
# # # import streamlit as st
# # # import datetime

# # # @st.cache_data(show_spinner=False)
# # # def load_all_data():
# # #     current_dir = Path.cwd()
# # #     possible_dirs = [current_dir / "data", current_dir, Path(__file__).resolve().parents[1] / "data", Path(__file__).resolve().parents[1]]
    
# # #     def find_file(pattern, dirs):
# # #         for d in dirs:
# # #             if d.exists() and d.is_dir():
# # #                 matches = list(d.glob(pattern))
# # #                 if matches: return matches[0]
# # #         return None

# # #     # Locate files based on your provided naming conventions
# # #     bops_file = find_file("*BOPS*.xlsx", possible_dirs) or find_file("*log*sheet*.xlsx", possible_dirs)
# # #     csp_delay = find_file("*CSP DELAY*.xlsx", possible_dirs)
# # #     elec_delay = find_file("*Electrical Delay*.xlsx", possible_dirs)
# # #     chem_file = find_file("*Chemistry*.xlsx", possible_dirs)
# # #     pm_file = find_file("*PM*.xlsx", possible_dirs)
# # #     target_file = find_file("*MBP*.xlsx", possible_dirs) or find_file("*target*.xlsx", possible_dirs)
# # #     rca_file = find_file("*RCA*.xlsx", possible_dirs)

# # #     if not bops_file:
# # #         st.error("❌ Could not find BOPS/Log Sheet file. Please ensure files are in the /data folder.")
# # #         return {k: pd.DataFrame() for k in ["main", "delays", "targets", "pm", "chem", "rca"]}

# # #     # --- 1. Load BOPS / Log Sheet (Production) ---
# # #     df_bops = pd.DataFrame()
# # #     try:
# # #         xls = pd.ExcelFile(bops_file)
# # #         sheets = [pd.read_excel(bops_file, sheet_name=s, skiprows=0) for s in xls.sheet_names]
# # #         df_bops = pd.concat(sheets, ignore_index=True)
        
# # #         # Locate the Date column safely
# # #         date_col = next((c for c in df_bops.columns if 'DATE' in str(c).upper()), None)
# # #         if date_col:
# # #             df_bops = df_bops.dropna(subset=[date_col])
# # #             df_bops['Timestamp'] = pd.to_datetime(df_bops[date_col], errors='coerce')

# # #         # EXACT MATCHING based on your uploaded images
# # #         def get_col(keyword):
# # #             for col in df_bops.columns:
# # #                 if keyword.upper() in str(col).upper(): return col
# # #             return None

# # #         rename_map = {}
# # #         if get_col('SHIFT'): rename_map[get_col('SHIFT')] = 'Shift'
# # #         if get_col('HEAT NO'): rename_map[get_col('HEAT NO')] = 'Heat Number'
# # #         if get_col('SEQUENCE'): rename_map[get_col('SEQUENCE')] = 'Sequence Number'
# # #         if get_col('SPEED'): rename_map[get_col('SPEED')] = 'Casting Speed'
# # #         if get_col('DISCHARGE'): rename_map[get_col('DISCHARGE')] = 'Production'
# # #         if get_col('LIFTING TEMP'): rename_map[get_col('LIFTING TEMP')] = 'Lifting Temp'
# # #         if get_col('AVG. TEMP'): rename_map[get_col('AVG. TEMP')] = 'Tundish Temp'
# # #         if get_col('CASTING TIME'): rename_map[get_col('CASTING TIME')] = 'Casting Time'

# # #         df_bops = df_bops.rename(columns=rename_map)
        
# # #         # Clean Shift Column (fixes "botha", spaces, NaN)
# # #         if 'Shift' in df_bops.columns:
# # #             df_bops['Shift'] = df_bops['Shift'].astype(str).str.strip().str.upper()
# # #             df_bops['Shift'] = df_bops['Shift'].replace(['NAN', 'NONE', ''], np.nan)

# # #         # Force Numeric Types safely
# # #         for col in ['Casting Speed', 'Production', 'Tundish Temp', 'Lifting Temp', 'Casting Time']:
# # #             if col in df_bops.columns:
# # #                 df_bops[col] = pd.to_numeric(df_bops[col], errors='coerce').fillna(0)
# # #             else:
# # #                 df_bops[col] = 0.0

# # #     except Exception as e:
# # #         st.error(f"Error reading BOPS: {e}")

# # #     # --- 2. Load Delays (CSP & Electrical) ---
# # #     df_delays = pd.DataFrame()
# # #     delay_list = []
# # #     for f in [csp_delay, elec_delay]:
# # #         if f:
# # #             try:
# # #                 xls = pd.ExcelFile(f)
# # #                 for sheet in xls.sheet_names:
# # #                     temp_df = pd.read_excel(f, sheet_name=sheet)
# # #                     delay_col = next((c for c in temp_df.columns if 'DELAY' in str(c).upper() and 'MIN' in str(c).upper()), None)
# # #                     date_col = next((c for c in temp_df.columns if 'DATE' in str(c).upper()), None)
                    
# # #                     if date_col and delay_col:
# # #                         temp_df = temp_df.rename(columns={delay_col: 'Delay (mins)', date_col: 'Date'})
# # #                         temp_df['Agency'] = temp_df.get('Agency', 'Unknown')
# # #                         temp_df['Reason'] = temp_df.get('Reason', 'Unknown')
# # #                         temp_df['Type'] = 'Electrical' if 'elect' in str(f).lower() else temp_df.get('Type', 'Mechanical/Process')
# # #                         delay_list.append(temp_df[['Date', 'Delay (mins)', 'Agency', 'Reason', 'Type']])
# # #             except Exception:
# # #                 pass
            
# # #     if delay_list:
# # #         df_delays = pd.concat(delay_list, ignore_index=True)
# # #         df_delays['Date'] = pd.to_datetime(df_delays['Date'], errors='coerce')
# # #         df_delays['Delay (mins)'] = pd.to_numeric(df_delays['Delay (mins)'], errors='coerce').fillna(0)
# # #         df_delays = df_delays.drop_duplicates(subset=['Date', 'Delay (mins)', 'Reason', 'Agency'])

# # #     # --- 3. Load Targets, Chemistry, PM, RCA ---
# # #     df_targets = pd.read_excel(target_file) if target_file else pd.DataFrame(columns=['MONTH', 'TARGET', 'ACTUAL'])
# # #     df_chem = pd.read_excel(chem_file) if chem_file else pd.DataFrame()
# # #     df_pm = pd.read_excel(pm_file) if pm_file else pd.DataFrame()
# # #     df_rca = pd.read_excel(rca_file) if rca_file else pd.DataFrame()

# # #     return {
# # #         "main": df_bops.sort_values('Timestamp').reset_index(drop=True) if not df_bops.empty else df_bops,
# # #         "delays": df_delays,
# # #         "targets": df_targets,
# # #         "pm": df_pm,
# # #         "chem": df_chem,
# # #         "rca": df_rca
# # #     }

# # import pandas as pd
# # import numpy as np
# # from pathlib import Path
# # import streamlit as st
# # import datetime

# # @st.cache_data(show_spinner=False)
# # def load_all_data():
# #     current_dir = Path.cwd()
# #     possible_dirs = [current_dir / "data", current_dir, Path(__file__).resolve().parents[1] / "data", Path(__file__).resolve().parents[1]]
    
# #     def find_file(pattern, dirs):
# #         for d in dirs:
# #             if d.exists() and d.is_dir():
# #                 matches = list(d.glob(pattern))
# #                 if matches: return matches[0]
# #         return None

# #     # Locate files based on your provided naming conventions
# #     bops_file = find_file("*BOPS*.xlsx", possible_dirs) or find_file("*log*sheet*.xlsx", possible_dirs)
# #     csp_delay = find_file("*CSP DELAY*.xlsx", possible_dirs)
# #     elec_delay = find_file("*Electrical Delay*.xlsx", possible_dirs)
# #     chem_file = find_file("*Chemistry*.xlsx", possible_dirs)
# #     # pm_file = find_file("*PM*.xlsx", possible_dirs)
# #     pm_file = find_file("*PM*.xlsx", possible_dirs) or find_file("*PM*.XLSX", possible_dirs)
# #     target_file = find_file("*MBP*.xlsx", possible_dirs) or find_file("*target*.xlsx", possible_dirs)
# #     rca_file = find_file("*RCA*.xlsx", possible_dirs)
# #     # Added search for Grid Gap file
# #     grid_file = find_file("*Grid*.xlsx", possible_dirs) or find_file("*Gap*.xlsx", possible_dirs)

# #     if not bops_file:
# #         st.error("❌ Could not find BOPS/Log Sheet file. Please ensure files are in the /data folder.")
# #         return {k: pd.DataFrame() for k in ["main", "delays", "targets", "pm", "chem", "rca", "grid"]}

# #     # --- 1. Load BOPS / Log Sheet (Production) ---
# #     df_bops = pd.DataFrame()
# #     try:
# #         xls = pd.ExcelFile(bops_file)
# #         sheets = [pd.read_excel(bops_file, sheet_name=s, skiprows=0) for s in xls.sheet_names]
# #         df_bops = pd.concat(sheets, ignore_index=True)
        
# #         # Locate the Date column safely
# #         date_col = next((c for c in df_bops.columns if 'DATE' in str(c).upper()), None)
# #         if date_col:
# #             df_bops = df_bops.dropna(subset=[date_col])
# #             df_bops['Timestamp'] = pd.to_datetime(df_bops[date_col], errors='coerce')

# #         # EXACT MATCHING based on your uploaded images
# #         def get_col(keyword):
# #             for col in df_bops.columns:
# #                 if keyword.upper() in str(col).upper(): return col
# #             return None

# #         rename_map = {}
# #         if get_col('SHIFT'): rename_map[get_col('SHIFT')] = 'Shift'
# #         if get_col('HEAT NO'): rename_map[get_col('HEAT NO')] = 'Heat Number'
# #         if get_col('SEQUENCE'): rename_map[get_col('SEQUENCE')] = 'Sequence Number'
# #         if get_col('SPEED'): rename_map[get_col('SPEED')] = 'Casting Speed'
# #         if get_col('DISCHARGE'): rename_map[get_col('DISCHARGE')] = 'Production'
# #         if get_col('LIFTING TEMP'): rename_map[get_col('LIFTING TEMP')] = 'Lifting Temp'
# #         if get_col('AVG. TEMP'): rename_map[get_col('AVG. TEMP')] = 'Tundish Temp'
# #         if get_col('CASTING TIME'): rename_map[get_col('CASTING TIME')] = 'Casting Time'

# #         df_bops = df_bops.rename(columns=rename_map)
        
# #         # Clean Shift Column (fixes "botha", spaces, NaN)
# #         if 'Shift' in df_bops.columns:
# #             df_bops['Shift'] = df_bops['Shift'].astype(str).str.strip().str.upper()
# #             df_bops['Shift'] = df_bops['Shift'].replace(['NAN', 'NONE', ''], np.nan)

# #         # Force Numeric Types safely
# #         for col in ['Casting Speed', 'Production', 'Tundish Temp', 'Lifting Temp', 'Casting Time']:
# #             if col in df_bops.columns:
# #                 df_bops[col] = pd.to_numeric(df_bops[col], errors='coerce').fillna(0)
# #             else:
# #                 df_bops[col] = 0.0

# #     except Exception as e:
# #         st.error(f"Error reading BOPS: {e}")

# #     # --- 2. Load Delays (CSP & Electrical) ---
# #     df_delays = pd.DataFrame()
# #     delay_list = []
# #     for f in [csp_delay, elec_delay]:
# #         if f:
# #             try:
# #                 xls = pd.ExcelFile(f)
# #                 for sheet in xls.sheet_names:
# #                     temp_df = pd.read_excel(f, sheet_name=sheet)
# #                     delay_col = next((c for c in temp_df.columns if 'DELAY' in str(c).upper() and 'MIN' in str(c).upper()), None)
# #                     date_col = next((c for c in temp_df.columns if 'DATE' in str(c).upper()), None)
                    
# #                     if date_col and delay_col:
# #                         temp_df = temp_df.rename(columns={delay_col: 'Delay (mins)', date_col: 'Date'})
# #                         temp_df['Agency'] = temp_df.get('Agency', 'Unknown')
# #                         temp_df['Reason'] = temp_df.get('Reason', 'Unknown')
# #                         temp_df['Type'] = 'Electrical' if 'elect' in str(f).lower() else temp_df.get('Type', 'Mechanical/Process')
# #                         delay_list.append(temp_df[['Date', 'Delay (mins)', 'Agency', 'Reason', 'Type']])
# #             except Exception:
# #                 pass
            
# #     if delay_list:
# #         df_delays = pd.concat(delay_list, ignore_index=True)
# #         df_delays['Date'] = pd.to_datetime(df_delays['Date'], errors='coerce')
# #         df_delays['Delay (mins)'] = pd.to_numeric(df_delays['Delay (mins)'], errors='coerce').fillna(0)
# #         df_delays = df_delays.drop_duplicates(subset=['Date', 'Delay (mins)', 'Reason', 'Agency'])

# #     # --- 3. Load Targets, Chemistry, PM, RCA, Grid ---
# #     df_targets = pd.read_excel(target_file) if target_file else pd.DataFrame(columns=['MONTH', 'TARGET', 'ACTUAL'])
# #     df_chem = pd.read_excel(chem_file) if chem_file else pd.DataFrame()
# #     df_pm = pd.read_excel(pm_file) if pm_file else pd.DataFrame()
# #     df_rca = pd.read_excel(rca_file) if rca_file else pd.DataFrame()
# #     df_grid = pd.read_excel(grid_file) if grid_file else pd.DataFrame()

# #     return {
# #         "main": df_bops.sort_values('Timestamp').reset_index(drop=True) if not df_bops.empty else df_bops,
# #         "delays": df_delays,
# #         "targets": df_targets,
# #         "pm": df_pm,
# #         "chem": df_chem,
# #         "rca": df_rca,
# #         "grid": df_grid # Added grid key to return dictionary
# #     }

# import pandas as pd
# import numpy as np
# from pathlib import Path
# import streamlit as st
# import datetime

# @st.cache_data(show_spinner=False)
# def load_all_data():
#     current_dir = Path.cwd()
#     possible_dirs = [current_dir / "data", current_dir, Path(__file__).resolve().parents[1] / "data", Path(__file__).resolve().parents[1]]
    
#     def find_file(pattern, dirs):
#         for d in dirs:
#             if d.exists() and d.is_dir():
#                 matches = list(d.glob(pattern))
#                 if matches: return matches[0]
#         return None

#     # Locate files based on your provided naming conventions
#     bops_file = find_file("*BOPS*.xlsx", possible_dirs) or find_file("*log*sheet*.xlsx", possible_dirs)
#     csp_delay = find_file("*CSP DELAY*.xlsx", possible_dirs)
#     elec_delay = find_file("*Electrical Delay*.xlsx", possible_dirs)
#     chem_file = find_file("*Chemistry*.xlsx", possible_dirs)
#     # PM and Target files with robust fallbacks
#     pm_file = find_file("*PM*.xlsx", possible_dirs) or find_file("*PM*.XLSX", possible_dirs)
#     target_file = find_file("*MBP*.xlsx", possible_dirs) or find_file("*target*.xlsx", possible_dirs)
#     rca_file = find_file("*RCA*.xlsx", possible_dirs)
#     grid_file = find_file("*Grid*.xlsx", possible_dirs) or find_file("*Gap*.xlsx", possible_dirs)

#     if not bops_file:
#         st.error("❌ Could not find BOPS/Log Sheet file. Please ensure files are in the /data folder.")
#         return {k: pd.DataFrame() for k in ["main", "delays", "targets", "pm", "chem", "rca", "grid"]}

#     # --- 1. Load BOPS / Log Sheet (Production) ---
#     df_bops = pd.DataFrame()
#     try:
#         xls = pd.ExcelFile(bops_file)
#         sheets = [pd.read_excel(bops_file, sheet_name=s, skiprows=0) for s in xls.sheet_names]
#         df_bops = pd.concat(sheets, ignore_index=True)
        
#         # EXACT MATCHING based on your uploaded images (Merged Header Fix)
#         def get_col(keyword):
#             # Check headers
#             for col in df_bops.columns:
#                 if keyword.upper() in str(col).upper(): return col
#             # Check first row for sub-headers
#             if not df_bops.empty:
#                 for col in df_bops.columns:
#                     if keyword.upper() in str(df_bops.iloc[0][col]).upper(): return col
#             return None

#         rename_map = {}
#         if get_col('SHIFT'): rename_map[get_col('SHIFT')] = 'Shift'
#         if get_col('HEAT NO'): rename_map[get_col('HEAT NO')] = 'Heat Number'
#         if get_col('SEQUENCE'): rename_map[get_col('SEQUENCE')] = 'Sequence Number'
#         if get_col('SPEED'): rename_map[get_col('SPEED')] = 'Casting Speed'
#         if get_col('DISCHARGE'): rename_map[get_col('DISCHARGE')] = 'Production'
#         if get_col('LIFTING TEMP'): rename_map[get_col('LIFTING TEMP')] = 'Lifting Temp'
#         if get_col('AVG. TEMP'): rename_map[get_col('AVG. TEMP')] = 'Tundish Temp'
#         if get_col('CASTING TIME'): rename_map[get_col('CASTING TIME')] = 'Casting Time'

#         df_bops = df_bops.rename(columns=rename_map)
        
#         # Clean up the leftover sub-header row safely BEFORE dropping NAs
#         if not df_bops.empty and 'Tundish Temp' in df_bops.columns:
#             if str(df_bops.iloc[0]['Tundish Temp']).upper() == 'AVG. TEMP':
#                 df_bops = df_bops.drop(0).reset_index(drop=True)

#         # Locate the Date column safely
#         date_col = next((c for c in df_bops.columns if 'DATE' in str(c).upper()), None)
#         if date_col:
#             df_bops = df_bops.dropna(subset=[date_col])
#             df_bops['Timestamp'] = pd.to_datetime(df_bops[date_col], errors='coerce')

#         # Clean Shift Column
#         if 'Shift' in df_bops.columns:
#             df_bops['Shift'] = df_bops['Shift'].astype(str).str.strip().str.upper()
#             df_bops['Shift'] = df_bops['Shift'].replace(['NAN', 'NONE', ''], np.nan)

#         # Force Numeric Types safely
#         for col in ['Casting Speed', 'Production', 'Tundish Temp', 'Lifting Temp', 'Casting Time']:
#             if col in df_bops.columns:
#                 df_bops[col] = pd.to_numeric(df_bops[col], errors='coerce').fillna(0)
#             else:
#                 df_bops[col] = 0.0

#     except Exception as e:
#         st.error(f"Error reading BOPS: {e}")

#     # --- 2. Load Delays (CSP & Electrical) ---
#     df_delays = pd.DataFrame()
#     delay_list = []
#     for f in [csp_delay, elec_delay]:
#         if f:
#             try:
#                 xls = pd.ExcelFile(f)
#                 for sheet in xls.sheet_names:
#                     temp_df = pd.read_excel(f, sheet_name=sheet)
#                     delay_col = next((c for c in temp_df.columns if 'DELAY' in str(c).upper() and 'MIN' in str(c).upper()), None)
#                     date_col = next((c for c in temp_df.columns if 'DATE' in str(c).upper()), None)
                    
#                     if date_col and delay_col:
#                         temp_df = temp_df.rename(columns={delay_col: 'Delay (mins)', date_col: 'Date'})
#                         temp_df['Agency'] = temp_df.get('Agency', 'Unknown')
#                         temp_df['Reason'] = temp_df.get('Reason', 'Unknown')
#                         temp_df['Type'] = 'Electrical' if 'elect' in str(f).lower() else temp_df.get('Type', 'Mechanical/Process')
#                         delay_list.append(temp_df[['Date', 'Delay (mins)', 'Agency', 'Reason', 'Type']])
#             except Exception:
#                 pass
            
#     if delay_list:
#         df_delays = pd.concat(delay_list, ignore_index=True)
#         df_delays['Date'] = pd.to_datetime(df_delays['Date'], errors='coerce')
#         df_delays['Delay (mins)'] = pd.to_numeric(df_delays['Delay (mins)'], errors='coerce').fillna(0)
#         df_delays = df_delays.drop_duplicates(subset=['Date', 'Delay (mins)', 'Reason', 'Agency'])

#     # --- 3. Load Targets, Chemistry, PM, RCA, Grid ---
    
#     # Target file loading with merged title row fix
#     df_targets = pd.DataFrame(columns=['MONTH', 'TARGET', 'ACTUAL'])
#     if target_file:
#         try:
#             temp_targets = pd.read_excel(target_file)
#             if not temp_targets.empty and 'MONTH' not in [str(c).upper() for c in temp_targets.columns]:
#                 first_row_vals = [str(x).upper() for x in temp_targets.iloc[0].values]
#                 if 'MONTH' in first_row_vals:
#                     temp_targets.columns = temp_targets.iloc[0]
#                     temp_targets = temp_targets[1:].reset_index(drop=True)
#             temp_targets.columns = [str(c).upper().strip() for c in temp_targets.columns]
#             df_targets = temp_targets
#         except Exception:
#             pass

#     df_chem = pd.read_excel(chem_file) if chem_file else pd.DataFrame()
#     df_pm = pd.read_excel(pm_file) if pm_file else pd.DataFrame()
#     df_rca = pd.read_excel(rca_file) if rca_file else pd.DataFrame()
#     df_grid = pd.read_excel(grid_file) if grid_file else pd.DataFrame()

#     return {
#         "main": df_bops.sort_values('Timestamp').reset_index(drop=True) if not df_bops.empty else df_bops,
#         "delays": df_delays,
#         "targets": df_targets,
#         "pm": df_pm,
#         "chem": df_chem,
#         "rca": df_rca,
#         "grid": df_grid 
#     }


import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st
import datetime

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

    # Locate files based on your provided naming conventions
    bops_file = find_file("*BOPS*.xlsx", possible_dirs) or find_file("*log*sheet*.xlsx", possible_dirs)
    csp_delay = find_file("*CSP DELAY*.xlsx", possible_dirs)
    elec_delay = find_file("*Electrical Delay*.xlsx", possible_dirs)
    chem_file = find_file("*Chemistry*.xlsx", possible_dirs)
    # PM and Target files with robust fallbacks
    pm_file = find_file("*PM*.xlsx", possible_dirs) or find_file("*PM*.XLSX", possible_dirs)
    target_file = find_file("*MBP*.xlsx", possible_dirs) or find_file("*target*.xlsx", possible_dirs)
    rca_file = find_file("*RCA*.xlsx", possible_dirs)
    grid_file = find_file("*Grid*.xlsx", possible_dirs) or find_file("*Gap*.xlsx", possible_dirs)

    if not bops_file:
        st.error("❌ Could not find BOPS/Log Sheet file. Please ensure files are in the /data folder.")
        return {k: pd.DataFrame() for k in ["main", "delays", "targets", "pm", "chem", "rca", "grid"]}

    # --- 1. Load BOPS / Log Sheet (Production) ---
    df_bops = pd.DataFrame()
    try:
        xls = pd.ExcelFile(bops_file)
        sheets = [pd.read_excel(bops_file, sheet_name=s, skiprows=0) for s in xls.sheet_names]
        df_bops = pd.concat(sheets, ignore_index=True)
        
        # EXACT MATCHING with Line-Break and Space removal
        def get_col(keyword):
            clean_key = keyword.upper().replace(" ", "")
            # Check headers
            for col in df_bops.columns:
                clean_col = str(col).upper().replace("\n", "").replace(" ", "")
                if clean_key in clean_col: return col
            # Check first row for sub-headers
            if not df_bops.empty:
                for col in df_bops.columns:
                    clean_cell = str(df_bops.iloc[0][col]).upper().replace("\n", "").replace(" ", "")
                    if clean_key in clean_cell: return col
            return None

        rename_map = {}
        if get_col('SHIFT'): rename_map[get_col('SHIFT')] = 'Shift'
        if get_col('HEAT NO'): rename_map[get_col('HEAT NO')] = 'Heat Number'
        if get_col('SEQUENCE'): rename_map[get_col('SEQUENCE')] = 'Sequence Number'
        if get_col('SPEED'): rename_map[get_col('SPEED')] = 'Casting Speed'
        if get_col('DISCHARGE'): rename_map[get_col('DISCHARGE')] = 'Production'
        if get_col('LIFTING TEMP'): rename_map[get_col('LIFTING TEMP')] = 'Lifting Temp'
        # if get_col('AVG. TEMP'): rename_map[get_col('AVG. TEMP')] = 'Tundish Temp'
        target_cols = [
    # ... other columns ...
    ('LIFTINGTEMP', 'Lifting Temp'),
    ('AVGTEMP', 'Tundish Temp')
]
        if get_col('CASTING TIME'): rename_map[get_col('CASTING TIME')] = 'Casting Time'

        df_bops = df_bops.rename(columns=rename_map)
        
        # Clean up the leftover sub-header row safely BEFORE dropping NAs
        # (Updated to also ignore spaces/newlines during cleanup)
        if not df_bops.empty and 'Tundish Temp' in df_bops.columns:
            cell_val = str(df_bops.iloc[0]['Tundish Temp']).upper().replace("\n", "").replace(" ", "")
            if cell_val == 'AVG.TEMP':
                df_bops = df_bops.drop(0).reset_index(drop=True)

        # Locate the Date column safely
        date_col = next((c for c in df_bops.columns if 'DATE' in str(c).upper()), None)
        if date_col:
            df_bops = df_bops.dropna(subset=[date_col])
            df_bops['Timestamp'] = pd.to_datetime(df_bops[date_col], errors='coerce')

        # Clean Shift Column
        if 'Shift' in df_bops.columns:
            df_bops['Shift'] = df_bops['Shift'].astype(str).str.strip().str.upper()
            df_bops['Shift'] = df_bops['Shift'].replace(['NAN', 'NONE', ''], np.nan)

        # Force Numeric Types safely
        for col in ['Casting Speed', 'Production', 'Tundish Temp', 'Lifting Temp', 'Casting Time']:
            if col in df_bops.columns:
                df_bops[col] = pd.to_numeric(df_bops[col], errors='coerce').fillna(0)
            else:
                df_bops[col] = 0.0

    except Exception as e:
        st.error(f"Error reading BOPS: {e}")

    # --- 2. Load Delays (CSP & Electrical) ---
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

    # --- 3. Load Targets, Chemistry, PM, RCA, Grid ---
    
    # Target file loading with merged title row fix
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

    df_chem = pd.read_excel(chem_file) if chem_file else pd.DataFrame()
    df_pm = pd.read_excel(pm_file) if pm_file else pd.DataFrame()
    df_rca = pd.read_excel(rca_file) if rca_file else pd.DataFrame()
    df_grid = pd.read_excel(grid_file) if grid_file else pd.DataFrame()

    return {
        "main": df_bops.sort_values('Timestamp').reset_index(drop=True) if not df_bops.empty else df_bops,
        "delays": df_delays,
        "targets": df_targets,
        "pm": df_pm,
        "chem": df_chem,
        "rca": df_rca,
        "grid": df_grid 
    }
