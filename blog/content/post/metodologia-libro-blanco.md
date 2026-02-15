---
title: "Metodología OSINT: El Libro Blanco del Nodo"
date: 2026-02-08T23:04:22+01:00
report_types: ["metodologia"]  # <--- SIN TILDE
tags: ["metodologia", "osint"]
---


### 1. Introducción
El Intel Center opera bajo una arquitectura de **"Texto a Números"**. El motor procesa fuentes globales en tiempo real utilizando NLP para convertir narrativas en indicadores cuantitativos.



### 2. El Semáforo de Tensión (Umbral ±0.05)
Hemos establecido un umbral de **±0.05** para filtrar el "Ruido Basal Diplomático" (palabras como "preocupación" o "discusión" que sesgan los diccionarios estándar).

| Rango | Estado | Interpretación |
| :--- | :--- | :--- |
| **Electoral** | 🔵 Azul | Vigilancia de procesos democráticos activos. |
| **> +0.05** | 🟢 Estabilidad | Optimismo económico o distensión diplomática. |
| **-0.05 a 0.05** | 🟡 Neutral | Ruido mediático estándar / Sin tendencia clara. |
| **< -0.05** | 🔴 Hostilidad | Incremento de retórica bélica o inestabilidad. |



### 3. Jerarquía y Datos
* **Prioridad**: Líderes > Alertas Críticas > Vigilancia Electoral.
* **Persistencia**: Ventana de **15 días** en base de datos SQLite.
* **Actualización**: Ejecución programada cada **60 minutos**.

---
*Documento sincronizado con el Manual de Operaciones v2.1 bajo el tag #Metodología.*
---
*Nota: Este sistema se actualiza cada hora. Los datos históricos se mantienen durante 15 días para garantizar la relevancia de las gráficas de tendencia.*
