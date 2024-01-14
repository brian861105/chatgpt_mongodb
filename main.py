from line.line_bot import line_bot_blueprint
from backend.flask_app.flaskapi import linebot_receive_blueprint
from flask import Flask

app = Flask(__name__)

app.register_blueprint(line_bot_blueprint, url_prefix='/')
app.register_blueprint(linebot_receive_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)