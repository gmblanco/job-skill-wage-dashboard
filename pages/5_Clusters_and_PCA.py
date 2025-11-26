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
from src.clustering import run_clustering, plot_clusters, plot_heatmap_clusters


@st.cache_data
def get_data():
    return load_all_data()


def main():
    st.title("Clusters de ocupaciones según perfiles de habilidades")

    oews_clean, merged, df_plot, df_rec, occ, skills_clean, tasks_clean = get_data()

    n_clusters = st.slider("Número de clusters", 3, 12, 6)

    df_pivot, top_skills_per_cluster, cluster_summary = run_clustering(
        df_rec, n_clusters=n_clusters
    )

    st.subheader("Visualización de clusters")
    fig_clusters = plot_clusters(df_pivot)
    st.plotly_chart(fig_clusters, use_container_width=True)

    st.subheader("Mapa de calor de habilidades por cluster")
    fig_heatmap = plot_heatmap_clusters(top_skills_per_cluster)
    st.pyplot(fig_heatmap)

    st.subheader("Top skills por cluster")
    st.dataframe(cluster_summary)


if __name__ == "__main__":
    main()
