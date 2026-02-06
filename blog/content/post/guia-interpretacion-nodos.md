---
title: "📌 MANUAL: Operaciones e Interpretación de Inteligencia"
date: 2026-02-06T17:00:00Z
description: "Protocolo técnico para la interpretación del Semáforo Geopolítico, Alertas Críticas y Vigilancia Electoral."
type: "post"
weight: 1
featured_image: "images/header_intel.jpg"
---

### Protocolo de Inteligencia Consolidado (v2.0)
Este documento define la metodología de análisis aplicada por el motor OSINT de la Odroid C2 para transformar datos masivos en indicadores tácticos.

#### 1. Semáforo de Tensión y Dinámica Política
El color de cada nodo es un indicador calculado mediante Procesamiento de Lenguaje Natural (NLP) y detección de contextos específicos:

* 🔵 **Nivel 0 (Vigilancia Electoral):** **Color Azul (#3498db)**. Detectado mediante keywords de procesos democráticos. Indica que la región está en fase de campaña, votación o transición de poder. Prevalece sobre el sentimiento si hay actividad electoral activa.
* 🟢 **Nivel 1 (Estabilidad):** Polaridad > 0.1. El flujo sugiere cooperación, acuerdos o normalidad.
* 🟡 **Nivel 2 (Informativo/Neutral):** Polaridad entre -0.1 y 0.1. Noticias de carácter técnico o administrativo.
* 🔴 **Nivel 3 (Crisis/Hostilidad):** Polaridad < -0.1. Detección de lenguaje agresivo, conflictos o inestabilidad grave.



#### 2. Clasificación de Alertas en el Informe
El sistema segrega la información en tres niveles de prioridad para optimizar el tiempo del analista:
1.  **Vigilancia Electoral (🗳️):** Seguimiento de urnas, candidatos y procesos democráticos.
2.  **Alertas Críticas (🚩):** Eventos con términos de alta peligrosidad (Nuclear, Ataque, Misil, Golpe).
3.  **Resumen Global (🌍):** Flujo informativo estándar para contexto general.

#### 3. Detección de Anomalías (⚠️)
El motor compara el volumen de noticias actual con la media móvil de los últimos 7 días. Una anomalía (`anomaly: true`) indica que la región está generando un interés informativo inusual, lo cual suele preceder a eventos de gran impacto.

#### 4. Cobertura de Nodos Activos
El despliegue actual monitoriza 11 ejes estratégicos mediante fuentes directas:

| Región | Indicador Clave | Alcance Operativo |
| :--- | :--- | :--- |
| **Rusia_Eurasia** | Tensión Bélica | Rusia, Ucrania y Asia Central. |
| **Medio_Oriente** | Geopolítica Energética | Mundo Árabe e Irán. |
| **Africa_Sahel** | Seguridad Regional | Inestabilidad y movimientos insurgentes. |
| **USA_NORTE** | Dinámica Electoral | Política federal y defensa en EE.UU. |
| **MEXICO** | Seguridad Interna | Frontera y política nacional. |
| **Europa_DW** | Estabilidad UE | Dinámicas continentales y diplomacia. |

#### 5. Mantenimiento y Resiliencia
* **Base de Datos:** SQLite con almacenamiento persistente de 7 días de histórico.
* **Ciclo de Ingesta:** Automatizado vía `cron` cada 180 minutos.
* **Integridad:** El sistema opera de forma autónoma en hardware dedicado, con despliegue estático en GitHub para asegurar la disponibilidad incluso en caso de fallo de red local.

> **Nota del Operador:** Un nodo **Azul** que súbitamente cambia a **Rojo** con un indicador de **Anomalía** activado sugiere una crisis post-electoral o desestabilización del proceso democrático.
