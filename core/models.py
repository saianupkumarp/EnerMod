from flask.ext.sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, pre_load
import datetime
import settings

#SQLAlchemy
db = SQLAlchemy()

######### MODELS #########

#User Class for Auth
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
 
    def __init__(self, username, password):
        self.username = username
 
    @staticmethod
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

#ModelType
class ModelType(db.Model):
    __tablename__ = 'ModelType'
    __table_args__ = {'schema': 'EMD'}
    MODEL_ID = db.Column(db.Integer, primary_key=True)
    MODEL_TYPE_LONG_NAME = db.Column(db.String(20))
    MODEL_TYPE_SHORT_NAME = db.Column(db.String(10))
    MODEL_TYPE_DESC = db.Column(db.String(50))

#Sub Models
class SubModels(db.Model):
    __tablename__ = 'SubModelDetails'
    __table_args__ = {'schema': 'EMD'}
    SM_ID = db.Column(db.Integer, primary_key=True)
    SM_LONG_NAME = db.Column(db.String(20))
    SM_SHORT_NAME = db.Column(db.String(10))
    SM_DESC = db.Column(db.String(50))

#Fuel Allocation
class FunctionDetails(db.Model):
    __tablename__ = 'FunctionDetails'
    __table_args__ = {'schema': 'EMD'}
    FUNC_ID = db.Column(db.Integer, primary_key=True)
    FUNC_LONG_NAME = db.Column(db.String(20))
    FUNC_SHORT_NAME = db.Column(db.String(10))
    FUNC_DESC = db.Column(db.String(50))

#FuelType
class FuelType(db.Model):
    __tablename__ = 'FuelType'
    __table_args__ = {'schema': 'EMD'}
    FUEL_ID = db.Column(db.Integer, primary_key=True)
    FUEL_TYPE_LONG_NAME = db.Column(db.String(20))
    FUEL_TYPE_SHORT_NAME = db.Column(db.String(10))
    FUEL_TYPE_DESC = db.Column(db.String(50))

#Indicator
class Indicator(db.Model):
    __tablename__ = 'Indicator'
    __table_args__ = {'schema': 'EMD'}
    IND_ID = db.Column(db.Integer, primary_key=True)
    IND_NAME = db.Column(db.String(50))
    IND_DESC = db.Column(db.String(100))
    IND_UNIT = db.Column(db.String(10))

#LoadSegment
class LoadSegment(db.Model):
    __tablename__ = 'LoadSegment'
    __table_args__ = {'schema': 'EMD'}
    LS_ID = db.Column(db.Integer, primary_key=True)
    LS_LONG_NAME = db.Column(db.String(20))
    LS_SHORT_NAME = db.Column(db.String(10))
    LS_DESC = db.Column(db.String(50))

#Model Country
class ModelCountry(db.Model):
    __tablename__ = 'ModelCountry'
    __table_args__ = {'schema': 'EMD'}
    CNTRY_ID = db.Column(db.Integer, primary_key=True)
    CNTRY_NAME = db.Column(db.String(100))

#Model Year
class ModelYear(db.Model):
    __tablename__ = 'ModelYear'
    __table_args__ = {'schema': 'EMD'}
    YEAR_ID = db.Column(db.Integer, primary_key=True)
    YEAR_LONG_NAME = db.Column(db.String(20))
    YEAR_SHORT_NAME = db.Column(db.String(10))

#Plant Type
class PlantType(db.Model):
    __tablename__ = 'PlantType'
    __table_args__ = {'schema': 'EMD'}
    PLANT_ID = db.Column(db.Integer, primary_key=True)
    PLANT_SHORT_NAME = db.Column(db.String(10))
    PLANT_LONG_NAME = db.Column(db.String(20))
    PLANT_DESC = db.Column(db.String(50))

#Region
class Region(db.Model):
    __tablename__ = 'Region'
    __table_args__ = {'schema': 'EMD'}
    REG_ID = db.Column(db.Integer, primary_key=True)
    REG_LONG_NAME = db.Column(db.String(20))
    REG_SHORT_NAME = db.Column(db.String(10))
    REG_DESC = db.Column(db.String(50))
    # factregion = db.relationship('FactEntitlements', backref='Region', lazy='dynamic')

#Season
class Season(db.Model):
    __tablename__ = 'Season'
    __table_args__ = {'schema': 'EMD'}
    SEA_ID = db.Column(db.Integer, primary_key=True)
    SEA_TYPE_LONG_NAME = db.Column(db.String(20))
    SEA_TYPE_SHORT_NAME = db.Column(db.String(10))
    SEA_TYPE_DESC = db.Column(db.String(50))

#WeekDetails
class WeekDetails(db.Model):
    __tablename__ = 'WeekDetails'
    __table_args__ = {'schema': 'EMD'}
    WEEK_ID = db.Column(db.Integer, primary_key=True)
    WEEK_LONG_NAME = db.Column(db.String(20))
    WEEK_SHORT_NAME = db.Column(db.String(10))
    WEEK_DESC = db.Column(db.String(50))

#FactEntitlements
class FactEntitlements(db.Model):
    __tablename__ = 'FactEntitlements'
    __table_args__ = {'schema': 'EMD'}
    FACT_ID = db.Column(db.Integer, primary_key=True)
    PLANT_ID = db.Column(db.Integer, db.ForeignKey('EMD.PlantType.PLANT_ID'))
    plants =  db.relationship('PlantType', lazy='joined')
    WEEK_ID = db.Column(db.Integer, db.ForeignKey('EMD.WeekDetails.WEEK_ID'))
    weeks =  db.relationship('WeekDetails', lazy='joined')
    MODEL_ID = db.Column(db.Integer, db.ForeignKey('EMD.ModelType.MODEL_ID'))
    modeltypes =  db.relationship('ModelType', lazy='joined')
    FUEL_ID = db.Column(db.Integer, db.ForeignKey('EMD.FuelType.FUEL_ID'))
    fuels = db.relationship('FuelType', lazy='joined')
    LS_ID = db.Column(db.Integer, db.ForeignKey('EMD.LoadSegment.LS_ID'))
    loadsegments = db.relationship('LoadSegment', lazy='joined')
    IND_ID = db.Column(db.Integer, db.ForeignKey('EMD.Indicator.IND_ID'))
    indicators = db.relationship('Indicator', lazy='joined')
    SEA_ID = db.Column(db.Integer, db.ForeignKey('EMD.Season.SEA_ID'))
    seasons = db.relationship('Season', lazy='joined')
    CNTRY_ID = db.Column(db.Integer, db.ForeignKey('EMD.ModelCountry.CNTRY_ID'))
    countries = db.relationship('ModelCountry', lazy='joined')
    REG_ID = db.Column(db.Integer, db.ForeignKey('EMD.Region.REG_ID'))
    region = db.relationship('Region', lazy='joined')
    YEAR_ID = db.Column(db.Integer, db.ForeignKey('EMD.ModelYear.YEAR_ID'))
    modelyears = db.relationship('ModelYear', lazy='joined')
    SM_ID = db.Column(db.Integer, db.ForeignKey('EMD.SubModelDetails.SM_ID'))
    submodels = db.relationship('SubModels', lazy='joined')
    FUNC_ID = db.Column(db.Integer, db.ForeignKey('EMD.FunctionDetails.FUNC_ID'))
    functions = db.relationship('FunctionDetails', lazy='joined')
    UNIT = db.Column(db.String(50))
    VALUE = db.Column(db.Float)
    USERNAME = db.Column(db.String(50))
    MAIN_VERSION = db.Column(db.Integer)
    SUB_VERSION = db.Column(db.Integer)
    INITIAL_LOAD_START_DATE = db.Column(db.DateTime)
    INITIAL_LOAD_END_DATE = db.Column(db.DateTime)
    LAST_EDIT_START_DATE = db.Column(db.DateTime)
    LAST_EDIT_END_DATE = db.Column(db.DateTime)

    ######### SCHEMAS #########

class ModelTypeSchema(Schema):
    MODEL_ID = fields.Int(dump_only=True)
    MODEL_TYPE_LONG_NAME = fields.Str()
    MODEL_TYPE_SHORT_NAME = fields.Str()
    MODEL_TYPE_DESC = fields.Str()

class SubModelsSchema(Schema):
    SM_ID = fields.Int(dump_only=True)
    SM_LONG_NAME = fields.Str()
    SM_SHORT_NAME = fields.Str()
    SM_DESC = fields.Str()

class FunctionDetailsSchema(Schema):
    FUNC_ID = fields.Int(dump_only=True)
    FUNC_LONG_NAME = fields.Str()
    FUNC_SHORT_NAME = fields.Str()
    FUNC_DESC = fields.Str()

class FuelTypeSchema(Schema):
    FUEL_ID = fields.Int(dump_only=True)
    FUEL_TYPE_LONG_NAME = fields.Str()
    FUEL_TYPE_SHORT_NAME = fields.Str()
    FUEL_TYPE_DESC = fields.Str()

class IndicatorSchema(Schema):
    IND_ID = fields.Int(dump_only=True)
    IND_NAME = fields.Str()
    IND_DESC = fields.Str()
    IND_UNIT = fields.Str()

class LoadSegmentSchema(Schema):
    LS_ID = fields.Int(dump_only=True)
    LS_LONG_NAME = fields.Str()
    LS_SHORT_NAME = fields.Str()
    LS_DESC = fields.Str()

class ModelCountrySchema(Schema):
    CNTRY_ID = fields.Int(dump_only=True)
    CNTRY_NAME = fields.Str()

class ModelYearSchema(Schema):
    YEAR_ID = fields.Int(dump_only=True)
    YEAR_LONG_NAME = fields.Str()
    YEAR_SHORT_NAME = fields.Str()

class PlantTypeSchema(Schema):
    PLANT_ID = fields.Int(dump_only=True)
    PLANT_SHORT_NAME = fields.Str()
    PLANT_LONG_NAME = fields.Str()
    PLANT_DESC = fields.Str()

class RegionSchema(Schema):
    REG_ID = fields.Int(dump_only=True)
    REG_LONG_NAME = fields.Str()
    REG_SHORT_NAME = fields.Str()
    REG_DESC = fields.Str()

class SeasonSchema(Schema):
    SEA_ID = fields.Int(dump_only=True)
    SEA_TYPE_LONG_NAME = fields.Str()
    SEA_TYPE_SHORT_NAME = fields.Str()
    SEA_TYPE_DESC = fields.Str()

class WeekDetailsSchema(Schema):
    WEEK_ID = fields.Int(dump_only=True)
    WEEK_LONG_NAME = fields.Str()
    WEEK_SHORT_NAME = fields.Str()
    WEEK_DESC = fields.Str()

class FactEntitlementsSchema(Schema):
    FACT_ID = fields.Int(dump_only=True)
    REG_ID = fields.Int(dump_only=True)
    plants = fields.Nested("PlantTypeSchema")
    weeks = fields.Nested("WeekDetailsSchema")
    modeltypes = fields.Nested("ModelTypeSchema")
    fuels = fields.Nested("FuelTypeSchema")
    loadsegments = fields.Nested("LoadSegmentSchema")
    indicators = fields.Nested("IndicatorSchema")
    seasons = fields.Nested("SeasonSchema")
    countries = fields.Nested("ModelCountrySchema")
    region = fields.Nested("RegionSchema")    
    modelyears = fields.Nested("ModelYearSchema")
    submodels = fields.Nested("SubModelsSchema")
    functions = fields.Nested("FunctionDetailsSchema")
    UNIT = fields.Str()
    VALUE = fields.Float()
    USERNAME = fields.Str()
    MAIN_VERSION = fields.Int(dump_only=True)
    SUB_VERSION = fields.Int(dump_only=True)
    INITIAL_LOAD_START_DATE = fields.DateTime()
    INITIAL_LOAD_END_DATE = fields.DateTime()
    LAST_EDIT_START_DATE = fields.DateTime()
    LAST_EDIT_END_DATE = fields.DateTime()

modeltype_schema = ModelTypeSchema()
submodel_schema = SubModelsSchema()
funcdetails_schema = FunctionDetailsSchema()
fueltype_schema = FuelTypeSchema()
indicator_schema = IndicatorSchema()
ls_schema = LoadSegmentSchema()
modcountry_schema = ModelCountrySchema()
modyear_schema = ModelYearSchema()
plant_schema = PlantTypeSchema()
region_schema = RegionSchema()
season_schema = SeasonSchema()
week_schema = WeekDetailsSchema()
fact_schema = FactEntitlementsSchema(many=True)
facts_schema = FactEntitlementsSchema(many=True, only=('FACT_ID', 'VALUE', 'region', 'models'))