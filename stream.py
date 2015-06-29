from gevent import monkey
monkey.patch_all()

import time
import random
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, disconnect

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

def generate_random(a, b):
    """Generate a random integer between a and b"""
    return random.randint(a, b)

def background_thread():
    """Send server generated events to clients."""
    while True:
        sleep_time = generate_random(200, 1000) / float(1000)
        print sleep_time
        time.sleep(sleep_time)
        watts = random.randint(0, 3000) / float(10)
        socketio.emit('my response',
                      {'data': 'Server generated event', 'watts': watts, 'sleep_time': sleep_time},
                      namespace='/test')

@app.route('/')
def index():
    """Render index.html"""
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('index.html')

@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    """Disconnect thread"""
    disconnect()

if __name__ == '__main__':
    socketio.run(app)
