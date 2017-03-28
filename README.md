# PySigua
Visor de Sigua desarrollado en Python

Captura de pantalla:
![alt text](https://github.com/josemamira/PySigua/raw/master/VisorSigua/doc/captura_sigua.png "Captura")
### Descripción
Aplicación standalone para ver e imprimir los edificios y plantas de la Universidad de Alicante  utilizando simbología avanzada. Se trata de una aplicación más de SIGUA [www.sigua.ua.es]

### Version
1.0

### Autor
José Manuel Mira Martínez

### Programación
Se trata de un proyecto programado en Python que utiliza
- Librería PyQgis
- Librería PyQt
- El interfaz de usuario (UI) ha sido diseñado con QtDesigner

### Especificaciones
Se trata de un proyecto programado en Python que utiliza
- Librería PyQgis
- Librería PyQt
- El interfaz de usuario (UI) ha sido diseñado con QtDesigner

### Requerimientos
Necesita tener instalado Qgis 2.18 o superior, programa GIS open source. Descargas en http://www.qgis.org/es/site/
No es necesario tener instalado Python, puesto que utiliza la versión instalada en la aplicación Qgis. Se ha testeado con otras versiones de Qgis (2.14) y funciona sin problemas.

### Instalación
> Linux

Solo hay copiar la carpeta. Luego ejecutar el script principal del proyecto en la terminal
```sh
$ cd <Path a la carpeta VisorSigua>
$ python main.py
```
Testeado en Ubuntu (16.04, 14.04), Elementary (Freya, Loki)

> Windows

Copiar la carpeta "VisorSIGUA" a donde se quiera. Por ejemplo en " Documentos"
Ejecutar el fichero batch de arranque "run_win.bat" con un doble clic.
Este fichero llama a las librerías de Python en Qgis. Por defecto está pensaWindowsdo para la versión Qgis 2.18. Se Qgis utiliza otra versión hay que editar la segunda línea, indicando el path a la versión de Qgis
```sh
set OSGEO4W_ROOT=C:\Program Files\QGIS 2.18
```
Recomendamos crear un acceso directo al fichero, que podrás llamar "Visor SIGUA", y ubicarla en el escritorio. Se puede cambiar el icono por el que se proporciona (icono.ico)

Testeado satisfactoriamente en Windows XP, 7, 8 y 10

> Os X

Instalar Qgis 2.18 con el paquete Instalador de Mac para los OS X Mavericks (10.9), Mountain Lion (10.8) y Lion (10.7), procedente de KingChaos Qgis (http://www.kyngchaos.com/software/qgis). Descargar la 
versión 2.18 (http://www.kyngchaos.com/files/software/qgis/QGIS-2.18.2-1.dmg). Durante la instalación es necesario instalar cada paquete por pasos, siguiendo el nº de cada paquete. 

Copiar la carpeta "VisorSIGUA" a donde se quiera. Por ejemplo en "Documentos"
Ejecutar el fichero de bash "run_osx.sh" o bien "run_osx.command"
Recomendamos crear un alias al fichero command, que podrás llamar "Visor SIGUA", y ubicarla en el escritorio. Se puede cambiar el icono por el que se proporciona (icono.ico)
Si se desea abrir por terminal es necesario ejecutar estas líneas
```sh
export PATH="/Applications/QGIS.app/Contents/MacOS/bin:$PATH"
export PYTHONPATH="/Applications/QGIS.app/Contents/Resources/python"
python main_osx.py
```
Testeado en OS X 10.11 El Capitan

### Conexión de base de datos
PySigua se conecta a la geodatabase PostgreSQL con Postgis de SIGUA. Para que esta aplicación funcione se proporciona un fichero dbsettings.pyc ya compilado. Sin embargo si quieres realizar cambios puedes crear un fichero llamado dbsettings.py, con el contenido proporcionado abajo y realizar los cambios pertinentes.
Los parámetros de conexión dados sólo permiten acceso de lectura a la base de datos.

Contenido de dbsettings.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0'
VERSION = tuple(map(int, __version__.split('.')))
params = ['<YOUR IP>', "5432",'<YOUR SIGUA DBNAME>', '<YOUR USER>', '<YOUR PASSWORD>']

```
Para que la aplicación funcione se proporciona un fichero dbsettings.pyc ya compilado

### Funcionamiento
Aplicación extremadamente sencilla de utilizar. Seguir estos pasos:
1. Seleccionar un edificio del combo desplegable y oprimir el botón "Cargar edificio"
2. Cambia la simbolización por usos o por organización
3. Opcionalmente selecciona un etiquetado de estancias por código Sigua o por denominación
4. Crear un PDF y un PNG del edificio. Previamente deberás indicar donde se guardarán los archivos de impresión



