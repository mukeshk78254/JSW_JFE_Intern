from pathlib import Path

import numpy as np
import pandas as pd


def generate_dataset(path: str | None = None) -> Path:
    output_path = Path(path) if path else Path(__file__).resolve().parent / "caster_data.csv"
    rng = np.random.default_rng(42)

    start_time = pd.Timestamp("2026-01-01 06:00:00")
    timestamps = pd.date_range(start=start_time, periods=1200, freq="10min")

    shifts = []
    for ts in timestamps:
        hour = ts.hour
        if 6 <= hour < 14:
            shifts.append("Morning")
        elif 14 <= hour < 22:
            shifts.append("Evening")
        else:
            shifts.append("Night")

    speeds = 1.15 + np.sin(np.arange(len(timestamps)) / 18) * 0.12 + rng.normal(0, 0.03, len(timestamps))
    speeds = np.clip(speeds, 0.85, 1.75)

    mold_levels = 80 + np.sin(np.arange(len(timestamps)) / 12) * 1.5 + rng.normal(0, 0.4, len(timestamps))
    mold_levels = np.clip(mold_levels, 74, 86)

    production = np.clip(speeds * 12.5 + rng.normal(0, 0.7, len(timestamps)), 0, None)

    temperatures = 1515 + np.sin(np.arange(len(timestamps)) / 20) * 8 + rng.normal(0, 2.5, len(timestamps))
    water_flow = 1900 + np.sin(np.arange(len(timestamps)) / 15) * 40 + rng.normal(0, 8, len(timestamps))
    hydraulic_pressure = 120 + np.sin(np.arange(len(timestamps)) / 10) * 6 + rng.normal(0, 1.2, len(timestamps))

    downtime = np.zeros(len(timestamps), dtype=float)
    downtime_reason = []
    alarms = []
    severities = []
    statuses = []
    plc_status = []
    mold_status = []
    oscillation_status = []
    hydraulic_status = []
    water_cooling_status = []
    shear_status = []
    roller_table_status = []

    for i, ts in enumerate(timestamps):
        if rng.random() < 0.06:
            downtime[i] = float(rng.integers(5, 16))
            reason = rng.choice(["Mechanical", "Electrical", "Process"])
            downtime_reason.append(reason)
            alarm_name = rng.choice(["Mold Level Low", "Hydraulic Pressure Drop", "Water Flow Alarm", "Roller Jam"])
            severity_level = rng.choice(["Low", "Medium", "High", "Critical"])
            alarms.append(alarm_name)
            severities.append(severity_level)
        else:
            downtime_reason.append("None")
            alarms.append("No Alarm")
            severities.append("None")

        if downtime[i] > 0:
            statuses.append("Stopped")
        else:
            statuses.append("Running")

        health = rng.choice(["Healthy", "Warning", "Fault"], p=[0.88, 0.09, 0.03])
        plc_status.append(health)
        mold_status.append("Healthy" if rng.random() > 0.08 else "Warning")
        oscillation_status.append("Healthy" if rng.random() > 0.1 else "Warning")
        hydraulic_status.append("Healthy" if rng.random() > 0.07 else "Warning")
        water_cooling_status.append("Healthy" if rng.random() > 0.06 else "Warning")
        shear_status.append("Healthy" if rng.random() > 0.09 else "Warning")
        roller_table_status.append("Healthy" if rng.random() > 0.08 else "Warning")

    df = pd.DataFrame(
        {
            "Timestamp": timestamps,
            "Shift": shifts,
            "Heat Number": rng.integers(10001, 11001, size=len(timestamps)),
            "Casting Speed": speeds,
            "Mold Level": mold_levels,
            "Downtime": downtime,
            "Production": production,
            "Temperature": temperatures,
            "Water Flow": water_flow,
            "Hydraulic Pressure": hydraulic_pressure,
            "Alarm": alarms,
            "Alarm Severity": severities,
            "Downtime Category": downtime_reason,
            "Machine Status": statuses,
            "PLC_Status": plc_status,
            "Mold_Status": mold_status,
            "Oscillation_Status": oscillation_status,
            "Hydraulic_Status": hydraulic_status,
            "Water_Cooling_Status": water_cooling_status,
            "Shear_Status": shear_status,
            "Roller_Table_Status": roller_table_status,
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    generate_dataset()
