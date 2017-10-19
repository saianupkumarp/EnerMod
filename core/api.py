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

@rest_api.route('/getdistModelCountry',  methods=['GET'])
def dists_modelCountry():
    query = models.db.session.query(models.FactEntitlements.CNTRY_ID.distinct().label('CNTRY_ID'), 
                                        models.ModelCountry).filter(models.FactEntitlements.MODEL_ID == request.args.get('modelTypeID'),\
                                                                    models.FactEntitlements.CNTRY_ID == models.ModelCountry.CNTRY_ID)
    return jsonify( modelCountry = [{'cntryid':row.CNTRY_ID,'cntryName':row.ModelCountry.CNTRY_NAME.strip()} for row in query.all()])

@rest_api.route('/getdistUsers',  methods=['GET'])
def dists_users():
    query = models.db.session.query(models.FactEntitlements.USERNAME.distinct().label('USERNAME'), 
                                        models.User).filter(models.FactEntitlements.MODEL_ID == request.args.get('modelTypeID'),\
                                                            models.FactEntitlements.CNTRY_ID == request.args.get('modelCountry'),\
                                                            models.FactEntitlements.USERNAME == models.User.username)
    return jsonify( users = [{'username':row.USERNAME.strip(),'fname':row.User.first_name.strip() ,'lname':row.User.last_name.strip(),'dname':row.User.display_name.strip()} for row in query.all()])

@rest_api.route('/getdistmainversion',  methods=['GET'])
def dists_main_version():
    query = models.db.session.query(models.FactEntitlements.MAIN_VERSION.distinct().label('MAIN_VERSION')).filter(models.FactEntitlements.MODEL_ID == request.args.get('modelTypeID'),\
                                                            models.FactEntitlements.CNTRY_ID == request.args.get('modelCountry'),\
                                                            models.FactEntitlements.USERNAME == request.args.get('owner'))
    return jsonify( mainversion = [{'version':row.MAIN_VERSION } for row in query.all()])

@rest_api.route('/getdistsubmodel',  methods=['GET'])
def dists_subModel():
    query = models.db.session.query(models.FactEntitlements.SM_ID.distinct().label('SM_ID'), 
                                        models.SubModels).filter(models.FactEntitlements.MODEL_ID == request.args.get('modelTypeID'),\
                                                            models.FactEntitlements.CNTRY_ID == request.args.get('modelCountry'),\
                                                            models.FactEntitlements.USERNAME == request.args.get('owner'),\
                                                            models.FactEntitlements.MAIN_VERSION == request.args.get('version'),\
                                                            models.FactEntitlements.SM_ID == models.SubModels.SM_ID)
    return jsonify( submodel = [{'submodelid':row.SM_ID,'submodelName':row.SubModels.SM_LONG_NAME.strip() } for row in query.all()])

@rest_api.route('/getdistfunc',  methods=['GET'])
def dists_func():
    query = models.db.session.query(models.FactEntitlements.FUNC_ID.distinct().label('FUNC_ID'), 
                                        models.FunctionDetails).filter(models.FactEntitlements.MODEL_ID == request.args.get('modelTypeID'),\
                                                            models.FactEntitlements.CNTRY_ID == request.args.get('modelCountry'),\
                                                            models.FactEntitlements.USERNAME == request.args.get('owner'),\
                                                            models.FactEntitlements.MAIN_VERSION == request.args.get('version'),\
                                                            models.FactEntitlements.SM_ID == request.args.get('subModel'),\
                                                            models.FactEntitlements.FUNC_ID == models.FunctionDetails.FUNC_ID)
    return jsonify( func = [{'funcid':row.FUNC_ID,'funcName':row.FunctionDetails.FUNC_LONG_NAME.strip() } for row in query.all()])

@rest_api.route('/getdistcolumns',  methods=['GET'])
def dists_columns():
    query = models.db.session.query(models.FactEntitlements.FUNC_ID.distinct().label('FUNC_ID'), 
                                        models.FunctionDetails).filter(models.FactEntitlements.MODEL_ID == request.args.get('modelTypeID'),\
                                                            models.FactEntitlements.CNTRY_ID == request.args.get('modelCountry'),\
                                                            models.FactEntitlements.USERNAME == request.args.get('owner'),\
                                                            models.FactEntitlements.MAIN_VERSION == request.args.get('version'),\
                                                            models.FactEntitlements.SM_ID == request.args.get('subModel'),\
                                                            models.FactEntitlements.FUNC_ID == request.args.get('func'),\
                                                            models.FactEntitlements.FUNC_ID == models.FunctionDetails.FUNC_ID)
    return jsonify( columns = [row.FunctionDetails.FUNC_COLUMNS.strip() for row in query.all()])

@rest_api.route('/getTableData',  methods=['GET'])
def get_table_data():
    columns = [x.encode('utf-8') for x in request.args.get('cols').split(',')]
    schemaFilter = [dimDetails[k] for k in columns]
    schemaFilter.append('VALUE')
    schemaFilter.append('UNIT')
    listTbldata = models.FactEntitlements.query.filter(models.FactEntitlements.USERNAME==request.args.get('user'), \
                        models.FactEntitlements.MODEL_ID==request.args.get('model'), \
                            models.FactEntitlements.SM_ID==request.args.get('sm'), \
                                models.FactEntitlements.FUNC_ID==request.args.get('fnname'), \
                                    models.FactEntitlements.MAIN_VERSION==request.args.get('version'), \
                                        models.FactEntitlements.CNTRY_ID==request.args.get('country'), \
                                            models.FactEntitlements.LAST_EDIT_END_DATE==None)
    result = models.fact_schema.dump(listTbldata.all())
    filtered_result = data.flatten(data._key_filter(result.data, schemaFilter))
    return jsonify({'result': data.match_list_with_dict(filtered_result, colPropDetails), 'colHeaders': [colPropDetails[k] for k in schemaFilter], 'handsOnColumns': data.get_handson_columns(colPropDetails, schemaFilter)})

@rest_api.route('/postToFact', methods=['GET', 'POST'])
def post_fact_data():
    res = data.fact_insertion(json.loads(request.args.get('header')), json.loads(request.args.get('editeddata')), request.args.get('model'), request.args.get('sm'), request.args.get('fnname'), request.args.get('mainversion'), request.args.get('country'), current_user.username)
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