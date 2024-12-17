import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from routes import auth_bp, schedule_bp, task_bp

app = Flask(__name__)
CORS(app)


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(schedule_bp, url_prefix='/schedule')
app.register_blueprint(task_bp, url_prefix='/task')


if __name__ == '__main__':
    load_dotenv()
    app_port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=app_port)
