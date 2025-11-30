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

import plotly.graph_objects as go
import pandas as pd

# Convertir color HEX a rgba(r,g,b,a)
def hex_to_rgba(hex_color, alpha=0.25):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def radar_chart(df_plot: pd.DataFrame, occupations: list[str], max_skills: int = 10):

    # Colores fijos y contrastados (hex)
    fixed_colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

    # Skills más importantes del subconjunto
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

    # Añadir cada ocupación con color sólido + relleno rgba transparente
    for idx, occ in enumerate(occupations):
        values = get_profile_for_occ(occ)

        base_hex = fixed_colors[idx % 3]               # Azul, naranja, verde
        rgba_fill = hex_to_rgba(base_hex, 0.25)        # Relleno transparente
        rgba_line = hex_to_rgba(base_hex, 1.0)         # Línea color sólido

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=skill_list,
                fill="toself",
                name=occ,
                line=dict(color=rgba_line, width=2),
                fillcolor=rgba_fill,
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
        height=800,
    )

    return fig



def ai_exposure_by_group(df_occ_level, top_n=10):
    """
    Crea un bar chart horizontal mostrando exposición a IA (dv_rating_gamma)
    por familias ocupacionales O*NET (primeros 2 dígitos del SOC).
    """

    group_names = {
        "11": "Management",
        "13": "Business & Financial Operations",
        "15": "Computer & Mathematical",
        "17": "Architecture & Engineering",
        "19": "Life, Physical & Social Science",
        "21": "Community & Social Service",
        "23": "Legal Occupations",
        "25": "Education & Library",
        "27": "Arts, Media & Sports",
        "29": "Healthcare Practitioners",
        "31": "Healthcare Support",
        "33": "Protective Service",
        "35": "Food Preparation & Serving",
        "37": "Cleaning & Maintenance",
        "39": "Personal Care & Service",
        "41": "Sales",
        "43": "Office & Administrative Support",
        "45": "Farming, Fishing & Forestry",
        "47": "Construction & Extraction",
        "49": "Installation & Repair",
        "51": "Production",
        "53": "Transportation & Material Moving",
        "55": "Military"
    }

    # Preparación de datos
    df = df_occ_level.copy()
    df["OCC_GROUP"] = df["O*NET-SOC Code"].astype(str).str.slice(0, 2)

    df_grouped = (
        df.groupby("OCC_GROUP")["dv_rating_gamma"]
          .mean()
          .reset_index()
    )

    df_grouped["Group_Name"] = df_grouped["OCC_GROUP"].map(group_names)
    df_grouped = df_grouped.dropna(subset=["Group_Name"])
    df_grouped = df_grouped.sort_values("dv_rating_gamma", ascending=False)

    df_top = df_grouped.head(top_n)

    fig = px.bar(
        df_top,
        x="dv_rating_gamma",
        y="Group_Name",
        orientation="h",
        color="dv_rating_gamma",
        color_continuous_scale="Reds",
        title=f"Top {top_n} Familias Ocupacionales con Mayor Exposición a IA",
        height=max(500, top_n * 35)
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Exposición a IA (dv_rating_gamma)",
        yaxis_title="Familia ocupacional",
        margin=dict(l=40, r=40, t=80, b=40)
    )

    return fig

