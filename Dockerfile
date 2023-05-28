# Selecciona una imagen base con la versión de Python deseada
FROM python:3.10.11

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la carpeta app al directorio de trabajo
COPY app /app/app

# Expone el puerto en el que se ejecutará tu aplicación FastAPI
EXPOSE 8000

# Establece el comando de inicio de tu aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
