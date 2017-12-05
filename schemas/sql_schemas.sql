#-------------------------------------- Chnage Log -------------------------------------------
__author__ = "Anup Kumar"
__copyright__ = "Copyright 2017"
__credits__ = ["Anup Kumar"]
__license__ = "MIT License"
__version__ = "1.0.0"
__maintainer__ = "Anup Kumar"
__status__ = "Production"
------------------------------------- Change Details ------------------------------------------
-- 11/29/2017 - Anup Kumar - Initial code to export all tables data to csv from sql server
----------------------------------------------------------------------------------------------

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `first_name` char(25) DEFAULT NULL,
  `last_name` char(25) DEFAULT NULL,
  `display_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE FuelType(
    `FUEL_ID` int AUTO_INCREMENT NOT NULL,
    `FUEL_TYPE_LONG_NAME` char(20) NULL,
    `FUEL_TYPE_SHORT_NAME` char(10) NULL,
    `FUEL_TYPE_DESC` varchar(50) NULL,
    PRIMARY KEY (`FUEL_ID` ASC) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE FunctionDetails(
    `FUNC_ID` int AUTO_INCREMENT NOT NULL,
    `FUNC_LONG_NAME` char(20) NULL,
    `FUNC_SHORT_NAME` char(10) NULL,
    `FUNC_DESC` varchar(50) NULL,
    `FUNC_COLUMNS` varchar(255) NULL,
    `SM_ID` int NULL,
    PRIMARY KEY (`FUNC_ID` ASC) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE Indicator(
    `IND_ID` int AUTO_INCREMENT NOT NULL,
    `IND_NAME` varchar(50) NULL,
    `IND_DESC` varchar(100) NULL,
    `IND_UNIT` varchar(10) NULL,
    PRIMARY KEY (`IND_ID` ASC) 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE LoadSegment(
    `LS_ID` int AUTO_INCREMENT NOT NULL,
    `LS_LONG_NAME` char(20) NULL,
    `LS_SHORT_NAME` char(10) NULL,
    `LS_DESC` varchar(50) NULL,
    PRIMARY KEY (`LS_ID` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE ModelCountry(
    `CNTRY_ID` int AUTO_INCREMENT NOT NULL,
    `CNTRY_NAME` char(100) NULL,
    PRIMARY KEY (`CNTRY_ID` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE ModelType(
    `MODEL_ID` int AUTO_INCREMENT NOT NULL,
    `MODEL_TYPE_LONG_NAME` char(20) NULL,
    `MODEL_TYPE_SHORT_NAME` char(10) NULL,
    `MODEL_TYPE_DESC` varchar(50) NULL,
    PRIMARY KEY (`MODEL_ID` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE ModelYear(
    `YEAR_ID` int AUTO_INCREMENT NOT NULL,
    `YEAR_LONG_NAME` varchar(20) NULL,
    `YEAR_SHORT_NAME` varchar(10) NULL,
    PRIMARY KEY (`YEAR_ID` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE PlantType(
    `PLANT_ID` int AUTO_INCREMENT NOT NULL,
    `PLANT_SHORT_NAME` char(10) NULL,
    `PLANT_LONG_NAME` char(20) NULL,
    `PLANT_DESC` varchar(50) NULL,
    PRIMARY KEY (`PLANT_ID` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE Region(
    `REG_ID` int AUTO_INCREMENT NOT NULL,
    `REG_LONG_NAME` char(20) NULL,
    `REG_SHORT_NAME` char(10) NULL,
    `REG_DESC` varchar(50) NULL,
    PRIMARY KEY (`REG_ID` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE Season(
    `SEA_ID` int AUTO_INCREMENT NOT NULL,
    `SEA_TYPE_LONG_NAME` char(20) NULL,
    `SEA_TYPE_SHORT_NAME` char(10) NULL,
    `SEA_TYPE_DESC` varchar(50) NULL,
    PRIMARY KEY (`SEA_ID` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE SubModelDetails(
    `SM_ID` int AUTO_INCREMENT NOT NULL,
    `SM_LONG_NAME` char(20) NULL,
    `SM_SHORT_NAME` char(10) NULL,
    `SM_DESC` varchar(50) NULL,
    `MODEL_ID` int NULL,
    PRIMARY KEY (`SM_ID` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE WeekDetails(
    `WEEK_ID` int AUTO_INCREMENT NOT NULL,
    `WEEK_LONG_NAME` char(20) NULL,
    `WEEK_SHORT_NAME` char(10) NULL,
    `WEEK_DESC` varchar(50) NULL,
    PRIMARY KEY (`WEEK_ID` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `factentitlements` (
  `FACT_ID` int(11) NOT NULL AUTO_INCREMENT,
  `PLANT_ID` int(11) DEFAULT NULL,
  `WEEK_ID` int(11) DEFAULT NULL,
  `MODEL_ID` int(11) DEFAULT NULL,
  `FUEL_ID` int(11) DEFAULT NULL,
  `LS_ID` int(11) DEFAULT NULL,
  `IND_ID` int(11) DEFAULT NULL,
  `SEA_ID` int(11) DEFAULT NULL,
  `CNTRY_ID` int(11) DEFAULT NULL,
  `REG_ID` int(11) DEFAULT NULL,
  `YEAR_ID` int(11) DEFAULT NULL,
  `SM_ID` int(11) DEFAULT NULL,
  `FUNC_ID` int(11) DEFAULT NULL,
  `VALUE` double DEFAULT NULL,
  `USERNAME` char(100) DEFAULT NULL,
  `MAIN_VERSION` int(11) DEFAULT NULL,
  `SUB_VERSION` int(11) DEFAULT NULL,
  `INITIAL_LOAD_START_DATE` datetime(3) DEFAULT NULL,
  `INITIAL_LOAD_END_DATE` datetime(3) DEFAULT NULL,
  `LAST_EDIT_START_DATE` datetime(3) DEFAULT NULL,
  `LAST_EDIT_END_DATE` datetime(3) DEFAULT NULL,
  `UNIT` char(100) DEFAULT NULL,
  PRIMARY KEY (`FACT_ID`),
  KEY `FK_FuelType` (`FUEL_ID`),
  KEY `FK_FunctionDetails` (`FUNC_ID`),
  KEY `FK_Indicator` (`IND_ID`),
  KEY `FK_LoadSegment` (`LS_ID`),
  KEY `FK_ModelCountry` (`CNTRY_ID`),
  KEY `FK_ModelType` (`MODEL_ID`),
  KEY `FK_ModelYear` (`YEAR_ID`),
  KEY `FK_PlantType` (`PLANT_ID`),
  KEY `FK_Region` (`REG_ID`),
  KEY `FK_Season` (`SEA_ID`),
  KEY `FK_SubModelDetails` (`SM_ID`),
  KEY `FK_WeekDetails` (`WEEK_ID`),
  CONSTRAINT `FK_FuelType` FOREIGN KEY (`FUEL_ID`) REFERENCES `fueltype` (`FUEL_ID`),
  CONSTRAINT `FK_FunctionDetails` FOREIGN KEY (`FUNC_ID`) REFERENCES `functiondetails` (`FUNC_ID`),
  CONSTRAINT `FK_Indicator` FOREIGN KEY (`IND_ID`) REFERENCES `indicator` (`IND_ID`),
  CONSTRAINT `FK_LoadSegment` FOREIGN KEY (`LS_ID`) REFERENCES `loadsegment` (`LS_ID`),
  CONSTRAINT `FK_ModelCountry` FOREIGN KEY (`CNTRY_ID`) REFERENCES `modelcountry` (`CNTRY_ID`),
  CONSTRAINT `FK_ModelType` FOREIGN KEY (`MODEL_ID`) REFERENCES `modeltype` (`MODEL_ID`),
  CONSTRAINT `FK_ModelYear` FOREIGN KEY (`YEAR_ID`) REFERENCES `modelyear` (`YEAR_ID`),
  CONSTRAINT `FK_PlantType` FOREIGN KEY (`PLANT_ID`) REFERENCES `planttype` (`PLANT_ID`),
  CONSTRAINT `FK_Region` FOREIGN KEY (`REG_ID`) REFERENCES `region` (`REG_ID`),
  CONSTRAINT `FK_Season` FOREIGN KEY (`SEA_ID`) REFERENCES `season` (`SEA_ID`),
  CONSTRAINT `FK_SubModelDetails` FOREIGN KEY (`SM_ID`) REFERENCES `submodeldetails` (`SM_ID`),
  CONSTRAINT `FK_WeekDetails` FOREIGN KEY (`WEEK_ID`) REFERENCES `weekdetails` (`WEEK_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

ALTER TABLE `FactEntitlements` ADD CONSTRAINT `FK_FuelType` FOREIGN KEY(`FUEL_ID`) REFERENCES FuelType(`FUEL_ID`);

ALTER TABLE `FactEntitlements` ADD CONSTRAINT `FK_FunctionDetails` FOREIGN KEY(`FUNC_ID`) REFERENCES FunctionDetails(`FUNC_ID`)

ALTER TABLE `FactEntitlements` ADD CONSTRAINT `FK_Indicator` FOREIGN KEY(`IND_ID`) REFERENCES Indicator(`IND_ID`)

ALTER TABLE `FactEntitlements` ADD  CONSTRAINT `FK_LoadSegment` FOREIGN KEY(`LS_ID`) REFERENCES LoadSegment(`LS_ID`)

ALTER TABLE `FactEntitlements` ADD  CONSTRAINT `FK_ModelCountry` FOREIGN KEY(`CNTRY_ID`) REFERENCES ModelCountry(`CNTRY_ID`)

ALTER TABLE `FactEntitlements` ADD  CONSTRAINT `FK_ModelType` FOREIGN KEY(`MODEL_ID`) REFERENCES ModelType(`MODEL_ID`)

ALTER TABLE `FactEntitlements` ADD  CONSTRAINT `FK_ModelYear` FOREIGN KEY(`YEAR_ID`) REFERENCES ModelYear(`YEAR_ID`)

ALTER TABLE `FactEntitlements` ADD  CONSTRAINT `FK_PlantType` FOREIGN KEY(`PLANT_ID`) REFERENCES PlantType(`PLANT_ID`)

ALTER TABLE `FactEntitlements` ADD  CONSTRAINT `FK_Region` FOREIGN KEY(`REG_ID`) REFERENCES Region(`REG_ID`)

ALTER TABLE `FactEntitlements` ADD  CONSTRAINT `FK_Season` FOREIGN KEY(`SEA_ID`) REFERENCES Season(`SEA_ID`)

ALTER TABLE `FactEntitlements` ADD  CONSTRAINT `FK_SubModelDetails` FOREIGN KEY(`SM_ID`) REFERENCES SubModelDetails(`SM_ID`)

ALTER TABLE `FactEntitlements` ADD  CONSTRAINT `FK_WeekDetails` FOREIGN KEY(`WEEK_ID`) REFERENCES WeekDetails(`WEEK_ID`)