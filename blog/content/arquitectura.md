---
title: "Arquitectura del Sistema: Inteligencia en Tiempo Real"
date: 2026-02-09T18:10:00+01:00
draft: false
tags: ["Arquitectura", "OSINT", "Odroid-C2", "Sistemas"]
categories: ["Infraestructura"]
author: "Odroid-C2 Node"
featured_image: "/images/monitor_intel_center_architecture.png"
---

### Descripción General del Flujo de Datos

El Intel Center opera sobre una infraestructura descentralizada en hardware dedicado (Odroid-C2). Siguiendo el diagrama de arquitectura adjunto, el sistema se divide en cuatro capas críticas que garantizan la transformación de ruido mediático en inteligencia accionable.

![Arquitectura General del Sistema OSINT](/images/monitor_intel_center_architecture.png)

#### 1. Capa de Ingestión (Fuentes OSINT)
El sistema monitoriza fuentes externas mediante APIs de noticias y canales RSS/Feeds. Esta capa filtra la entrada inicial basándose en los **8 ejes estratégicos** definidos (incluyendo la reciente incorporación del nodo Sudamérica para Brasil y Argentina).

#### 2. Motor de Análisis (NLP & Clasificación)
Es el núcleo del sistema. Aquí, el texto crudo es procesado mediante:
* **Clasificación Heurística**: Identificación de Mandatarios, Alertas Críticas y Procesos Electorales.
* **Análisis de Sentimiento**: Cálculo de índices de polaridad con un umbral de seguridad de **±0.05** para neutralizar el sesgo diplomático.

#### 3. Persistencia (Base de Datos de Tendencias)
Los índices de polaridad y las etiquetas de categoría se almacenan en una base de datos **SQLite** local. 
* **Retención**: Se mantiene una ventana deslizante de **15 días** de datos.
* **Propósito**: Esta base permite al sistema comparar el flujo actual con la media histórica para detectar anomalías en tiempo real.

#### 4. Visualización (Interfaz Web Intel Center)
La capa final utiliza el generador de sitios estáticos **Hugo** (con el tema Ananke). 
* **Despliegue**: El motor reconstruye el sitio cada 60 minutos o tras detecciones críticas.
* **Accesibilidad**: Proporciona una interfaz táctica optimizada para el análisis rápido de la tensión global.

---
*Nota técnica: Toda la arquitectura corre bajo entorno Linux (DietPi) optimizado para bajo consumo y alta disponibilidad.*
