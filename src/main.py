import face_recognition
from flask import Flask, jsonify, request, redirect, Response
import numpy as np
import codecs, json

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/facerecog', methods=['POST'])
def upload_image():
    if request.method == 'POST':

        file = request.files['file']

        if file and allowed_file(file.filename):
            return detect_faces_in_image(file)

    return Response(response="ok", status=200)


def detect_faces_in_image(file_stream):

    file_path = "./data/faces/path.json" 
    obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    known_face_encoding = np.array(b_new)

    print(type(known_face_encoding))

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    is_obama = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_obama = True

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_obama": is_obama
    }
    return jsonify(result)


@app.route('/inputface', methods=['POST'])
def conver_image():
    if request.method == 'POST':

        file = request.files['file']

        if file and allowed_file(file.filename):
            
            return conver_image_to_encoded(file, file.filename)


def conver_image_to_encoded(file_encoded, file_name):
    img = face_recognition.load_image_file(file_encoded)
    encoding = face_recognition.face_encodings(img)[0]
    b = encoding.tolist()
    file_path = "./data/faces/"+ str(file_name).replace(".jpg",'') + ".json" ## your path variable
    json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format

    return Response(response="ok", status=200)





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)