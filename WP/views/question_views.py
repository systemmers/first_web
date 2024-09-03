from datetime import datetime

from flask import Blueprint, render_template, request, url_for,g, flash
from werkzeug.utils import redirect

from .. import db
from WP.models import Question, Answer, User
from WP.forms import QuestionForm, AnswerForm
from WP.views.auth_views import login_required

question_bp = Blueprint('question', __name__, url_prefix='/question')



# @question_bp.route('/question_list')
# def question_list():
#     page = request.args.get('page', type=int, default=1) # 페이지
#     question_list = Question.query.order_by(Question.create_date.desc())
#     question_list = question_list.paginate(page=page, per_page=10)
#     return render_template('question/question_list.html', question_list=question_list)

@question_bp.route('/question_list/')
def question_list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) | # 질문제목
                    Question.content.ilike(search) | # 질문내용
                    User.username.ilike(search) | # 질문작성자
                    sub_query.c.content.ilike(search) | # 답변내용
                    sub_query.c.username.ilike(search) # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)
    


@question_bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm() # Forms.py .AnswerForm()
    question = Question.query.get_or_404(question_id) # 404 : Not Found 오류 메시지
    return render_template('question/question_detail.html', question=question, form=form)



@question_bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm() # Forms.py .QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question.question_list'))
    return render_template('question/question_form.html', form=form)



@question_bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required # @데코레이터, 에너테이션, 함수가 실행되기 전에 먼저 실행되어짐
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST': # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now() # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else: # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)



@question_bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question.question_list'))



@question_bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        flash('본인이 작성한글은 추천할수 없습니다.')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
