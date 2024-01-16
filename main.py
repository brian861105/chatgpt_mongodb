from line.line_bot import line_bot_blueprint
from backend.flask_app.flaskapi import linebot_receive_blueprint, database_blueprint
from frontend.front import static_server_bp
from flask import Flask

app = Flask(__name__)

app.register_blueprint(line_bot_blueprint, url_prefix='/')
app.register_blueprint(linebot_receive_blueprint, url_prefix='/line_receive')
app.register_blueprint(static_server_bp, url_prefix='/')
app.register_blueprint(database_blueprint, url_prefix='/database')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)