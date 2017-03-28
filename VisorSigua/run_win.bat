@echo off
set VISOR_FOLDER=%~dp0 
set OSGEO4W_ROOT=C:\Program Files\QGIS 2.18
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis
rem segunda parte
set GDAL_DATA=%OSGEO4W_ROOT%\share\gdal
set PYTHONPATH=%OSGEO4W_ROOT%\apps\Python27;%OSGEO4W_ROOT%\apps\Python27\lib;%OSGEO4W_ROOT%\apps\Python27\sip;%OSGEO4W_ROOT%\apps\qgis\python
path %OSGEO4W_ROOT%\bin;%OSGEO4W_ROOT%\apps\qgis\bin;%WINDIR%\system32;%WINDIR%;%WINDIR%\WBem;%PATH%
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python27
rem ejecuta python script
REM cd C:\visorSigua
cd %VISOR_FOLDER%
python main.py
