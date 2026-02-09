---
title: "📌 MANUAL: Operaciones e Interpretación de Inteligencia"
date: 2026-02-06T17:00:00Z
description: "Protocolo técnico para la interpretación del Semáforo Geopolítico, Alertas Críticas y Vigilancia Electoral."
type: "post"
tags: ["Metodología", "Protocolo", "Manual"]
weight: 1
featured_image: "images/header_intel.jpg"
---

📌 **PROTOCOLO DE INTELIGENCIA CONSOLIDADO (v2.1)**

Este documento define la metodología aplicada por el motor OSINT de la **Odroid-C2** para transformar datos masivos en indicadores tácticos.

#### 1. Semáforo de Tensión y Dinámica Política
El color de cada nodo se calcula mediante NLP y detección de contextos:

* 🔵 **Azul (Vigilancia)**: Fase electoral o transición. Prevalece sobre el sentimiento.
* 🟢 **Verde (Estabilidad)**: Polaridad **> 0.05**. Cooperación y normalidad.
* 🟡 **Amarillo (Neutral)**: Polaridad entre **-0.05 y 0.05**. Ruido basal diplomático.
* 🔴 **Rojo (Hostilidad)**: Polaridad **< -0.05**. Conflictos o inestabilidad grave.

#### 2. Clasificación de Alertas
Jerarquía de prioridad para el analista:
1. 👤 **Líderes Mundiales**: Seguimiento de mandatarios (Trump, Putin, Xi, etc.).
2. 🚩 **Alertas Críticas**: Términos de peligro (Nuclear, Ataque, Misil).
3. 🌍 **Resumen Global**: Flujo informativo de contexto general.

#### 3. Mantenimiento y Resiliencia
* **Base de Datos**: SQLite con **15 días** de histórico persistente.
* **Ciclo de Ingesta**: Automatizado cada **60 minutos**.

#### 4. Cobertura de Nodos Activos

### Cobertura de Nodos y Regiones Monitorizadas (v2.2)

| Eje Estratégico | Indicador Crítico | Alcance Operativo | Tag de Sistema |
| :--- | :--- | :--- | :--- |
| **Rusia / Eurasia** | Tensión Bélica / OTAN | Rusia, Ucrania, Asia Central. | `#Rusia_Eurasia` |
| **USA / Norte** | Dinámica Electoral | Política Federal y Defensa EE.UU. | `#USA_NORTE` |
| **Sudamérica** | Estabilidad BRICS/Mercosur | Brasil, Argentina, Cono Sur. | `#Sudamerica` |
| **Medio Oriente** | Geopolítica Energética | Mundo Árabe, Irán, Israel. | `#Medio_Oriente` |
| **África / Sahel** | Seguridad Regional | Inestabilidad y movimientos insurgentes. | `#Africa_Sahel` |
| **México** | Seguridad Interna | Frontera y política nacional. | `#MEXICO` |
| **Europa / DW** | Estabilidad UE | Dinámicas continentales y diplomacia. | `#Europa_DW` |
| **España** | Estabilidad Institucional | Política nacional y territorial. | `#España` |

#### 5. Mantenimiento y Resiliencia
* **Base de Datos:** SQLite con almacenamiento persistente de 15 días de histórico.
* **Ciclo de Ingesta:** Automatizado vía `cron` cada 60 minutos.
* **Integridad:** El sistema opera de forma autónoma en hardware dedicado, con despliegue estático en GitHub para asegurar la disponibilidad incluso en caso de fallo de red local.

> **Nota del Operador:** Un nodo **Azul** que súbitamente cambia a **Rojo** con un indicador de **Anomalía** activado sugiere una crisis post-electoral o desestabilización del proceso democrático.
