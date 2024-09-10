
#!/bin/bash

# 가상 환경 활성화
cd ~/venvs/Web_Projekt/bin
source activate

# 프로젝트 디렉토리로 이동
cd ~/projekts/Web_Projekt

# 환경 변수 설정
export FLASK_APP=WP
export FLASK_DEBUG=true
export APP_CONFIG_FILE=/home/ubuntu/projekts/Web_Projekt/config/production.py

# Flask 실행
flask run --host=0.0.0.0
