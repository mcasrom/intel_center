#!/bin/bash
# Lanzador de entorno de desarrollo local

cd ~/intel_center_test/blog

echo -e "\e[34m[*] Levantando servidor local en puerto 1313...\e[0m"
echo -e "\e[34m[*] URL: http://localhost:1313/intel_center/\e[0m"

# Ejecuta Hugo con:
# -D (ver borradores)
# --disableFastRender (para que no ignore cambios de CSS/Layouts)
# --navigateToChanged (te lleva a la página que editas)
hugo server -D --disableFastRender --navigateToChanged
