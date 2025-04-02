from app import create_app
from flask_socketio import SocketIO

flask_app = create_app()
socketio = SocketIO(flask_app, cors_allowed_origins="*")

if __name__ == "__main__":
    socketio.run(flask_app, debug=True, host="localhost")




