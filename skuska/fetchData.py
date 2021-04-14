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

  sqlQuery = 'SELECT * FROM rooms'
  cursor.execute(sqlQuery)

  data = cursor.fetchall()

  cnx.close()

  return data