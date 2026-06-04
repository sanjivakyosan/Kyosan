# Copyright © Charles Roux 2026
from app import app, socketio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    # Run the application on port 5001
    socketio.run(
        app,
        host='0.0.0.0',
        port=5001,
        debug=os.getenv('FLASK_ENV') == 'development',
        allow_unsafe_werkzeug=True
    ) 