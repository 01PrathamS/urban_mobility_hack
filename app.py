from flask import Flask, render_template, request, jsonify
import mysql.connector
import random

random.seed(42)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

map_data = {}

for day in days:
    lower_bound = 8 
    upper_bound = 12 
    map_data[day] = [
        [random.randint(min(lower_bound, upper_bound), max(lower_bound, upper_bound)) for _ in range(30)],
        [random.randint(lower_bound, upper_bound) for _ in range(30)]
    ]

def predict_data_for_day(day):
    return round(sum(map_data[day][1]) / len(map_data[day][1]))

app = Flask(__name__)

# MySQL database configuration
db_config = {}

# Connect to the MySQL server
connection = mysql.connector.connect(**db_config)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Define the table structure
create_table_query = """
CREATE TABLE IF NOT EXISTS passengers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_station VARCHAR(50) NOT NULL,
    destination_station VARCHAR(50) NOT NULL,
    passenger_count INT NOT NULL,
    UNIQUE KEY unique_stations (source_station, destination_station)
)
"""

cursor.execute(create_table_query)
connection.commit()

# Close the cursor (Note: Connection remains open for the duration of the application)
cursor.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_database', methods=['POST'])
def update_database():
    try:
        source_station = request.form['source_station']
        destination_station = request.form['destination_station']

        # Increment passenger count in the database
        query = """
        INSERT INTO passengers (source_station, destination_station, passenger_count) 
        VALUES (%s, %s, 1) 
        ON DUPLICATE KEY UPDATE passenger_count = passenger_count + 1
        """
        values = (source_station, destination_station)

        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

        return jsonify({'status': 'success', 'message': 'Passenger count updated successfully'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/total_passengers')
def total_passengers():
    try:
        # Query to get the total number of passengers
        total_passengers_query = "SELECT SUM(passenger_count) FROM passengers"
        cursor = connection.cursor()
        cursor.execute(total_passengers_query)
        total_passengers = cursor.fetchone()[0]

        return render_template('total_passengers.html', total_passengers=total_passengers)

    except Exception as e:
        return render_template('error.html', error_message=str(e))
    
@app.route('/total_passengers_by_station/<station>')
def total_passengers_by_station(station):
    try:
        # Query to get the total number of passengers for a specific destination station
        total_passengers_query = """
        SELECT SUM(passenger_count) 
        FROM passengers 
        WHERE destination_station = %s
        """
        cursor = connection.cursor()
        cursor.execute(total_passengers_query, (station,))
        total_passengers = cursor.fetchone()[0]

        return render_template('total_passengers_by_station.html', station=station, total_passengers=total_passengers)

    except Exception as e:
        return render_template('error.html', error_message=str(e))


# @app.route('/passengers_at_specific_station/<station>')
# def passengers_at_specific_station(station):
#     try:
#         # Query to get the total number of passengers
#         total_passengers_query = "SELECT SUM(passenger_count) FROM passengers"
#         cursor = connection.cursor()
#         cursor.execute(total_passengers_query)
#         total_passengers = cursor.fetchone()[0]

#         # Query to get the total number of passengers for a specific destination station
#         total_passengers_by_station_query = """
#         SELECT SUM(passenger_count) 
#         FROM passengers 
#         WHERE destination_station = %s
#         """
#         cursor.execute(total_passengers_by_station_query, (station,))
#         total_passengers_by_station = cursor.fetchone()[0]

#         # Calculate the difference
#         passengers_at_specific_station = total_passengers - total_passengers_by_station

#         return render_template('passengers_at_specific_station.html', station=station, passengers_at_specific_station=passengers_at_specific_station)

#     except Exception as e:
#         return render_template('error.html', error_message=str(e))
    
@app.route('/passengers_at_specific_station/<station>')
def passengers_at_specific_station(station):
    try:
        # Query to get the total number of passengers
        total_passengers_query = "SELECT SUM(passenger_count) FROM passengers"
        cursor = connection.cursor()
        cursor.execute(total_passengers_query)
        total_passengers = cursor.fetchone()[0]

        # Query to get the total number of passengers for a specific destination station
        total_passengers_by_station_query = """
        SELECT SUM(passenger_count) 
        FROM passengers 
        WHERE destination_station = %s
        """
        cursor.execute(total_passengers_by_station_query, ('s2',))
        total_passengers_by_station_s2 = cursor.fetchone()[0]
    
        cursor.execute(total_passengers_by_station_query, ('s3',))
        total_passengers_by_station_s3 = cursor.fetchone()[0]
    
        cursor.execute(total_passengers_by_station_query, ('s4',))
        total_passengers_by_station_s4 = cursor.fetchone()[0]

        # Calculate the difference
        if station == 's2':
            passengers_at_specific_station = total_passengers - total_passengers_by_station_s2
        if station == 's3':
            passengers_at_specific_station = total_passengers - total_passengers_by_station_s3 - total_passengers_by_station_s2 
        if station == 's4':
            passengers_at_specific_station = total_passengers - total_passengers_by_station_s4 - total_passengers_by_station_s3 - total_passengers_by_station_s2

        return render_template('passengers_at_specific_station.html', station=station, passengers_at_specific_station=passengers_at_specific_station)

    except Exception as e:
        return render_template('error.html', error_message=str(e))
    

@app.route('/predict_data', methods=['GET', 'POST'])
def predict_data():
    if request.method == 'POST':
        selected_day = request.form['selected_day']
        prediction = predict_data_for_day(selected_day)
        return jsonify({'prediction': prediction})

    return render_template('predict_data.html', days=days)



if __name__ == '__main__':
    app.run(debug=True)
