import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


def build_recommender_matrices(df_rec: pd.DataFrame):
    """
    df_rec: columnas ['SOC', 'Skill', 'Importance', 'Title']
    Devuelve:
    - occ_skill_scaled: matriz ocupación × skill escalada
    - all_skills: lista de skills en el mismo orden que columnas
    """
    occ_skill = (
        df_rec.pivot_table(
            index=["SOC", "Title"],
            columns="Skill",
            values="Importance",
            aggfunc="mean",
        )
        .fillna(0)
    )

    scaler = MinMaxScaler()
    occ_skill_scaled = pd.DataFrame(
        scaler.fit_transform(occ_skill),
        index=occ_skill.index,
        columns=occ_skill.columns,
    )

    all_skills = list(occ_skill_scaled.columns)
    return occ_skill_scaled, all_skills


def recommend_occupations(
    df_rec: pd.DataFrame,
    user_skills: list[str],
    top_n: int = 10,
    skill_weights: dict | None = None,
):
    """
    Devuelve un DataFrame con columnas: SOC, Title, Similarity
    """
    if not user_skills:
        return pd.DataFrame(columns=["SOC", "Title", "Similarity"])

    occ_skill_scaled, all_skills = build_recommender_matrices(df_rec)

    user_vec = np.zeros(len(all_skills))

    if skill_weights is None:
        skill_weights = {s: 1.0 for s in user_skills}

    for skill, w in skill_weights.items():
        if skill in all_skills:
            idx = all_skills.index(skill)
            user_vec[idx] = w

    user_vec = user_vec.reshape(1, -1)
    sims = cosine_similarity(user_vec, occ_skill_scaled.values)[0]

    result = pd.DataFrame(
        {
            "SOC": occ_skill_scaled.index.get_level_values("SOC"),
            "Title": occ_skill_scaled.index.get_level_values("Title"),
            "Similarity": sims,
        }
    ).sort_values("Similarity", ascending=False)

    return result.head(top_n)


def top_skills_for_soc(df_rec: pd.DataFrame, soc: str, top_k: int = 15):
    occ_skills = (
        df_rec[df_rec["SOC"] == soc][["Skill", "Importance"]]
        .sort_values("Importance", ascending=False)
        .head(top_k)
    )
    return occ_skills
