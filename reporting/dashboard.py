import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def build_dashboard(df: pd.DataFrame, metrics: dict, output_path: str) -> None:
    fig = make_subplots(rows=2, cols=2,
        subplot_titles=["Price + SMAs", "Daily returns", "Rolling volatility", "Metrics"])

    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], name="Close", line=dict(width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["Date"], y=df["sma_50"], name="SMA 50", line=dict(dash="dash")), row=1, col=1)

    fig.add_trace(go.Bar(x=df["Date"], y=df["daily_return"], name="Daily return",
                         marker_color=df["daily_return"].apply(lambda x: "#1D9E75" if x >= 0 else "#E24B4A")), row=1, col=2)

    fig.add_trace(go.Scatter(x=df["Date"], y=df["rolling_vol_20d"], name="20d vol",
                              fill="tozeroy", line=dict(color="#534AB7", width=1)), row=2, col=1)

    # Metrics summary as a table
    fig.add_trace(go.Table(
        header=dict(values=["Metric", "Value"]),
        cells=dict(values=[list(metrics.keys()), [round(v, 4) for v in metrics.values()]])
    ), row=2, col=2)

    fig.update_layout(height=700, title_text=f"FinSight Dashboard — {df['Ticker'].iloc[0]}", showlegend=False)
    fig.write_html(output_path)