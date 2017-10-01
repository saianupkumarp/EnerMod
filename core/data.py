from core import models
from datetime import datetime
import copy
import collections

def get_dist_username():
    query = models.db.session.query(models.FactEntitlements.USERNAME.distinct().label('USERNAME'),models.User).filter(models.FactEntitlements.USERNAME == models.User.username)
    result = [{'username':row.USERNAME,'fname':row.User.first_name ,'lname':row.User.last_name} for row in query.all()]
    return result

def get_dist_modelType():
    query = models.db.session.query(models.ModelType.MODEL_TYPE_LONG_NAME.distinct().label('MODEL_TYPE_LONG_NAME'))
    result = [row.MODEL_TYPE_LONG_NAME.strip() for row in query.all()]
    return result

def get_dist_sub_models():
    query = models.db.session.query(models.SubModels.SM_LONG_NAME.distinct().label('SM_LONG_NAME'))
    result = [row.SM_LONG_NAME.strip() for row in query.all()]
    return result

def get_dist_func():
    query = models.db.session.query(models.FunctionDetails.FUNC_LONG_NAME.distinct().label('FUNC_LONG_NAME'))
    result = [row.FUNC_LONG_NAME.strip() for row in query.all()]
    return result

def get_main_version(username):
    query = models.db.session.query(models.FactEntitlements.MAIN_VERSION.distinct().label('MAIN_VERSION'))#.filter_by(USERNAME=username)
    result = [row.MAIN_VERSION for row in query.all()]
    return result

def get_model_type_id(modelType):
    if modelType == None:
        result = None
    else:
        query = models.db.session.query(models.ModelType.MODEL_ID.label('MODEL_ID')).filter_by(MODEL_TYPE_LONG_NAME=modelType)
        for row in query.first():
            result = row
    return result

def get_sub_model_id(submodel_name):
    if submodel_name == None:
        result = None
    else:
        query = models.db.session.query(models.SubModels.SM_ID.label('SM_ID')).filter_by(SM_LONG_NAME=submodel_name)
        for row in query.first():
            result = row
    return result

def get_function_id(func_name):
    if func_name == None:
        result = None
    else:
        query = models.db.session.query(models.FunctionDetails.FUNC_ID.label('FUNC_ID')).filter_by(FUNC_LONG_NAME=func_name)
        for row in query.first():
            result = row
    return result

def get_plant_id(plant_name):
    if plant_name == None:
        result = None
    else:
        query = models.db.session.query(models.PlantType.PLANT_ID.label('PLANT_ID')).filter_by(PLANT_LONG_NAME=plant_name)
        for row in query.first():
            result = row
    return result

def get_country_id(country_name):
    if country_name == None:
        result = None
    else:
        query = models.db.session.query(models.ModelCountry.CNTRY_ID.label('CNTRY_ID')).filter_by(CNTRY_NAME=country_name)
        for row in query.first():
            result = row
    return result

def get_week_id(week_name):
    if week_name == None:
        result = None
    else:
        query = models.db.session.query(models.WeekDetails.WEEK_ID.label('WEEK_ID')).filter_by(WEEK_LONG_NAME=week_name)
        for row in query.first():
            result = row
    return result

def get_fuel_id(fuel_name):
    if fuel_name == None:
        result = None
    else:
        query = models.db.session.query(models.FuelType.FUEL_ID.label('FUEL_ID')).filter_by(FUEL_TYPE_LONG_NAME=fuel_name)
        for row in query.first():
            result = row
    return result

def get_ls_id(ls_name):
    if ls_name == None:
        result = None
    else:
        query = models.db.session.query(models.LoadSegment.LS_ID.label('LS_ID')).filter_by(LS_LONG_NAME=ls_name)
        for row in query.first():
            result = row
    return result

def get_ind_id(ind_name):
    if ind_name == None:
        result = None
    else:
        query = models.db.session.query(models.Indicator.IND_ID.label('IND_ID')).filter_by(IND_NAME=ind_name)
        for row in query.first():
            result = row
    return result

def get_reg_id(reg_name):
    if reg_name == None:
        result = None
    else:
        query = models.db.session.query(models.Region.REG_ID.label('REG_ID')).filter_by(REG_LONG_NAME=reg_name)
        for row in query.first():
            result = row
    return result

def get_sea_id(sea_name):
    if sea_name == None:
        result = None
    else:
        query = models.db.session.query(models.Season.SEA_ID.label('SEA_ID')).filter_by(SEA_TYPE_LONG_NAME=sea_name)
        for row in query.first():
            result = row
    return result

def get_year_id(year_name):
    if year_name == None:
        result = None
    else:
        query = models.db.session.query(models.ModelYear.YEAR_ID.label('YEAR_ID')).filter_by(YEAR_LONG_NAME=year_name)
        for row in query.first():
            result = row
    return result

def _key_filter(obj, obj_filter):
    if isinstance(obj, dict):
        retdict = {}
        for key, value in obj.iteritems():
            if key in obj_filter:
                retdict[key] = copy.deepcopy(value)
            elif isinstance(value, (dict, list)):
                child = _key_filter(value, obj_filter)
                if child:
                    retdict[key] = child
        return retdict if retdict else None
    elif isinstance(obj, list):
        retlist = []
        for key in obj:
            child = _key_filter(key, obj_filter)
            if child:
                retlist.append(child)
        return retlist if retlist else None
    else:
        return None

def flatten(my_dict):
    res = []
    for sub in my_dict:
        dict_ = {}
        for k, v in sub.items():
            if isinstance(v, dict):
                for k_new, v_new in v.items():
                    dict_[k_new] = v_new
            else:
                dict_[k] = v
        res.append(dict_)
    return res

def match_list_with_dict(src_list, map_dict):
    res = []
    for sub_dict in src_list:
        output = {}
        for key, value in sub_dict.items():
            if isinstance(value, dict):
                output[map_dict[key]] = match_list_with_dict(value, map_dict)
            else:
                output[map_dict[key]] = value
        res.append(output)
    return res

def get_handson_columns(colpros, colFiter):
    handsOnColumns = []
    for k in colFiter:
        col = {}
        col['data'] = colpros[k]
        if colpros[k] == 'Value':
            col['type'] = 'numeric'
            col['format'] = '0.00'
        else:
            col['type'] = 'text'
            col['editor'] = 'false'
        handsOnColumns.append(col)
    return handsOnColumns

def fact_insertion(key, values, modelName, subModel, funcName, mainVerion, username):
    utcNow = datetime.utcnow()
    #Updating the Last End Date
    factsUpdate = models.FactEntitlements.query.filter_by(MODEL_ID=get_model_type_id(modelName),SM_ID=get_sub_model_id(subModel),FUNC_ID=get_function_id(funcName),MAIN_VERSION=mainVerion,USERNAME=username,LAST_EDIT_END_DATE=None).update({"LAST_EDIT_END_DATE": utcNow})
    models.db.session.commit()
    retdict = {}
    for val in values:
        retdict.update(dict(zip(key, val)))
        #Insert new records with Last Start Date
        factIns = models.FactEntitlements(CNTRY_ID=get_country_id(retdict.get('Country Name')),UNIT=retdict.get('Unit of Measure'),YEAR_ID=get_year_id(retdict.get('Year')),SEA_ID=get_sea_id(retdict.get('Season')),WEEK_ID=get_week_id(retdict.get('Week')),FUEL_ID=get_fuel_id(retdict.get('Fuel Type')),LS_ID=get_ls_id(retdict.get('Load Segment')),REG_ID=get_reg_id(retdict.get('Region')),IND_ID=get_ind_id(retdict.get('Indicator')),PLANT_ID=get_plant_id(retdict.get('Plant Type')),VALUE=retdict.get('Value'),MODEL_ID=get_model_type_id(modelName),SM_ID=get_sub_model_id(subModel),FUNC_ID=get_function_id(funcName),MAIN_VERSION=mainVerion,USERNAME=username,LAST_EDIT_START_DATE=utcNow)
        models.db.session.add(factIns)
        models.db.session.commit()
    return "success"

def facts_insert_initial_data(username):
    utcNow = datetime.utcnow()
    initial_data = models.GetFacts.dump(models.FactEntitlements.query.filter(models.FactEntitlements.USERNAME=='SYSADMIN', models.FactEntitlements.MAIN_VERSION=='0').all())
    for item in initial_data.data:
        factIns = models.FactEntitlements(CNTRY_ID=item.get('CNTRY_ID'),UNIT=item.get('UNIT'),YEAR_ID=item.get('YEAR_ID'),SEA_ID=item.get('SEA_ID'),WEEK_ID=item.get('WEEK_ID'),FUEL_ID=item.get('FUEL_ID'),LS_ID=item.get('LS_ID'),REG_ID=item.get('REG_ID'),IND_ID=item.get('IND_ID'),PLANT_ID=item.get('PLANT_ID'),VALUE=item.get('VALUE'),MODEL_ID=item.get('MODEL_ID'),SM_ID=item.get('SM_ID'),FUNC_ID=item.get('FUNC_ID'),MAIN_VERSION='1',USERNAME=username,LAST_EDIT_START_DATE=utcNow,INITIAL_LOAD_START_DATE=utcNow,LAST_EDIT_END_DATE=None,INITIAL_LOAD_END_DATE=None,SUB_VERSION=None)
        models.db.session.add(factIns)
        models.db.session.commit()
    return "success"