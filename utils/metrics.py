def compute_metrics(df):
    if df.empty:
        return {
            "avg_speed": 0.0,
            "max_speed": 0.0,
            "min_speed": 0.0,
            "mold_level_stability": 0.0,
            "availability": 0.0,
            "productivity": 0.0,
            "oee": 0.0,
            "yield_pct": 0.0,
        }

    runtime_minutes = max(len(df) * 10, 1)
    total_downtime = df["Downtime"].sum()
    availability = max(0.0, 100.0 * (1 - total_downtime / runtime_minutes))

    avg_speed = df["Casting Speed"].mean()
    max_speed = df["Casting Speed"].max()
    min_speed = df["Casting Speed"].min()
    mold_level_stability = max(0.0, 100.0 - (df["Mold Level"].std() * 12.5))

    productivity = df["Production"].sum() / (runtime_minutes / 60.0)
    target_speed = 1.6
    target_output_per_hour = 220.0

    performance = min(100.0, (avg_speed / target_speed) * 100.0)
    quality = min(100.0, max(0.0, 100.0 - (total_downtime / runtime_minutes) * 100.0))
    oee = availability * (performance / 100.0) * (quality / 100.0) * 100.0
    yield_pct = min(100.0, (df["Production"].sum() / ((runtime_minutes / 60.0) * target_output_per_hour)) * 100.0)

    return {
        "avg_speed": avg_speed,
        "max_speed": max_speed,
        "min_speed": min_speed,
        "mold_level_stability": mold_level_stability,
        "availability": availability,
        "productivity": productivity,
        "oee": oee,
        "yield_pct": yield_pct,
    }
