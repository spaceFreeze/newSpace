import os
# ORM 적용하기 위한 코드

BASE_DIR = os.path.dirname(__file__)  # c:\projects\sksk

# DB 접속 주소, SQLAlchemy 이벤트 처리 옵션, ascii 인코딩 해제, 비즈니스 로직 후 Commit 실행 여부
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'sksk.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
JSON_AS_ASCII = False
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True