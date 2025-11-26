import streamlit as st
import plotly.express as px

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


@st.cache_data
def get_data():
    return load_all_data()


def main():
    st.title("Recomendador de Carreras Basado en Habilidades")

    oews_clean, merged, df_plot, df_rec, occ, skills_clean, tasks_clean = get_data()

    all_skills = sorted(df_rec["Skill"].unique())

    col_input, col_output = st.columns([1, 2])

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

    if "recommend_triggered" in st.session_state and st.session_state["recommend_triggered"]:
        selected_skills = st.session_state.get("selected_skills", [])
        top_n = st.session_state.get("top_n", 10)

        with col_output:
            if not selected_skills:
                st.warning("Selecciona al menos una habilidad.")
                return

            recs = recommend_occupations(df_rec, selected_skills, top_n=top_n)

            if recs.empty:
                st.info("No se encontraron recomendaciones.")
                return

            st.subheader("Ocupaciones recomendadas")

            recs_show = recs.copy()
            recs_show["Label"] = recs_show["Title"] + " (" + recs_show["SOC"] + ")"
            st.dataframe(recs_show[["SOC", "Title", "Similarity"]])

            fig = px.bar(
                recs_show,
                x="Similarity",
                y="Title",
                orientation="h",
                title="Ocupaciones Recomendadas (Puntaje de Similitud)",
                color="Similarity",
                color_continuous_scale="Blues",
                height=600,
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)

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
            fig_skills.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_skills, use_container_width=True)


if __name__ == "__main__":
    main()
