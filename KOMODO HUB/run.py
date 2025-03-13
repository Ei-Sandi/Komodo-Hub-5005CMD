from app import create_app
from flask_socketio import SocketIO

flask_app = create_app()
socketio = SocketIO(flask_app)

if __name__ == "__main__":
<<<<<<< HEAD
    socketio.run(flask_app, debug=True, host="localhost")
=======
    socketio.run(flask_app, debug=True, host= "localhost")
>>>>>>> 6805f6ec8762af1aa86ed6a999f64509d3e3b519
