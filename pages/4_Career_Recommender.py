import streamlit as st
import plotly.express as px
import pandas as pd

st.markdown("""
<style>
.block-container {
    padding-left: 6%;
    padding-right: 6%;
    padding-top: 1.2rem;
    padding-bottom: 1.2rem;
    max-width: 88%;  
}

h1, h2, h3 {
    padding-left: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

from src.load_data import load_all_data
from src.recommender import recommend_occupations, top_skills_for_soc


# ============================
# Load OEWS + O*NET + IA risk
# ============================

@st.cache_data
def get_data():
    return load_all_data()

@st.cache_data
def load_ai_exposure():
    df_ai = pd.read_csv("data/raw/occ_level.csv")  # AJUSTA si está en otra carpeta

    # Categorías de riesgo IA según gamma
    df_ai["AI_Risk_Level"] = pd.cut(
        df_ai["dv_rating_gamma"],
        bins=[0, 0.33, 0.66, 1],
        labels=["Low", "Medium", "High"],
        include_lowest=True
    )
    return df_ai


def main():

    st.title("Recomendador de Carreras Basado en Habilidades")

    # Cargar datos
    oews_clean, merged, df_plot, df_rec, occ, skills_clean, tasks_clean = get_data()
    df_ai = load_ai_exposure()

    all_skills = sorted(df_rec["Skill"].unique())

    col_input, col_output = st.columns([1, 2])

    # ============================================================
    # PANEL IZQUIERDO — INPUTS
    # ============================================================
    with col_input:
        st.subheader("Tus habilidades")

        selected_skills = st.multiselect(
            "Selecciona habilidades",
            all_skills,
        )

        top_n = st.slider("Top N ocupaciones", 5, 30, 10)

        if st.button("Recomendar"):
            st.session_state["recommend_triggered"] = True
            st.session_state["selected_skills"] = selected_skills
            st.session_state["top_n"] = top_n

    # ============================================================
    # PANEL DERECHO — RESULTADOS
    # ============================================================
    if "recommend_triggered" in st.session_state and st.session_state["recommend_triggered"]:
        selected_skills = st.session_state.get("selected_skills", [])
        top_n = st.session_state.get("top_n", 10)

        with col_output:
            if not selected_skills:
                st.warning("Selecciona al menos una habilidad.")
                return

            # Obtener recomendaciones base
            recs = recommend_occupations(df_rec, selected_skills, top_n=top_n)

            if recs.empty:
                st.info("No se encontraron recomendaciones.")
                return

            # =========================================
            # MERGE con riesgo IA (gamma + categoría)
            # =========================================
            recs = recs.merge(
                df_ai.rename(columns={"O*NET-SOC Code": "SOC"})[
                    ["SOC", "dv_rating_gamma", "AI_Risk_Level"]
                ],
                on="SOC",
                how="left"
            )

            st.subheader("Ocupaciones recomendadas")

            recs_show = recs.copy()
            recs_show["Label"] = recs_show["Title"] + " (" + recs_show["SOC"] + ")"

            # Mostrar tabla mejorada
            st.dataframe(
                recs_show[
                    ["SOC", "Title", "Similarity", "AI_Risk_Level", "dv_rating_gamma"]
                ]
            )

            # =========================================
            # GRÁFICO DE SIMILITUD
            # =========================================
            fig = px.bar(
                recs_show,
                x="Similarity",
                y="Title",
                orientation="h",
                title="Ocupaciones Recomendadas por similitud",
                color="Similarity",
                color_continuous_scale="Blues",
                height=600,
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

            # =========================================
            # SELECCIONAR UNA OCUPACIÓN PARA VER SKILLS
            # =========================================
            st.subheader("Ver habilidades de una ocupación recomendada")

            selected_label = st.selectbox(
                "Selecciona una ocupación",
                recs_show["Label"],
            )

            row = recs_show[recs_show["Label"] == selected_label].iloc[0]
            soc = row["SOC"]
            title = row["Title"]

            occ_skills = top_skills_for_soc(df_rec, soc, top_k=15)
            st.write(f"Habilidades más importantes para: **{title} ({soc})**")
            st.dataframe(occ_skills)

            fig_skills = px.bar(
                occ_skills,
                x="Importance",
                y="Skill",
                orientation="h",
                title="Habilidades Principales (Importancia)",
                height=500,
            )
            fig_skills.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_skills, use_container_width=True)


if __name__ == "__main__":
    main()
