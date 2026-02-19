---
title: "Metodología del Índice de Intensidad Estratégica (IIE)"
date: 2026-02-19T16:00:00Z
report_types: "metodologia"
tags: ["algoritmos", "metodología", "inteligencia", "geopolitica", "automatización"]
description: "Explicación técnica sobre el cálculo del parámetro Pp y la lógica de normalización de datos."
---

# 📑 Fundamentos Técnicos del IIE

Para que el sistema de monitorización en la **Odroid-C2** sea efectivo, no basta con contar noticias. El script `cronista_iie.py` aplica una capa de normalización económica sobre el flujo de información bruta.

## 📐 1. El Parámetro de Intensidad ($P_p$)

El cálculo central del sistema es el **Poder de Presión Informativa** ($P_p$). Este parámetro busca responder a la pregunta: *¿Cuánta relevancia tiene este volumen de noticias en relación al peso real de la región en el mundo?*

### La Fórmula 
$$P_p = \frac{N_{24h}}{GDP_{nominal} \times \Omega}$$

Donde:
* **$N_{24h}$**: Volumen total de noticias capturadas en las últimas 24 horas por región. 📰
* **$GDP_{nominal}$**: Producto Interior Bruto (en trillones de $) según el `GEO_CONTEXT`. 💰
* **$\Omega$**: Coeficiente de ajuste dinámico (actualmente 1.0) para equilibrar sesgos regionales.



---

## 🚦 2. Lógica de Semáforos y Umbrales

El sistema traduce el valor numérico $P_p$ en un estado visual para facilitar la toma de decisiones rápida:

| Rango de $P_p$ | Estado | Interpretación |
| :--- | :--- | :--- |
| **0 - 15** | 🟢 ESTABLE | Flujo de noticias estándar. Sin anomalías detectadas. |
| **15 - 50** | 🟠 ELEVADO | Tensión en aumento. El volumen informativo supera la capacidad económica de la región. |
| **> 50** | 🔴 CRÍTICO | Saturación informativa. Evento disruptivo de alto impacto en curso. |

---

## 🚨 3. Análisis de Actividad y Fuentes

El script no solo calcula el número, sino que identifica la **Fuente Principal** mediante una consulta SQL de agregación:

```sql
SELECT link, COUNT(*) as c FROM news 
WHERE region = ? AND timestamp > ? 
GROUP BY link ORDER BY c DESC


---
