#!/bin/bash
echo "📦 Empaquetando sistema para Odroid C2..."
tar -czvf intel_project_ready.tar.gz \
    --exclude='blog/public' \
    --exclude='blog/resources' \
    automation/ \
    config/ \
    core/ \
    data/ \
    blog/content/ \
    blog/layouts/ \
    blog/static/ \
    blog/config.toml
echo "✅ Archivo 'intel_project_ready.tar.gz' listo para enviar a DietPi."
