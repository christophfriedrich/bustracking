from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

import re   # regex for input sanitation

import configparser
config = configparser.ConfigParser()
config.read('/home/chrfrd/.my.cnf')

app = Flask(__name__, static_folder='/home/chrfrd/srv/bustracking')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = config['client']['user']
app.config['MYSQL_PASSWORD'] = config['client']['password']
app.config['MYSQL_DB'] = 'chrfrd_bustracking'
mysql = MySQL(app)

@app.route('/')
def frontend():
    return app.send_static_file('index.html')

@app.route('/api/lines', methods=['GET'])
def get_lines():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT DISTINCT line FROM `trips` ORDER BY line''')
    data = cur.fetchall()
    cur.close()
    data_as_array = [row[0] for row in data]
    return jsonify(data_as_array)

@app.route('/api/delays', methods=['GET'])
def get_data():
    # input sanitation: remove all characters that are not in the list of expected characters
    line = re.sub('[^a-zA-Z0-9:]', '', request.args.get('line', ''))
    date = re.sub('[^0-9]', '', request.args.get('date', ''))
    # get data from database
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT line, date, tripCode,
                          time_format(trips.departureTimePlanned, '%H:%i') AS start,
                          time_format(trips.arrivalTimePlanned, '%H:%i') AS end,
                          GROUP_CONCAT(time_to_sec(timediff(arrivalTimeEstimated, stopEvents.arrivalTimePlanned)) ORDER BY stopEvents.arrivalTimePlanned ASC) AS arrivalDelays,
                          GROUP_CONCAT(time_to_sec(timediff(departureTimeEstimated, stopEvents.departureTimePlanned)) ORDER BY stopEvents.departureTimePlanned ASC) AS departureDelays
                FROM stopEvents LEFT JOIN stops ON stops.globalId=stopId RIGHT OUTER JOIN trips ON stopEvents.tripId=trips.id
                WHERE line='{line}' AND date={date}
                GROUP BY trips.id
                ORDER BY line, date, start''')
    data = cur.fetchall()
    cur.close()
    # output as JSON
    column_names = ['line', 'date', 'tripCode', 'start', 'end', 'arrivalDelays', 'departureDelays']
    data_as_dict = [dict(zip(column_names, row)) for row in data]
    return jsonify(data_as_dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')