import pandas as pd


SELECTED_OCC = [
    "Software Developers",
    "Computer and Mathematical Occupations",
    "Computer Systems Analysts",
    "Information Security Analysts",
    "Management Occupations",
    "Accountants and Auditors",
    "Financial Managers",
    "Market Research Analysts and Marketing Specialists",
    "Lawyers",
    "Paralegals and Legal Assistants",
    "Elementary School Teachers, Except Special Education",
    "Secondary School Teachers, Except Special and Career/Technical Education",
    "Registered Nurses",
    "Pharmacists",
    "Radiologic Technologists and Technicians",
    "Medical Assistants",
    "Retail Salespersons",
    "First-Line Supervisors of Retail Sales Workers",
    "Waiters and Waitresses",
    "Security Guards",
]


FIPS_TO_STATE = {
    1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC",
    12: "FL", 13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS",
    21: "KY", 22: "LA", 23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS",
    29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY",
    37: "NC", 38: "ND", 39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI", 45: "SC",
    46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV",
    55: "WI", 56: "WY",
}


OEWS_COLS = [
    "AREA", "AREA_TITLE",
    "OCC_CODE", "OCC_TITLE",
    "TOT_EMP", "JOBS_1000", "LOC_QUOTIENT",
    "A_MEAN", "A_MEDIAN", "A_PCT10", "A_PCT90",
    "H_MEAN", "H_MEDIAN",
]


def clean_oews(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Replica la lógica del Notebook1 para limpiar el OEWS."""
    # Filtrar ocupaciones seleccionadas
    df_occ = df_raw[df_raw["OCC_TITLE"].isin(SELECTED_OCC)].copy()

    # Seleccionar columnas relevantes
    df_trim = df_occ[OEWS_COLS].copy()

    # Reemplazar símbolos especiales
    df_trim = df_trim.replace({"*": None, "**": None, "~": None, "#": None})
    df_trim = df_trim.apply(pd.to_numeric, errors="ignore")

    # Eliminar filas sin salario mediano
    df_trim = df_trim.dropna(subset=["A_MEDIAN"])

    # Añadir sigla de estado desde código FIPS (AREA)
    df_trim["STATE_ABBR"] = df_trim["AREA"].map(FIPS_TO_STATE)
    df_trim = df_trim.dropna(subset=["STATE_ABBR"])

    # Renombrar OCC_CODE a SOC para armonizar con O*NET
    df_trim = df_trim.rename(columns={"OCC_CODE": "SOC"})

    # SOC como string normalizado
    df_trim["SOC"] = df_trim["SOC"].astype(str).str.strip()
    df_trim["SOC"] = df_trim["SOC"].apply(lambda x: x if "." in x else x + ".00")

    return df_trim
