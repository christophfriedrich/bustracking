from flask import Flask, jsonify
from flask_mysqldb import MySQL

import configparser
config = configparser.ConfigParser()
config.read('/home/chrfrd/.my.cnf')

app = Flask(__name__, static_folder='/home/chrfrd')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = config['client']['user']
app.config['MYSQL_PASSWORD'] = config['client']['password']
app.config['MYSQL_DB'] = 'chrfrd_bustracking'
mysql = MySQL(app)

@app.route('/')
def frontend():
    return app.send_static_file('index.html')

@app.route('/api/delays', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT line, date, tripCode, time_format(trips.departureTimePlanned, '%H:%i') AS start, time_format(trips.arrivalTimePlanned, '%H:%i') AS end, GROUP_CONCAT(time_to_sec(timediff(arrivalTimeEstimated, stopEvents.arrivalTimePlanned)) ORDER BY stopEvents.arrivalTimePlanned ASC) AS arrivalDelays, GROUP_CONCAT(time_to_sec(timediff(departureTimeEstimated, stopEvents.departureTimePlanned)) ORDER BY stopEvents.departureTimePlanned ASC) AS departureDelays FROM stopEvents LEFT JOIN stops ON stops.globalId=stopId LEFT JOIN trips ON stopEvents.tripId=trips.id WHERE line='wvv:10010:E:H:24d' AND date=20250129 GROUP BY tripId ORDER BY line, date, start''')
    data = cur.fetchall()
    cur.close()
    column_names = ['line', 'date', 'tripCode', 'start', 'end', 'arrivalDelays', 'departureDelays']
    data_as_dict = [dict(zip(column_names, row)) for row in data]
    return jsonify(data_as_dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')