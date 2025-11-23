from flask import Flask, render_template, json, request, jsonify
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")


app.config["MYSQL_USER"] = db_user
app.config["MYSQL_PASSWORD"] = db_password
app.config["MYSQL_HOST"] = db_host
app.config["MYSQL_DB"] = db_name

# Create a mysql connection object to interact with the database
mysql = pymysql.connect(                
    user = app.config["MYSQL_USER"],
    password = app.config["MYSQL_PASSWORD"],
    host = app.config["MYSQL_HOST"],
    db = app.config["MYSQL_DB"]
)

# Creates the SUPPLIER-SHIPMENT-PART database 
def create_table():
    with app.app_context():
        try:
            cur = mysql.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS SUPPLIER (
                    Sno CHAR(2) PRIMARY KEY,
                    Sname VARCHAR(255) NOT NULL,
                    Status INT UNSIGNED,
                    City VARCHAR(255)
                );
            """)
            cur.execute("""    
                CREATE TABLE IF NOT EXISTS PART (
	                Pno CHAR(2) PRIMARY KEY,
                    Pname VARCHAR(255) NOT NULL,
                    Color VARCHAR(100),
                    Weight TINYINT CHECK (Weight >= 0 AND Weight <= 100),
                    City VARCHAR(255),
    
                    UNIQUE(Pname, Color)
                );
            """)
            
            cur.execute("""    
                CREATE TABLE IF NOT EXISTS SHIPMENT(
	                Sno CHAR(2),
                    Pno CHAR(2),
                    Qty INT UNSIGNED DEFAULT 100,
                    Price DECIMAL(5,3) CHECK (Price > 0),
    
                    PRIMARY KEY(Sno, Pno),
    
                    FOREIGN KEY (Pno) REFERENCES PART(Pno),
                    FOREIGN KEY (Sno) REFERENCES SUPPLIER(Sno)
                );
            """)
            mysql.commit()
            cur.close()
            print("Tables successfully created")
        except Exception as e:
            print(f"Exception occured while creating a table: {e}")

# Insert the data into the database using this function
def insert_data():
    with app.app_context():
        try:
            cur = mysql.cursor()
            cur.execute("""
                INSERT INTO SUPPLIER (Sno, Sname, Status, City) VALUES
                ('s1', 'Smith', 20, 'London'),
                ('s2', 'Jones', 10, 'Paris'),
                ('s3', 'Blake', 30, 'Paris'),
                ('s4', 'Clark', 20, 'London'),
                ('s5', 'Adams', 30, NULL);
            """)
            
            cur.execute("""
                INSERT INTO PART (Pno, Pname, Color, Weight, City) VALUES
                ('p1', 'Nut', 'Red', 12, 'London'),
                ('p2', 'Bolt', 'Green', 17, 'Paris'),
                ('p3', 'Screw', NULL, 17, 'Rome'),
                ('p4', 'Screw', 'Red', 14, 'London'),
                ('p5', 'Cam', 'Blue', 12, 'Paris'),
                ('p6', 'Cog', 'Red', 19, 'London');  
            """)

            cur.execute("""
                INSERT INTO SHIPMENT (Sno, Pno, Qty, Price) VALUES
                ('s1', 'p1', 300, 0.005),
                ('s1', 'p2', 200, 0.009),
                ('s1', 'p3', 400, 0.004),
                ('s1', 'p4', 200, 0.009),
                ('s1', 'p5', 100, 0.01),
                ('s1', 'p6', 100, 0.01),
                ('s2', 'p1', 300, 0.006),
                ('s2', 'p2', 400, 0.004),
                ('s3', 'p2', 200, 0.009),
                ('s3', 'p3', 200, NULL),
                ('s4', 'p2', 200, 0.008),
                ('s4', 'p3', NULL, NULL),
                ('s4', 'p4', 300, 0.006),
                ('s4', 'p5', 400, 0.003);        
            """)
            
            mysql.commit()
            cur.close()
        except Exception as e:
            mysql.rollback()
            print(f"Exception occurred while inserting data: {e}")
            print("Data likely previously inserted if you get this error")

# This insert route is for Questions 1 and 2, inserts data entered in by user into
# the database. Route is called by the javascript code and then displays 
# a success for failure message if insertion fails or not.
# Uses paramterized queries to protect against SQL Injection attacks
@app.route("/insert", methods=["POST"])
def insert():
    try:
        data = request.get_json()
        
        sno = data["supplierId"]
        pno = data["partNo"]
        qty = data["quantity"]
        price = data["price"]
        
        cur = mysql.cursor()
        cur.execute("""INSERT INTO SHIPMENT (Sno, Pno, Qty, Price) VALUES (%s, %s, %s, %s)""",
                    (sno, pno, qty, price))
        mysql.commit()
        cur.close()
        
        response = {
            "success": True,
            "message": f"Tuple {sno}, {pno}, {qty}, {price} was entered into the database"
        }
        
        return jsonify(response), 201
    
    except Exception as e:
        mysql.rollback()
        response = {
            "success": False,
            "message": f"Error Occurred: {e}"
        }
        
        return jsonify(response), 500

# This route is for raising the status of SUPPLIER by the amount selected by the user on the frontend.
# Javascript calls the route and performs the calculations and then returns a success message
# Uses paramterized queries to protect against SQL Injection attacks
@app.route("/raise_status", methods=["POST"])
def raise_status(): 
    try:
        data = request.get_json()
        
        percentage =  data["percentage"]
        
        multipler = 1 + (float(percentage) / 100)
        
        cur = mysql.cursor()
        cur.execute("UPDATE SUPPLIER SET Status = Status * (%s)", (multipler,))
        mysql.commit()
        cur.close()
        
        response = {
            "success": True,
            "message": f"Successfully updated status for suppliers"
        }
        
        return jsonify(response), 201
    except Exception as e:
        mysql.rollback()
        response = {
            "success": False,
            "message": f"Error increasing status: {e}"
        }
        
        return jsonify(response), 500

# The function selects all the supplier information and then sends it to the frontend to be displayed
# Then displays an error message 
@app.route("/get_suppliers", methods=["GET"])
def get_suppliers():
    try:
        cur = mysql.cursor()
        cur.execute("SELECT * FROM SUPPLIER")
        data = cur.fetchall()
        
        cur.close()
        items = [{"Sno": item[0], "Sname": item[1], "Status": item[2], "City": item[3]} for item in data]
        
        response = {
            "success": True,
            "message": "Info from Supplier table successfully fetched",
            "data": items
        }
        
        return jsonify(response), 200
    except Exception as e:
        mysql.rollback()
        response = {
            "success": False,
            "message": f"Error occurred fetching data: {e}",
            "data": None
        }

        return jsonify(response), 500

# This route will find all the suppliers that ship the corresponding part 
# entered in by the user, uses a inner join to join supplier and part tables
# then returns a success or failure message to the frontend
# Uses paramterized queries to protect against SQL Injection attacks
@app.route("/find_suppliers_by_part", methods=["POST"])
def find_suppliers_by_part(): 
    try:
        data = request.get_json()
        
        pno = data["partNo"]
        
        cur = mysql.cursor()
        cur.execute("""SELECT DISTINCT S.Sno, S.Sname, S.Status, S.City
                       FROM SUPPLIER S
                       JOIN SHIPMENT SH ON S.Sno = SH.Sno
                       WHERE SH.Pno = (%s)
        """, (pno))
        
        data = cur.fetchall()
        cur.close()
        
        items = [{"Sno": item[0], "Sname": item[1], "Status": item[2], "City": item[3]} for item in data]
        
        response = {
            "success": True,
            "message": "Suppliers successfully fetched by parts",
            "data": items
        }
        
        return jsonify(response), 201
        
    except Exception as e:
        mysql.rollback()
        response = {
            "success": False,
            "message": f"Error occurred fetching by part: {e}",
            "data": None
        }
        
        return jsonify(response), 500
    
# This route will reset the database when the user clicks the button
@app.route("/reset_database", methods=["GET"])
def reset_database():
    try:
        cur = mysql.cursor()
        cur.execute("SET SESSION GROUP_CONCAT_MAX_LEN = 32768")
        cur.execute("""
            SELECT CONCAT('DROP TABLE IF EXISTS', GROUP_CONCAT(table_name))
            FROM information_schema.tables
            WHERE table_schema = 'HOMEWORK_6'
        """)
        cur.execute("DROP TABLE IF EXISTS SUPPLIER, SHIPMENT, PART")
        
        create_table()
        insert_data()
        
        mysql.commit()
        cur.close()
        
        response = {
            "success": True,
            "message": "Success resetting the database"
        }
        
        return jsonify(response), 201
    except Exception as e:
        mysql.rollback()
        response = {
            "success": False,
            "message": f"Error resetting the database: {e}"
        }

        return jsonify(response), 500
    
# Renders the html template 
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__": 
    create_table()
    insert_data()
    app.run(debug=True)