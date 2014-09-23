import MySQLdb
import serial
import time 

def parseBuffer(bufferSerial):
    parsedData = []
    commaLocation = []
    commaIndex = 0
    count = 0
    if bufferSerial[0] == "$" and bufferSerial[-1] == "*":
       for c in bufferSerial:
          if c == ",":
              commaLocation.append(commaIndex)
          commaIndex +=1
    for count in range(len(commaLocation)-1):
        data = bufferSerial[commaLocation[count]+1:commaLocation[count+1]]
        parsedData.append(data)
    return parsedData
      

ser = serial.Serial(2)
count = 100
while(count>0):
   time.sleep(1)
   count = count - 1




   while (ser.inWaiting()):
      #print ser.inWaiting
      if (ser.inWaiting()<20):
         bufferSerial = ser.read(ser.inWaiting())
         parsedData = parseBuffer(bufferSerial)

         deviceID = int(parsedData[0])
         temperature = float(parsedData[1])
         humidity = float(parsedData[2])

         print deviceID,temperature,humidity
            

         

         # Open database connection
         db = MySQLdb.connect(host="127.0.0.1",user="sanamshakya",passwd="starfish",db="test_data")
         # prepare a cursor object using cursor() method
         cursor = db.cursor()
   
         # Prepare SQL query to INSERT a record into the database.
         # creating static query using string
         sql1= """INSERT INTO `test_data`.`erts_lab_data` (`id`, `timestamp`, `Temperature`, `Humidity`) VALUES (NULL, CURRENT_TIMESTAMP, '45', '98')"""
   
         # creating dynamic query using string
         sql = "INSERT INTO `erts_lab_data` ( `Temperature`, `Humidity`)  VALUES ('%f','%f') " % (temperature, humidity)
   
   
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
      else:
          ser.flushInput()

ser.close()      
