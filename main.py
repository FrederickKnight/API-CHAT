from app import create_app,socketio
from app.chat import *

app = create_app()

if __name__ == "__main__":
    
    # app.run(debug=True)
    socketio.run(app, host="0.0.0.0", port=5000,debug=True)