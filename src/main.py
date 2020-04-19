from flask import Flask, jsonify, request, redirect, Response, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import enum 

from glob import glob
import face_recognition
import numpy as np
import codecs, json
import os.path
import eventlet
import cv2
from time import sleep
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'flask_mqtt'
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '../images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

is_obama = 0
face_found = 0
name = ''
pesan = ''

    
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/facerecog', methods=['POST'])
def upload_image():
    
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            return search_face_from_json(file)
    return Response(response="ok", status=200)


def get_face(face_found, is_obama, nama):
    if face_found == 1:
        ketemu = "founded"
    result = {
        "is_there_face": ketemu,
        "is_picture_of_obama": is_obama,
        "name" : nama
    }
    return result

def search_face_from_json(file_stream):
    pattern = os.path.join('./data/faces/','*.json')
    for file_name in glob(pattern):
        obj_text = codecs.open(file_name, 'r', encoding='utf-8').read()
        b_new = json.loads(obj_text)
        a_new = np.array(b_new)
        nam = str(file_name).replace(".json",'')
        name = nam.replace('./data/faces/','')
        known_face_encoding = np.array(a_new)
        img = face_recognition.load_image_file(file_stream)
        unknown_face_encodings = face_recognition.face_encodings(img)

        if len(unknown_face_encodings) > 0:
            match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
            face_found = 1
            if match_results[0]:
                mqtt.publish('helloop', "1")
                is_obama = 1
                nama = name
                return get_face(face_found, is_obama, nama)
    result = {
        "is_there_face": "not found",
    }      
    return result

def ayam():
    cam = cv2.VideoCapture(0)
    retval, frame = cam.read()
    if retval != True:
        raise ValueError("Can't read frame")
    
    cv2.imwrite('./tmp/tmp.jpg', frame)
    sleep(1)
    return "ayam"
                
@app.route('/inputface', methods=['POST'])
def conver_image():
    if request.method == 'POST':

        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        if file and allowed_file(file.filename):
            
            return conver_image_to_encoded(file, file.filename)


def conver_image_to_encoded(file_encoded, file_name):
    img = face_recognition.load_image_file(file_encoded)
    encoding = face_recognition.face_encodings(img)[0]
    b = encoding.tolist()
    file_path = "./data/faces/"+ str(file_name).replace(".jpg",'') + ".json" 
    json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
    resp = {"message":"face registered"}
    return jsonify(resp), 200

@app.route('/')
def alert():
    return render_template("alert.html", name=pesan)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('hello')


    

@mqtt.on_topic('hello')
def handle_mqtt_message(client, userdata, message):
    data = []
    a = 0
    with open("./db/data", "a") as myfile:
        myfile.write("1 \n")
        file = open("./db/data", 'r')
        lines = file.readlines()
        
    for line in lines:
        a += 1

    
    ayam()
    kenal = search_face_from_json('./tmp/tmp.jpg')
    if len(kenal) > 1:
        data = dict(
            topic=message.topic,
            payload=message.payload.decode(),
            qos=message.qos,
            muka = str(kenal['is_there_face']),
            jumlah = a,
            name = str(kenal['name']),

        )
    else:
        data = dict(
            topic=message.topic,
            payload=message.payload.decode(),
            qos=message.qos,
            muka = str(kenal['is_there_face']),
            jumlah = a
        )

    print(data)
    
    socketio.emit('mqtt_message', data=data)
    
        
   

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # print(level, buf)
    pass


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
