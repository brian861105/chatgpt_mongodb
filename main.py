from line.line_bot import line_bot_blueprint
from flask import Flask

app = Flask(__name__)

app.register_blueprint(line_bot_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True, port=80)