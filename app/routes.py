from flask import render_template, request, jsonify, session
from app import app, db, login_manager
# from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
# from werkzeug.urls import url_parse
# from urllib.parse import urlparse
from app.errors import bad_request, error_response
 
@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'Thai'}
    posts = [
        {
            'author': {'username': 'tcm1'},
            'body': 'post1'
        },
        {
            'author': {'username': 'tcm2'},
            'body': 'post2'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/users/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    # if not current_user.is_authenticated:
    #     return error_response(401, 'login required')
    return jsonify(User.query.get_or_404(id).to_dict())

@app.route('/login', methods=['POST'])
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return bad_request('username or password is missing')
    user = User.query.filter_by(username=request.form['username']).first()
    if user is None or not user.check_password(request.form['password']):
        return bad_request('invalid username or password')
    login_user(user, remember=True)
    session['user_id'] = user.id
    response = jsonify(user.to_dict())
    response.status_code = 200
    # response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # if not current_user.is_authenticated:
    #     return error_response(401, 'login required')
    logout_user()
    session.pop('user_id', None)
    return jsonify({'message': 'logout success'})

@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return error_response(400, 'logout required')
    if 'username' not in request.form or 'email' not in request.form or 'password' not in request.form:
        return bad_request('username, email, or password is missing')
    if User.query.filter_by(username=request.form['username']).first():
        return bad_request('username exists')
    if User.query.filter_by(email=request.form['email']).first():
        return bad_request('email exists')
    user = User()
    user.from_dict(request.form, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    return response

# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = [
#         {'author': user, 'body': 'post1'},
#         {'author': user, 'body': 'post2'}
#     ]
#     return render_template('user.html', user=user, posts=posts)

@login_manager.unauthorized_handler
def unauthorized():
    return error_response(401, 'login required')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))