from os import path

# Flask
APP_NAME = 'enermod'
DEBUG = False
SERVER_HOST = 'localhost'
SERVER_PORT = 8010
SECRET_KEY = 'C{2{]fKbo91G7IpkZniy'

# Localization
CURRENT_TIMEZONE = 'Asia/Riyadh'
FALLBACK_LOCALE = 'en'

# Paths
APP_ROOT = path.dirname(path.abspath(__file__))
TEMPLATES_ROOT = path.join(APP_ROOT, 'templates')
