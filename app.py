from flask import Flask, redirect, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from pymongo.errors import DuplicateKeyError
from db import get_user, save_user

app = Flask(__name__)
app.secret_key = "@DK090234tir-kf"
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/chat")
@login_required
def chat():
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template('chat.html', username=username, room=room)
    return redirect('/')

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info(f"{data['username']} has joined the room {data['room']}")
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info(f"{data['username']} has sent message to the room {data['room']}: {data['message']}")
    socketio.emit('recive_message', data, room=data['room'])

@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info(f"{data['username']} has left the room {data['room']}")
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])

@login_manager.user_loader
def load_user(username):
    return get_user(username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        submited_password = request.form.get('password')
        user = get_user(username)
        if user and user.check_password(submited_password):
            login_user(user)
            return redirect('/')
        else:
            message = 'Failed to login. Wrong username or password.'
    return render_template('login.html', message=message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect('/')

    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            save_user(username, email, password)
            return redirect('/login')
        except DuplicateKeyError:
            message = 'Such username already exists'
    return render_template('signup.html', message=message)

if __name__ == '__main__':
    socketio.run(app, debug=True)