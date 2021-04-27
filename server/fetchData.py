import mysql.connector

config = {
    'user': '**REMOVED**',
    'password': '**REMOVED**',
    'host': '**REMOVED**',
    'database': '**REMOVED**',
    'port': '**REMOVED**',
    'raise_on_warnings': True
}


def fetch():
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()

    sql_query = "SELECT * FROM rooms WHERE (`date_time` > DATE_SUB(now(), INTERVAL 30 DAY))"
    cursor.execute(sql_query)

    data = cursor.fetchall()

    cnx.close()

    return data
