from os import path

# Flask
APP_NAME = 'enermod'
DEBUG = True
SERVER_HOST = 'localhost'
SERVER_PORT = 8010
SECRET_KEY = 'C{2{]fKbo91G7IpkZniy'

# Localization
CURRENT_TIMEZONE = 'Asia/Riyadh'
FALLBACK_LOCALE = 'en'

# Paths
APP_ROOT = path.dirname(path.abspath(__file__))
TEMPLATES_ROOT = path.join(APP_ROOT, 'templates')

# SQL ALCHEMY
# SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://eim_enermod_d_rw:eimUser@KAPS@10.200.69.132\EIM/EnerMod'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://scot:tiger@localhost/Enermod'

# WTF Secret key
WTF_CSRF_SECRET_KEY = 'nrX:z]C^wO<w5{,'

# LDAP
LDAP_PROVIDER_URL = 'ldap://127.0.0.1:389'
LDAP_PROTOCOL_VERSION = 3

# Default Records UserName
DEFAULT_USERNAME = 'SYSADMIN'