import pandas as pd
import plotly.express as px


# ============================================================
#   MAPA SALARIAL — INTERACTIVO, AMPLIADO Y RESPONSIVO
# ============================================================

def choropleth_wage_map(df: pd.DataFrame, occupation: str):
    df_occ = df[df["OCC_TITLE"] == occupation].copy()

    fig = px.choropleth(
        df_occ,
        locations="STATE_ABBR",
        locationmode="USA-states",
        color="A_MEDIAN",
        color_continuous_scale="Viridis",
        scope="usa",
        labels={"A_MEDIAN": "Salario anual mediano ($)"},
        title=f"Salario anual mediano de {occupation} por estado",
    )

    # --- Hover template profesional ---
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br><br>"
                      "Estado: %{location}<br>"
                      "Salario anual mediano: $%{z:,.0f}<br>"
                      "Empleo total: %{customdata[0]:,}<br>"
                      "Índice de concentración (LQ): %{customdata[1]:.2f}<br>"
                      "<extra></extra>",
        hovertext=df_occ["AREA_TITLE"],
        customdata=df_occ[["TOT_EMP", "LOC_QUOTIENT"]].values,
    )

    fig.update_layout(
        height=750,
        margin=dict(l=20, r=20, t=80, b=20),
        title_font=dict(size=28),
        geo=dict(bgcolor="rgba(0,0,0,0)")
    )

    return fig


# ============================================================
#   TOP N ESTADOS — BARRAS RESPONSIVAS
# ============================================================

def top_n_states_bar(df: pd.DataFrame, occupation: str, top_n: int):
    df_occ = df[df["OCC_TITLE"] == occupation].copy()
    df_occ = df_occ.sort_values("A_MEDIAN", ascending=False)
    df_top = df_occ.head(int(top_n))

    fig = px.bar(
        df_top,
        x="STATE_ABBR",
        y="A_MEDIAN",
        text="A_MEDIAN",
        color="A_MEDIAN",
        color_continuous_scale="Teal",
        hover_name="AREA_TITLE",
        labels={
            "STATE_ABBR": "Estado",
            "A_MEDIAN": "Salario anual mediano ($)",
        },
        title=f"Top {top_n} estados con mayor salario — {occupation}",
    )

    fig.update_traces(texttemplate="$%{text:.0f}", textposition="outside")

    fig.update_layout(
        height=550,
        margin=dict(l=20, r=20, t=80, b=40),
        coloraxis_showscale=False,
        title_font=dict(size=26),
    )

    return fig


# ============================================================
#   SCATTER EMPLEO vs SALARIO — RESPONSIVO
# ============================================================

def employment_vs_wage_scatter(df: pd.DataFrame, occupation: str, xscale: str = "linear"):
    df_occ = df[df["OCC_TITLE"] == occupation].copy()
    df_occ = df_occ.dropna(subset=["TOT_EMP", "A_MEDIAN", "LOC_QUOTIENT"])

    fig = px.scatter(
        df_occ,
        x="TOT_EMP",
        y="A_MEDIAN",
        color="LOC_QUOTIENT",
        size="LOC_QUOTIENT",
        hover_name="AREA_TITLE",
        hover_data={
            "TOT_EMP": "Empleo total",
            "A_MEDIAN": "Salario anual mediano ($)",
            "LOC_QUOTIENT": "Índice de concentración (LQ)",
            "STATE_ABBR": "Estado",
        },
        color_continuous_scale="Viridis",
        labels={
            "TOT_EMP": "Empleo total",
            "A_MEDIAN": "Salario anual mediano ($)",
            "LOC_QUOTIENT": "Índice de concentración (LQ)",
        },
        title=f"Relación entre empleo y salario — {occupation}",
    )

    fig.update_xaxes(type=xscale)

    fig.update_layout(
        height=650,
        margin=dict(l=20, r=20, t=80, b=40),
        title_font=dict(size=26),
    )

    return fig


# ============================================================
#   HEATMAP TOP ESTADOS — RESPONSIVO
# ============================================================

def heatmap_top_states(df: pd.DataFrame, occupation: str, top_n: int = 5):
    df_occ = df[df["OCC_TITLE"] == occupation].copy()
    df_sorted = df_occ.sort_values("A_MEDIAN", ascending=False).head(top_n)

    mat = df_sorted[["STATE_ABBR", "A_MEDIAN"]].set_index("STATE_ABBR")

    fig = px.imshow(
        mat,
        labels=dict(color="Salario anual mediano ($)"),
        color_continuous_scale="Viridis",
        aspect="auto",
    )

    fig.update_layout(
        height=450,
        margin=dict(l=20, r=20, t=60, b=20),
        title=f"Top {top_n} estados con mayor salario — {occupation}",
        title_font=dict(size=24),
        xaxis_title="",
        yaxis_title="Estado",
    )

    return fig
