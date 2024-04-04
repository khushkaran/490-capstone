from flask import Flask, jsonify
from flask_cors import CORS

# how to run it: flask --app server --debug ru
def create_app():
    app = Flask(__name__)
    CORS(app)



    @app.route('/members')
    def api():
        return jsonify({'data': "Hello World"})

    return app