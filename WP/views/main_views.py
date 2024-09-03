from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect


main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/') # Url 주소창에 보이는 주소
def main_index():
    return render_template('index.html') # 실제 연결된 파일을 가져오는 파일이름

@main_bp.route('/iQ')
def index_questionlist():
    return redirect(url_for('question.question_list'))

@main_bp.route('/page2')
def page2():
    return render_template('page2.html')

@main_bp.route('/page3')
def page3():
    return render_template('page3.html')

@main_bp.route('/page4')
def page4():
    return render_template('page4.html')

@main_bp.route('/page5')
def page5():
    return render_template('page5.html')



