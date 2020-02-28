from app.api import bp
from flask import jsonify, g, request
from app.api.errors import bad_request
from app.models import *
from app.api.auth import token_auth
from app.util import check_body_response, make_response


# @bp.route('/results/statistic/<int:poll_id>', methods=['GET'])
# @token_auth.login_required
# def get_result_count(poll_id):
#     response = {}
#     results = Result.query.filter_by(poll_id=poll_id).all()
#     current = Result.query.filter_by(poll_id=poll_id).filter_by(user_id=g.current_user.id).first()
#     for result in results:
#         if g.current_user.id == result.user_id:
#             poll_count = len(results)
#
#         return , 200


@bp.route('/results', methods=['POST'])
@token_auth.login_required
def mcoake_result():
    print(g.current_user)
    data = request.get_json() or {}
    if check_body_response('poll_id', 'question_id', 'answer_id', data=data) is False:
        return bad_request('must include poll_id, question_id and answer_id fields')
    if Result.query.filter_by(user_id=g.current_user.id).filter_by(question_id=data['question_id']).first():
        return bad_request('Ответ на вопрос уже есть. Используйте метод ...')
    result = Result(user_id=g.current_user.id, poll_id=0, question_id=0, answer_id=0)
    result.from_dict(data)
    response = make_response(result, data)
    return response


@bp.route('/results/<int:id>', methods=['GET'])
@token_auth.login_required
def get_result(id):
    return jsonify(Result.query.get_or_404(id).to_dict())


@bp.route('/results', methods=['PUT'])
@token_auth.login_required
def update_result():
    data = request.get_json() or {}
    result = Result.query.filter_by(user_id=g.current_user.id).filter_by(question_id=data['question_id']).first()
    result.from_dict(data)
    db.session.commit()
    return jsonify(result.to_dict())


@bp.route('/polls', methods=['POST'])
@token_auth.login_required
def create_poll():
    data = request.get_json() or {}
    if check_body_response('name', 'describe', data=data) is False:
        return bad_request('must include name and describe fields')
    if Poll.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    poll = Poll()
    poll.from_dict(data)
    response = make_response(poll, data)
    return response


@bp.route('/polls/<int:id>', methods=['GET'])
@token_auth.login_required
def get_poll(id):
    return jsonify(Poll.query.get_or_404(id).to_dict())


@bp.route('/polls/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_poll(id):
    Poll.query.filter_by(id=id).delete()
    db.session.commit()
    return '', 204


@bp.route('/polls/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_poll(id):
    data = request.get_json() or {}
    poll = Poll.query.get_or_404(id)
    if 'name' in data and data['name'] != Poll.name and Question.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    poll.from_dict(data)
    db.session.commit()
    return jsonify(poll.to_dict())


@bp.route('/questions', methods=['POST'])
@token_auth.login_required
def create_question():
    data = request.get_json() or {}
    if check_body_response('name', 'describe', 'poll_id', data=data) is False:
        return bad_request('must include name and describe fields')
    if Question.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    question = Question()
    question.from_dict(data)
    response = make_response(question, data)
    return response


@bp.route('/questions/<int:id>', methods=['GET'])
@token_auth.login_required
def get_question(id):
    return jsonify(Question.query.get_or_404(id).to_dict())


@bp.route('/polls/questions/<int:id>', methods=['GET'])
@token_auth.login_required
def get_poll_questions(id):
    questions = Question.query.filter_by(poll_id=id).all()
    response = list()
    for q in questions:
        q = q.to_dict()
        response.append(q)
    return jsonify(response)


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


@bp.route('/questions/answers/<int:id>', methods=['GET'])
@token_auth.login_required
def get_question_answers(id):
    answers = Answer.query.filter_by(question_id=id).all()
    response = list()
    for a in answers:
        a = a.to_dict()
        response.append(a)
    return jsonify(response)


@bp.route('/answers', methods=['POST'])
@token_auth.login_required
def create_answer():
    data = request.get_json() or {}
    if check_body_response('response', 'question_id', data=data):
        return bad_request('must include describe and question_id fields')
    answer = Answer()
    answer.from_dict(data)
    response = make_response(answer, data)
    return response


@bp.route('/answers/<int:id>', methods=['GET'])
@token_auth.login_required
def get_answer(id):
    return jsonify(Answer.query.get_or_404(id).to_dict())


@bp.route('/answers/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_answer(id):
    Answer.query.filter_by(id=id).delete()
    db.session.commit()
    return '', 204


@bp.route('/answers/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_answer(id):
    data = request.get_json() or {}
    answer = Answer.query.get_or_404(id)
    if 'response' in data and data['response'] != answer.response and Question.query.filter_by(
            name=data['response']).first():
        return bad_request('please use a different response')
    answer.from_dict(data)
    db.session.commit()
    return jsonify(answer.to_dict())


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if check_body_response('username', 'email', 'password', data=data) is False:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    response = make_response(user, data)
    return response
