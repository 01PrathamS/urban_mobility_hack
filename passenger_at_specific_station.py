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