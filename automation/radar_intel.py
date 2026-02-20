#!/usr/bin/env python3
import sqlite3
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
BASE_DIR = "/home/dietpi/intel_center_odroid"
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
SHORTCODE_PATH = os.path.join(BASE_DIR, "blog/layouts/shortcodes/radar_mapa.html")
MAX_WIDTH = 600

def generar_shortcode_completo():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        # Últimos 7 días, sentimiento != 0
        query = """
            SELECT region, AVG(sentimiento)
            FROM news
            WHERE timestamp > datetime('now','-7 days') AND sentimiento != 0.0
            GROUP BY region
        """
        cur.execute(query)
        datos = cur.fetchall()
        conn.close()

        if not datos:
            print("No hay datos recientes para generar el radar y mapa.")
            return

        labels = [f"'{d[0]}'" for d in datos]
        valores = [str(round((1 - (d[1] or 0)) * 50)) for d in datos]

        html_content = f"""
<div class="radar-wrapper" style="max-width:{MAX_WIDTH}px; margin: 0 auto; padding: 15px; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <canvas id="radarChartIntel"></canvas>
    <p style="text-align:center; font-size:0.9em; color:#555;">Radar de tensión geopolítica (Actualizado: {datetime.now().strftime('%Y-%m-%d %H:%M')})</p>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
(function() {{
    const initRadar = () => {{
        const ctx = document.getElementById('radarChartIntel');
        if (!ctx) return;
        new Chart(ctx, {{
            type: 'radar',
            data: {{
                labels: [{', '.join(labels)}],
                datasets: [{{
                    label: 'Índice de Tensión',
                    data: [{', '.join(valores)}],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(255, 99, 132, 1)'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    r: {{
                        min: 0,
                        max: 100,
                        ticks: {{ stepSize: 20 }}
                    }}
                }}
            }}
        }});
    }};
    if (document.readyState === 'complete') {{ initRadar(); }}
    else {{ window.addEventListener('load', initRadar); }}
}})();
</script>

<div id="map" style="width: 100%; height: 650px; margin-top: 30px; border-radius: 8px; border: 2px solid #333;"></div>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
(function() {{
    var map = L.map('map').setView([20.0, 0.0], 2);
    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
        attribution: '© OpenStreetMap | Intel Center OSINT'
    }}).addTo(map);

    fetch('{BASE_DIR}/data/hotspots.json')
    .then(r => r.json())
    .then(data => {{
        data.forEach(spot => {{
            var radius = Math.max(spot.intensity * 18000, 120000);
            var finalRadius = spot.anomaly ? radius * 2 : radius;
            var color = spot.color || '#00ff00';

            L.circle([spot.lat, spot.lon], {{
                color: color,
                fillColor: color,
                fillOpacity: 0.25,
                weight: spot.anomaly ? 5 : 2,
                radius: finalRadius
            }}).addTo(map);

            var numberIcon = L.divIcon({{
                className: 'number-label',
                html: `<div style="color:${{color}}; font-weight:bold;">${{spot.intensity}}${{spot.anomaly ? '⚠️' : ''}}</div>`,
                iconSize: [60, 40]
            }});
            L.marker([spot.lat, spot.lon], {{icon: numberIcon}}).addTo(map);
        }});
    }})
    .catch(e => console.error("Error cargando hotspots:", e));
}})();
</script>

<style>
.number-label {{
    background: none; border: none; font-weight: bold; font-size: 18px; text-shadow: 2px 2px 4px #000; text-align: center;
}}
</style>
"""
        with open(SHORTCODE_PATH, "w") as f:
            f.write(html_content)

        print(f"Shortcode radar+mapa generado correctamente: {SHORTCODE_PATH}")

    except Exception as e:
        print(f"Error generando shortcode: {e}")

if __name__ == "__main__":
    generar_shortcode_completo()
