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
SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://eim_enermod_d_rw:eimUser@KAPS@10.200.69.132\EIM/EnerMod'

# WTF Secret key
WTF_CSRF_SECRET_KEY = 'nrX:z]C^wO<w5{,'

# LDAP
LDAP_PROVIDER_URL = 'ldap://blueberry-03.KAPSARC.ORG:389'
LDAP_PROTOCOL_VERSION = 3