"""
Model exported as python.
Name : model3
Group : 
With QGIS : 31608
"""
# Parte del material obtenido de https://github.com/sebastianhohmann/gis_course/tree/master/QGIS/research_course
# Resumen: A partir de archivos raster se calculará la elevación del relieve promedio y la cantidad de población promedio en 1800, 1900 y 2000 por pais
# Se importan e instalan los paquetes necesarios
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing

# Se crea y nombra al modelo 3
class Model3(QgsProcessingAlgorithm):
    # Se obtendrán 7 layers en qgis
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_3', 'fixgeo_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Landq', 'landq', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1800', 'pop1800', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop1900', 'pop1900', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Pop2000', 'pop2000', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Topo', 'topo', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Drop_field_3', 'drop_field_3', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
    # Se correran 8 algoritmos
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(8, model_feedback)
        results = {}
        outputs = {}
        #####################################################################
        # Se arreglan las geometrias del shapefile "ne_10m_admin_0_countries"
        #####################################################################
        alg_params = {
            'INPUT': 'C:/Udesa/Herramientas/Clase_5/input/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_3']
        }
        outputs['CorregirGeometras'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_3'] = outputs['CorregirGeometras']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}
        #########################################################################
        # Se borran columnas tal que solo la base se queda con "ADMIN" y "ISO A3"
        #########################################################################
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9'],
            'INPUT': outputs['CorregirGeometras']['OUTPUT'],
            'OUTPUT': parameters['Drop_field_3']
        }
        outputs['QuitarCampos'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Drop_field_3'] = outputs['QuitarCampos']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}
        #########################################################################################
        # Se calcula el promedio zonal de la calidad de la tierra para la agricultura por pais
        #########################################################################################
        alg_params = {
            'COLUMN_PREFIX': 'landq_',
            'INPUT': outputs['QuitarCampos']['OUTPUT'],
            'INPUT_RASTER': 'C:/Udesa/Herramientas/Clase_5/output/landquality.tif',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Landq']
        }
        outputs['EstadsticasDeZona'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Landq'] = outputs['EstadsticasDeZona']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}
        ##################################################################################
        # Se calcula el promedio zonal de la cantidad de población en el año 1800 por pais
        ##################################################################################
        alg_params = {
            'COLUMN_PREFIX': '1800_',
            'INPUT': outputs['EstadsticasDeZona']['OUTPUT'],
            'INPUT_RASTER': 'C:/Udesa/Herramientas/Clase_5/input/pop/popd_1800AD.asc',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Pop1800']
        }
        outputs['EstadsticasDeZona2'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1800'] = outputs['EstadsticasDeZona2']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}
        ##################################################################################
        # Se calcula el promedio zonal de la cantidad de población en el año 1900 por pais
        ##################################################################################
        alg_params = {
            'COLUMN_PREFIX': '1900_',
            'INPUT': outputs['EstadsticasDeZona2']['OUTPUT'],
            'INPUT_RASTER': 'C:/Udesa/Herramientas/Clase_5/input/pop/popd_1900AD.asc',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Pop1900']
        }
        outputs['EstadsticasDeZona3'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop1900'] = outputs['EstadsticasDeZona3']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}
        ##################################################################################
        # Se calcula el promedio zonal de la cantidad de población en el año 2000 por pais
        ##################################################################################
        alg_params = {
            'COLUMN_PREFIX': '2000_',
            'INPUT': outputs['EstadsticasDeZona3']['OUTPUT'],
            'INPUT_RASTER': 'C:/Udesa/Herramientas/Clase_5/input/pop/popd_2000AD.asc',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Pop2000']
        }
        outputs['EstadsticasDeZona4'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pop2000'] = outputs['EstadsticasDeZona4']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}
        ###################################################################
        # Se calcula el promedio zonal de la elevación del relieve por pais
        ###################################################################
        alg_params = {
            'COLUMN_PREFIX': 'topo_',
            'INPUT': outputs['EstadsticasDeZona4']['OUTPUT'],
            'INPUT_RASTER': 'C:/Udesa/Herramientas/Clase_5/input/topo30.grd',
            'RASTER_BAND': 1,
            'STATISTICS': [2],
            'OUTPUT': parameters['Topo']
        }
        outputs['EstadsticasDeZona5'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Topo'] = outputs['EstadsticasDeZona5']['OUTPUT']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}
        ##############################################################
        # Se guarda el vector con todos los resultados en formato csv
        ##############################################################
        alg_params = {
            'DATASOURCE_OPTIONS': '',
            'INPUT': outputs['EstadsticasDeZona5']['OUTPUT'],
            'LAYER_NAME': '',
            'LAYER_OPTIONS': '',
            'OUTPUT': 'C:/Udesa/Herramientas/Clase_5/output/raster_stats.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['SaveVectorFeaturesToFile'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model3'

    def displayName(self):
        return 'model3'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model3()
