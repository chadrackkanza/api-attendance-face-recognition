# -*- coding: utf-8 -*-
import  cv2
import face_recognition 
import os
from face_recognition.api import face_encodings
import numpy as np
from datetime import date, datetime
from flask import Flask, request, redirect, url_for, Response
import databaseScript
from datetime import date,datetime
import json


# create the Flask app
app = Flask(__name__)
message = {}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file, id):
    file.save(os.path.join(f'Images/',f"{id}-{file.filename}"))
    

def findEncodingImg(images):       
    encodeList = []
    
    for img in images:
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            encodings = face_recognition.face_encodings(img)
            print(encodings)
            if len(encodings) > 0:
                encodeList.append(encodings[0])
            else:
                print("[WARNING] Aucun visage détecté dans l'image.")

        except Exception as e:
            print(f"[ERROR] Une erreur s'est produite : {e}")

    return encodeList



@app.route('/employees', methods=['GET'])
def getEmployeesdata():
    print("ok")
    return databaseScript.getEmployees()
     


@app.route('/enroll/<id>', methods=['POST'])
def enrollement(id):
    file = request.files['photo']

    if file.filename == '':
        message = { 'message' : 'No file selected'}
        return Response(json.dumps(message), status=400, mimetype='application/json')


    if file and allowed_file(file.filename):
        if not os.path.exists(f'Images/'):
            os.makedirs(f'Images/')
        
        today = date.today()

        path_image = f'Images/{id}-{file.filename}'
        result = databaseScript.enroll_employee(id, path_image)
        save_file(file, id)
        return result


@app.route('/check', methods=['POST'])
def check():
    
    file = request.files['photo']


    if file.filename == '':
        message = { 'message' : 'No file selected'}
        return Response(json.dumps(message), status=400, mimetype='application/json')
        
    if file and allowed_file(file.filename):
        path=f'Images'
        if not os.path.exists(path):
            message = {'message' : 'Employee isn\'t enrolled'}
            return Response(json.dumps(message), status=400, mimetype='application/json')

        else:
            images=[]
            classNames=[]
            myList=os.listdir(path)
            
            for cl in myList:
                curImage=cv2.imread(f'{path}/{cl}')
                images.append(curImage)
                classNames.append(os.path.splitext(cl)[0])
            known_face_encodings=findEncodingImg(images)
            print("Encoding complete.....")
            
            npImage = np.fromfile(file,np.uint8)
        
            img = cv2.imdecode(npImage, cv2.COLOR_BGR2RGB)
            faceEncodings=face_recognition.face_encodings(img)
            if (len(faceEncodings)):
                if(len(known_face_encodings)):
                    myEncode= faceEncodings[0]
                    matches=face_recognition.compare_faces(known_face_encodings, myEncode, tolerance=0.4)
                    faceDis=face_recognition.face_distance(known_face_encodings, myEncode)
                    matcheIndexes=np.argmin(faceDis)

                    print("matches")
                    print(matches)

                    print("faceDis")
                    print(faceDis)

                    print("matcheIndexes")
                    print(matcheIndexes)

                    print(matches[matcheIndexes])
                    
                    if(matches[matcheIndexes]):
                        today = date.today()
                        path_image = f'{path}/{file.filename}'
                        id = ((classNames[matcheIndexes]).split('-'))[0]
                        result = databaseScript.get_etudiant_info(id) 
                        print(result)
                        return result


                    else :
                        message = {'message' : 'Visage inconnu'}
                        return Response(json.dumps(message), status=400, mimetype='application/json')
                else :
                    message = {'message' : 'Aucune personne n\'a été trouvé'}
                    return Response(json.dumps(message), status=400, mimetype='application/json')
            else : 
                message = {'message' : 'Envoyer l\' image d\'une personne'}
                return Response(json.dumps(message), status=400, mimetype='application/json')
            
if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True,host='0.0.0.0', port=5500)
    