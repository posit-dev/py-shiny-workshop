import plotly.express as px
from pandas import DataFrame
import pandas as pd
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import numpy as np

import plotly.io as pio

# Set the default plotly theme to resemble ggplot's theme_light
pio.templates.default = "plotly_white"


def plot_score_distribution(df: DataFrame):
    fig = px.histogram(df, x="training_score", nbins=50, title="Model scores")
    fig.update_layout(xaxis_title="Score", yaxis_title="Density")
    return fig


def plot_auc_curve(df: DataFrame, true_col: str, pred_col: str):
    fpr, tpr, _ = roc_curve(df[true_col], df[pred_col])
    roc_auc = auc(fpr, tpr)

    roc_df = DataFrame({"False Positive Rate": fpr, "True Positive Rate": tpr})

    fig = px.line(
        roc_df,
        x="False Positive Rate",
        y="True Positive Rate",
        title=f"Receiver Operating Characteristic (ROC) - AUC: {roc_auc.round(2)}",
        labels={
            "False Positive Rate": "False Positive Rate",
            "True Positive Rate": "True Positive Rate",
        },
    )
    fig.add_shape(type="line", line=dict(dash="dash"), x0=0, x1=1, y0=0, y1=1)
    return fig


def plot_precision_recall_curve(df: DataFrame, true_col: str, pred_col: str):
    precision, recall, _ = precision_recall_curve(df[true_col], df[pred_col])

    pr_df = DataFrame({"Recall": recall, "Precision": precision})

    fig = px.line(
        pr_df,
        x="Recall",
        y="Precision",
        title="Precision-Recall Curve",
        labels={"Recall": "Recall", "Precision": "Precision"},
    )
    return fig


def plot_api_response(df):
    account = df["account"].unique()

    data = np.random.lognormal(0, 1 / len(account), 10000)
    df = pd.DataFrame({"Value": data})
    fig = px.histogram(df, x="Value", nbins=50, title="API response time")
    fig.update_layout(xaxis_title="Seconds", yaxis_title="Density")
    return fig
