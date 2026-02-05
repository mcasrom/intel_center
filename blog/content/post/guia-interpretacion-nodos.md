---
title: "📌 MANUAL: Operaciones e Interpretación de Inteligencia"
date: 2026-02-05T18:00:00Z
description: "Protocolo técnico para la interpretación del Semáforo Geopolítico y Alertas Críticas."
type: "post"
weight: 1
featured_image: "images/header_intel.jpg"
---

### Protocolo de Inteligencia Avanzada (Plus)
Este documento define la metodología de análisis aplicada por el motor OSINT para transformar datos en bruto en indicadores de tensión global.

#### 1. Semáforo de Tensión Geopolítica
A diferencia de versiones anteriores, el color del nodo no es estético, sino un indicador de **sentimiento analítico** procesado mediante Procesamiento de Lenguaje Natural (NLP):

* 🟢 **Nivel 1 (Estabilidad):** Polaridad > 0.1. El flujo informativo sugiere cooperación, acuerdos o normalidad institucional.
* 🟡 **Nivel 2 (Informativo):** Polaridad entre -0.1 y 0.1. Reportes estándar o noticias de carácter técnico/administrativo.
* 🔴 **Nivel 3 (Crisis/Tensión):** Polaridad < -0.1. El sistema ha detectado lenguaje hostil, conflictos o inestabilidad social.



#### 2. Watchlist y Alerta Temprana (🚨)
El sistema ejecuta un escaneo de palabras clave críticas en cada ciclo de ingesta. Los eventos que contienen términos de alta prioridad se segregan automáticamente en la sección **"ALERTAS DE ALTA PRIORIDAD"** del informe diario.
* **Términos de Vigilancia:** Golpe, Nuclear, Ataque, Misil, Emergencia, Crisis, Dictador, Coup.

#### 3. Red Global de Nodos (Cobertura Actualizada)
El despliegue actual cubre 11 ejes estratégicos:

| Región | Fuente Primaria | Alcance Operativo |
| :--- | :--- | :--- |
| **Eurasia** | TASS | Rusia, Europa del Este y Asia Central. |
| **Medio Oriente** | Al Jazeera | Mundo Árabe, Golfo Pérsico e Irán. |
| **África Sahel** | Africanews | Franja del Sahel y África Subsahariana. |
| **Asia-Pacífico** | Nikkei Asia | China, Japón y Sudeste Asiático. |
| **Europa Central** | DW | Unión Europea y dinámica continental. |
| **LATAM** | BBC / Jornada | Cono Sur, Región Andina y México. |
| **Norteamérica** | The Guardian | Política y Defensa en USA. |
| **Ártico** | Arctic Today | Groenlandia y geopolítica del deshielo. |
| **Oceanía** | ABC News | Australia y el eje del Pacífico Sur. |
| **Canadá** | CBC | Región Norte y política transatlántica. |

#### 4. Arquitectura de Datos y Resiliencia
* **Análisis NLP:** Implementado mediante librerías de procesamiento de texto integradas en el pipeline de Python.
* **Integridad Linux:** El sistema corre en un entorno Debian/Ubuntu, optimizado para resiliencia en hardware dedicado (Odroid/Vivobook) con base de datos SQLite en modo WAL (Write-Ahead Logging).
* **Visualización:** Renderizado dinámico sobre Leaflet.js con capas de mapa oscuras para reducir la fatiga visual en entornos de monitorización continua.

> **Nota del Operador:** Un nodo en color **Rojo Carmesí** con un valor de intensidad **>15** constituye una alerta de grado operativo. Se recomienda verificar inmediatamente el enlace directo en el informe diario.
