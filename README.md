# Aplicación de tendencias en empleo y mercado laboral

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

