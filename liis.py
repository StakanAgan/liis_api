from app import create_app, db
from app.models import User, Question, Answer, Result, Poll

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Question': Question,
            'Answer': Answer, 'Result': Result, 'Poll': Poll}
