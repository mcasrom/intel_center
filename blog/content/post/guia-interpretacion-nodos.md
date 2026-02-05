---
title: "📌 MANUAL: Interpretación de Nodos y Mapas"
date: 2026-02-05T10:15:00Z
description: "Protocolo técnico para la lectura de la carga informativa global y nodos regionales."
type: "post"
weight: 1
---

### Protocolo de Lectura Operativa
Este documento constituye la base metodológica para la interpretación de los datos dinámicos desplegados en el Intel Center.

#### 1. Dinámica del Mapa de Calor
* **Intensidad Geográfica:** El radio y la opacidad de los círculos son directamente proporcionales al volumen de cables procesados exclusivamente en las últimas **24 horas**.
* **Umbrales de Alerta (Normalización):**
    * **Valor 15:** Indica un flujo informativo estándar y estabilidad en el nodo regional.
    * **Valor >30:** Identificado como un "Hotspot". Sugiere una crisis diplomática, militar o humanitaria en desarrollo que requiere atención inmediata.

#### 2. Nodos de Inteligencia y Cobertura
El centro de datos monitoriza actualmente siete ejes estratégicos mediante fuentes de inteligencia de código abierto (OSINT):

| Región | Nodo Principal | Alcance Operativo |
| :--- | :--- | :--- |
| **Eurasia** | TASS | Federación Rusa, Estados post-soviéticos y Europa del Este. |
| **Medio Oriente** | Al Jazeera | Mundo Árabe, Golfo Pérsico e Irán. |
| **África Sahel** | Africanews | Franja del Sahel (Mali, Níger, Chad) y África Subsahariana. |
| **Asia-Pacífico** | Nikkei Asia | Mercado asiático, Mar de China Meridional y Japón. |
| **Europa** | Deutsche Welle | Dinámicas de la Unión Europea y geopolítica continental. |
| **Américas (LATAM)** | BBC Mundo / Jornada | América Latina, Cono Sur y México. |
| **Américas (Norte)** | The Guardian | Política interna y defensa en USA y Canadá. |

#### 3. Ciclo de Vida y Gestión del Dato
* **Sincronización:** Los informes se generan y compilan automáticamente cada **6 horas**.
* **Housekeeping:** La base de datos realiza una rotación y purga cada **30 días** para eliminar ruido histórico y garantizar la relevancia operativa de las búsquedas.
* **Integridad:** El sistema opera bajo una arquitectura Linux pura, libre de dependencias de software privativo, asegurando la trazabilidad del dato desde la ingesta hasta la visualización.

> **Aviso de Seguridad:** Este nodo es un agregador automatizado. La presencia de un punto de alta intensidad debe ser contrastada con los informes individuales generados en la sección cronológica inferior.
