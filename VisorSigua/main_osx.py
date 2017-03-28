# -*- coding: utf-8 -*-


import sys

from qgis.core import *
from PyQt4.QtCore import *
from PyQt4 import QtGui,QtSql,QtXml
QtGui.QApplication.addLibraryPath("/Applications/QGIS.app/Contents/PlugIns")
#QgsApplication.setPrefixPath("/Applications/QGIS.app/Contents/PlugIns", True)
#QgsApplication.setPrefixPath("/Applications/QGIS.app/Contents/MacOS", True)
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from PyQt4.QtXml import QDomDocument
#QgsApplication.setPrefixPath("/Applications/QGIS.app/Contents/MacOS", True)

import colorbrewer
import dbsettings
import time

from qgis.gui import *
from qgis import *
from qgis import QgsGeometry
import os

qgis_prefix = "/Applications/QGIS.app/Contents/MacOS" #os.getenv("QGISHOME")



#from PyQt4 import QtGui # Import the PyQt4 module we'll need
#import sys # We need sys so that we can pass argv to QApplication

import form # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer

class runApp(QtGui.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined

        # MI CÓDIGO VA AQUÍ

        # cargar combo
        db = QSqlDatabase('QPSQL')
        db.setHostName(dbsettings.params[0])
        db.setDatabaseName(dbsettings.params[2])
        db.setUserName(dbsettings.params[3])
        db.setPassword(dbsettings.params[4])
        db.setPort(5432)
        if (db.open()==False):
            QMessageBox.critical(None, "Database Error", db.lastError().text())

        ok = db.open()
        if ok:
            sql = "select cod_zona || cod_edificio ||'PB'||' - ' || txt_edificio ||' (PLANTA BAJA)' as zzee from edificios WHERE pb=true  UNION select cod_zona || cod_edificio ||'P1'||' - ' || txt_edificio ||' (PLANTA 1)'  as zzee from edificios WHERE p1=true UNION select cod_zona || cod_edificio ||'P2'||' - ' || txt_edificio ||' (PLANTA 2)' as zzee from edificios WHERE p2=true  UNION select cod_zona || cod_edificio ||'P3'||' - ' || txt_edificio ||' (PLANTA 3)' as zzee from edificios WHERE p3=true UNION select cod_zona || cod_edificio ||'P4'||' - ' || txt_edificio ||' (PLANTA 4)' as zzee from edificios WHERE p4=true  UNION select cod_zona || cod_edificio ||'PS'||' - ' || txt_edificio ||' (PLANTA SOTANO)' as zzee from edificios WHERE ps=true ORDER BY 1"
            query = db.exec_(sql)
            while query.next():
                zzeetxt = unicode(query.value(0))
                self.comboBox.addItem(zzeetxt)

            db.close()

        # botonera
        self.pushButtonOpen.clicked.connect(self.testMapa)
        self.pushButtonUsos.clicked.connect(self.tematico)
        self.pushButtonDptos.clicked.connect(self.tematico2)
        #self.pushButtonPrint.clicked.connect(self.addLayer)
        self.pushButtonCodigo.clicked.connect(self.labelCodigo)
        self.pushButtonDeno.clicked.connect(self.labelDeno)
        self.pushButtonDirectorio.clicked.connect(self.OpenBrowse)
        self.pushButtonPrint.clicked.connect(self.mapaPlantillaPdf)

        # Visibilidad botones
        self.pushButtonUsos.setEnabled(False)
        self.pushButtonDptos.setEnabled(False)
        self.pushButtonCodigo.setEnabled(False)
        self.pushButtonDeno.setEnabled(False)
        self.pushButtonPrint.setEnabled(False)



        # canvas
        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(QColor(255,255,255))
        self.canvas.enableAntiAliasing(True)
        self.canvas.useImageToRender(False)
        # Se agrega el Map canvas a la ventana principal, dentro del marco
        self.layout = QVBoxLayout(self.frame)
        self.layout.addWidget(self.canvas)
        # mostrar canvas
        self.canvas.show()



        # leyenda
        self.root = QgsProject.instance().layerTreeRoot()
        self.bridge = QgsLayerTreeMapCanvasBridge(self.root, self.canvas)
        self.model = QgsLayerTreeModel(self.root)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.model.setFlag(QgsLayerTreeModel.ShowLegend)
        self.view = QgsLayerTreeView()
        self.view.setModel(self.model)
        # leyenda
        self.LegendDock = QDockWidget("Leyenda", self)
        self.LegendDock.setObjectName("Capas" )
        self.LegendDock.setMinimumWidth(300)
        self.LegendDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.LegendDock.setWidget(self.view)
        self.LegendDock.setContentsMargins (9, 9, 9, 9)
        self.addDockWidget(Qt.RightDockWidgetArea, self.LegendDock)


        # Crear los comportamientos de los botones zoom in/out/pan/zoomFull
        self.actionZoomIn = QAction(QIcon('img/mActionZoomIn.png'),"Acercar", self.frame)
        self.connect(self.actionZoomIn, SIGNAL("activated()"), self.zoomIn)

        self.actionZoomOut = QAction(QIcon('img/mActionZoomOut.png'), "Alejar", self.frame)
        self.connect(self.actionZoomOut, SIGNAL("activated()"), self.zoomOut)

        self.actionPan = QAction(QIcon('img/mActionPan.png'), "Desplazarse", self.frame)
        self.connect(self.actionPan, SIGNAL("activated()"), self.pan)

        self.actionZoomFull = QAction(QIcon('img/mActionZoomFullExtent.png'), "Vista completa", self.frame)
        self.connect(self.actionZoomFull, SIGNAL("activated()"), self.zoomFull)

        # Crear una toolbar
        self.toolbar = self.addToolBar("Map")
        self.toolbar.addAction(self.actionZoomIn)
        self.toolbar.addAction(self.actionZoomOut)
        self.toolbar.addAction(self.actionPan)
        self.toolbar.addAction(self.actionZoomFull)


        # Crear las herramientas (tools) para el mapa
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = Acercar
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = Alejar

    def zoomIn(self):
        """ Acercar """
        self.canvas.setMapTool(self.toolZoomIn)
        print "Acercar"

    def zoomOut(self):
        """ Alejar """		
        self.canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        """ Desplazarse """
        self.canvas.setMapTool(self.toolPan)

    def zoomFull(self):
        """ Vista total """
        self.canvas.zoomToFullExtent()





    # función de prueba para cargar shapefile (no se utiliza)
    def addLayer(self):
        self.borrarRegistro()
        file = QFileDialog.getOpenFileName(self,
                   "Open Shapefile", ".", "Shapefiles (*.shp)")
        fileInfo = QFileInfo(file)

        # Add the layer
        layer = QgsVectorLayer(file, fileInfo.fileName(), "ogr")

        if not layer.isValid():
            raise IOError("Invalid Shapefile")


        # Add layer to the registry
        QgsMapLayerRegistry.instance().addMapLayer(layer)

        # Set extent to the extent of our layer

        self.canvas.setExtent(layer.extent())

        # Set up the map canvas layer set
        c1 = QgsMapCanvasLayer(layer)
        layers = [c1]
        self.canvas.setLayerSet(layers)
        self.canvas.zoomToFullExtent()

        self.canvas.show()


    # Borra del registro la/s capa/s
    def borrarRegistro(self):
        registryLayers = QgsMapLayerRegistry.instance().mapLayers().keys()
        QgsMapLayerRegistry.instance().removeMapLayers( registryLayers )

    # Función para test (no se utiliza)
    def testMsg(self):
        QMessageBox.information(QWidget(), "Hola", u"Esto es un test")

    # Función para abrir cuadro de diálogo ficheros y elegir directorio (no se utiliza)
    def browse_folder(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self,"Pick a folder")

        if directory: # sí el usuario no selecciona un directorio no se continua la función
            for file_name in os.listdir(directory):
                self.listWidget.addItem(file_name)  # añade ficero al listWidget

    def testMapa(self):
        self.borrarRegistro()
        self.canvas.refresh()
        # asignamos variables a las selecciones de los combos
        varZZEEPP = self.comboBox.currentText()[:6]
        varPlanta = varZZEEPP[4:6]
        planta = ("sig"+ varPlanta).lower()
        print varPlanta
        varTocZZEEPP = 'E' + varZZEEPP
        # Añadir layer de PostGIS a QGIS
        uri = QgsDataSourceURI()
        # indicar host name, port, database name, username and password
        uri.setConnection(dbsettings.params[0], dbsettings.params[1],dbsettings.params[2],dbsettings.params[3], dbsettings.params[4])
        sql="(SELECT e.gid, e.codigo,e.coddpto,d.txt_dpto_sigua,e.actividad,a.txt_actividad,a.activresum,e.denominaci,e.observacio,e.geometria FROM "+planta+" e, actividades a, departamentossigua d WHERE e.actividad = a.codactividad AND e.coddpto = d.cod_dpto_sigua AND e.codigo LIKE '"+varZZEEPP+"%')"
        uri.setDataSource("",sql,"geometria","","gid")
        # Definir la vlayer de PostGIS
        layer = QgsVectorLayer(uri.uri(), varTocZZEEPP, "postgres")
        # validar
        if not layer.isValid():
            QMessageBox.critical(QWidget(), "ERROR", "Layer failed to load!")
        #else:
            #QMessageBox.information(QWidget(), "MENSAJE", "Layer loaded!")
            #QgsMapLayerRegistry.instance().addMapLayers([layer])

        # Visibilidad botones
        self.pushButtonUsos.setEnabled(True)
        self.pushButtonDptos.setEnabled(True)
        self.pushButtonCodigo.setEnabled(True)
        self.pushButtonDeno.setEnabled(True)
        self.pushButtonPrint.setEnabled(True)

        # mostrar capa
        QgsMapLayerRegistry.instance().addMapLayer(layer) # añade capa al registro
        # Define la extensión de nuestra layer
        self.canvas.setExtent(layer.extent())
        # Configura el map canvas layer set
        c1 = QgsMapCanvasLayer(layer)
        layers = [c1]
        self.canvas.setLayerSet(layers)
        self.canvas.zoomToFullExtent()
        self.canvas.show()



    # crea un mapa temático de usos
    def tematico(self):
        layers = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layers.iteritems():
            print name, layer.type()
        usos = {
            u"Administración": ("#b3cde3", u"Administración"),
            "Despacho": ("#fbb4ae", "Despacho"),
            "Docencia": ("#ccebc5", "Docencia"),
            "Laboratorio": ("#decbe4", "Laboratorio"),
            "Salas": ("#fed9a6", "Salas"),
            "Muros": ("#808080", "Muros"),
            "": ("white", "Resto")}
        categorias = []
        for estancia, (color, label) in usos.items():
            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(color))
            category = QgsRendererCategoryV2(estancia, sym, label)
            categorias.append(category)

            field = "activresum"
            index = layer.fieldNameIndex("activresum")
            # comprueba que existe el campo activresum
            if (index == -1):
                QMessageBox.critical(None, "Field error", "No existe el campo activresum. Seleccione la capa adecuada")
                break

            renderer = QgsCategorizedSymbolRendererV2(field, categorias)
            layer.setRendererV2(renderer)
            QgsMapLayerRegistry.instance().addMapLayer(layer)
            layer.triggerRepaint()
            layer.setName(layer.name()[:7] + u' (uso)')
            # actualizar metadatos
            layer.setTitle(u"Planta de edificio " + layer.name() + u' (uso)')
            layer.setAbstract(u"Edificio procedente del Sistema de Informacion Geografica de la Universidad de Alicante (SIGUA)")




    # crea un temático de unidades/dptos
    def tematico2(self):
        layers = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layers.iteritems():
            print name, layer.type()
        # array de dptos
        idx = layer.fieldNameIndex('txt_dpto_sigua')
        dptosArr = layer.uniqueValues( idx )
        total = len(dptosArr)
        if total < 3:
            coloresArr = colorbrewer.Set3[3]
        elif total <= 12:
            coloresArr = colorbrewer.Set3[total]
        else:
            exceso = total - 12
            if exceso < 3:
                coloresArr = colorbrewer.Set3[12] + colorbrewer.Paired[3]
            else:
                coloresArr = colorbrewer.Set3[12] + colorbrewer.Paired[exceso]

        print coloresArr
        dptoDic = {}
        for i in range(0, len(dptosArr)):
            if  dptosArr[i] == u"GESTIÓN DE ESPACIOS":
                dptoDic[dptosArr[i]] = ("white", dptosArr[i])
            else:
                dptoDic[dptosArr[i]] = (coloresArr[i], dptosArr[i])

        #print dptoDic
        categories = []
        for estancia, (color, label) in dptoDic.items():
            sym = QgsSymbolV2.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(color))
            category = QgsRendererCategoryV2(estancia, sym, label)
            categories.append(category)

        field = "txt_dpto_sigua"
        renderer = QgsCategorizedSymbolRendererV2(field, categories)
        layer.setRendererV2(renderer)
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        layer.triggerRepaint()
        layer.setName(layer.name()[:7] + u" (organización)" )
        # actualizar metadatos
        layer.setTitle(u"Planta de edificio " + layer.name() + u" (organización)")
        layer.setAbstract(u"Edificio procedente del Sistema de Información Geográfica de la Universidad de Alicante (SIGUA)")



    def labelCodigo(self):
        layers = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layers.iteritems():
            print name, layer.type()
        #layer = iface.activeLayer()
        palyr = QgsPalLayerSettings()
        palyr.readFromLayer(layer)
        palyr.enabled = True
        palyr.bufferDraw = True
        palyr.bufferColor = QColor("white")
        palyr.bufferSize = 1
        palyr.scaleVisibility = True
        palyr.scaleMax = 2000
        palyr.isExpression = True
        palyr.fieldName =  'if( "codigo" NOT LIKE \'%000\', right(  "codigo" ,3),"")'
        palyr.size = 15
        palyr.textColor = QColor("black")
        palyr.drawLabels = True
        palyr.fitInPolygonOnly = True  #solo dibuja las label que caben dentro del poligono
        palyr.placement = QgsPalLayerSettings.OverPoint
        palyr.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '7', '')
        palyr.writeToLayer(layer)
        self.canvas.refresh()


    def labelDeno(self):
        layers = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layers.iteritems():
            print name, layer.type()
        #layer = iface.activeLayer()
        palyr = QgsPalLayerSettings()
        palyr.readFromLayer(layer)
        palyr.enabled = True
        palyr.bufferDraw = True
        palyr.bufferColor = QColor("white")
        palyr.bufferSize = 1
        palyr.scaleVisibility = True
        palyr.scaleMax = 2000
        palyr.isExpression = False
        palyr.fieldName = 'denominaci'
        palyr.size = 15
        palyr.textColor = QColor("black")
        palyr.drawLabels = True
        palyr.wrapChar = ' '
        palyr.placement = QgsPalLayerSettings.OverPoint
        palyr.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '7', '')
        palyr.writeToLayer(layer)
        self.canvas.refresh()

    # Función para seleccionar un directorio
    def OpenBrowse(self):
        from os.path import expanduser
        self.settings = QSettings()
        home = expanduser("~") # obtiene el /home o el c:\User
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(None, self.tr('Save to directory'), home,options)
        if directory:
            self.lineEditDirectorio.setText(self.settings.value('rootDir', directory))
        else:
            QMessageBox.critical(QWidget(), "ERROR", u"NO se ha indicado un directorio para guardar los archivos")

    # Función para generar un mapa a partir de plantillas
    def mapaPlantillaPdf(self):
        # definir directorio para guardar pdf y png
        directory = self.lineEditDirectorio.text()
        if not directory:
            QMessageBox.critical(QWidget(), "ERROR", u"Indica el directorio para guardar los archivos")
        else:
            registry = QgsMapLayerRegistry.instance()
            layers = QgsMapLayerRegistry.instance().mapLayers()
            for name, layer in layers.iteritems():
                print name, layer.type()

            # Add layer to map render
            myMapRenderer = QgsMapRenderer()
            lst = [layer.id()]
            myMapRenderer.setLayerSet(lst)
            myMapRenderer.setProjectionsEnabled(False)

            self.canvas.refresh()
            extent = layer.extent()
            ms = self.canvas.mapSettings()
            myComposition = QgsComposition(ms)

            # uso plantilla
            import platform
            if (extent.width() > extent.height()):
                tipo = 'h'
                if platform.system() == 'Linux':
                    myFile = 'templates/template_h.qpt'
                if platform.system() == 'Windows':
                    myFile = 'templates/template_hw.qpt'
                if platform.system() == 'Darwin':
                    myFile = 'templates/template_hmac.qpt'
            else:
                # plantilla vertical
                tipo = 'v'
                if platform.system() == 'Linux':
                    myFile = 'templates/template_v.qpt'
                if platform.system() == 'Windows':
                    myFile = 'templates/template_vw.qpt'
                if platform.system() == 'Darwin':
                    myFile = 'templates/template_vmac.qpt'

            myTemplateFile = file(myFile, 'rt')
            myTemplateContent = myTemplateFile.read()
            myTemplateFile.close()
            myDocument = QDomDocument()
            myDocument.setContent(myTemplateContent)
            myComposition.loadFromTemplate(myDocument)

            # Sustituir textos
            substitution_map = {'TITULO': u'TEMÁTICO','EDIFICIO':self.comboBox.currentText(),'FECHA': time.strftime("%d/%m/%Y") ,'AUTOR': u'José Manuel Mira','ORGANISMO': 'Universidad de Alicante'}
            self.setAttribute(Qt.WA_DeleteOnClose) #para evitar warnings en time
            myComposition.loadFromTemplate(myDocument, substitution_map)

            # Definir extensión mapa y ajustar composición
            myMap = myComposition.getComposerMapById(0)
            extent = layer.extent()
            print "oldExtent:"
            print extent.xMinimum ()
            print extent.yMinimum ()
            print extent.xMaximum ()
            print extent.yMaximum ()
            rW = extent.width()
            rH = extent.height()
            print "rW: " + str(rW)
            print "rH: " + str(rH)

            if (tipo == 'v'):
                # recalcular extent
                print "es vertical"
                pH = 255 #alto en mm del recuadro del mapa
                pW =(rW*pH)/rH
                print "pW es: " + str(pW)
                # caso para edificios verticales muy largos (ej: derecho)
                # 200 son los mm del ancho del recuadro del mapa
                if (pW < 200):
                    # recalcular xMax
                    print "caso 1"
                    xMin = extent.xMinimum()
                    print "xMin es "+ str(xMin)
                    yMin = extent.yMinimum()
                    yMax = extent.yMaximum()
                    dXp = 200 - pW
                    print "dXp es " + str(dXp)
                    newXmax = ((rH*(pW+dXp))/pH) + extent.xMinimum()
                    print "newXmax es " + str(newXmax)
                    # centrar mapa
                    deltaX = (newXmax - extent.xMaximum())/2
                    print "deltaX es: "+ str(deltaX)
                    newExtent = QgsRectangle(xMin - deltaX,yMin,newXmax - deltaX,yMax)
                    #newExtent = QgsRectangle(xMin,yMin,newXmax,yMax)
                    print "newExtent:"
                    print str(newExtent.xMinimum ())
                    print newExtent.yMinimum ()
                    print newExtent.xMaximum ()
                    print newExtent.yMaximum ()
                    myMap.setNewExtent(newExtent)

                # caso para edificios verticales muy anchos (ej: 0005PB, EPS III -0014)
                else:
                    # recalcular Ymin
                    print "caso 2"
                    xMin = extent.xMinimum()
                    xMax = extent.xMaximum()
                    yMax = extent.yMaximum()
                    dYp = 255 -pH
                    newYmin = extent.yMinimum() - ((rW*(pH+dYp))/pW)
                    newExtent = QgsRectangle(xMin,newYmin,xMax,yMax)
                    #QMessageBox.information(QWidget(), "New Extent",  str(newExtent.xMinimum ()) + ","+ str(newExtent.yMinimum ()) + ","+ str(newExtent.xMaximum ()) + ","+ str(newExtent.yMaximum ())  )
                    myMap.setNewExtent(newExtent)
                    # pasar extent a composicion
                    #myMap = myComposition.getComposerMapById(0)
                    #myMap.setNewExtent(newExtent)

            if (tipo == 'h'):
                print "mapa horizontal"
                # Hay que diferenciar el caso 1  como el rectorado, que es muy alargado
                # del caso 2, edificios casi alargados, pero casi cuadrados, como el 0039PB (que no sale bien)
                myExtent = layer.extent()
                myMap.setNewExtent(myExtent)

                pW=235
                pH = (pW*rH)/rW
                # caso 1: Edificios muy alargados (ej: 0028, 0007)
                if (pH < 203):
                    newRH = (203*rW)/pW
                    xMin = extent.xMinimum()
                    xMax = extent.xMaximum()
                    yMin = extent.yMinimum()
                    yMax = extent.yMaximum()

                    deltaY = (newRH-rH)/2 #(yMax - newYmin)/2
                    print "deltaY: "+ str(deltaY)
                    newExtent = QgsRectangle(xMin, yMin - deltaY, xMax, yMax + deltaY)
                    myMap.setNewExtent(newExtent)

                # caso 2: edificios alargados, pero casi cuadrados. Ej 0039PB
                else:
                    pH= 203
                    xMin = extent.xMinimum()
                    xMax = extent.xMaximum()
                    yMin = extent.yMinimum()
                    yMax = extent.yMaximum()
                    newRW = (235*rH)/pH
                    newXmax = xMin+newRW
                    print "newXmax: " + str(newXmax)
                    deltaX = (newRW - rW)/2
                    print "deltaX: "+ str(deltaX)
                    newExtent = QgsRectangle(xMin - deltaX, yMin, newXmax - deltaX, yMax)
                    myMap.setNewExtent(newExtent)

                    #myExtent = layer.extent()
                    #myMap.setNewExtent(myExtent)


            # Save image
            salidaPNG = os.path.join(directory, "mapa_" + layer.name() + "_" + time.strftime("%Y%m%d%H%M%S") + ".png")
            self.setAttribute(Qt.WA_DeleteOnClose) #para evitar warnings en time
            myImage = myComposition.printPageAsRaster(0)
            myImage.save(salidaPNG)

            # export PDF
            salidaPDF = os.path.join(directory, "mapa_" + layer.name() + "_" + time.strftime("%Y%m%d%H%M%S") + ".pdf")
            self.setAttribute(Qt.WA_DeleteOnClose) #para evitar warnings en time
            myComposition.exportAsPDF(salidaPDF)

            QMessageBox.information(QWidget(), "Resultado", "Los mapas, " + salidaPNG + " y "+ salidaPDF+ " han sido creados exitosamente.")


def main():

    #app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
    app = QgsApplication([], True)
    # Initialize qgis libraries
    app.setPrefixPath(qgis_prefix, True) # no poner true/false al final
    #app.setPrefixPath("/usr/bin/qgis")


    app.initQgis()

    form = runApp()                 # We set the form to be our runApp (form)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app

    app.exitQgis()



if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function

