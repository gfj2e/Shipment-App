# Shipment-App
This project is for Homework 6 Database management

## Homework 6 for Database

My homework 6 uses HTML/Javascript/Flask to enable you to insert
data into a MySQL database and to perform queries to update/show data in
the database.

## Requirements
In order to run this program you need:

- Python 3.10 or above

- MySQL Server and optionally MySQL Workbench

- Virtual environment(optional but recommended)

- Python package manager (pip)

## Setup Instructions

### Clone Repository
1. Clone the repository into your selected folder:
```bash
git clone "https://github.com/gfj2e/Shipment-App.git"
```

### Configure the MySQL Server
1. Launch MySQL terminal or Workbench
2. Create or use existing connection and create a new database for storing the data from the homework:
```mysql
CREATE DATABASE IF NOT EXISTS homework_6;
```

### Install Required Modules
1. Create virtual environment in root directory of project:
```bash
python -m venv venv
venv/Scripts/activate       # Windows
source venv/bin/activate    # Linux or MacOS
```
2. In bash run:
```bash
pip install -r requirements.txt
```
to install the required Python modules

3. Create .env file in root directory:
```bash
touch .env
```

4. Then put in MySQL credentials in the .env to use the database:
```text
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_NAME=your_database_name
```
### Run the App

1. Run the Flask application:
```bash
python app.py
```

2. Open the local server
```text
http://127.0.0.1:5000
```

3. Now run the queries on the GUI

## Demo
Youtube Link