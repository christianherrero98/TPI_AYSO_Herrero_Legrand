# TPI_AYSO_Herrero_Legrand
Repositorio destinado a trabajo practico integrador de Arquitectura y Sistemas operativos - UTN

Gestión de Países — Versión Docker

Descripción
Este proyecto contiene la versión en Docker de la aplicación de gestión de países, desarrollada originalmente en Python. La aplicación permite agregar, buscar, filtrar, ordenar y obtener estadísticas de un listado de países, persistiendo los datos en un archivo CSV.
Este mismo trabajo integrador también incluye una comparación con una máquina virtual (Ubuntu Server, virtualizada con UTM, accedida por SSH). El detalle completo de ambos enfoques y la comparación de recursos se encuentra en el informe técnico en PDF.

--------------------------------------
Requisitos previos
--------------------------------------

Tener instalado Docker Desktop
Python versión 3.14

--------------------------------------
Cómo ejecutar el proyecto
--------------------------------------

1  -Clonar este repositorio:
Comando:
git clone <URL-del-repositorio>
cd tp_integrador_docker

2 - Levantar el contenedor con Docker Compose:
Comando:
Docker compose run app

Este comando construye la imagen automáticamente (si no existe todavía) y ejecuta la aplicación de forma interactiva, mostrando el menú principal.
3 -Para salir de la aplicación, seleccionar la opción 8 - Salir del menú. Esto guarda los cambios en datos/paises.csv


Alumnos:
Christian Herrero
Claudio Legrand

