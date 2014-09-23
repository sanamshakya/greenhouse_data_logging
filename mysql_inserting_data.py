import MySQLdb

humidity = 75
temperature = 28.5

# Open database connection
db = MySQLdb.connect(host="127.0.0.1",user="sanamshakya",passwd="starfish",db="test_data")
# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
# creating static query using string
sql1= """INSERT INTO `test_data`.`erts_lab_data` (`id`, `timestamp`, `Temperature`, `Humidity`) VALUES (NULL, CURRENT_TIMESTAMP, '45', '98')"""

# creating dynamic query using string
sql = "INSERT INTO `erts_lab_data` ( `Temperature`, `Humidity`)  VALUES ('%f','%d') " % (temperature, humidity)


try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
