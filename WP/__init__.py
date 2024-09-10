

# 가상환경 생성
# python -m venv myproject : root_Directory


# requirements.txt
# pip freeze > requirements.txt
# pip install -r requirements.txt

# 가상환경 설정_Scripts
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser : 실행정책 변경 > 해제, activate 
# Set-ExecutionPolicy Restricted -Scope CurrentUser 

# flask run_루트디렉토리, 환경변수 설정 
# $env:FLASK_APP = "app" : "파일이름"
# $env:FLASK_ENV = "development" : 개발모드
# $env:FLASK_DEBUG = "true"
# flask run
# flask run --host=0.0.0.0 : 접속 ip

# export FLASK_APP=WP
# export FLASK_DEBUG=true
# export APP_CONFIG_FILE=/home/ubuntu/projects/WP/config/production.py

# #https://github.com/systemmers/first_web.git

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    
    from . import models

    # 블루프린트 등록
    from .views import main_views, question_views, answer_views, auth_views # 1차 경로, 임포트
    app.register_blueprint(main_views.main_bp)
    app.register_blueprint(question_views.question_bp) # 2차경로 임포트, 함수
    app.register_blueprint(answer_views.answer_bp)
    app.register_blueprint(auth_views.auth_bp)

    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)