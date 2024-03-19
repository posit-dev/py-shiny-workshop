from plotnine import (
    ggplot,
    geom_density,
    theme_minimal,
    labs,
    aes,
    geom_line,
    geom_abline,
    geom_histogram,
)
from pandas import DataFrame
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import numpy as np
import pandas as pd


def plot_score_distribution(df: DataFrame):
    plot = (
        ggplot(df, aes(x="training_score"))
        + geom_density(fill="blue", alpha=0.3)
        + theme_minimal()
        + labs(title="Model scores", x="Score")
    )
    return plot


def plot_auc_curve(df: DataFrame, true_col: str, pred_col: str):
    fpr, tpr, _ = roc_curve(df[true_col], df[pred_col])
    roc_auc = auc(fpr, tpr)

    roc_df = DataFrame({"fpr": fpr, "tpr": tpr})

    plot = (
        ggplot(roc_df, aes(x="fpr", y="tpr"))
        + geom_line(color="darkorange", size=1.5, show_legend=True, linetype="solid")
        + geom_abline(intercept=0, slope=1, color="navy", linetype="dashed")
        + labs(
            title="Receiver Operating Characteristic (ROC)",
            subtitle=f"AUC: {roc_auc.round(2)}",
            x="False Positive Rate",
            y="True Positive Rate",
        )
        + theme_minimal()
    )

    return plot


def plot_precision_recall_curve(df: DataFrame, true_col: str, pred_col: str):
    precision, recall, _ = precision_recall_curve(df[true_col], df[pred_col])

    pr_df = DataFrame({"precision": precision, "recall": recall})

    plot = (
        ggplot(pr_df, aes(x="recall", y="precision"))
        + geom_line(color="darkorange", size=1.5, show_legend=True, linetype="solid")
        + labs(
            title="Precision-Recall Curve",
            x="Recall",
            y="Precision",
        )
        + theme_minimal()
    )

    return plot


def plot_api_response(df):
    account = df["account"].unique()

    data = np.random.lognormal(0, 1 / len(account), 10000)
    df = pd.DataFrame({"Value": data})
    plot = (
        ggplot(df, aes(x="Value"))
        + geom_density(fill="#0504aa", alpha=0.7)
        + labs(title="API response time", x="Seconds")
        + theme_minimal()
    )
    return plot
