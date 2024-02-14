## TCNJ Fleet Vehicle Management

## Objective of the Project
The objective of our model is to build a user-friendly interface that gives the user control to execute commands that bring up a vehicle of his own wishes that would then provide the user with information regarding the vehicle's cost and emission data. This model would allow administrators to have complete control of the different vehicles and could compare on the database. For example, the user could request to compare the cost and emission data of one of TCNJ’s Ford F450’s with a Ram 1500, easily comparing the annual emissions and the effects on the environment. The database will be able to store thousands of vehicle information, allowing the user to find the most optimal group of vehicles to make up the fleet vehicle management at TCNJ. 

## Table of Contents
** **
- Features
- Updates
- Installation and Usage
- Technology and Concepts


## Features
-- --
- User-Interface can retrieve information such as car emissions, emission types, vehicle classifications, and general information about the cars
- Compare different vehicles to find which is the most environmentally friendly
- User-Interface contains dropdown menu to assist the users in quickly gaining access to the data
- Displays annual emissions and emission type for each car
- Retrieves maintenance, repairs, tires, and insurance cost for all vehicles
 
## Updates
-- --
- January 31: Project topic selection
    - **~Janurary 31: Stage I due**
- February 2: Created a rough draft regarding the project specifications
- February 5: Finished the project proposal rough draft and submitted it
    - **February 6: Stage IIa due**
- February 13: Used instructor feedback to edit the project proposal
- February 15: Finished revising the project proposal and submitted the final copy
    - **February 16: Stage IIb due**
- February 23: Started developing the ER Diagram needed to begin conceptualizing the database
- February 26-27: Used the knowledge presented in class to start fixing the original ER
- March 3: With help from Dr. DeGood, we updated our ER Diagram and schema
- March 6: Talked with our group and started developing the Mid-Semester Project Presentation and the **planned** User Inteface model/diagram
- March 8: Created the Mid-Semester Project Report and started filling it out
- March 9: Finished and submitted Stage III and the Mid-Semester Project Report and Presentation
    - **March 9: Stage III due**
    - **March 10: Mid-Semester Project Report and Presentation due**
- March 12: Used presentation feedback and edited our User Interface model
- March 14: Attempted to start normalizing our ER Diagram to BC-NF, this endeavor would take a long time
- March 17: Started defining the different views (virtual tables) required
- March 20: Finished the different views and started to develop a set of queries that could fulfill our transaction requirements 
- March 25: With much assistance from Dr. DeGood, the ER Diagram was normalized to BC-NF and the set of queries was finished
    - **March 27: Stage IV due**
- March 29-April 5: Started/continued writing and executing SQL commands to create tables and insert data
    - **April 6: Stage Va due**
- April 10-13: Implemented a simple User Interface in it's most basic form, with text boxes
- April 19: Experimented with the interface and query interaction to get our first query working
- April 25: Finished adding the rest of the queries to the interface
    - **April 25: Stage Vb due**
- April 28: Added drop downs to replace the text boxes to ensure valid inputs, even if the inputs returned null
- April 30: Made visual modifications to the HTML and CSS of the interface
    - **May 1: Stage VI due (CSC315)**
- May 3: Added the feature allowing the user to compare the costs of two different vehicles
- May 4: Started to wrap up changes and finished the Final Project Report and Presentation
    - **May 5: Stage VI-Final Project Presentation due (CSC315/ACC311)**
    - **May 6: Stage VII-Final Project Report due**
    - **May 6: Stage VIII due**

## How to Install and Use
- Clone the repository or download the project file (Final Draft of UI) in "src" folder
- Must perform the one time installation in Virtual Machine
```
# install python pip and psycopg2 packages
sudo pacman -Syu
sudo pacman -S python-pip python-psycopg2

# install flask
pip install flask
```
To run the Flask application, simply execute:

```
export FLASK_APP=app.py
flask run
# then browse to http://127.0.0.1:5000/
```

- Now you are ready to use the application. 
- Use the dropdown menus to select different parameters for the queries.
- Results will be displayed in a seperate table

## Technologies and Concepts
** **
- Tables and queries were used to store and fetch the data
- An open-source relational database known as PostgreSQL is used
- As for the implementation of the web-based interface, Python programming language is used to integrate all the SQL queries into User-Interface
- HTML code is used to structure the web page's content and structure
