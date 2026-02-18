---
title: "Arquitectura del Sistema: Inteligencia en Tiempo Real con Alta Disponibilidad"
date: 2026-02-18T08:30:00+01:00
draft: false
tags: ["Arquitectura", "OSINT", "Odroid-C2", "Sistemas", "Redundancia", "Failover", "AltaDisponibilidad"]
categories: ["Infraestructura", "Soberanía de Datos"]
author: "Odroid-C2 Cluster"
background_image: "/images/monitor_intel_center_architecture.png" # Mantener la original o actualizar si la nueva imagen es para el fondo.
---

### Descripción General del Flujo de Datos

El Intel Center opera sobre una **infraestructura descentralizada y redundante** en hardware dedicado (Odroid-C2). El sistema se divide en **cinco capas críticas** que garantizan la transformación de ruido mediático en inteligencia accionable, incluso frente a fallos de hardware.

21 ![Arquitectura del Clúster de Inteligencia OSINT con Redundancia](images/intel_center_architecture_redundancy.png)

---

### **Arquitectura del Clúster (Redundancia Activo-Pasivo)**

Aquí se muestra la interconexión lógica de los nodos y el flujo de la inteligencia, destacando la robustez del sistema de failover.

![Arquitectura General del Sistema OSINT](/images/monitor_intel_center_architecture.png)


---

### Las Cinco Capas Críticas del Sistema

#### 1. Capa de Ingestión (Fuentes OSINT)

El sistema monitoriza fuentes externas mediante APIs de noticias y canales RSS/Feeds. Esta capa filtra la entrada inicial basándose en los **8 ejes estratégicos** definidos, incluyendo la reciente incorporación de vectores geográficos específicos para una cobertura más granular. La información de esta capa alimenta directamente al motor de análisis.

#### 2. Motor de Análisis (NLP & Clasificación)

Este es el cerebro del sistema. El texto crudo es procesado mediante:
* **Clasificación Heurística**: Identificación de Mandatarios, Alertas Críticas (militar, conflictos) y Procesos Electorales, categorizando la información para un acceso rápido.
* **Análisis de Sentimiento**: Cálculo de índices de polaridad con un umbral de seguridad de **±0.05** para neutralizar el sesgo inherente a los medios y obtener una valoración más objetiva.

#### 3. Persistencia (Base de Datos de Tendencias Sincronizada)

Los índices de polaridad y las etiquetas de categoría se almacenan en una base de datos **SQLite** local.
* **Retención**: Se mantiene una ventana deslizante de **15 días** de datos históricos.
* **Redundancia de Datos**: A diferencia de una configuración tradicional, esta base de datos es **sincronizada activamente** a través de un repositorio Git, garantizando que ambos nodos (Principal y Respaldo) tengan la última versión de la inteligencia procesada. Esto es clave para la continuidad operativa.
* **Propósito**: Permite al sistema comparar el flujo actual con la media histórica para detectar anomalías en tiempo real.

#### 4. Alta Disponibilidad y Failover (La Capa de Resistencia)

Esta es la nueva capa fundamental para la robustez del Intel Center.
* **Monitorización Proactiva**: Un script `watchdog_intel.sh` se ejecuta periódicamente (cada 15 minutos vía Cron) en el Nodo de Respaldo (`192.168.1.154`). Este script envía un `ping` al Nodo Principal (`192.168.1.147`).
* **Activación del Failover**: Si el Nodo Principal no responde, el Nodo de Respaldo inicia automáticamente el ciclo completo:
    1.  **Sincronización de Emergencia**: Realiza un `git pull` para asegurar la última versión de la base de datos y los scripts desde el repositorio.
    2.  **Asunción de Rol**: Ejecuta el orquestador `run_intel.sh`, asumiendo las tareas de ingesta, análisis y despliegue que normalmente realiza el nodo principal.
* **Tiempos de Recuperación**: Este proceso garantiza un tiempo medio de recuperación (MTTR) de **menos de 15 minutos**, minimizando la interrupción del servicio.

#### 5. Visualización (Interfaz Web Intel Center)

La capa final utiliza el generador de sitios estáticos **Hugo** (con el tema Ananke), que reconstruye un sitio web ligero y rápido.
* **Despliegue Continuo**: El motor reconstruye el sitio cada 60 minutos o inmediatamente después de detecciones críticas y, por supuesto, tras un evento de failover.
* **Accesibilidad**: Proporciona una interfaz táctica optimizada para el análisis rápido de la tensión global, con mapas de calor y gráficos de tendencia.

---
*Nota técnica: Toda la arquitectura corre bajo entorno Linux (DietPi) optimizado para bajo consumo y alta disponibilidad, garantizando una operación resiliente y eficiente.*
