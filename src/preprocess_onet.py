import pandas as pd


def clean_soc(x):
    if isinstance(x, str):
        return x.strip()
    return x


def load_and_clean_onet(
    occ_df: pd.DataFrame,
    skills_df: pd.DataFrame,
    tasks_df: pd.DataFrame,
):
    """
    Aplica la lógica del Notebook2:
    - Limpieza de SOC
    - Filtro de skills (Scale ID = 'IM', Not Relevant != 'Y')
    - Selección de columnas
    """
    # Limpiar SOC
    occ_df["O*NET-SOC Code"] = occ_df["O*NET-SOC Code"].apply(clean_soc)
    skills_df["O*NET-SOC Code"] = skills_df["O*NET-SOC Code"].apply(clean_soc)
    tasks_df["O*NET-SOC Code"] = tasks_df["O*NET-SOC Code"].apply(clean_soc)

    # Occupation Data
    occ = occ_df[["O*NET-SOC Code", "Title", "Description"]].rename(
        columns={"O*NET-SOC Code": "SOC"}
    )

    # Skills
    skills_clean = skills_df[
        (skills_df["Scale ID"] == "IM") &
        (skills_df["Not Relevant"] != "Y")
    ].copy()

    skills_clean = skills_clean[
        ["O*NET-SOC Code", "Element Name", "Data Value"]
    ].rename(
        columns={
            "O*NET-SOC Code": "SOC",
            "Element Name": "Skill",
            "Data Value": "Importance",
        }
    )

    # Tasks
    tasks_clean = tasks_df[
        ["O*NET-SOC Code", "Task ID", "Task", "Task Type"]
    ].rename(columns={"O*NET-SOC Code": "SOC"})

    # Normalización de strings
    skills_clean["SOC"] = skills_clean["SOC"].astype(str).str.strip()
    skills_clean["Skill"] = skills_clean["Skill"].astype(str).str.strip()

    return occ, skills_clean, tasks_clean
