"""
Model exported as python.
Name : model2
Group : 
With QGIS : 31608
"""
# Parte del material obtenido de https://github.com/sebastianhohmann/gis_course/tree/master/QGIS/research_course
# Se prepará "agricultural suitability raster"
# Se importan e instalan los paquetes necesarios
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
import processing

# Se nombra y da inicia al Modelo2
class Model2(QgsProcessingAlgorithm):
    # En este caso solo obtendremos un layer
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Suitout', 'suitout', createByDefault=True, defaultValue=None))
    # Se ejecutaran 2 algoritmos
    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}
        ##########################################
        # Se proyecta el raster hdr.adf en WGS 84
        ##########################################
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': 'C:/Udesa/Herramientas/Clase_5/input/suit/hdr.adf',
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Suitout']
        }
        outputs['CombarReproyectar'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Suitout'] = outputs['CombarReproyectar']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        #########################################################################
        # Se extrae la proyección para crear una proyeccion permanente del raster 
        #########################################################################
        alg_params = {
            'INPUT': outputs['CombarReproyectar']['OUTPUT'],
            'PRJ_FILE_CREATE': True
        }
        outputs['ExtraerProyeccin'] = processing.run('gdal:extractprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model2'

    def displayName(self):
        return 'model2'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model2()
