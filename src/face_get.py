


def get_face(face_found, is_obama, nama):
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_obama": is_obama,
        "name" : nama
    }
    return jsonify(result), 201

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
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])

        if len(unknown_face_encodings) > 0:
            face_found = 1
            if match_results[0]:
                is_obama = 1
                nama = name
                return get_face(face_found, is_obama, nama)
            elif match_results[0] == False:
                result = {
                        "is_there_face": "not found",
                    }
    a = 0
    with open("./db/data", "a") as myfile:
        myfile.write("1 \n")
        file = open("./db/data", 'r')
        lines = file.readlines()
        
    for line in lines:
        a += 1

    mqtt.publish('helloop', a)
    return jsonify(result), 404