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
from src.charts_wages import (
    choropleth_wage_map,
    top_n_states_bar,
    employment_vs_wage_scatter,
    heatmap_top_states,
)


@st.cache_data
def get_data():
    return load_all_data()


def main():
    st.title("Mapas y Tendencias Salariales")

    oews_clean, merged, df_plot, df_rec, occ, skills_clean, tasks_clean = get_data()

    # Tabs principales
    tab1, tab2, tab3 = st.tabs(
        ["Mapa + Top N", "Empleo vs Salario", "Comparador entre Ocupaciones"]
    )

    # --------------------------------------------------------------------
    # TAB 1: MAPA + TOP N EN LA MISMA PÁGINA (conectados entre sí)
    # --------------------------------------------------------------------
    with tab1:
        st.subheader("Mapa salarial por estado")

        occupation_list = sorted(oews_clean["OCC_TITLE"].unique())
        occupation = st.selectbox(
            "Selecciona una ocupación",
            occupation_list,
            index=occupation_list.index("Software Developers")
            if "Software Developers" in occupation_list
            else 0,
            key="tab1_occ",
        )

        # Mostrar mapa
        fig_map = choropleth_wage_map(oews_clean, occupation)
        st.plotly_chart(fig_map, use_container_width=True, config={"responsive": True})

        st.subheader("Top N estados con mayor salario")

        top_n = st.slider(
            "Número de estados (Top N)",
            1,
            50,
            10,
            key="tab1_topn",
        )

        fig_bar = top_n_states_bar(oews_clean, occupation, top_n)
        st.plotly_chart(fig_bar, use_container_width=True)

    # --------------------------------------------------------------------
    # TAB 2: SCATTER EMPLEO vs SALARIO (filtro independiente)
    # --------------------------------------------------------------------
    with tab2:
        st.subheader("Relación entre Empleo y Salario Medio")

        occupation_list2 = sorted(oews_clean["OCC_TITLE"].unique())
        occupation2 = st.selectbox(
            "Selecciona una ocupación",
            occupation_list2,
            index=0,
            key="tab2_occ",
        )

        xscale = st.radio(
            "Escala del eje X",
            ["lineal", "log"],
            horizontal=True,
            key="tab2_scale",
        )

        fig_scatter = employment_vs_wage_scatter(
            oews_clean, occupation2, "linear" if xscale == "lineal" else "log"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --------------------------------------------------------------------
    # TAB 3: COMPARADOR ENTRE DOS OCUPACIONES
    # --------------------------------------------------------------------
    with tab3:
        st.subheader("Comparador de dos ocupaciones (Top N estados)")

        colA, colB = st.columns(2)

        occupation_list3 = sorted(oews_clean["OCC_TITLE"].unique())

        with colA:
            st.markdown("### Ocupación A")
            occA = st.selectbox(
                "Selecciona ocupación A",
                occupation_list3,
                index=occupation_list3.index("Software Developers")
                if "Software Developers" in occupation_list3
                else 0,
                key="tab3_occA",
            )

            topA = st.slider(
                "Top N estados (A)",
                1,
                20,
                5,
                key="tab3_topA",
            )

            figA = heatmap_top_states(oews_clean, occA, topA)
            st.plotly_chart(figA, use_container_width=True)

        with colB:
            st.markdown("### Ocupación B")
            occB = st.selectbox(
                "Selecciona ocupación B",
                occupation_list3,
                index=occupation_list3.index("Registered Nurses")
                if "Registered Nurses" in occupation_list3
                else 0,
                key="tab3_occB",
            )

            topB = st.slider(
                "Top N estados (B)",
                1,
                20,
                5,
                key="tab3_topB",
            )

            figB = heatmap_top_states(oews_clean, occB, topB)
            st.plotly_chart(figB, use_container_width=True)


if __name__ == "__main__":
    main()
