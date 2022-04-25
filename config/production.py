from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'sksk.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\xdemp\xd5\x9b\xda\xf7E\xe3\xa6\x87i\xbc\x00\xb8\x85'