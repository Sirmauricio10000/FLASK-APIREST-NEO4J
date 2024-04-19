#!/bin/sh

# Imprime la URI basada en las variables de entorno
echo "Conectando a Neo4j con URI: $NEO4J_URI"

# Ejecuta el comando pasado como argumentos al script (CMD de Dockerfile)
exec "$@"
