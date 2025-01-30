from time import time
tic = time()
from datetime import datetime
print("crawler run at", datetime.now())

import configparser
config = configparser.ConfigParser()
config.read('/home/chrfrd/.my.cnf')

import mysql.connector
con = mysql.connector.connect(user=config['client']['user'], password=config['client']['password'], host='127.0.0.1', database='chrfrd_bustracking')

import urllib.request
import json
crawlTasks = ['de:09663:22', 'de:09663:358']   # Adalberokirche, Skyline Hill Center
for stopParentId in crawlTasks:
    stopParentIdForUrl = stopParentId.replace(':', '%3A')
    url = f"https://whitelabel.bahnland-bayern.de/efa/XML_DM_REQUEST?commonMacro=dm&type_dm=any&name_dm={stopParentIdForUrl}&outputFormat=rapidJSON&mode=direct&useRealtime=1&includeCompleteStopSeq=1&depType=stopEvents"
    print(url)
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        #for se in data['stopEvents']:
        #    print(se['transportation']['id'], se['transportation']['properties']['tripCode'], se['departureTimePlanned'][0:10].replace('-',''))
        cursor = con.cursor()
        sql = "INSERT INTO trips (line, tripCode, date, departureTimePlanned, arrivalTimePlanned) VALUES (%s, %s, %s, CONVERT_TZ(%s, 'UTC', 'Europe/Berlin'), CONVERT_TZ(%s, 'UTC', 'Europe/Berlin')) ON DUPLICATE KEY UPDATE updated=NOW()"
        val = [(
                stopEvent['transportation']['id'],
                stopEvent['transportation']['properties']['tripCode'],
                stopEvent['departureTimePlanned'][0:10].replace('-',''),
                stopEvent['previousLocations'][0]['departureTimePlanned'],
                stopEvent['onwardLocations'][-1]['arrivalTimePlanned']
            )
            for stopEvent in data['stopEvents']
            ]
        print(val)
        cursor.executemany(sql, val)
        con.commit()

cursor.execute("SELECT `id`, `line`, `tripCode`, `date` FROM `trips` WHERE `departureTimePlanned` < NOW() and `arrivalTimePlanned` < addtime(NOW(), '00:05:00') and NOT `completed`")
rows = cursor.fetchall()
for row in rows:
    print(row)
    dbid, line, tripCode, date = row
    url = f"https://whitelabel.bahnland-bayern.de/efa/XML_TRIPSTOPTIMES_REQUEST?commonMacro=tripstoptimes&outputFormat=rapidJSON&line={line}&tripCode={tripCode}&date={date}&useRealtime=1"
    print(url)
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
        if 'stopSequence' in data['leg']:
            print('yeah, data!')
            sql = "INSERT IGNORE INTO stops (globalId, parentId, disassembledName) VALUES (%s, %s, %s)"
            vals = [(
                     stop['id'],
                     stop['parent']['id'],
                     stop['disassembledName']
                    )
                    for stop in data['leg']['stopSequence']
                   ]
            print(vals)
            cursor.executemany(sql, vals)
            con.commit()
            
            sql = "INSERT INTO stopEvents (tripId, stopId, arrivalTimePlanned, departureTimePlanned, arrivalTimeEstimated, departureTimeEstimated) VALUES (%s, %s, CONVERT_TZ(%s, 'UTC', 'Europe/Berlin'), CONVERT_TZ(%s, 'UTC', 'Europe/Berlin'), CONVERT_TZ(%s, 'UTC', 'Europe/Berlin'), CONVERT_TZ(%s, 'UTC', 'Europe/Berlin')) ON DUPLICATE KEY UPDATE arrivalTimePlanned=VALUES(arrivalTimePlanned), departureTimePlanned=VALUES(departureTimePlanned), arrivalTimeEstimated=VALUES(arrivalTimeEstimated), departureTimeEstimated=VALUES(departureTimeEstimated)"
            vals = [(
                     dbid,
                     stop['id'],
                     'NULL' if 'arrivalTimePlanned' not in stop else stop['arrivalTimePlanned'],
                     'NULL' if 'departureTimePlanned' not in stop else stop['departureTimePlanned'],
                     'NULL' if 'arrivalTimeEstimated' not in stop else stop['arrivalTimeEstimated'],
                     'NULL' if 'departureTimeEstimated' not in stop else stop['departureTimeEstimated'],
                    )
                    for stop in data['leg']['stopSequence']
                   ]
            print(vals)
            cursor.executemany(sql, vals)
            con.commit()
        else:
            cursor.execute("UPDATE trips SET completed=1 WHERE id=%s", (dbid,))
            con.commit()
            print('set to completed')
        print("---")

con.close()

toc = time()
print(datetime.now())
print ("execution took", toc - tic, "seconds")
print("======================================================================")
