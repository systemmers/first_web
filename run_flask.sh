
#!/bin/bash

# ���� ȯ�� Ȱ��ȭ
cd ~/venvs/Web_Projekt/bin
source activate

# ������Ʈ ���丮�� �̵�
cd ~/projekts/Web_Projekt

# ȯ�� ���� ����
export FLASK_APP=WP
export FLASK_DEBUG=true
export APP_CONFIG_FILE=/home/ubuntu/projekts/Web_Projekt/config/production.py

# Flask ����
flask run --host=0.0.0.0
