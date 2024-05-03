

import pymysql
from flask import Flask, jsonify, request, render_template
import datetime
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse
import psycopg2

load_dotenv()

app = Flask(__name__)


# MySQL database connection configuration
def get_mysql_connection():
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="informasi_wisata",
        host="mysql-389773d8-eai-uts.e.aivencloud.com",
        password=os.getenv("AVNS_9oUuhZxFkw8IAvYvBUx"),
        read_timeout=timeout,
        port=28925,
        user="avnadmin",
        write_timeout=timeout,
    )
    return connection


# PostgreSQL database connection configuration
def get_postgres_connection():
    return os.getenv("POSTGRES_CONNECTION_STRING")


# Convert timedelta to string
def convert_to_dict_with_string_timedelta(records):
    converted_records = []
    for record in records:
        converted_record = {}
        for key, value in record.items():
            if isinstance(value, datetime.timedelta):
                converted_record[key] = str(value)
            else:
                converted_record[key] = value
        converted_records.append(converted_record)
    return converted_records


# Get flight ticket data from PostgreSQL
@app.route("/flight", methods=["GET"])
def get_flight_tickets():
    try:
        response = requests.get("http://localhost:3000/flight")
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get train ticket data from PostgreSQL
@app.route("/train", methods=["GET"])
def get_train_tickets():
    try:
        response = requests.get("http://localhost:3000/train")
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get hotel data from PostgreSQL
@app.route("/hotel", methods=["GET"])
def get_hotels():
    try:
        response = requests.get("http://localhost:3000/hotel")
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get attractions data from PostgreSQL
@app.route("/attractions", methods=["GET"])
def get_attractions():
    try:
        response = requests.get("http://localhost:3000/attractions")
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_postgres_connection():
    # Database URL
    db_url = "postgres://ticker_order_user:DX6mgTvJCqqtSfrqFz7tHBNls1RgHMwy@dpg-con0p7q1hbls73fak2r0-a.singapore-postgres.render.com/ticker_order"
    
    # Parse the database URL
    parsed_url = urlparse(db_url)
    
    # Establish a connection
    connection = psycopg2.connect(
        user=parsed_url.username,
        password=parsed_url.password,
        host=parsed_url.hostname,
        port=parsed_url.port,
        database=parsed_url.path[1:]
    )
    
    return connection
# Endpoint to create an order
@app.route("/order", methods=["POST"])
def create_order():
    try:
        order_data = request.json
        order_type = order_data.get("order_type")
        customer_name = order_data.get("customer_name")
        email = order_data.get("email")
        phone_number = order_data.get("phone_number")

        # Insert the order into PostgreSQL database
        connection = get_postgres_connection()
        cursor = connection.cursor()
        query = "INSERT INTO orders (customer_name, email, phone_number, order_type, order_date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(
            query,
            (customer_name, email, phone_number, order_type, datetime.datetime.now()),
        )
        connection.commit()
        connection.close()

        return jsonify({"success": True, "message": "Order created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to get data from your Python API
@app.route("/infowisata", methods=["GET"])
def get_infowisata():
    try:
        # Assuming your Python API is running on a different port or IP
        response = requests.get("http://localhost:5432/infowisata")
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def main():
    try:
        # Fetch data from different endpoints
        train_data = requests.get("http://localhost:5000/train").json()
        flight_data = requests.get("http://localhost:5000/flight").json()
        hotel_data = requests.get("http://localhost:5000/hotel").json()
        attractions_data = requests.get("http://localhost:5000/attractions").json()
        wisata_data = requests.get("http://localhost:5000/infowisata").json()

        # Render the index.html template with the fetched data
        return render_template(
            "index.html",
            train=train_data,
            flight=flight_data,
            hotel=hotel_data,
            attractions=attractions_data,
            wisata=wisata_data,
        )
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
