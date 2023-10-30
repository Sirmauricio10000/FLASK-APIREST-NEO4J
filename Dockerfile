# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . .

EXPOSE 80

# Instala las dependencias de tu aplicación
RUN pip install -r requirements.txt

# Define el comando de inicio de tu aplicación
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "80"]