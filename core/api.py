from flask import Blueprint, abort, current_app, jsonify, request, Flask, Response, send_from_directory, redirect, flash, url_for, render_template
from flask.ext.login import current_user
from datetime import datetime
import settings
import json
from core import models, data

#Rest API
rest_api = Blueprint('rest_api', __name__)

dimDetails = {'YEAR_ID': 'YEAR_LONG_NAME', 'SEA_ID': 'SEA_TYPE_LONG_NAME', 
                            'FUEL_ID': 'FUEL_TYPE_LONG_NAME', 'CNTRY_ID': 'CNTRY_NAME',
                                'REG_ID': 'REG_LONG_NAME', 'WEEK_ID': 'WEEK_LONG_NAME', 'LS_ID': 'LS_LONG_NAME', 'IND_ID': 'IND_NAME', 'PLANT_ID': 'PLANT_LONG_NAME'}
colPropDetails = {'CNTRY_NAME': 'Country Name', 'FUEL_TYPE_LONG_NAME': 'Fuel Type', 
                    'SEA_TYPE_LONG_NAME': 'Season', 'YEAR_LONG_NAME': 'Year', 
                        'REG_LONG_NAME': 'Region', 'WEEK_LONG_NAME':'Week', 'LS_LONG_NAME': 'Load Segment', 'IND_NAME': 'Indicator', 'PLANT_LONG_NAME': 'Plant Type', 'VALUE': 'Value', 'UNIT': 'Unit of Measure'}

tableDetails = {'Region': 'EMD.Region', 'Country Name': 'EMD.ModelCountry', 'Fuel Type': 'EMD.FuelType', 'Value': 'EMD.FactEntitlements', 'Unit of Measure': 'EMD.FactEntitlements'}          

@rest_api.route('/getdistModels')
def get_dists_modelType():
    listModelType = models.db.session.query(models.ModelType.MODEL_TYPE_LONG_NAME.distinct().label('MODEL_TYPE_LONG_NAME'))
    return jsonify( DistModelType = [row.MODEL_TYPE_LONG_NAME.strip() for row in listModelType.all()])

@rest_api.route('/getTableData',  methods=['GET'])
def get_table_data():
    columns = [x.encode('utf-8') for x in request.args.get('cols').split(',')]
    schemaFilter = [dimDetails[k] for k in columns]
    schemaFilter.append('VALUE')
    schemaFilter.append('UNIT')
    listTbldata = models.FactEntitlements.query.filter(models.FactEntitlements.USERNAME==request.args.get('user'), \
                        models.FactEntitlements.MODEL_ID==data.get_model_type_id(request.args.get('model')), \
                            models.FactEntitlements.SM_ID==data.get_sub_model_id(request.args.get('sm')), \
                                models.FactEntitlements.FUNC_ID==data.get_function_id(request.args.get('fnname')), \
                                    models.FactEntitlements.LAST_EDIT_END_DATE==None)
    result = models.fact_schema.dump(listTbldata.all())
    filtered_result = data.flatten(data._key_filter(result.data, schemaFilter))
    return jsonify({'result': data.match_list_with_dict(filtered_result, colPropDetails), 'colHeaders': [colPropDetails[k] for k in schemaFilter], 'handsOnColumns': data.get_handson_columns(colPropDetails, schemaFilter)})

@rest_api.route('/postToFact', methods=['GET', 'POST'])
def post_fact_data():
    res = data.fact_insertion(json.loads(request.args.get('header')), json.loads(request.args.get('editeddata')), request.args.get('model'), request.args.get('sm'), request.args.get('fnname'), request.args.get('mainversion'), current_user.username)
    sql_col_list = []
    sql_join_list = []
    sql_where_list = []
    for dim in json.loads(request.args.get('header')):
        sql_col_list.append(str(tableDetails[dim] + '.' +  colPropDetails.keys()[colPropDetails.values().index(dim)]))
        if dim != 'Value' and dim != 'Unit of Measure':
            sql_join_list.append(str('Inner Join ' + tableDetails[dim] + ' On ' + tableDetails[dim] + '.' + dimDetails.keys()[dimDetails.values().index(colPropDetails.keys()[colPropDetails.values().index(dim)])] + ' = ' + 'EMD.FactEntitlements' + '.' + dimDetails.keys()[dimDetails.values().index(colPropDetails.keys()[colPropDetails.values().index(dim)])]))    
    sql_join_list.append(str('Inner Join EMD.ModelType On EMD.ModelType.MODEL_ID = EMD.FactEntitlements.MODEL_ID Inner Join EMD.SubModelDetails On EMD.SubModelDetails.SM_ID = EMD.FactEntitlements.SM_ID Inner Join EMD.FunctionDetails On EMD.FunctionDetails.FUNC_ID = EMD.FactEntitlements.FUNC_ID'))
    sql_where_list.append(str(" Where EMD.ModelType.MODEL_TYPE_LONG_NAME = '" + request.args.get('model') + "'" + " AND EMD.SubModelDetails.SM_LONG_NAME = '" + request.args.get('sm') + "'" + " AND EMD.FunctionDetails.FUNC_LONG_NAME = '" + request.args.get('fnname') + "'" + " AND EMD.FactEntitlements.MAIN_VERSION = '" + request.args.get('mainversion') + "'" + " AND EMD.FactEntitlements.LAST_EDIT_END_DATE IS NULL" + " AND EMD.FactEntitlements.USERNAME = '" + current_user.username + "'"))
    return 'Select ' + ','.join(sql_col_list) + ' From EMD.FactEntitlements ' + ' '.join(sql_join_list) + ' '.join(sql_where_list)