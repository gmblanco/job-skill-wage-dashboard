import streamlit as st


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
from src.charts_skills import radar_chart


@st.cache_data
def get_data():
    return load_all_data()


def main():
    st.title("Comparador de Ocupaciones por habilidades")

    oews_clean, merged, df_plot, df_rec, occ, skills_clean, tasks_clean = get_data()

    occ_list = sorted(df_plot["OCC_TITLE"].dropna().unique())
    selected = st.multiselect(
        "Selecciona hasta 3 ocupaciones",
        occ_list,
        default=["Software Developers", "Information Security Analysts"][: min(2, len(occ_list))],
    )

    if len(selected) == 0:
        st.info("Selecciona al menos una ocupación.")
        return
    if len(selected) > 3:
        st.warning("Máximo 3 ocupaciones. Se usarán las primeras 3 seleccionadas.")
        selected = selected[:3]

    max_skills = st.slider("Número de habilidades en el radar", 5, 20, 10)
    fig_radar = radar_chart(df_plot, selected, max_skills)
    st.plotly_chart(fig_radar, use_container_width=True)


if __name__ == "__main__":
    main()
