---
title: "Metodología de Análisis e Inteligencia de Datos"
date: 2026-02-23T09:55:00
author: "M. Castillo"
tags: ["Metodología", "Documentos", "IRL", "Inteligencia"]
categories: ["Protocolos"]
---

## 🏛️ Marco Metodológico: Índice de Realidad de Libertad (IRL)

Este documento define los criterios técnicos utilizados por el nodo Odroid-C2 para auditar la salud informativa global. Bajo la supervisión de **M. Castillo**, el sistema procesa datos en tres capas de profundidad:

### 1. Vectores de Auditoría Estructural (Macro)
La base del índice se calcula mediante la media ponderada de:
* **P_Prensa:** Capacidad de ejercicio periodístico sin coacción.
* **P_Digital:** Nivel de apertura de la red y ausencia de firewalls estatales.
* **P_Legal:** Robustez del marco jurídico en protección de la expresión.

### 2. El Diferencial de Disonancia (Análisis de GAP)
Herramienta clave para la detección de propaganda. Se calcula restando el sentimiento de la fuente oficial del sentimiento de la fuente de contraste:
> 1735GAP = |Sentimiento_{Oficial} - Sentimiento_{Oposición}|1735
* Un **GAP > 0.6** dispara una alerta de conflicto narrativo o desinformación activa.

### 3. Dinámica de Sentimiento IA
Escaneo en tiempo real de la polaridad de las noticias. Los valores fluctúan entre **-1.0 (Crisis/Caos)** y **+1.0 (Estabilidad/Progreso)**.

---
### 🛡️ Registro de Actualización (Feb 2026)
Se han integrado estos vectores para permitir la trazabilidad evolutiva de 90 días y el ranking rotatorio de países.

**Responsable del Nodo:** M. Castillo
