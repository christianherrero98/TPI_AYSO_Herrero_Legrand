# 1. Trae el motor de Python 3.14 en su versión más liviana. 
# funciona como la base del contenedor
FROM python:3.14-slim

# 2. WORKDIR ->  crea una carpeta llamada "app" adentro del contenedor 
# y se "mueve" automáticamente ahí adentro. Es el equivalente a hacer `mkdir /app` y luego `cd /app`.
WORKDIR /app

# 3. COPY agarra el  archivo de Python que tenemos en la pc  y lo pega adentro del contenedor.
# El punto "." al final significa pegá el archivo exactamente en la carpeta donde estoy parado ahora
COPY gestion_de_paises.py .

# 4. CMD es la instrucción final. Le dice al contenedor: 
# "Apenas te enciendas, ejecutá este comando en consola". 
CMD ["python3", "gestion_de_paises.py"]
