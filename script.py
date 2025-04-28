# script.py

from preswald import (
    connect, get_df, sidebar,
    text, separator,
    checkbox, table, plotly,
    progress
)
import plotly.express as px

connect()
df = get_df("gym_data")

sidebar(defaultopen=True)
text("## 📊 Show / Hide Sections")
show_table       = checkbox("Show Exercise Table", default=True)
show_eq_chart    = checkbox("Show Equipment Usage Chart", default=True)
show_bp_chart    = checkbox("Show Body Part Focus Chart", default=True)
show_insight     = checkbox("Show Avg Rating by Level (Bar)", default=True)
show_trend_chart = checkbox("Show Avg Rating Trend by Equipment", default=True)
separator()

text("# 🏋️ Gym Data Analysis")
separator()

text("## 📋 Data Overview")
text("### 🗒️ All Exercises (top 15)")
if show_table:
    table(
        df[["Title", "Type", "Equipment", "Level", "Rating"]],
        limit=200
    )
    separator()

if show_eq_chart:
    eq_counts = (
        df["Equipment"]
        .value_counts()
        .reset_index(name="Count")
        .rename(columns={"index": "Equipment"})
    )
    fig_eq = px.bar(
        eq_counts,
        x="Equipment", y="Count",
        title="🏷️ Equipment Usage Frequency",
        text="Count"
    )
    plotly(fig_eq)
    separator()

if show_insight:
    ins_df = (
        df.groupby("Level")["Rating"]
          .mean()
          .reset_index(name="AvgRating")
    )
    fig_insight = px.bar(
        ins_df,
        x="Level", y="AvgRating",
        title="📈 Avg Rating by Difficulty Level",
        text="AvgRating"
    )
    expert_pct = 0
    if "Expert" in ins_df["Level"].values:
        expert_pct = ins_df.loc[ins_df["Level"]=="Expert","AvgRating"].iloc[0] / 10 * 100
    progress(label="Expert Avg Rating (% of 10)", value=expert_pct)
    plotly(fig_insight)
    separator()

if show_bp_chart:
    bp_counts = (
        df["BodyPart"]
        .value_counts()
        .reset_index(name="Count")
        .rename(columns={"index": "BodyPart"})
    )
    fig_bp = px.bar(
        bp_counts,
        x="BodyPart", y="Count",
        title="💪 Body Part Focus",
        text="Count"
    )
    plotly(fig_bp)
    separator()

if show_insight:
    ins_df = (
        df.groupby("Level")["Rating"]
          .mean()
          .reset_index(name="AvgRating")
    )
    fig_insight = px.bar(
        ins_df,
        x="Level", y="AvgRating",
        title="📈 Avg Rating by Difficulty Level",
        text="AvgRating"
    )
    plotly(fig_insight)
    separator()

if show_trend_chart:
    # pick top 3 equipment by count
    top3 = df["Equipment"].value_counts().nlargest(3).index.tolist()
    trend_df = (
        df[df["Equipment"].isin(top3)]
        .groupby(["Level", "Equipment"])["Rating"]
        .mean()
        .reset_index(name="AvgRating")
    )
    fig_trend = px.line(
        trend_df,
        x="Level", y="AvgRating",
        color="Equipment",
        markers=True,
        line_shape="spline",
        title="📊 Avg Rating Trend for Top Equipment Across Levels"
    )
    plotly(fig_trend)
    separator()
