from flask import Flask, render_template, Response, jsonify, request, session

# FlaskForm = used for file input forms

from flask_wtf import FlaskForm

from wtforms import FileField, SubmitField, StringField, DecimalRangeField, IntegerRangeField, IntegerField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, NumberRange
import os

from math import floor
from bson.json_util import dumps


import json
import cv2

# YOLO_Video is the python file which contains the code for our object detection model
# Video Detection is the Function which performs Object Detection on Input Video
from db_connection import find_traffic_data

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tofuhermit'
app.config['UPLOAD_FOLDER'] = 'static/files'

@app.route('/', methods=['GET', 'POST'])
@app.route('/find', methods=['GET', 'POST'])
def find():
    query_params = request.args.to_dict()

    documents = list(find_traffic_data(query_params))

    json_data = dumps(documents, indent=2)
    return Response(json_data, mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
