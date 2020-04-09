from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import ast
import os
import json


app = Flask(__name__)
CORS(app)


@app.route('/', methods=["GET"])
def root_handler():

    if os.path.exists('data/den.json'):
        with open('data/den.json', 'r') as f:
            den = json.load(f)

        response = {
           'response': 'OK',
            'data': den
        }

    else:
        response = {
            'response' : 'NG',
            'message': 'No den data'
        }


    return response





if __name__ == '__main__':
    app.run()

