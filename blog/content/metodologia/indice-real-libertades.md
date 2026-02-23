---
title: "Metodología: Índice Real de Libertades (IRL)"
date: 2026-02-23
report_types: "metodologia"
section: "metodologia"
summary: "Protocolo de cálculo del índice IRL basado en sentimiento ponderado y varianza histórica de 30 días en el nodo Odroid-C2."
---

# Protocolo Evolutivo IRL (Índice Real de Libertades)

Este documento define la metodología técnica aplicada por el nodo **Odroid-C2** para transformar datos masivos de noticias en un indicador de salud democrática.

### 1. Extracción de Datos
El script `generador_evolutivo_irl.py` realiza "catas" semanales en la base de datos `news.db`, analizando fuentes regionales en 14 zonas estratégicas.

### 2. El Algoritmo de Sentimiento
Se aplica un modelo de NLP que clasifica las noticias en tres vectores:
* **Positivo (Estabilidad):** Avances en derechos, acuerdos diplomáticos.
* **Neutral (Ruido):** Flujo administrativo diario.
* **Negativo (Tensión):** Conflictos, censura o inestabilidad.

### 3. Cálculo de la Varianza (Delta)
El IRL no es una foto fija; es un indicador dinámico. Comparamos el promedio de sentimiento de la semana actual contra el histórico de las últimas 4 semanas. 

> **Alerta Crítica:** Se marca en rojo cualquier región con una caída superior al **15%** en su índice de libertad respecto al mes anterior.

### 4. Visualización Táctica
Los resultados se integran automáticamente en el Dashboard principal bajo el tag `#IRL_Global`, permitiendo al analista detectar puntos de inflexión antes de que se conviertan en crisis abiertas.
