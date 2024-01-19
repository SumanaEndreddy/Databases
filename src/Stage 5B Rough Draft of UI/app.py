#! /usr/bin/python3

"""
This is an example Flask | Python | Psycopg2 | PostgreSQL
application that connects to the 7dbs database from Chapter 2 of
_Seven Databases in Seven Weeks Second Edition_
by Luc Perkins with Eric Redmond and Jim R. Wilson.
The CSC 315 Virtual Machine is assumed.

John DeGood
degoodj@tcnj.edu
The College of New Jersey
Spring 2020

----

One-Time Installation

You must perform this one-time installation in the CSC 315 VM:

# install python pip and psycopg2 packages
sudo pacman -Syu
sudo pacman -S python-pip python-psycopg2

# install flask
pip install flask

----

Usage

To run the Flask application, simply execute:

export FLASK_APP=app.py 
flask run
# then browse to http://127.0.0.1:5000/

----

References

Flask documentation:  
https://flask.palletsprojects.com/  

Psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgreSQL database server
def connect(query):
    print(query)
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py
app = Flask(__name__)


# serve form web page
@app.route("/")
def form():
    makes = connect("SELECT DISTINCT M.make FROM Model M")
    models = connect("SELECT DISTINCT M.model FROM Model M")
    departments = connect("SELECT D.department_name FROM Departments D")
    costtypes = connect("SELECT CT.cost_type_name FROM Cost_Types CT")
    years = connect("SELECT DISTINCT M.year FROM Model M")
    return render_template('my-form.html', makes=makes, models=models, departments=departments, costtypes=costtypes, years=years)

# handle venue POST and serve result web page
@app.route('/make-model', methods=['POST'])
def vehicle_category():
    rows = connect("SELECT DISTINCT M.make, M.model, VC.vehicle_category FROM Vehicle_Categories VC JOIN Model M ON M.current_vehicleCategory_id = VC.vehicleCategory_id WHERE M.make = '" + request.form['make'] + "' AND M.model = '" + request.form['model'] + "';")
    heads = ['make', 'model', 'current_vehicle_category']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make1-model1', methods=['POST'])
def proposed_vehicle_category():
    rows = connect("SELECT M.make, M.model, VC.vehicle_category FROM Vehicle_Categories VC JOIN Model M ON M.proposed_vehicleCategory_id = VC.vehicleCategory_id  WHERE M.make = '" + request.form['make1'] + "' AND M.model = '" + request.form['model1'] + "';")
    heads = ['make', 'model', 'proposed_vehicle_category']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make2-model2', methods=['POST'])
def future_vehicle_category():
    rows = connect("SELECT M.make, M.model, VC.vehicle_category FROM Vehicle_Categories VC JOIN Model M ON M.future_vehicleCategory_id = VC.vehicleCategory_id  WHERE M.make = '" + request.form['make2'] + "' AND M.model = '" + request.form['model2'] + "';")
    heads = ['make', 'model', 'future_vehicle_category']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/deptname', methods=['POST'])
def count_dept_name():
    rows = connect("SELECT COUNT(V.license_plate_number) FROM Vehicle V JOIN Departments D ON D.department_id = V.department_id WHERE D.department_name = '" + request.form['deptname'] + "';")  
    heads = ['total_number_of_cars']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make3-model3', methods=['POST'])
def department_name():
    rows = connect("SELECT d.department_name FROM Departments D JOIN Vehicle V ON V.department_id = D.department_id JOIN Model M ON M.model_id = V.model_id WHERE M.make = '" + request.form['make3'] + "' AND M.model = '" + request.form['model3'] + "';" )
    heads = ['department_name']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/costtype-make4-model4', methods=['POST'])
def different_cost_types():
    rows = connect("SELECT IT.amount FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Invoices I ON I.license_plate_number = V.license_plate_number JOIN Invoice_Items IT ON IT.invoice_number = I.invoice_number JOIN Cost_Types CT ON CT.cost_type_id = IT.cost_type_id AND CT.cost_type_name = '" + request.form['costtype'] + "' WHERE M.make = '" + request.form['make4'] + "' AND M.model = '" + request.form['model4'] + "';")
    heads = ['Cost']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make5-model5', methods=['POST'])
def emissions():
    rows = connect("SELECT ED.annual_emissions FROM Model M JOIN Vehicle V ON V.model_id = M.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Emission_Details ED ON ED.emission_id = E.emission_id WHERE M.make = '" + request.form['make5'] + "' AND M.model = '" + request.form['model5'] + "';")
    heads = ['annual_emissions']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/total-emission', methods=['POST'])
def total_emissions():
    rows = connect("SELECT SUM(ED.annual_emissions) FROM Model M JOIN Vehicle V ON V.model_id = M.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Emission_Details ED ON ED.emission_id = E.emission_id WHERE M.make = '" + request.form['total-emission'] + "';")
    heads = ['total_annual_emission']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/emission-type', methods=['POST'])
def emission_type():
    rows = connect("SELECT DISTINCT ET.emission_type_name, M.make FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Emission_Details ED ON ED.emission_id = E.emission_id JOIN Emission_Types ET ON ET.emission_type_id = ED.emission_type_id WHERE M.make = '" + request.form['emission-type'] + "';")  
    heads = ['emission_type', 'make', 'model']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make6-model6', methods=['POST'])
def current_engine_type():
    rows = connect("SELECT DISTINCT ET.engine_type FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Engine_Types ET ON ET.engine_type_id = M.current_engine_type_id WHERE M.make = '" + request.form['make6'] + "' AND M.model = '" + request.form['model6'] + "';")                           
    heads = ['current_engine_type']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make7-model7', methods=['POST'])
def proposed_engine_type():
    rows = connect("SELECT DISTINCT ET.engine_type FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Engine_Types ET ON ET.engine_type_id = M.proposed_engine_type_id WHERE M.make = '" + request.form['make7'] + "' AND M.model = '" + request.form['model7'] + "';")                           
    heads = ['proposed_engine_type']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make8-model8', methods=['POST'])
def future_engine_type():
    rows = connect("SELECT DISTINCT ET.engine_type FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Engine_Types ET ON ET.engine_type_id = M.future_engine_type_id WHERE M.make = '" + request.form['make8'] + "' AND M.model = '" + request.form['model8'] + "';")                           
    heads = ['future_engine_type']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/year1', methods=['POST'])
def year1():
    rows = connect('SELECT M.make, M.model, V.license_plate_number FROM Model M JOIN Vehicle V ON V.model_id = M.model_id WHERE M.year < ' + request.form['year1'] + ';')
    heads = ['make', 'model', 'license_plate_number']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/year2', methods=['POST'])
def year2():
    rows = connect('SELECT M.make, M.model, V.license_plate_number FROM Model M JOIN Vehicle V ON V.model_id = M.model_id WHERE M.year > ' + request.form['year2'] + ';')
    heads = ['make', 'model', 'license_plate_number']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/year3', methods=['POST'])
def year3():
    rows = connect('SELECT M.make, M.model, V.license_plate_number FROM Model M JOIN Vehicle V ON V.model_id = M.model_id WHERE M.year = ' + request.form['year3'] + ';')
    heads = ['make', 'model', 'license_plate_number']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make9-model9', methods=['POST'])
def proposed_future():
    rows = connect("SELECT M.make, M.model, M.proposed_year, M.future_year FROM Model M WHERE M.make = '" + request.form['make9'] + "' AND M.model = '" + request.form['model9'] + "';")
    heads = ['make', 'model', 'proposed_year', 'future_year']
    return render_template('my-result.html', rows=rows, heads=heads)

if __name__ == '__main__':
    app.run(debug = True)


