import streamlit as st

# -------------------------------
# Configuración de la página
# -------------------------------
st.set_page_config(
    page_title="Job Skills & Wages Explorer",
    layout="wide",
    page_icon="📊"
)

# -------------------------------
# Estilo visual
# -------------------------------
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


# -------------------------------
# TÍTULO PRINCIPAL
# -------------------------------
st.title("WorkScope - Análisis de Competencias Profesionales y Empleo")
st.markdown("### Una plataforma interactiva para explorar habilidades, salarios y tendencias laborales en EE. UU.")


# -------------------------------
# INTRODUCCIÓN
# -------------------------------
st.markdown("""
Este dashboard integra **tres grandes fuentes de información laborales de Estados Unidos** para analizar cómo las **habilidades**, 
los **salarios** y la **exposición a la inteligencia artificial** afectan a cientos de ocupaciones.

Las principales fuentes utilizadas son:

---

## 🗂️ Datos utilizados

### **OEWS — Occupational Employment & Wage Statistics**
- Publicado por el **US Bureau of Labor Statistics (BLS)**
- Información salarial anual y por hora
- Empleo total por ocupación
- Distribución geográfica por estado
- Índices de concentración laboral (Location Quotient)

### **O*NET — Occupational Information Network**
- Base de datos oficial de competencias laborales en EE. UU.
- Contiene:
  - Habilidades (Skills)
  - Importancia y nivel de cada habilidad
  - Tareas típicas del puesto
  - Descripción detallada de cada ocupación

### **Dataset de exposición a IA (gamma)**
- Basado en modelos de exposición ocupacional a inteligencia artificial
- Incluye:
  - Puntuaciones α, β y γ
  - Medida agregada del impacto esperado de IA por ocupación
  - Clasificación del nivel de riesgo IA por familia ocupacional

---

## 🧭 Navegación del Dashboard

### **1. Mapas y Tendencias Salariales**
Explora:
- Salarios por estado
- Top N estados con salarios más altos
- Relación Empleo ↔ Salario

Ideal para entender **dónde** se encuentran las mejores oportunidades económicas.

---

### **2. Importancia de Habilidades y Salario**
Incluye:
- Ranking de habilidades más importantes por ocupación
- Correlación entre importancia de habilidades y salario
- Exposición a IA por familias ocupacionales

Ayuda a analizar **qué habilidades realmente importan** en el mercado.

---

### **3. Comparador de Ocupaciones (Radar)**
Permite comparar **hasta 3 ocupaciones** simultáneamente usando:
- Radar chart de las habilidades clave

Muy útil para ver diferencias entre puestos o planificar desarrollo profesional.

---

### **4. Recomendador de Carreras**
Basado en:
- Similitud de habilidades (cosine similarity)
- Importancia media de skills
- Nivel de riesgo IA
- Ranking de ocupaciones personalizadas

Te ofrece **ocupaciones compatibles con tu perfil** y sus habilidades esenciales.

---

### **5. Clustering de Ocupaciones**
Agrupa ocupaciones en función de:
- Perfil de habilidades
- PCA en 2D para visualización
- Heatmaps de habilidades por cluster

Sirve para entender patrones laborales de forma **macro**.

---

## 🎯 Objetivo del Dashboard

Este proyecto combina análisis estadístico, ingeniería de datos y visualización avanzada para:

- Comprender cómo se estructuran las habilidades laborales  
- Explorar cómo cambia la demanda según la ocupación y región  
- Medir cómo la inteligencia artificial podría impactar cada ocupación  
- Ayudar a estudiantes y profesionales a identificar oportunidades laborales  

---

## 🚀 ¿Cómo empezar?

Usa la barra lateral izquierda para navegar entre los módulos del dashboard  
y comenzar a explorar **salarios, habilidades y oportunidades laborales**.

""")

