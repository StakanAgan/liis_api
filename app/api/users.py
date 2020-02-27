from app.api import bp
from flask import url_for, jsonify, g, abort, request
from app import db
from app.api.errors import bad_request
from app.models import *
from app.api.auth import token_auth


@bp.route('/results/count/<int:question_id>', methods=['GET'])
@token_auth.login_required
def get_result_count(question_id):
    results = Result.query.filter_by(question_id=question_id).all()
    return 'Count of response for this question = '+str(len(results)), 200


@bp.route('/results', methods=['POST'])
@token_auth.login_required
def make_result():
    data = request.get_json() or {}
    if 'user_id' not in data or 'question_id' not in data or 'answer_id' not in data:
        return bad_request('must include user_id, question_id and answer_id fields')
    if Result.query.filter_by(user_id=data['user_id']).filter_by(question_id=data['question_id']).first():
        return bad_request('Ответ на вопрос уже есть. Используйте метод ...')
    result = Result()
    result.from_dict(data)
    db.session.add(result)
    db.session.commit()
    response = jsonify(result.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_result', id=result.id)
    return response


@bp.route('/results', methods=['GET'])
@token_auth.login_required
def get_result():
    username = request.args.get('user_id')
    question = request.args.get('question_id')
    result = Result.query.filter_by(user_id=username).filter_by(question_id=question).first().to_dict()
    return jsonify(result)


@bp.route('/results', methods=['PUT'])
@token_auth.login_required
def update_result():
    data = request.get_json() or {}
    result = Result.query.filter_by(user_id=data['user_id']).filter_by(question_id=data['question_id']).first()
    result.from_dict(data)
    db.session.commit()
    return jsonify(result.to_dict())


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json() or {}
    if 'name' not in data or 'describe' not in data:
        return bad_request('must include name and describe fields')
    if Question.query.filter_by(name=data['name']).first():
        return bad_request('pleasy use a different name')
    question = Question()
    question.from_dict(data)
    db.session.add(question)
    db.session.commit()
    response = jsonify(question.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_question', id=question.id)
    return response


@bp.route('/questions/<int:id>', methods=['GET'])
@token_auth.login_required
def get_question(id):
    return jsonify(Question.query.get_or_404(id).to_dict())


@bp.route('/questions/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_question(id):
    Question.query.filter_by(id=id).delete()
    db.session.commit()
    return '', 204


@bp.route('/questions/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_question(id):
    data = request.get_json() or {}
    question = Question.query.get_or_404(id)
    if 'name' in data and data['name'] != question.name and Question.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    question.from_dict(data)
    db.session.commit()
    return jsonify(question.to_dict())


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())
