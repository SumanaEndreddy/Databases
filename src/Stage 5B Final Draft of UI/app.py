#! /usr/bin/python3

"""

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
    # gets attributes from tables
    platenumber = connect("SELECT DISTINCT V.license_plate_number FROM Vehicle V ORDER BY V.license_plate_number asc")
    makes = connect("SELECT DISTINCT M.make FROM Model M ORDER BY M.make asc")
    models = connect("SELECT DISTINCT M.model FROM Model M ORDER BY M.model asc")
    departments = connect("SELECT D.department_name FROM Departments D ORDER BY D.department_name asc")
    costtypes = connect("SELECT CT.cost_type_name FROM Cost_Types CT ORDER BY CT.cost_type_name asc")
    years = connect("SELECT DISTINCT M.year FROM Model M ORDER BY M.year asc")
    return render_template('my-form.html', makes=makes, models=models, departments=departments, costtypes=costtypes, years=years, platenumber=platenumber)

# handle venue POST and serve result web page
@app.route('/make-model', methods=['POST'])
def vehicle_category():
    rows = connect("SELECT DISTINCT M.make, M.model, VC.vehicle_category FROM Vehicle_Categories VC JOIN Model M ON M.current_vehicleCategory_id = VC.vehicleCategory_id WHERE M.make = '" + request.form['make'] + "' AND M.model = '" + request.form['model'] + "';")
    heads = ['Make', 'Model', 'Current_Vehicle_Category']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/license0-license1', methods=['POST'])
def low_emissions():
    rows = connect("SELECT T1.* FROM (SELECT V1.license_plate_number, M1.make, M1.model, M1.year, SUM(ED1.annual_emissions) AS vehicle_annual_emission FROM Vehicle V1 JOIN Model M1 ON V1.model_id = M1.model_id JOIN Emissions E1 ON V1.license_plate_number = E1.license_plate_number JOIN Emission_Details ED1 ON ED1.emission_id = E1.emission_id WHERE V1.license_plate_number IN ('" + request.form['license0'] + "','" + request.form['license1'] + "') GROUP BY V1.license_plate_number, M1.make, M1.model, M1.year ) AS T1 ORDER BY T1.vehicle_annual_emission fetch first 1 rows only ;")
    heads = ['License_Plate_Number', 'Make', 'Model', 'Year', 'Vehicle_Annual_Emission']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make1-model1', methods=['POST'])
def proposed_vehicle_category():
    rows = connect("SELECT M.make, M.model, VC.vehicle_category FROM Vehicle_Categories VC JOIN Model M ON M.proposed_vehicleCategory_id = VC.vehicleCategory_id  WHERE M.make = '" + request.form['make1'] + "' AND M.model = '" + request.form['model1'] + "';")
    heads = ['Make', 'Model', 'Proposed_Vehicle_Category']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make2-model2', methods=['POST'])
def future_vehicle_category():
    rows = connect("SELECT M.make, M.model, VC.vehicle_category FROM Vehicle_Categories VC JOIN Model M ON M.future_vehicleCategory_id = VC.vehicleCategory_id  WHERE M.make = '" + request.form['make2'] + "' AND M.model = '" + request.form['model2'] + "';")
    heads = ['Make', 'Model', 'Future_Vehicle_Category']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/deptname', methods=['POST'])
def count_dept_name():
    rows = connect("SELECT COUNT(V.license_plate_number) FROM Vehicle V JOIN Departments D ON D.department_id = V.department_id WHERE D.department_name = '" + request.form['deptname'] + "';")  
    heads = ['Total_Number_Of_Cars']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make3-model3', methods=['POST'])
def department_name():
    rows = connect("SELECT M.make, M.model, d.department_name FROM Departments D JOIN Vehicle V ON V.department_id = D.department_id JOIN Model M ON M.model_id = V.model_id WHERE M.make = '" + request.form['make3'] + "' AND M.model = '" + request.form['model3'] + "';" )
    heads = ['Make', 'Model', 'department_name']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/costtype-make4-model4', methods=['POST'])
def different_cost_types():
    rows = connect("SELECT M.make, M.model, IT.amount FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Invoices I ON I.license_plate_number = V.license_plate_number JOIN Invoice_Items IT ON IT.invoice_number = I.invoice_number JOIN Cost_Types CT ON CT.cost_type_id = IT.cost_type_id AND CT.cost_type_name = '" + request.form['costtype'] + "' WHERE M.make = '" + request.form['make4'] + "' AND M.model = '" + request.form['model4'] + "';")
    heads = ['Make', 'Model', 'Cost']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make5-model5', methods=['POST'])
def emissions():
    rows = connect("SELECT M.make, M.model, ED.annual_emissions FROM Model M JOIN Vehicle V ON V.model_id = M.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Emission_Details ED ON ED.emission_id = E.emission_id WHERE M.make = '" + request.form['make5'] + "' AND M.model = '" + request.form['model5'] + "';")
    heads = ['Make', 'Model', 'Annual_Emissions']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/total-emission', methods=['POST'])
def total_emissions():
    rows = connect("SELECT M.make, SUM(ED.annual_emissions) FROM Model M JOIN Vehicle V ON V.model_id = M.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Emission_Details ED ON ED.emission_id = E.emission_id WHERE M.make = '" + request.form['total-emission'] + "' GROUP BY M.make ;")
    heads = ['Make','Total_Annual_Emission']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/emission-type', methods=['POST'])
def emission_type():
    rows = connect("SELECT DISTINCT ET.emission_type_name, M.make FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Emission_Details ED ON ED.emission_id = E.emission_id JOIN Emission_Types ET ON ET.emission_type_id = ED.emission_type_id WHERE M.make = '" + request.form['emission-type'] + "';")  
    heads = ['Emission_Type','Make']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make6-model6', methods=['POST'])
def current_engine_type():
    rows = connect("SELECT DISTINCT ET.engine_type FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Engine_Types ET ON ET.engine_type_id = M.current_engine_type_id WHERE M.make = '" + request.form['make6'] + "' AND M.model = '" + request.form['model6'] + "';")                           
    heads = ['Current_Engine_Type']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make7-model7', methods=['POST'])
def proposed_engine_type():
    rows = connect("SELECT M.make, M.model, ET.engine_type FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Engine_Types ET ON ET.engine_type_id = M.proposed_engine_type_id WHERE M.make = '" + request.form['make7'] + "' AND M.model = '" + request.form['model7'] + "';")                           
    heads = ['Make', 'Model', 'Proposed_Engine_Type']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/make8-model8', methods=['POST'])
def future_engine_type():
    rows = connect("SELECT M.make, M.model, ET.engine_type FROM Vehicle V JOIN Model M ON M.model_id = V.model_id JOIN Emissions E ON E.license_plate_number = V.license_plate_number JOIN Engine_Types ET ON ET.engine_type_id = M.future_engine_type_id WHERE M.make = '" + request.form['make8'] + "' AND M.model = '" + request.form['model8'] + "';")                           
    heads = ['Make', 'Model', 'Future_Engine_Type']
    return render_template('my-result.html', rows=rows, heads=heads)

# handle venue POST and serve result web page
@app.route('/year1', methods=['POST'])
def year1():
    rows = connect('SELECT M.make, M.model, V.license_plate_number FROM Model M JOIN Vehicle V ON V.model_id = M.model_id WHERE M.year < ' + request.form['year1'] + ';')
    heads = ['Make', 'Model', 'License_Plate_Number']
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
    rows = connect("SELECT M.make, M.model, M.year, M.proposed_year, M.future_year FROM Model M WHERE M.make = '" + request.form['make9'] + "' AND M.model = '" + request.form['model9'] + "';")
    heads = ['make', 'model', 'year', 'proposed_year', 'future_year']
    return render_template('my-result.html', rows=rows, heads=heads)

if __name__ == '__main__':
    app.run(debug = True)


