import os.path
from glob import glob
import codecs, json
import numpy as np
import face_recognition

pattern = os.path.join('./data/faces/','*.json')
is_obama = 0
face_found = 0
name = ''

def get_face(face_found, is_obama, name):
    
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_obama": is_obama,
        "name" : name
    }
    return result

for file_name in glob(pattern):
    obj_text = codecs.open(file_name, 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    a_new = np.array(b_new)
    known_face_encoding = np.array(a_new)
    known_face_encoding = np.array(a_new)
    img = face_recognition.load_image_file("../images/obama.jpg")
    unknown_face_encodings = face_recognition.face_encodings(img)
    match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])

    if len(unknown_face_encodings) > 0:
        face_found = 1
        if match_results[0]:
            is_obama = 1
            name = file_name
            print(get_face(face_found, is_obama, name))
       
            




