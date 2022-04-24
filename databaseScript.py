#importing module  
import pypyodbc  
from dotenv import dotenv_values
from collections import OrderedDict
from datetime import date,datetime
from flask import Response
import json
import mysql.connector
# from flask import jsonify

#Config 
config = dict(dotenv_values(".env"))

#creating connection Object which will contain MySQL Server Connection  
connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="archi-tech",
  database="attendances"
)


#creating connection Object which will contain SQL Server Connection  
# connection = pypyodbc.connect(f"Driver={config['DB_DRIVER']};Server={config['DB_HOST']};Database={config['DB_DATABASE']};uid={config['DB_USERNAME']};pwd={config['DB_PASSWORD']}", autocommit=True)  
cursor = connection.cursor()
def getEmployees():
    sql = "SELECT * FROM employees "
    param_values = ()
    cursor.execute(sql,param_values)
    results = cursor.fetchall()
    employees = []
    content = {}
    for result in results:
        content = {'id': result[0], 'name': result[1]}
        employees.append(content)
    return json.dumps(employees, default = str)

def enroll_employee(employee_id, picture):
    
    date_enrolment = datetime.now()
    sql = "INSERT INTO attendance_enrolments (employee_id, date_enrolment, picture) values(%s, %s, %s)"
    param_values = (employee_id, date_enrolment , picture)
    cursor.execute(sql,param_values)
    connection.commit()

    message = {'message' : 'Employee is enrolled with success'}
    return Response(json.dumps(message), status=200, mimetype='application/json')

def save_attendance(employee_id):
    sql = "INSERT INTO attendance_lists (employee_id , time) values(%s, %s)"
    param_values = (employee_id,datetime.now())
    cursor.execute(sql,param_values)
    connection.commit()

    message = {'message' : 'La présence a été enregistrée'}
    return Response(json.dumps(message), status=200, mimetype='application/json')

   
        
        
 