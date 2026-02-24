---
title: "Análisis de Estado - 2026-02-25 00:00"
date: 2026-02-25T00:00:01
layout: "post"
tags: ["monitor", "sistema"]
---

# 🛡️ Dashboard Operativo: Nodo odroid-c2
Actualización: 25/02/2026 00:00:01

## 🌡️ Telemetría de Hardware
- **Temperatura CPU**: 19°C
- **Carga Sistema**:  0.05, 0.03, 0.00
- **Uptime**: up 1 day, 16 hours, 0 minutes

## 📜 Verificación de Scripts Críticos
- ✅ **OK**: /home/dietpi/intel_center_odroid/automation/run_intel.sh
- ✅ **OK**: /home/dietpi/intel_center_odroid/automation/radar_intel.py
- ✅ **OK**: /home/dietpi/intel_center_odroid/automation/analitica_varianza.py
- ✅ **OK**: /home/dietpi/intel_center_odroid/automation/analista_historico.py
- ✅ **OK**: /home/dietpi/intel_center_odroid/automation/analista_mensual.py
- ✅ **OK**: /home/dietpi/scripts/monitor_hw.sh
- ✅ **OK**: /home/dietpi/scripts/archive_data.py

## 📊 Calidad de Ingesta (Últimas 24h)
| Región | Noticias Ingeridas |
| :--- | :--- |
| INDIA_CORE | 183 |
| Rusia_Eurasia | 87 |
| UCRANIA | 78 |
| MAR_CHINA | 72 |
| Medio_Oriente | 67 |


## 📊 Perfil Geo-Estratégico de las Áreas en Observación
| Región | Población | PIB | Religión | Riesgo |
| :--- | :--- | :--- | :--- | :--- |
| **INDIA_CORE** | 1,428M | $3.7T | Hinduismo | Alto |
| **Rusia_Eurasia** | 144M | $2.2T | Ortodoxia | Extremo |
| **Medio_Oriente** | 450M | $4.5T | Islam | Crítico |
| **USA_NORTE** | 335M | $26.9T | Cristian. | Moderado |

## 🕵️ Análisis de Errores (Últimas 12h)
- ⚠️ **Alertas en logs detectadas**:
```text
2026-02-24 06:00:14,868 - ERROR - [46519] - Error en feed ESPAÑA: database is locked
2026-02-24 06:00:20,148 - ERROR - [46519] - Error en feed ARGENTINA: database is locked
2026-02-24 18:00:08,734 - ERROR - [69852] - Error en feed USA_NORTE: database is locked
2026-02-24 18:00:14,311 - ERROR - [69852] - Error en feed ESPAÑA: database is locked
2026-02-24 18:00:19,604 - ERROR - [69852] - Error en feed ARGENTINA: database is locked
```

## 🔄 Redundancia (Espejo .149)
- 🔑 Enlace SSH: **VERIFICADO** (Backup garantizado)

## 💾 Almacenamiento
- **Uso de Disco**: 13%

---
*Auto-reporte generado por el Nodo de Inteligencia odroid-c2.*
