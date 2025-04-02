from app import create_app
from flask_socketio import SocketIO

flask_app = create_app()
socketio = SocketIO(flask_app, cors_allowed_origins="*")

if __name__ == "__main__":
<<<<<<< HEAD
    socketio.run(flask_app, debug=True, host="localhost")
=======
    socketio.run(flask_app, debug=True, host="localhost")
>>>>>>> f56c54d104846e56db8efb80dc9c69408f61594e
