from flask import Flask, Response, request
import csv
from io import StringIO
from bson.json_util import dumps


import json
import cv2

# YOLO_Video is the python file which contains the code for our object detection model
# Video Detection is the Function which performs Object Detection on Input Video
from db_connection import find_traffic_data

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tofuhermit'
app.config['UPLOAD_FOLDER'] = 'static/files'

@app.route('/')
@app.route('/find')
def find():
    query_params = request.args.to_dict()

    documents = list(find_traffic_data(query_params))

    json_data = dumps(documents, indent=2)
    return Response(json_data, mimetype='application/json')


@app.route('/export')
def export():
    query_params = request.args.to_dict()
    documents = list(find_traffic_data(query_params))

    # Create a CSV buffer
    csv_buffer = StringIO()

    headers = documents[-1].keys()

    csv_writer = csv.DictWriter(csv_buffer, fieldnames=headers)

    csv_writer.writeheader()

    for document in documents:
        csv_writer.writerow(document)

    csv_data = csv_buffer.getvalue()

    response = Response(csv_data, mimetype='text/csv')

    response.headers.set("Content-Disposition", "attachment", filename="traffic_data.csv")

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
