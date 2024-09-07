from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'wp.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'h\xedB\x85\x168\xb0\x9d\xe0\xec:!%\xed! '