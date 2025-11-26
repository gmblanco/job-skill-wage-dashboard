from pathlib import Path

import pandas as pd

from .preprocess_oews import clean_oews
from .preprocess_onet import load_and_clean_onet
from .merge_datasets import build_merged


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"


def load_oews_raw() -> pd.DataFrame:
    path = RAW_DIR / "oews.xlsx"
    return pd.read_excel(path, engine="openpyxl")


def load_onet_raw():
    occ_path = RAW_DIR / "Occupation Data.xlsx"
    skills_path = RAW_DIR / "Skills.xlsx"
    tasks_path = RAW_DIR / "Task Statements.xlsx"

    occ = pd.read_excel(occ_path)
    skills = pd.read_excel(skills_path)
    tasks = pd.read_excel(tasks_path)
    return occ, skills, tasks


def load_all_data():
    """
    Pipeline completo:
    - Carga OEWS y O*NET (raw)
    - Limpieza
    - Unión
    - Devuelve:
      oews_clean, merged, df_plot, df_rec
    """
    # OEWS
    oews_raw = load_oews_raw()
    oews_clean = clean_oews(oews_raw)

    # O*NET
    occ_raw, skills_raw, tasks_raw = load_onet_raw()
    occ, skills_clean, tasks_clean = load_and_clean_onet(
        occ_raw, skills_raw, tasks_raw
    )

    # Merge
    merged, df_plot, df_rec = build_merged(
        oews_clean, occ, skills_clean, tasks_clean
    )

    return oews_clean, merged, df_plot, df_rec, occ, skills_clean, tasks_clean
