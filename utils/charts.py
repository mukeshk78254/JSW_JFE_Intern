# import plotly.express as px
# import plotly.graph_objects as go


# def create_gauge(value, title, reference):
#     fig = go.Figure(
#         go.Indicator(
#             mode="gauge+number+delta",
#             value=value,
#             title={"text": title},
#             delta={"reference": reference, "suffix": "%"},
#             gauge={
#                 "axis": {"range": [0, 100]},
#                 "bar": {"color": "#00d4ff"},
#                 "steps": [
#                     {"range": [0, 60], "color": "#440000"},
#                     {"range": [60, 85], "color": "#444400"},
#                     {"range": [85, 100], "color": "#004400"},
#                 ],
#                 "threshold": {
#                     "line": {"color": "red", "width": 4},
#                     "thickness": 0.75,
#                     "value": reference,
#                 },
#             },
#         )
#     )

#     fig.update_layout(
#         template="plotly_dark",
#         margin=dict(l=10, r=10, t=30, b=10),
#         height=220,
#     )

#     return fig


# def create_pareto(df, group_col="Reason"):
#     if df.empty:
#         return go.Figure()

#     if group_col not in df.columns:
#         return go.Figure()

#     delay_col = None

#     for c in df.columns:
#         if "Delay" in str(c):
#             delay_col = c
#             break

#     if delay_col is None:
#         return go.Figure()

#     summary = (
#         df.groupby(group_col)[delay_col]
#         .sum()
#         .sort_values(ascending=False)
#         .reset_index()
#     )

#     summary["Cumulative"] = (
#         summary[delay_col].cumsum()
#         / summary[delay_col].sum()
#         * 100
#     )

#     fig = go.Figure()

#     fig.add_bar(
#         x=summary[group_col],
#         y=summary[delay_col],
#         name="Downtime",
#     )

#     fig.add_scatter(
#         x=summary[group_col],
#         y=summary["Cumulative"],
#         mode="lines+markers",
#         yaxis="y2",
#         name="Cumulative %",
#     )

#     fig.update_layout(
#         template="plotly_dark",
#         title=f"Pareto - {group_col}",
#         yaxis=dict(title="Minutes"),
#         yaxis2=dict(
#             overlaying="y",
#             side="right",
#             range=[0, 100],
#             title="Cumulative %",
#         ),
#     )

#     return fig


# def create_target_chart(df):

#     if df is None or df.empty:
#         fig = go.Figure()
#         fig.add_annotation(
#             text="No Target Data Found",
#             showarrow=False,
#             font=dict(size=18),
#         )
#         return fig

#     plot_df = df.copy()

#     # Remove completely empty columns
#     plot_df = plot_df.dropna(axis=1, how="all")

#     # Fix Excel header if first row contains column names
#     if "Unnamed: 0" in plot_df.columns:
#         plot_df.columns = plot_df.iloc[0]
#         plot_df = plot_df.iloc[1:]

#     plot_df.columns = [str(c).strip() for c in plot_df.columns]

#     if len(plot_df.columns) < 3:
#         fig = go.Figure()
#         fig.add_annotation(
#             text="Target file must contain at least 3 columns",
#             showarrow=False,
#             font=dict(size=18),
#         )
#         return fig

#     x_col = plot_df.columns[0]
#     y1 = plot_df.columns[1]
#     y2 = plot_df.columns[2]

#     fig = px.bar(
#         plot_df,
#         x=x_col,
#         y=[y1, y2],
#         barmode="group",
#         title="Target vs Actual Production",
#     )

#     fig.update_layout(
#         template="plotly_dark",
#         xaxis_title=x_col,
#         yaxis_title="Production",
#     )

#     return fig


import plotly.express as px
import plotly.graph_objects as go

def create_gauge(value, title, reference):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            title={"text": title},
            delta={"reference": reference, "suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00d4ff"},
                "steps": [
                    {"range": [0, 60], "color": "#440000"},
                    {"range": [60, 85], "color": "#444400"},
                    {"range": [85, 100], "color": "#004400"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": reference,
                },
            },
        )
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=10, r=10, t=30, b=10),
        height=220,
    )

    return fig


def create_pareto(df, group_col="Reason"):
    if df.empty:
        return go.Figure()

    if group_col not in df.columns:
        return go.Figure()

    delay_col = None

    for c in df.columns:
        if "Delay" in str(c):
            delay_col = c
            break

    if delay_col is None:
        return go.Figure()

    summary = (
        df.groupby(group_col)[delay_col]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    summary["Cumulative"] = (
        summary[delay_col].cumsum()
        / summary[delay_col].sum()
        * 100
    )

    fig = go.Figure()

    fig.add_bar(
        x=summary[group_col],
        y=summary[delay_col],
        name="Downtime",
    )

    fig.add_scatter(
        x=summary[group_col],
        y=summary["Cumulative"],
        mode="lines+markers",
        yaxis="y2",
        name="Cumulative %",
    )

    fig.update_layout(
        template="plotly_dark",
        title=f"Pareto - {group_col}",
        yaxis=dict(title="Minutes"),
        yaxis2=dict(
            overlaying="y",
            side="right",
            range=[0, 100],
            title="Cumulative %",
        ),
    )

    return fig


def create_target_chart(df):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No Target Data Found",
            showarrow=False,
            font=dict(size=18),
        )
        return fig

    plot_df = df.copy()

    # Remove completely empty columns
    plot_df = plot_df.dropna(axis=1, how="all")

    # Fix Excel header if first row contains column names
    if "Unnamed: 0" in plot_df.columns:
        plot_df.columns = plot_df.iloc[0]
        plot_df = plot_df.iloc[1:]

    plot_df.columns = [str(c).strip() for c in plot_df.columns]

    if len(plot_df.columns) < 3:
        fig = go.Figure()
        fig.add_annotation(
            text="Target file must contain at least 3 columns",
            showarrow=False,
            font=dict(size=18),
        )
        return fig

    x_col = plot_df.columns[0]
    y1 = plot_df.columns[1]
    y2 = plot_df.columns[2]

    fig = px.bar(
        plot_df,
        x=x_col,
        y=[y1, y2],
        barmode="group",
        title="Target vs Actual Production",
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title=x_col,
        yaxis_title="Production",
    )

    return fig
