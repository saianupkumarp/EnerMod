from flask import Blueprint, abort, current_app, jsonify, request, Flask, Response, send_from_directory, redirect, flash, url_for, render_template
from flask.ext.login import current_user
from datetime import datetime
import settings
import json
from core import models, data

#Rest API
rest_api = Blueprint('rest_api', __name__)

dimDetails = {'YEAR_ID': 'YEAR_LONG_NAME', 
                    'SEA_ID': 'SEA_TYPE_LONG_NAME', 
                            'FUEL_ID': 'FUEL_TYPE_LONG_NAME',
                                'CNTRY_ID': 'CNTRY_NAME', 'REG_ID': 'REG_LONG_NAME'}
colPropDetails = {'CNTRY_NAME': 'Country Name', 'FUEL_TYPE_LONG_NAME': 'Fuel Type', 
                    'SEA_TYPE_LONG_NAME': 'Season', 'YEAR_LONG_NAME': 'Year', 
                        'REG_LONG_NAME': 'Region', 'VALUE': 'Value'}

@rest_api.route('/getdistModels')
def get_dists_modelType():
    listModelType = models.db.session.query(models.ModelType.MODEL_TYPE_LONG_NAME.distinct().label('MODEL_TYPE_LONG_NAME'))
    return jsonify( DistModelType = [row.MODEL_TYPE_LONG_NAME.strip() for row in listModelType.all()])

@rest_api.route('/getTableData')
def get_table_data():
    columns = [x.encode('utf-8') for x in request.args.get('cols').split(',')]
    schemaFilter = [dimDetails[k] for k in columns]
    schemaFilter.append('VALUE')
    listTbldata = models.FactEntitlements.query.filter(models.FactEntitlements.USERNAME==current_user.username, \
                        models.FactEntitlements.MODEL_ID==data.get_model_type_id(request.args.get('model')), \
                            models.FactEntitlements.SM_ID==data.get_sub_model_id(request.args.get('sm')), \
                                models.FactEntitlements.FUNC_ID==data.get_function_id(request.args.get('fnname')), \
                                    models.FactEntitlements.LAST_EDIT_END_DATE==None)
    result = models.fact_schema.dump(listTbldata.all())
    filtered_result = data.flatten(data._key_filter(result.data, schemaFilter))
    return jsonify({'result': data.match_list_with_dict(filtered_result, colPropDetails), 'colHeaders': [colPropDetails[k] for k in schemaFilter], 'handsOnColumns': data.get_handson_columns(colPropDetails, schemaFilter)})