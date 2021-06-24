import mysql.connector

config = {}
try:
    from secrets import *
except ImportError:
    pass


def fetch(date, id_class, sensor):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # sql_query = "SELECT * FROM rooms WHERE (`date_time` > DATE_SUB(now(), INTERVAL 30 DAY))"
    sql_query = "SELECT `date_time`, `sensor_value` FROM rooms WHERE CAST(`date_time` AS DATE)  = \'%s\' AND " \
                "`room_number` = \'%s\' AND `sensor_type` = \'%s\'" % (date, id_class, sensor)

    cursor.execute(sql_query)

    data = cursor.fetchall()

    cnx.close()

    return data
