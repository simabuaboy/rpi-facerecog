import numpy as np
import codecs, json 
import face_recognition
known_image = face_recognition.load_image_file("../images/2020-04-17-184126.jpg")
unknown_image = face_recognition.load_image_file("../images/barack-obama-12782369-1-402.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
b = biden_encoding.tolist()
file_path = "./data/faces/path.json" ## your path variable
json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format

obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
b_new = json.loads(obj_text)
a_new = np.array(b_new)

print(type(a_new))
# print(biden_encoding)
# print(unknown_encoding)

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)