#importing module  
import pypyodbc  
# from dotenv import dotenv_values
from collections import OrderedDict
from datetime import date,datetime
from flask import Response
import json
import mysql.connector
# from flask import jsonify

#Config 
# config = dict(dotenv_values(".env"))

#creating connection Object which will contain MySQL Server Connection  
connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="etudiants"
)


#creating connection Object which will contain SQL Server Connection  
# connection = pypyodbc.connect(f"Driver={config['DB_DRIVER']};Server={config['DB_HOST']};Database={config['DB_DATABASE']};uid={config['DB_USERNAME']};pwd={config['DB_PASSWORD']}", autocommit=True)  
cursor = connection.cursor()
def getEmployees():
    sql = "SELECT * FROM etudiants "
    param_values = ()
    cursor.execute(sql,param_values)
    results = cursor.fetchall()
    employees = []
    content = {}
    for result in results:
        content = {'id': result[0],
         'name': result[1],
         'sexe': result[2],
            'adresse': result[3],
            'promotion': result[4],
            'annee_academique': result[5]
         }
        employees.append(content)
    print(employees)
    return json.dumps(employees, default = str)

def enroll_employee(etudiant_id, picture):
    
    date_enrolment = datetime.now()
    sql = "INSERT INTO attendance_enrolments (etudiant_id, date_enrolment, picture) values(%s, %s, %s)"
    param_values = (etudiant_id, date_enrolment , picture)
    cursor.execute(sql,param_values)
    connection.commit()

    message = {'message' : 'Employee is enrolled with success'}
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