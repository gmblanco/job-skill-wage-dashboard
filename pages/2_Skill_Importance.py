import streamlit as st
from src.charts_skills import top_skills_bar, skills_salary_correlation, ai_exposure_by_group
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


@st.cache_data
def get_data():
    return load_all_data()


def main():
    st.title("Importancia de Habilidades y Salario")

    oews_clean, merged, df_plot, df_rec, occ, skills_clean, tasks_clean = get_data()

    # --------------------------------------------------------------
    # SECCIÓN 1: TOP SKILLS
    # --------------------------------------------------------------
    occupation_options = ["All"] + sorted(df_plot["OCC_TITLE"].dropna().unique())
    occupation = st.selectbox("Selecciona ocupación", occupation_options, index=0)

    top_n = st.slider("Top N habilidades", 3, 20, 10)
    fig_top = top_skills_bar(df_plot, occupation, top_n)
    st.plotly_chart(fig_top, use_container_width=True)

    # --------------------------------------------------------------
    # SECCIÓN 2: CORRELACIÓN SKILLS ↔ SALARIO
    # --------------------------------------------------------------
    st.subheader("Correlación: Importancia de Habilidades vs Salario")
    df_corr, fig_corr = skills_salary_correlation(df_plot)
    st.plotly_chart(fig_corr, use_container_width=True)

    st.dataframe(
        df_corr.sort_values("Correlation", ascending=False).reset_index(drop=True)
    )

    # --------------------------------------------------------------
    # SECCIÓN 3: EXPOSICIÓN A IA POR FAMILIAS OCUPACIONALES
    # --------------------------------------------------------------
    st.subheader("Exposición a la IA por familias ocupacionales")

    # Cargar dataset occ_level.csv (AJUSTA la ruta si está en otro sitio)
    df_occ_level = pd.read_csv("data/raw/occ_level.csv")

    top_groups = st.slider(
        "Número de familias ocupacionales (Top N)",
        5, 25, 10,
        key="ai_top_groups"
    )

    fig_ai = ai_exposure_by_group(df_occ_level, top_n=top_groups)
    st.plotly_chart(fig_ai, use_container_width=True)


if __name__ == "__main__":
    main()
