from core import models
import copy
import collections

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
    query = models.db.session.query(models.FactEntitlements.MAIN_VERSION.distinct().label('MAIN_VERSION')).filter_by(USERNAME=username)
    result = [row.MAIN_VERSION for row in query.all()]
    return result

def get_model_type_id(modelType):
    query = models.db.session.query(models.ModelType.MODEL_ID.label('MODEL_ID')).filter_by(MODEL_TYPE_LONG_NAME=modelType)
    for row in query.first():
        result = row
    return result

def get_sub_model_id(submodel_name):
    query = models.db.session.query(models.SubModels.SM_ID.label('SM_ID')).filter_by(SM_LONG_NAME=submodel_name)
    for row in query.first():
        result = row
    return result

def get_function_id(func_name):
    query = models.db.session.query(models.FunctionDetails.FUNC_ID.label('FUNC_ID')).filter_by(FUNC_LONG_NAME=func_name)
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