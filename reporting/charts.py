import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

def plot_cumulative_returns(df: pd.DataFrame, ticker: str, output_dir: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["Date"], df["cumulative_return"] * 100, linewidth=1.5, color="#185FA5")
    ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    ax.set_title(f"{ticker} — Cumulative return (%)", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Return (%)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    fig.savefig(f"{output_dir}/{ticker}_cumulative_return.png", dpi=150)
    plt.close()

def plot_correlation_heatmap(corr_df: pd.DataFrame, output_dir: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, ax=ax, linewidths=0.5)
    ax.set_title("Return correlation matrix")
    fig.tight_layout()
    fig.savefig(f"{output_dir}/correlation_heatmap.png", dpi=150)
    plt.close()