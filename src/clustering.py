import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# ============================================================
#   FUNCIÓN PRINCIPAL DE CLUSTERING
# ============================================================

def run_clustering(df_rec: pd.DataFrame, n_clusters: int = 6):
    """
    df_rec debe contener columnas:
        ['SOC', 'Skill', 'Importance', 'Title']

    Devuelve:
        - df_pivot: matriz SOC × skills con:
            * SOC
            * Title
            * Cluster (número)
            * Cluster_Label (nombre explicativo)
            * PC1, PC2 (coordenadas PCA)
        - top_skills_per_cluster: importancia media de skills por cluster
        - cluster_summary: top 10 skills por cluster
    """

    # ---------------------------------------
    # 1. Pivot ocupaciones × habilidades
    # ---------------------------------------
    df_pivot = (
        df_rec.pivot_table(
            index=["SOC", "Title"],
            columns="Skill",
            values="Importance",
            aggfunc="mean",
        )
        .fillna(0)
    )

    # ---------------------------------------
    # 2. Normalización
    # ---------------------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_pivot)

    # ---------------------------------------
    # 3. KMeans clustering
    # ---------------------------------------
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    df_pivot["Cluster"] = clusters

    # ---------------------------------------
    # 4. PCA para visualización 2D
    # ---------------------------------------
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)
    df_pivot["PC1"] = coords[:, 0]
    df_pivot["PC2"] = coords[:, 1]

    df_pivot.reset_index(inplace=True)

    # ---------------------------------------
    # 5. Nombres explicativos para cada cluster
    #    (basados en los skills dominantes del CSV exportado)
    # ---------------------------------------
    # OJO: estos índices (0–5) son los que devuelve KMeans
    # y los usamos tal cual para etiquetar.
    default_names = {
        0: "Grupo 1 – Habilidades cognitivas y de comunicación avanzadas",
        1: "Grupo 2 – Operaciones, control y supervisión de procesos",
        2: "Grupo 3 – Comunicación, comprensión y aprendizaje continuo",
        3: "Grupo 4 – Servicio, trato con personas y coordinación",
        4: "Grupo 5 – Análisis y resolución de problemas complejos",
        5: "Grupo 6 – Operaciones técnicas, calidad y mantenimiento",
    }

    # Si cambia el número de clusters, rellenamos con nombres genéricos
    cluster_labels = {
        c: default_names.get(c, f"Grupo {c+1}") 
        for c in sorted(df_pivot["Cluster"].unique())
    }

    df_pivot["Cluster_Label"] = df_pivot["Cluster"].map(cluster_labels)

    # ---------------------------------------
    # 6. Perfiles de skills por cluster
    # ---------------------------------------
    cluster_profiles = (
        df_rec.groupby(["SOC", "Title", "Skill"])["Importance"].mean().reset_index()
        .merge(df_pivot[["SOC", "Cluster"]], on="SOC")
    )

    top_skills_per_cluster = (
        cluster_profiles.groupby(["Cluster", "Skill"])["Importance"]
        .mean()
        .reset_index()
        .sort_values(["Cluster", "Importance"], ascending=[True, False])
    )

    # Top K skills por cluster
    topk = 10
    cluster_summary = (
        top_skills_per_cluster.groupby("Cluster")
        .head(topk)
        .reset_index(drop=True)
    )

    return df_pivot, top_skills_per_cluster, cluster_summary


# ============================================================
#   VISUALIZACIÓN PCA + CLUSTERS
# ============================================================

def plot_clusters(df_pivot: pd.DataFrame):
    """
    Visualiza las ocupaciones proyectadas en 2D (PCA),
    coloreadas según el grupo de habilidades.
    """

    fig = px.scatter(
        df_pivot,
        x="PC1",
        y="PC2",
        color="Cluster_Label",                        # leyendas explicativas
        hover_data={
            "SOC": True,
            "Title": True,
        },
        title="Agrupación de Ocupaciones Según Similitud en Perfiles de Habilidades",
        color_continuous_scale="Turbo",   # colores muy diferenciados
    )

    fig.update_traces(marker=dict(size=10, opacity=0.85))

    fig.update_layout(
        height=750,
        margin=dict(l=20, r=20, t=80, b=40),
        title_font=dict(size=26),
        legend_title="Grupos de ocupaciones",
        xaxis_title="Dimensión 1 (PCA – reducción de dimensionalidad)",
        yaxis_title="Dimensión 2 (PCA – reducción de dimensionalidad)",
    )

    return fig

def plot_heatmap_clusters(top_skills_per_cluster: pd.DataFrame):
    """
    Devuelve un heatmap profesional Cluster × Skill usando seaborn.
    """

    heatmap_df = (
        top_skills_per_cluster
        .pivot_table(
            index="Cluster",
            columns="Skill",
            values="Importance"
        )
        .fillna(0)
    )

    # Crear figura correctamente
    fig, ax = plt.subplots(figsize=(20, 8))

    sns.heatmap(
        heatmap_df,
        cmap="viridis",
        linewidths=0.3,
        linecolor="gray",
        ax=ax
    )

    ax.set_xlabel("Habilidad")
    ax.set_ylabel("Cluster")

    fig.tight_layout()

    return fig    
