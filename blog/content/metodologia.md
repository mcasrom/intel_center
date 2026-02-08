---
title: "Metodologia"
date: 2026-02-08T23:04:22+01:00
tags: ["metodología", "osint", "documentación"]
featured_image: "/images/metodologia_header.png"
description: "Documentación técnica sobre el procesamiento de datos, umbrales de sentimiento y lógica de alertas."
---

## 1. Introducción
El **Intel Center** opera bajo una arquitectura de "Texto a Números". El motor procesa fuentes globales en tiempo real utilizando Procesamiento de Lenguaje Natural (NLP) para convertir narrativas en indicadores cuantitativos.

## 2. El Semáforo de Tensión (Umbral ±0.05)
Una de las métricas clave es el **Sentimiento Dinámico**. Hemos establecido un umbral de **±0.05** como punto de corte por las siguientes razones técnicas:

* **Ruido Basal Diplomático:** En el lenguaje de noticias, palabras como "preocupación", "discusión" o "negociación" tienen una carga negativa inherente en los diccionarios estándar, pero son normales en geopolítica. 
* **Zona de Neutralidad:** Situar el umbral en 0.05 permite que el sistema ignore las fluctuaciones menores (ruido blanco).
* **Significancia:** Solo cuando el sentimiento acumulado supera el **+0.05 (Verde)** o cae por debajo de **-0.05 (Rojo)**, el nodo considera que hay un cambio de tendencia real en la narrativa regional.

| Rango | Estado | Interpretación |
| :--- | :--- | :--- |
| > +0.05 | 🟢 Estabilidad | Optimismo económico o distensión diplomática. |
| -0.05 a 0.05 | 🟡 Neutral | Ruido mediático estándar / Sin tendencia clara. |
| < -0.05 | 🔴 Hostilidad | Incremento de retórica bélica o inestabilidad social. |

## 3. Diccionario de Pesos y Alertas
El sistema utiliza un filtrado por palabras clave (Keywords) con jerarquía de prioridad. Si una noticia contiene términos de varias categorías, el motor prioriza la de mayor impacto (Líderes > Alertas > Electoral).

### Tabla de Disparo de Alertas
| Categoría | Palabras Clave (Keywords) | Acción del Sistema |
| :--- | :--- | :--- |
| **Crítica** | war, military, nuclear, attack, missile, bomb | Disparo de bandera roja 🚩 |
| **Líderes** | trump, putin, jinping, sánchez, milei | Clasificación en "Tablero de Mandatarios" 👤 |
| **Electoral** | election, voto, parliament, poll, campaña | Seguimiento de Vigilancia 🗳️ |

## 4. Arquitectura del Flujo de Datos
El nodo Odroid-C2 sigue un ciclo de 4 etapas: Ingesta (RSS) -> Clasificación (Python) -> Almacenamiento (SQLite) -> Visualización (Hugo/Git).



---
*Nota: Este sistema se actualiza cada hora. Los datos históricos se mantienen durante 15 días para garantizar la relevancia de las gráficas de tendencia.*
