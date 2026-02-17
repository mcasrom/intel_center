---
title: "Acerca del Proyecto"
date: 2026-02-04
layout: "about"
tags: ["OSINT", "NLP", "Big Data", "Geopolítica"]
status: "Operational"
---

### 📡 Descripción del Sistema
El **Intel Center 2026** no es un simple agregador de noticias; es un **pipeline de procesamiento ETL** (Extract, Transform, Load) diseñado para hardware de bajos recursos pero alta fiabilidad (**Odroid-C2**). El sistema funciona de forma autónoma, analizando miles de palabras por hora para detectar cambios de fase en la narrativa global.



### 📊 Regiones de Vigilancia Estratégica
El nodo supervisa actualmente 11 vectores de inteligencia, clasificados por su relevancia en la estabilidad mundial:

| Vector | Descripción Operativa | Fuentes Clave |
| :--- | :--- | :--- |
| **USA_NORTE** | Eje de política interior y exterior estadounidense. | The Guardian, Reuters |
| **ESPAÑA** | Monitoreo de estabilidad institucional y política europea. | El País, RTVE |
| **INDIA_CORE** | Sensor de potencia emergente y estabilidad en el Sudeste Asiático. | The Hindu |
| **CHINA_CORE** | Vigilancia de movimientos estratégicos de Beijing. | Nikkei Asia |
| **Rusia_Eurasia** | Seguimiento de la actividad del Kremlin y Europa del Este. | TASS, DW |
| **Medio_Oriente** | Alertas tempranas en zonas de conflicto activo. | Al Jazeera |
| **ARG/BRA** | Pulso político y económico de la zona Cono Sur. | Clarín, Agencia Brasil |

### 🧠 Metodología y Cálculos de Sentimiento
El núcleo del análisis reside en la cuantificación de la semántica mediante **Procesamiento de Lenguaje Natural (NLP)**.

#### 1. Índice de Sentimiento Crudo ($S$)
Utilizamos un motor basado en **TextBlob** adaptado para la jerga diplomática y militar. Cada titular recibe un puntaje:
$$S = \frac{\sum (Polaridad \times Peso_{keyword})}{N}$$
* **Peso Militar**: Palabras como "Nuclear", "Missile" o "Attack" aplican un multiplicador de impacto al sentimiento negativo.
* **Peso Diplomático**: "Agreement", "Talks" o "Summit" suavizan la polaridad.

#### 2. Radar de Varianza (Delta $\Delta$)
Este es nuestro indicador más potente. Compara el sentimiento acumulado de las últimas 24h ($T_{hoy}$) frente al periodo previo ($T_{ayer}$):
$$\Delta = T_{hoy} - T_{ayer}$$
* **$\Delta > +0.05$**: Proceso de **Distensión**.
* **$\Delta < -0.05$**: Alerta de **Escalada** informativa.



### 🛰️ Procesamiento Geográfico y Hotspots
Para la visualización en el mapa global, el sistema genera dinámicamente el archivo `hotspots.json`. 
* **Latitud/Longitud**: Coordenadas fijas en centros de decisión (Washington, Beijing, Madrid, Delhi).
* **Intensidad Visual**: Calculada según el volumen de noticias ($V$) y la desviación del sentimiento ($D$). 
* **Blindaje de Datos**: El nodo incluye una lógica de redundancia que mantiene la visibilidad de India y China incluso si sus feeds RSS presentan latencia, asegurando que el mapa nunca pierda su integridad visual.

### 🛠️ Especificaciones Técnicas (Hardware/Software)
* **Host**: Odroid-C2 (Arquitectura ARM Cortex-A53).
* **OS**: DietPi (Debian 12 derivate) optimizado para minimizar I/O en la microSD.
* **Base de Datos**: SQLite3 con mantenimiento automático (Auto-vacuum) y purga cada 15 días.
* **Motor Estático**: Hugo con orquestación mediante scripts en Python 3.11.

---

### 🛡️ Filosofía de Operación: "No romper lo que funciona"
El desarrollo sigue el principio de robustez industrial. Cada script de automatización (`main_intel.py`) incluye:
1.  **Manejo de Excepciones**: Blindaje ante caídas de red o feeds corruptos.
2.  **Higiene de Logs**: Auditoría constante en `/data/intel_process.log`.
3.  **Rotación de Posts**: Mantenimiento de un histórico de 30 días para evitar la saturación del sistema de archivos.


---

### Descargo de Responsabilidad
La información presentada en este panel es el resultado de un proceso automatizado de captura de noticias de terceros. **Intel Center 2026** no asume responsabilidad alguna por el contenido, veracidad, opiniones o sesgos presentes en las fuentes originales. Este es un experimento técnico de agregación de datos y no constituye asesoramiento político o militar profesional.

---
&copy; 2026 **Intel Center** | Desarrollo y Arquitectura por **M.Castillo**
