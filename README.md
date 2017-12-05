## Model Databrowser [![python version](https://img.shields.io/badge/python-v2.7.12-yellowgreen.svg)](https://www.python.org/download/releases/2.7/) [![Node version](https://img.shields.io/badge/npm-v4.4.1-green.svg)](http://nodejs.org/download/) [![mit](https://img.shields.io/npm/l/express.svg?style=plastic)](https://opensource.org/licenses/MIT) [![status](https://img.shields.io/pypi/status/Django.svg?style=plastic)]()


Enermod is a Model Data Editor to keep track of various versions of your data to run your models from softwares like eviews, gams, etc

Feature list:

 * Compatible with MYSQL and MS SQL
 * Use generated SQL queries in place of your current hardcoded tables
 * LDAP Integration
 * GAMS Data Exchange Integration
 * See other team members data versions

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
 
 * [Python 2.7][py27]
 * [Flask==0.10.1](https://www.python.org/download/releases/2.7/)
 * python-ldap==2.4.38
 * SQLAlchemy==1.1.12
 * flask-login==0.4.0
 * flask-sqlalchemy==2.2
 * flask-wtf==0.14.2
 * marshmallow==2.13.5
 * pymysql==0.7.11

##### And here's the code install the prerequisites packages! :heavy_check_mark:

```python
pip install -r requirements.txt
```
##### Add server, database, LDAP and other configuarations in the below file,

```python
settings.py
```

##### Sample SQL schema is added in schema folder,

```SQL
schema/schema.sql
```

##### Connection URI Format
Change the SQLALCHEMY_DATABASE_URI, For a complete list of connection URIs head over to the SQLAlchemy documentation under (Supported Databases). This here shows some common connection strings.

SQLAlchemy indicates the source of an Engine as a URI combined with optional keyword arguments to specify options for the Engine. The form of the URI is:

```
dialect+driver://username:password@host:port/database
```

Many of the parts in the string are optional. If no driver is specified the default one is selected (make sure to not include the + in that case).

MySQL:

```
mysql://scott:tiger@localhost/EnerMod
```

SQL Server:

```
mssql+pymssql://scott:tiger@localhost/EnerMod
```

SQLite (note that platform path conventions apply):

```
#Unix/Mac (note the four leading slashes)
sqlite:////absolute/path/to/EnerMod.db
#Windows (note 3 leading forward slashes and backslash escapes)
sqlite:///C:\\absolute\\path\\to\\EnerMod.db
#Windows (alternative using raw string)
r'sqlite:///C:\absolute\path\to\EnerMod.db'
```

##### LDAP configurations

* LDAP_PROVIDER_URL -  the hostname or IP address ldap server
* LDAP_PROTOCOL_VERSION - the protocal version
* LDAP_PORT - the port where ldap server is listening (Default: 389)

##### Code to start server! :heavy_check_mark:

```python
python enermod.py
```

#### TODO List:

* Angular 4
* Generic ORM
* Eviews, Pyomo Data Exchange Integration
* Admin panel

[py27]: <https://www.python.org/download/releases/2.7/>