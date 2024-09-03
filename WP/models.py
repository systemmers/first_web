from WP import db  
# WP 모듈(폴더나 파일)에서 __init__.py, db를 import, 
# 환경변수로 WP 폴더, __init__.py 지정, 자동 시작, __init__ 파일내, db 모듈, 즉 변수, db = SQLAlchemy() 인스턴스 생성


question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)


answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)


class Question(db.Model):  # Question 테이블 정의
    id = db.Column(db.Integer, primary_key=True)  # id 필드 정수형, 기본키
    subject = db.Column(db.String(200), nullable=False)  # subject 필드 문자열(200자 이하), 비어있지 않음
    content = db.Column(db.Text(), nullable=False)  # content 필드 텍스트 형식, 비어있지 않음
    create_date = db.Column(db.DateTime(), nullable=False)  # create_date 필드 날짜 및 시간 형식, 비어있지 않음
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # nullable=True, server_default='1'
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))


class Answer(db.Model):  # Answer 테이블 정의
    id = db.Column(db.Integer, primary_key=True)  # id 필드 정수형, 기본키
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))  # question_id 필드 정수형, question 테이블의 id와 외래키로 연결, CASCADE 삭제 규칙
    question = db.relationship('Question', backref=db.backref('answer_set'))  # question 필드와 Question 테이블과의 관계 설정, answer_set 역참조 설정
    content = db.Column(db.Text(), nullable=False)  # content 필드 텍스트 형식, 비어있지 않음
    create_date = db.Column(db.DateTime(), nullable=False)  # create_date 필드 날짜 및 시간 형식, 비어있지 않음
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

    
class User(db.Model):   # User 테이블 정의, 클래스 명의 소문자로 테이블 이름으로 저장된다. > user 디폴트 세팅값
    # __tablename__ = 'User", 클래스와 동일하게 저장할 수 있거나 임의 데로 저장할 수 있는 방법이다.
    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
