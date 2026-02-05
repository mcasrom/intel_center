---
title: "Manual de Operaciones: Interpretación de Nodos y Mapas"
date: 2026-02-05T09:45:00Z
description: "Protocolo técnico para la lectura de la carga informativa global"
type: "post"
---

### 1. Estructura del Mapa de Calor
La visualización en tiempo real utiliza un motor de densidad de puntos basado en **frecuencia de cables**.

* **Geolocalización:** Los puntos no indican el lugar exacto del suceso, sino el **Nodo de Emisión** de la fuente de inteligencia (ej. el nodo de Medio Oriente se centra en la sede de monitorización de Al Jazeera).
* **Escala de Intensidad:** El radio del círculo es directamente proporcional al volumen de noticias capturadas en las últimas **24 horas**. 
    * *Intensidad 10-20:* Flujo informativo estándar.
    * *Intensidad >30:* Alerta de saturación o evento geopolítico en curso.

### 2. Metodología de Captura (OSINT)
El sistema opera bajo una arquitectura Linux independiente que ejecuta ciclos de captura cada 6 horas:

1.  **Ingesta:** Conexión cifrada a feeds RSS de agencias gubernamentales y de prensa global.
2.  **Normalización:** Los datos se limpian de metadatos innecesarios y se eliminan duplicados mediante una base de datos SQLite.
3.  **Despliegue:** Hugo compila los reportes estáticos para garantizar máxima velocidad de carga y seguridad ante ataques externos.

### 3. Fuentes Monitorizadas
Para garantizar la neutralidad y la cobertura global, el nodo sincroniza con:
* **TASS:** Movimientos en el eje Rusia/Eurasia.
* **Al Jazeera:** Dinámicas en el Golfo y Oriente Próximo.
* **Nikkei Asia:** Indicadores económicos y militares en el Pacífico.
* **DW / BBC / The Guardian:** Perspectiva occidental y eventos en las Américas.

> **Aviso:** Este centro de inteligencia es automatizado. Los picos de intensidad en el mapa deben ser contrastados con los informes detallados en la sección lateral.
