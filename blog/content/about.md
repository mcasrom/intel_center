---
title: "Acerca del Proyecto"
date: 2026-02-04
layout: "about"
---

### Centro de Inteligencia Geopolítica
Este sistema es un monitor automatizado de fuentes abiertas (OSINT) diseñado para la vigilancia estratégica en tiempo real.

- **Motor:** Python 3 con lógica de procesamiento de lenguaje natural (NLP).
- **Persistencia:** Base de datos SQLite para histórico de 7 días.
- **Frontend:** Hugo (Tema Ananke) estático para máxima seguridad y velocidad.
- **Hardware:** Nodo dedicado Odroid-C2 bajo arquitectura ARM64 (DietPi).

**Objetivo:** Centralizar la información de regiones críticas en un solo panel visual para facilitar el análisis de tendencias y la detección de anomalías geopolíticas.

---

### Metodología de Análisis (NLP)
El sistema utiliza la librería **TextBlob** para evaluar el sentimiento de los titulares en tiempo real. Los valores oscilan entre:
* **+1.0 (Positivo):** Clima de cooperación, estabilidad o noticias favorables.
* **0.0 (Neutral):** Reportes fácticos o sin carga emocional detectable.
* **-1.0 (Negativo):** Conflictos, crisis, amenazas o tensión militar.

Los **Radares de Tendencia** calculan el promedio móvil de las últimas 24 horas para filtrar el ruido informativo y mostrar la dirección real del sentimiento regional.

---

### Descargo de Responsabilidad
La información presentada en este panel es el resultado de un proceso automatizado de captura de noticias de terceros. **Intel Center 2026** no asume responsabilidad alguna por el contenido, veracidad, opiniones o sesgos presentes en las fuentes originales. Este es un experimento técnico de agregación de datos y no constituye asesoramiento político o militar profesional.

---
&copy; 2026 **Intel Center** | Desarrollo y Arquitectura por **M.Castillo**
