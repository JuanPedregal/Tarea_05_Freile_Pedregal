"""
Model exported as python.
Name : model1
Group : 
With QGIS : 31608
"""
# Se importan los paquetes necesarios para estos procesos

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# Se crea el algoritmo con nombre "Model1" 
class Model1(QgsProcessingAlgorithm):

    # Se define la función "initAlgorithm" cuya variable es "self"
    def initAlgorithm(self, config=None):
        # Con .addParameter se agregan parámetros a self para que lo ejecute la función. En este caso, cada parametro es un proceso que realiza qgis.
        
        # Le agregamos una enumeración a las variables (un ID autoincremental) con 'Autoinc_id'
        self.addParameter(QgsProcessingParameterFeatureSink('Autoinc_id', 'autoinc_id', type=QgsProcessing.TypeVectorAnyGeometry, 
                                                            createByDefault=True, supportsAppend=True, defaultValue=None))
        
        self.addParameter(QgsProcessingParameterFeatureSink('Length', 'length', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, 
                                                            supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Field_calc', 'field_calc', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, 
                                                            supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output_menor_a_11', 'OUTPUT_menor_a_11', type=QgsProcessing.TypeVectorAnyGeometry, 
                                                            createByDefault=True, defaultValue=None))
        # Proceso para arreglar las geometrias 'Fix_geo'
        self.addParameter(QgsProcessingParameterFeatureSink('Fix_geo', 'fix_geo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, 
                                                            supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Widsout', 'widsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, 
                                                            supportsAppend=True, defaultValue=None))
    # Se define otra funcion que usará a self para ejecutar los 6 procesos
    def processAlgorithm(self, parameters, context, model_feedback):
        feedback = QgsProcessingMultiStepFeedback(6, model_feedback)
        results = {}
        outputs = {}

        # Primero se corrigen las geometrías, para esto se utiliza el archivo langa.shp 
        alg_params = {
            'INPUT': 'C:/Udesa/Herramientas/Clase_5/input/langa.shp',
            'OUTPUT': parameters['Fix_geo']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fix_geo'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Se agrega un campo auto-incremental que comienza desde el 1 
        alg_params = {
            'FIELD_NAME': 'GID',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['CorregirGeometras']['OUTPUT'],
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Autoinc_id']
        }
        outputs['AgregarCampoQueAutoincrementa'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Autoinc_id'] = outputs['AgregarCampoQueAutoincrementa']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos
        alg_params = {
            'FIELD_LENGTH': 2,
            'FIELD_NAME': 'length',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,
            'FORMULA': 'length(NAME_PROP)',
            'INPUT': outputs['AgregarCampoQueAutoincrementa']['OUTPUT'],
            'OUTPUT': parameters['Length']
        }
        outputs['CalculadoraDeCampos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Length'] = outputs['CalculadoraDeCampos']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Filtro de entidad
        alg_params = {
            'INPUT': outputs['CalculadoraDeCampos']['OUTPUT'],
            'OUTPUT_menor_a_11': parameters['Output_menor_a_11']
        }
        outputs['FiltroDeEntidad'] = processing.run('native:filter', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output_menor_a_11'] = outputs['FiltroDeEntidad']['OUTPUT_menor_a_11']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos clone
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Inm',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,
            'FORMULA': '\"NAME_PROP\"',
            'INPUT': outputs['FiltroDeEntidad']['OUTPUT_menor_a_11'],
            'OUTPUT': parameters['Field_calc']
        }
        outputs['CalculadoraDeCamposClone'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Field_calc'] = outputs['CalculadoraDeCamposClone']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s)
        alg_params = {
            'COLUMN': ['ID_ISO_A3','ID_ISO_A2','ID_FIPS','NAM_LABEL','NAME_PROP','NAME2','NAM_ANSI','CNT','C1','POP','LMP_POP1','G','LMP_CLASS','FAMILYPROP','FAMILY','langpc_km2','length'],
            'INPUT': outputs['CalculadoraDeCamposClone']['OUTPUT'],
            'OUTPUT': parameters['Widsout']
        }
        outputs['QuitarCampos'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Widsout'] = outputs['QuitarCampos']['OUTPUT']
        return results

    def name(self):
        return 'model1'

    def displayName(self):
        return 'model1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model1()
