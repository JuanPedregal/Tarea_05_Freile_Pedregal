"""
Model exported as python.
Name : model4a
Group : 
With QGIS : 31608
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Corregir geometrías wlds
        alg_params = {
            'INPUT': 'C:/Udesa/Herramientas/Clase_5/output/clean.shp',
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        outputs['CorregirGeometrasWlds'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_wlds'] = outputs['CorregirGeometrasWlds']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Corregir geometrías countries
        alg_params = {
            'INPUT': 'C:/Udesa/Herramientas/Clase_5/input/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['CorregirGeometrasCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['CorregirGeometrasCountries']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Intersección
        alg_params = {
            'INPUT': outputs['CorregirGeometrasWlds']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': outputs['CorregirGeometrasCountries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        outputs['Interseccin'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Intersection'] = outputs['Interseccin']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Estadísticas por categorías
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': outputs['Interseccin']['OUTPUT'],
            'OUTPUT': 'C:/Udesa/Herramientas/Clase_5/output/idiomas_por_pais.csv',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['EstadsticasPorCategoras'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model4a'

    def displayName(self):
        return 'model4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4a()
