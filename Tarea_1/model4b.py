"""
Model exported as python.
Name : model4b
Group : 
With QGIS : 31608
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model4b(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Pais_centroide', 'pais_centroide', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_by_attribute', 'Extract_by_attribute', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('ExtractVertices', 'extract vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust', 'nearest_cat_adjust', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lat', 'added_field_cent_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lon', 'added_field_cent_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lat', 'added_field_coast_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lon', 'added_field_coast_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_coast', 'fixgeo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_pais', 'fixgeo_pais', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('CentroidsNearestCoastJoined', 'centroids nearest coast joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined_dropfields', 'centroids_nearest_coast_joined_dropfields', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Coastout', 'coastout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidsout', 'centroidsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('NearestCatAdjustDropfields', 'nearest cat adjust dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined', 'centroids_nearest_coast_joined', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_lat_lon_drop_fields', 'centroids_lat_lon_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Csvout', 'csvout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroide_w_coord', 'centroide_w_coord', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Add_geo_coast', 'add_geo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(21, model_feedback)
        results = {}
        outputs = {}

        # Corregir geometrías coast
        alg_params = {
            'INPUT': 'C:/Udesa/Herramientas/Clase_5/input/ne_10m_coastline.shp',
            'OUTPUT': parameters['Fixgeo_coast']
        }
        outputs['CorregirGeometrasCoast'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_coast'] = outputs['CorregirGeometrasCoast']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Corregir geometrías pais
        alg_params = {
            'INPUT': 'C:/Udesa/Herramientas/Clase_5/input/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_pais']
        }
        outputs['CorregirGeometrasPais'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_pais'] = outputs['CorregirGeometrasPais']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s) costas
        alg_params = {
            'COLUMN': ['scalerank'],
            'INPUT': outputs['CorregirGeometrasCoast']['OUTPUT'],
            'OUTPUT': parameters['Coastout']
        }
        outputs['QuitarCamposCostas'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['QuitarCamposCostas']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Centroides pais
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['CorregirGeometrasPais']['OUTPUT'],
            'OUTPUT': parameters['Pais_centroide']
        }
        outputs['CentroidesPais'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Pais_centroide'] = outputs['CentroidesPais']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Agregar atributos de geometría
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': outputs['CentroidesPais']['OUTPUT'],
            'OUTPUT': parameters['Centroide_w_coord']
        }
        outputs['AgregarAtributosDeGeometra'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroide_w_coord'] = outputs['AgregarAtributosDeGeometra']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s) - centroide
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9'],
            'INPUT': outputs['AgregarAtributosDeGeometra']['OUTPUT'],
            'OUTPUT': parameters['Centroidsout']
        }
        outputs['QuitarCamposCentroide'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidsout'] = outputs['QuitarCamposCentroide']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # v.distance
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': False,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': outputs['QuitarCamposCentroide']['OUTPUT'],
            'from_output': '././nearout',
            'from_type': [0,1,3],
            'output': './distout',
            'to': outputs['QuitarCamposCostas']['OUTPUT'],
            'to_column': '',
            'to_type': [0,1,3],
            'upload': [0],
            'from_output': QgsProcessing.TEMPORARY_OUTPUT,
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos - cat adjust
        alg_params = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,
            'FORMULA': 'attribute($currentfeature,\'cat\')-1',
            'INPUT': outputs['Vdistance']['from_output'],
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        outputs['CalculadoraDeCamposCatAdjust'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['CalculadoraDeCamposCatAdjust']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s) nearest cat
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': outputs['CalculadoraDeCamposCatAdjust']['OUTPUT'],
            'OUTPUT': parameters['NearestCatAdjustDropfields']
        }
        outputs['QuitarCamposNearestCat'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['NearestCatAdjustDropfields'] = outputs['QuitarCamposNearestCat']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Unir atributos por valor de campo - centroide y costa
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ISO_A3',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ISO_A3',
            'INPUT': outputs['QuitarCamposCentroide']['OUTPUT'],
            'INPUT_2': outputs['QuitarCamposNearestCat']['OUTPUT'],
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters['CentroidsNearestCoastJoined']
        }
        outputs['UnirAtributosPorValorDeCampoCentroideYCosta'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['CentroidsNearestCoastJoined'] = outputs['UnirAtributosPorValorDeCampoCentroideYCosta']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s) - centroides_costa_juntos
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','APCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','GDP_MD_EST','POP_YEAR','LASTCENSUS','GDP_YEAR','ECONOMY','INCOME_GRP','WIKIPEDIA','FIPS_10_','ISO_A2','ISO_A3_EH','ISO_N3','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_A3_IS','ADM0_A3_US','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FR','NAME_EL','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_VI','NAME_ZH','MAPCOLOR9','ADMIN_2','ISO_A3_2'],
            'INPUT': outputs['UnirAtributosPorValorDeCampoCentroideYCosta']['OUTPUT'],
            'OUTPUT': parameters['Centroids_nearest_coast_joined']
        }
        outputs['QuitarCamposCentroides_costa_juntos'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined'] = outputs['QuitarCamposCentroides_costa_juntos']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Unir atributos por valor de campo - cat
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cat',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat',
            'INPUT': outputs['Vdistance']['output'],
            'INPUT_2': outputs['QuitarCamposCentroides_costa_juntos']['OUTPUT'],
            'METHOD': 1,
            'PREFIX': '',
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        outputs['UnirAtributosPorValorDeCampoCat'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['UnirAtributosPorValorDeCampoCat']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Extraer vértices
        alg_params = {
            'INPUT': outputs['UnirAtributosPorValorDeCampoCat']['OUTPUT'],
            'OUTPUT': parameters['ExtractVertices']
        }
        outputs['ExtraerVrtices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ExtractVertices'] = outputs['ExtraerVrtices']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Extraer por atributo - a
        alg_params = {
            'FIELD': 'distance',
            'INPUT': outputs['ExtraerVrtices']['OUTPUT'],
            'OPERATOR': 2,
            'VALUE': '0',
            'OUTPUT': parameters['Extract_by_attribute']
        }
        outputs['ExtraerPorAtributoA'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['ExtraerPorAtributoA']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos - cent_lat
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'ycoord\')',
            'INPUT': outputs['ExtraerPorAtributoA']['OUTPUT'],
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['CalculadoraDeCamposCent_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['CalculadoraDeCamposCent_lat']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos - cent_lon
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'xcoord\')',
            'INPUT': outputs['CalculadoraDeCamposCent_lat']['OUTPUT'],
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        outputs['CalculadoraDeCamposCent_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['CalculadoraDeCamposCent_lon']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s) - centroids_lat_lon
        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': outputs['CalculadoraDeCamposCent_lon']['OUTPUT'],
            'OUTPUT': parameters['Centroids_lat_lon_drop_fields']
        }
        outputs['QuitarCamposCentroids_lat_lon'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lat_lon_drop_fields'] = outputs['QuitarCamposCentroids_lat_lon']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Agregar atributos de geometría - add_geo_coast
        alg_params = {
            'CALC_METHOD': 0,
            'INPUT': outputs['QuitarCamposCentroids_lat_lon']['OUTPUT'],
            'OUTPUT': parameters['Add_geo_coast']
        }
        outputs['AgregarAtributosDeGeometraAdd_geo_coast'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['AgregarAtributosDeGeometraAdd_geo_coast']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos - coast_lat
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'ycoord\')',
            'INPUT': outputs['AgregarAtributosDeGeometraAdd_geo_coast']['OUTPUT'],
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        outputs['CalculadoraDeCamposCoast_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['CalculadoraDeCamposCoast_lat']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Calculadora de campos - coast_lon
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,
            'FORMULA': 'attribute($currentfeature,\'xcoord\')',
            'INPUT': outputs['CalculadoraDeCamposCoast_lat']['OUTPUT'],
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        outputs['CalculadoraDeCamposCoast_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['CalculadoraDeCamposCoast_lon']['OUTPUT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Quitar campo(s)
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': outputs['CalculadoraDeCamposCoast_lon']['OUTPUT'],
            'OUTPUT': parameters['Csvout']
        }
        outputs['QuitarCampos'] = processing.run('qgis:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Csvout'] = outputs['QuitarCampos']['OUTPUT']
        return results

    def name(self):
        return 'model4b'

    def displayName(self):
        return 'model4b'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4b()
