from flask import Flask, render_template, request, jsonify, redirect
import mysql.connector
from secret import db_config

app = Flask(__name__)

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(**db_config)

# Fetch stations
stations = ["s1", "s2", "s3", "s4", "s5"]

@app.route('/')
def index():
    return render_template('index.html', stations=stations)

@app.route('/move_bus', methods=['POST'])
def move_bus():
    current_station = request.json['current_station']
    next_station = stations[(stations.index(current_station) + 1) % len(stations)]
    
    conn = connect_db()
    cursor = conn.cursor()
    
    # Update total passenger count
    cursor.execute("SELECT passenger_count FROM passengers WHERE destination_station=%s", (next_station,))
    results = cursor.fetchall()
    total_passengers_dropping = sum(row[0] for row in results)
    
    cursor.execute("UPDATE total_passenger_count SET count = count - %s WHERE id = 1", (total_passengers_dropping,))
    
    # Remove passengers who have reached their destination
    # cursor.execute("DELETE FROM passengers WHERE destination_station=%s", (current_station,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify(next_station=next_station)

@app.route('/add_passenger', methods=['POST'])
def add_passenger():
    data = request.json
    source = data.get('source')
    destination = data.get('destination')
    
    if not source or not destination:
        return jsonify(success=False, message="Invalid input")

    conn = connect_db()
    cursor = conn.cursor()

    # Check if this route already exists
    cursor.execute("SELECT * FROM passengers WHERE source_station=%s AND destination_station=%s", (source, destination))
    result = cursor.fetchone()

    if result:
        # Route exists, increment passenger count
        cursor.execute("UPDATE passengers SET passenger_count = passenger_count + 1 WHERE source_station=%s AND destination_station=%s", (source, destination))
    else:
        # Route does not exist, insert new record
        cursor.execute("INSERT INTO passengers (source_station, destination_station, passenger_count, status) VALUES (%s, %s, %s, %s)", (source, destination, 1, 0))

    # Update total passenger count
    cursor.execute("UPDATE total_passenger_count SET count = count + 1 WHERE id = 1")

    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify(success=True)

@app.route('/get_total_passenger_count', methods=['GET'])
def get_total_passenger_count():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT count FROM total_passenger_count WHERE id = 1")
    result = cursor.fetchone()

    total_count = result[0] if result else 0
    
    cursor.close()
    conn.close()
    
    return jsonify(total_passenger_count=total_count)

# when restart the server, the total passenger count will be reset to 0 and all passengers will be removed
@app.route('/reset', methods=['POST', 'GET'])
def reset():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE total_passenger_count SET count = 0 WHERE id = 1")
    cursor.execute("DELETE FROM passengers")
    
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/')
    

## return details of all passengers # select * from passengers 
@app.route('/get_passenger_details', methods=['GET'])
def get_passenger_details():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM passengers")
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(passenger_details=results)


@app.route('/get_station_passenger_counts', methods=['GET'])
def get_station_passenger_counts():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT source_station, SUM(passenger_count) FROM passengers GROUP BY source_station")
    source_results = cursor.fetchall()

    cursor.execute("SELECT destination_station, SUM(passenger_count) FROM passengers GROUP BY destination_station")
    destination_results = cursor.fetchall()

    source_data = [{'station': row[0], 'count': row[1]} for row in source_results]
    destination_data = [{'station': row[0], 'count': row[1]} for row in destination_results]

    data = {
        'source': source_data,
        'destination': destination_data
    }

    cursor.close()
    conn.close()

    return jsonify(data)

@app.route('/statistics') 
def staistics():
    return render_template('statistics.html')

@app.route('/maps')
def maps():
    return render_template('maps.html')


if __name__ == '__main__':
    app.run(debug=True)
