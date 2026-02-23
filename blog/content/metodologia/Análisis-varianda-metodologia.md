---
weight: 2
title: "Metodología: Análisis de Varianza de Sentimiento"
date: 2026-02-17T15:35:00+01:00
report_types: ["metodologia"]
tags: ["Metodología", "Documentos", "OSINT", "Análisis"]
draft: false
type: "post"
---
weight: 2

### 📘 Introducción al Cálculo de Varianza Narrativa

Para que el análisis de inteligencia en este nodo sea accionable, no basta con conocer el sentimiento actual; es imprescindible medir su evolución. El **Análisis de Varianza** nos permite distinguir entre el ruido mediático habitual y una escalada de tensión real.

### 🧮 Metodología de Cálculo

El sistema procesa la base de datos `news.db` comparando dos ventanas temporales móviles:

1.  **Ventana Actual ($T_0$):** Media aritmética del sentimiento de todas las noticias capturadas en las últimas 24 horas.
2.  **Ventana de Control ($T_{-1}$):** Media aritmética del sentimiento del periodo previo (de 24 a 48 horas atrás).
3.  **Cálculo del Delta (Δ):** La diferencia neta entre ambas ventanas.

$$\Delta = \bar{x}(Sentimiento_{Hoy}) - \bar{x}(Sentimiento_{Ayer})$$

### 🚦 Interpretación de Resultados

Los informes de varianza clasifican automáticamente la tendencia según los siguientes umbrales críticos:

* 🔴 **Escalada ($> +0.05$):** Aumento significativo de la tensión narrativa. Sugiere el estallido de un conflicto o un endurecimiento de la retórica diplomática/militar.
* 🟢 **Distensión ($< -0.05$):** Caída de la tensión. Indica una resolución de crisis, el inicio de treguas o el desplazamiento del foco informativo hacia temas menos conflictivos.
* ⚪ **Estabilidad ($\pm 0.05$):** Fluctuación normal dentro del margen de error estadístico.

### 📂 Origen de los Datos y Documentos

* **Ingesta:** Los datos provienen de fuentes OSINT globales (RSS/API).
* **Procesamiento:** Nodo Odroid-C2 ejecutando motores de análisis de lenguaje natural (NLP).
* **Persistencia:** Todos los registros históricos se almacenan en el directorio `/data/` para auditorías posteriores.

---
weight: 2
*Este documento define el estándar de análisis para los informes automáticos de este centro de inteligencia.*

