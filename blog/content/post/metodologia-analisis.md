---
title: "Metodología y Criterios de Análisis"
date: 2026-02-15T19:30:00
report_types: ["Metodología"]
tags: ["metodologia", "osint", "documentacion"]
---

### 🧠 Fundamentos del Nodo Odroid-C2
Este portal de inteligencia opera bajo un modelo de procesamiento local y descentralizado. A continuación, se detallan los criterios técnicos que rigen la generación de informes.

### 📊 1. El Parámetro "Volumen"
En las tablas estratégicas, el **Volumen** es la métrica de confianza. 
* **Definición:** Representa el número total de noticias únicas procesadas y clasificadas para una región específica.
* **Interpretación:** Un volumen bajo (ej. <5) indica una anécdota informativa. Un volumen alto (>50) confirma una tendencia sólida en la narrativa regional.
* **Cálculo:** Es el sumatorio de registros (`COUNT`) en la base de datos SQL del nodo durante el periodo analizado.

### 📈 2. Índice de Sentimiento (NLP)
Cada titular pasa por un motor de Procesamiento de Lenguaje Natural (NLP) que asigna un valor numérico:
* **Valores Positivos (>0.05):** Narrativas de estabilidad, acuerdos o avances.
* **Rango Neutral (-0.05 a 0.05):** Información puramente fáctica o sin carga emocional.
* **Valores Negativos (<-0.05):** Retórica de conflicto, crisis o alertas de seguridad.

### 🔄 3. Comparativa de Tendencias
Comparamos el sentimiento medio de los últimos 7 días contra los 14 días previos para determinar la **Evolución**:
* **Mejorando:** El índice se desplaza hacia valores positivos.
* **Deterioro:** El índice cae hacia valores negativos.
* **Estable:** La variación es menor al 5%.

---
*Este documento es dinámico y se actualiza conforme evolucionan los algoritmos de clasificación del nodo.*
