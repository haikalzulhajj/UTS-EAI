import pymysql
from flask import Flask, jsonify
import datetime
import os 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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

@app.route('/infowisata', methods=['GET'])
def method_name():
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="informasi_wisata",  # Change to your database name
        host="mysql-389773d8-eai-uts.e.aivencloud.com",
        password="AVNS_9oUuhZxFkw8IAvYvBUx",
        read_timeout=timeout,
        port=28925,
        user="avnadmin",
        write_timeout=timeout,
    )
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tempat_wisata")
        records = cursor.fetchall()
    finally:
        connection.close()

    if records: 
        converted_records = convert_to_dict_with_string_timedelta(records)
        return jsonify(converted_records)
    else:
        return jsonify([]) 

if __name__ == '__main__':
    app.run(debug=True, port=5432)
