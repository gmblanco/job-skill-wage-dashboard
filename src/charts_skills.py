import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def top_skills_bar(df_plot: pd.DataFrame, occupation: str, top_n: int):
    if occupation == "All":
        df_filtered = df_plot.copy()
        title_occ = "All occupations"
    else:
        df_filtered = df_plot[df_plot["OCC_TITLE"] == occupation]
        title_occ = occupation

    ranking = (
        df_filtered.groupby("Skill_Name")["Importance"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    # Orden inverso para barra horizontal
    ranking = ranking.sort_values("Importance", ascending=True)

    fig = px.bar(
        ranking,
        x="Importance",
        y="Skill_Name",
        orientation="h",
        title=f"Top {top_n} Skills — {title_occ}",
        color="Importance",
        color_continuous_scale="Viridis",
        height=700,
    )

    fig.update_traces(
        text=ranking["Importance"].round(2),
        textposition="outside",
        textfont=dict(size=12, color="black"),
        marker=dict(line=dict(width=0.5, color="black")),
    )

    fig.update_layout(
        yaxis_title="Skill",
        xaxis_title="Average Importance (0–5)",
        font=dict(size=14, family="Arial"),
        title_font=dict(size=22, family="Arial", color="#333"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=120, r=40, t=80, b=40),
        coloraxis_showscale=True,
        bargap=0.25,
    )

    fig.update_xaxes(showgrid=True, gridcolor="#E1E1E1")
    fig.update_yaxes(showgrid=False)
    return fig


def skills_salary_correlation(df_plot: pd.DataFrame):
    corr_data = (
        df_plot.groupby(["SOC", "Skill_Name"])
        .agg(Importance=("Importance", "mean"), Salary=("A_MEAN", "mean"))
        .reset_index()
    )

    skill_corr = (
        corr_data.groupby("Skill_Name")
        .apply(lambda x: x["Importance"].corr(x["Salary"]))
        .sort_values(ascending=False)
    )

    df_corr = skill_corr.reset_index().rename(columns={0: "Correlation"})

    skill_categories = {
        "Complex Problem Solving": "Cognitive",
        "Critical Thinking": "Cognitive",
        "Judgment and Decision Making": "Cognitive",
        "Active Learning": "Cognitive",
        "Reading Comprehension": "Cognitive",
        "Writing": "Cognitive",
        "Mathematics": "STEM",
        "Science": "STEM",
        "Programming": "STEM",
        "Systems Analysis": "STEM",
        "Systems Evaluation": "STEM",
        "Speaking": "Social",
        "Social Perceptiveness": "Social",
        "Negotiation": "Social",
        "Coordination": "Social",
        "Persuasion": "Social",
        "Service Orientation": "Social",
        "Operation Monitoring": "Technical",
        "Operation and Control": "Technical",
        "Troubleshooting": "Technical",
        "Repairing": "Technical",
        "Equipment Maintenance": "Technical",
        "Quality Control Analysis": "Technical",
    }

    df_corr["Category"] = df_corr["Skill_Name"].map(skill_categories).fillna("Other")

    fig = px.bar(
        df_corr,
        x="Correlation",
        y="Skill_Name",
        orientation="h",
        color="Category",
        color_discrete_map={
            "Cognitive": "#1f77b4",
            "STEM": "#2ca02c",
            "Social": "#ff7f0e",
            "Technical": "#d62728",
            "Other": "#7f7f7f",
        },
        title="Correlation Between Skill Importance and Salary",
        height=900,
    )

    fig.update_layout(
        xaxis=dict(title="Correlation with Salary"),
        yaxis=dict(title="Skill"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
        showlegend=True,
    )

    fig.add_vline(x=0, line_width=2, line_dash="dash", line_color="black")

    return df_corr, fig


def radar_chart(df_plot: pd.DataFrame, occupations: list[str], max_skills: int = 10):
    # Skills más importantes globalmente en ese subconjunto de ocupaciones
    importance_means = (
        df_plot[df_plot["OCC_TITLE"].isin(occupations)]
        .groupby("Skill_Name")["Importance"]
        .mean()
        .sort_values(ascending=False)
    )

    skill_list = list(importance_means.head(max_skills).index)

    def get_profile_for_occ(occ):
        df_occ = df_plot[df_plot["OCC_TITLE"] == occ]
        avg = df_occ.groupby("Skill_Name")["Importance"].mean()
        return [avg.get(skill, 0) for skill in skill_list]

    fig = go.Figure()

    for occ in occupations:
        values = get_profile_for_occ(occ)
        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=skill_list,
                fill="toself",
                name=occ,
            )
        )

    fig.update_layout(
        title=f"Radar Chart — Top {len(skill_list)} Skills",
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
        height=800,
    )

    return fig
