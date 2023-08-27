# import all required libraries
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from datetime import datetime
import serial


# import functions from additional.py
from additional import error

# configure application
app = Flask(__name__)

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

"""
SQL COMMANDS
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL);
"""

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    
    id = session.get("user_id")

    # redirect to registration if user doesn't exist
    try:
        name = db.execute("SELECT name FROM users WHERE id = ?", id)[0]["name"]
        print(name)
    except:
        return redirect("/name")

    time_last_watered = int(datetime.now().timestamp())

    return render_template("index.html", name=name, time_last_watered=time_last_watered)


@app.route("/name", methods=["GET", "POST"])
def name():
    
    if request.method == "POST":

        name = request.form.get("name")
        if len(name) <= 1 or len(name) >= 20:
            return render_template(error("invalid name length"))

        
        db.execute("INSERT INTO users (name) VALUES(?)", name)
        user = db.execute("SELECT * FROM users WHERE name = ?", name)
        session["user_id"] = user[0]["id"]

        return redirect("/")
    
    # user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("name.html")

"""
#Initialize Serial port (make sure the baud rate matches with Arduino)
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Serial port name

@app.route("/get_sensor_data", methods=["GET"])
def get_sensor_data():
    if ser.inWaiting() > 0:
        # Read Serial data from Arduino
        read_serial = ser.readline().decode('utf-8').strip()

        # Parse the comma-separated sensor values
        # Assuming the order is temperature, humidity, light level, and soil moisture
        try:
            temp, hum, light_level, soil_moisture = map(float, read_serial.split(','))

            # Create a dictionary to store the sensor data
            sensor_data = {
                'Temperature': temp,
                'Humidity': hum,
                'Light Level': light_level,
                'Soil Moisture': soil_moisture
            }
            return jsonify(sensor_data)
        except ValueError:
            # Handle error in case of invalid data
            return jsonify({"error": "Invalid data received"}), 400

    return jsonify({"error": "No data received"}), 400
"""

if __name__ == "__main__":
     app.run(debug=True)