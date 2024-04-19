CONTAINER_NAME="turuta_back_cont"
IMAGE_NAME="turuta_back_img"
IMAGE_TAG="latest"
PORT_MAP="5000:5000"

if [ $(docker ps -q -f name=^/${CONTAINER_NAME}$) ]; then
    echo "El contenedor ${CONTAINER_NAME} está corriendo. Deteniéndolo..."
    docker stop ${CONTAINER_NAME}
    echo "Contenedor detenido."
else
    echo "El contenedor ${CONTAINER_NAME} no está corriendo."
fi

if [ $(docker ps -aq -f name=^/${CONTAINER_NAME}$) ]; then
    echo "El contenedor ${CONTAINER_NAME} existe. Eliminándolo..."
    docker rm ${CONTAINER_NAME}
    echo "Contenedor eliminado."
fi

if [ $(docker images -q ${IMAGE_NAME}:${IMAGE_TAG}) ]; then
    echo "La imagen ${IMAGE_NAME}:${IMAGE_TAG} existe. Eliminándola..."
    docker rmi ${IMAGE_NAME}:${IMAGE_TAG}
    echo "Imagen eliminada."
fi

echo "Construyendo la imagen Docker ${IMAGE_NAME}:${IMAGE_TAG}..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
echo "Imagen construida."

echo "Ejecutando el contenedor..."
docker run -d -p ${PORT_MAP} --restart unless-stopped --name ${CONTAINER_NAME}  -e NEO4J_URI=neo4j+s://neo4j:EKPkZ-JNRUQ_qYl4C3MspTIimc-a5Dvtc03bW-8H9rw@81995a9d.databases.neo4j.io  ${IMAGE_NAME}:${IMAGE_TAG}
echo "Contenedor ${CONTAINER_NAME} ejecutándose en background."

echo "Validando el estado del contenedor ${CONTAINER_NAME}, ESPERE..."
sleep 5

if [ $(docker ps -q -f name=^/${CONTAINER_NAME}$) ]; then
    echo "El contenedor ${CONTAINER_NAME} está corriendo normalmente. FIN SCRIPT."
else
    echo "El contenedor ${CONTAINER_NAME} NO está corriendo. Verificar el problema."
fi
