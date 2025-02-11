# importing module
import random
from collections import OrderedDict
from datetime import date, datetime
from flask import Response
import json
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='08294',
                             database='studentfacialerecognition',
                             cursorclass=pymysql.cursors.DictCursor)

# Creating connection Object which will contain MySQL Server Connection

print("connection")
print(connection)

cursor = connection.cursor()

def getEmployees():
    sql = "SELECT * FROM etudiants"
    param_values = ()
    cursor.execute(sql, param_values)
    results = cursor.fetchall()
    employees = []
    content = {}
    for result in results:
        content = {
            'id': result[0],
            'name': result[1],
            'sexe': result[2],
            'adresse': result[3],
            'promotion': result[4],
            'annee_academique': result[5]
        }
        employees.append(content)
    print(employees)
    return json.dumps(employees, default=str)

def enroll_employee(etudiant_id, picture):
    date_enrolment = datetime.now()
    sql = "INSERT INTO attendance_enrolments (etudiant_id, date_enrolment, picture) VALUES (%s, %s, %s)"
    param_values = (etudiant_id, date_enrolment, picture)
    cursor.execute(sql, param_values)
    connection.commit()

    message = {'message': 'Employee is enrolled with success'}
    return Response(json.dumps(message), status=200, mimetype='application/json')

def get_etudiant_info(etudiant_id):
    sql_select = """
        SELECT *
        FROM etudiants e 
        WHERE id = %s
    """
    cursor.execute(sql_select, (etudiant_id,))
    etudiant = cursor.fetchone()
    if etudiant:
        # Convertir le tuple en dictionnaire
        etudiant_dict = {
            "id": etudiant[0],
            "name": etudiant[1],
            "sexe": etudiant[2],
            "adresse": etudiant[3],
            "promotion": etudiant[4],
            "annee_academique": etudiant[5]
        }
        etudiant_json = json.dumps(etudiant_dict, ensure_ascii=False)
        return etudiant_json
    else:
        return Response(json.dumps({"error": "Étudiant introuvable"}), status=404, mimetype='application/json')

def register_student(name, sexe, adresse, promotion, annee_academique):
    print(sexe)
    sql_insert = """
        INSERT INTO etudiants (id,name, sexe, adresse, promotion, annee_academique) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    param_values = (random.randint(0,100), name, sexe, adresse, promotion, annee_academique)
    cursor.execute(sql_insert, param_values)
    connection.commit()

    message = {'message': 'Student is registered with success'}
    return Response(json.dumps(message), status=200, mimetype='application/json')
