import pandas as pd


def build_merged(
    oews_clean: pd.DataFrame,
    occ: pd.DataFrame,
    skills_clean: pd.DataFrame,
    tasks_clean: pd.DataFrame,
):
    """
    Une OEWS + O*NET y construye:
    - merged: info completa por SOC + estado
    - df_plot: base para análisis de skills vs salario
    - df_rec: base para recomendador (occupation-skill-importance)
    """
    # Merge OEWS con Occupation Data por SOC
    merged = oews_clean.merge(occ, on="SOC", how="left")

    # Agrupar skills y tasks en listas por SOC (para descripción cualitativa)
    skills_grouped = (
        skills_clean
        .groupby("SOC")["Skill"]
        .apply(list)
        .reset_index()
        .rename(columns={"Skill": "Skills_List"})
    )

    tasks_grouped = (
        tasks_clean
        .groupby("SOC")["Task"]
        .apply(list)
        .reset_index()
        .rename(columns={"Task": "Tasks_List"})
    )

    merged = merged.merge(skills_grouped, on="SOC", how="left")
    merged = merged.merge(tasks_grouped, on="SOC", how="left")

    # Filtrar ocupaciones que realmente mapean con O*NET
    merged = merged[merged["Title"].notna()].reset_index(drop=True)

    # ---------- df_plot: skill importance + salario medio por SOC ----------
    wages_by_soc = (
        merged.groupby(["SOC", "OCC_TITLE"])["A_MEAN"]
        .mean()
        .reset_index()
    )

    df_plot = wages_by_soc.merge(skills_clean, on="SOC", how="left")
    df_plot = df_plot.rename(columns={"Skill": "Skill_Name"})
    df_plot = df_plot.dropna(subset=["Importance", "A_MEAN"])

    # ---------- df_rec: base para recomendador ----------
    # df_rec = skills_clean + título ocupación
    occ_small = occ[["SOC", "Title"]]
    df_rec = skills_clean.merge(occ_small, on="SOC", how="left")

    return merged, df_plot, df_rec
