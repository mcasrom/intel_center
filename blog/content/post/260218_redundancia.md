---
title: "Soberanía de Datos y Alta Disponibilidad en el Edge"
date: 2026-02-18T08:15:00+01:00
draft: false
tags: ["documentacion", "metodologia", "redundancia", "failover", "Odroid", "OSINT"]
summary: "Implementación de un sistema de redundancia crítica utilizando hardware Odroid C2 para garantizar la persistencia de inteligencia geopolítica."
---

### Introducción

Un sistema de inteligencia OSINT que depende de un solo punto de fallo es, por definición, frágil. Para que el análisis de sentimiento geopolítico y la monitorización de noticias sean robustos, he evolucionado la infraestructura hacia un sistema de **Failover Activo-Pasivo**. El objetivo: si el Nodo Principal cae, la arquitectura se autogestiona.

---

### La Metodología: "Always Ready"

No se trata solo de copiar archivos, sino de asegurar que la **inteligencia acumulada** sea persistente. La metodología se basa en tres pilares:

1. **Sincronización de Estado (Data Persistence):** La base de datos SQLite (`news.db`) se integra en el flujo de Git. Esto garantiza que el historial de varianza y sentimiento esté disponible en cualquier nodo del clúster en tiempo real.
2. **Vigilancia Activa (Heartbeat):** El nodo secundario actúa como un centinela silencioso, verificando la salud del primario mediante un protocolo ICMP optimizado.
3. **Failover Automatizado:** En caso de interrupción del nodo `192.168.1.147`, el nodo de respaldo `192.168.1.154` descarga el último estado conocido y asume las tareas de procesamiento.

---

### Implementación Técnica y Aseguramiento

Para asegurar la longevidad del hardware (protegiendo las tarjetas eMMC/SD), el sistema implementa una política de logs inteligentes:

* **Estado Nominal:** El sistema solo mantiene un "latido" (heartbeat) confirmando que la red es estable.
* **Estado Crítico:** Solo bajo fallo real se activa el registro detallado en el historial de failover.

Esta aproximación permite un tiempo medio de recuperación (**MTTR**) de máximo 15 minutos, garantizando la continuidad del portal de inteligencia.

---

### Arquitectura del Clúster

```text
       +-----------------------+           +-----------------------+
       |   NODO 1 (Principal)  |           |   NODO 2 (Respaldo)   |
       |     192.168.n.nn1     |           |     192.168.n.nn2     |
       +-----------+-----------+           +-----------+-----------+
                   |                                   |
           [EJECUTA SCRIPTS]                   [WATCHDOG CRON]
      (Noticias -> DB -> Hugo)               (Ping cada 15 min)
                   |                                   |
                   v                                   |
       +-----------------------+           +-----------v-----------+
       |   REPOSITORIO GITHUB  | <-------+ | ¿Responde Nodo 1?     |
       |  (news.db + Site)     |           | NO -> [INICIAR FAILOVER]|
       +-----------------------+           +-----------+-----------+
                   ^                                   |
                   |                                   |
                   +-----------------------------------+
