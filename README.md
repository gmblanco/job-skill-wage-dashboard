# Aplicación de tendencias en empleo y mercado laboral

### Link to the project
Link: https://job-skill-wage-dashboard.onrender.com/Wage_Maps_and_Trends

## Breve descripción
Este proyecto es una aplicación web para visualizar tendencias del mercado laboral y del empleo. Proporciona un cuadro de mando interactivo que permite identificar los sectores que más crecen y las habilidades más demandadas. El objetivo es ayudar a estudiantes, profesionales, universidades e instituciones a tomar mejores decisiones sobre educación, formación y desarrollo profesional.

## Objetivos principales
- Desarrollar una aplicación web interactiva (o dashboard) para seguir tendencias laborales.
- Mostrar la evolución del empleo por sectores y regiones.
- Destacar las habilidades y puestos más demandados.
- Permitir comparaciones entre sectores o regiones a lo largo del tiempo.
- Ofrecer una herramienta útil para la orientación profesional y la planificación institucional.

## Usuarios objetivo
- Estudiantes y recién graduados que buscan integrarse en el mercado laboral.
- Profesionales que quieren actualizarse o cambiar de carrera.
- Universidades y centros de formación que necesitan adaptar sus programas a la demanda del mercado.
- Instituciones y administraciones públicas.
- Empresas que buscan contratar profesionales con habilidades demandadas.

## Plan inicial de trabajo
### Fase 1 – Investigación y planificación
- Definir fuentes de datos y estructura de la aplicación.
- Identificar métricas clave y visualizaciones.

### Fase 2 – Desarrollo del prototipo
- Construir el diseño inicial de la aplicación web.
- Implementar las primeras visualizaciones interactivas (gráficos, comparaciones, tendencias).

### Fase 3 – Funcionalidades
- Añadir funcionalidades adicionales y filtros interactivos.
- Permitir filtrar por sector, región y habilidades.

### Fase 4 – Optimización y despliegue
- Mejorar la usabilidad y el diseño.
- Preparar la documentación del proyecto.
- Finalizar el repositorio y el despliegue.

# Datasets
## 📊 Dataset 1 — Empleo por sector (Eurostat `lfsa_egan2`)

**Fuente:** [Eurostat – Employed persons by sex, age and economic activity (NACE Rev.2)](https://ec.europa.eu/eurostat/databrowser/view/lfsa_egan2/default/table?lang=en)

**Descripción:**  
Datos anuales del número de personas empleadas en **España** por **sector económico (clasificación NACE Rev.2)**, para la población de **15 a 64 años**.  
Las cifras están expresadas en **miles de personas**.

**Cobertura temporal:** 2008–2024  
**Unidad:** Miles de personas  

**Variables:**
| Columna | Descripción |
|----------|--------------|
| `sector` | Código NACE del sector económico (A, B–E, F, G–I, J, etc.) |
| `country` | País (`Spain`) |
| `year` | Año |
| `age_group` | Grupo de edad (15–64 años) |
| `employment_thousands` | Personas empleadas (miles) |

**Limpieza y formato:**
- Filtrado: España (`geo = ES`), total (`sex = T`), edad 15–64 años.  
- Eliminadas columnas de metadatos.  
- Renombradas columnas en formato `snake_case`.  
- Guardado como `employment_spain_by_sector.csv` en `/data/processed/`.

**Uso en la aplicación:**  
Gráficos de evolución y comparación del empleo por sector (series temporales, barras, áreas).

## 📊 Dataset 2 — Vacantes por sector (Eurostat `jvs_q_nace2`)

**Fuente:** [Eurostat – Job vacancies by NACE Rev.2 activity](https://ec.europa.eu/eurostat/databrowser/view/jvs_q_nace2/default/table?lang=en)

**Descripción:**  
Contiene la **tasa de vacantes** en España por **sector económico (clasificación NACE Rev.2)**.  
Los datos son **trimestrales** y expresan el porcentaje de puestos de trabajo no cubiertos sobre el total de empleos.  
Permite analizar la **demanda laboral** y las diferencias entre sectores.

**Cobertura temporal:** 2015Q1–2025Q2  
**Unidad:** % del total de puestos  

**Variables:**
| Columna | Descripción |
|----------|--------------|
| `sector` | Código NACE Rev.2 del sector económico |
| `country` | País (`Spain`) |
| `period` | Trimestre (formato `YYYYQn`) |
| `vacancy_rate` | Tasa de vacantes (%) |

**Limpieza y formato:**
- Filtrado: España (`geo = ES`), `NSA` (datos sin ajustar), indicador `Job vacancy rate (%)`.  
- Eliminadas columnas de metadatos.  
- Renombradas columnas en formato `snake_case`.  
- Guardado como `vacancies_spain_by_sector.csv` en `/data/processed/`.

**Uso en la aplicación:**  
Gráficos de evolución y comparación de la **demanda laboral por sector**, y cruces con el empleo total (Dataset 1).

---

## 💼 Dataset 3 — Ofertas de empleo y habilidades (LinkedIn Job Postings 2023–2024)

**Fuente:** [Kaggle – LinkedIn Job Postings (2023 – 2024)](https://www.kaggle.com/datasets/arshkoneru/linkedin-job-postings-2023-2024)

**Descripción:**  
Dataset con más de **120 000 ofertas de empleo publicadas en LinkedIn** durante 2023 y 2024.  
Incluye información sobre **puestos, ubicación, experiencia, salario y habilidades requeridas**.  
Permite identificar las **habilidades más demandadas** y los **perfiles profesionales en auge**.

**Cobertura temporal:** 2023–2024  
**Unidad:** Ofertas de empleo  

**Variables seleccionadas:**
| Columna | Descripción |
|----------|--------------|
| `title` | Título del puesto |
| `skills_desc` | Habilidades o competencias requeridas |
| `location` | Ubicación del empleo |
| `formatted_experience_level` | Nivel de experiencia (entry, associate, senior...) |
| `med_salary` | Salario medio estimado |
| `listed_time` | Fecha de publicación de la oferta |

**Limpieza y formato:**
- Descargado el archivo `job_postings.csv`.  
- Filtrado por columnas relevantes.  
- Eliminadas filas sin habilidades o ubicación.  
- Guardado como `linkedin_job_postings_skills.csv` en `/data/processed/`.

**Uso en la aplicación:**  
Visualizaciones sobre **habilidades más demandadas**, **evolución temporal de la demanda**, y **relación entre competencias y salario**.
