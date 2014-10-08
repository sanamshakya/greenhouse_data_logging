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

def loadDatainDB(bufferSerial):
    parsedData = parseBuffer(bufferSerial)

    deviceID = int(parsedData[2])
    temperature = float(parsedData[0])
    humidity = float(parsedData[1])

    m = 0.0066071428571428574
    c = -37.43
    m2 = 0.0052734375
    c2 = -62.94

    temperature = m * temperature + c
    humidity = m2 * humidity + c2

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

      

ser = serial.Serial(2)

count = 1000
in_flag = False
serialBuffer = ""
currentBuffer = ""
lastBuffer = ""
while(1):
   time.sleep(1)
   
   #time.sleep(1)
   #print "serial Buffer :", serialBuffer
   #print "count:",count
   #count = count - 1
   while (ser.inWaiting()):
       #print ser.inWaiting
       
       #serialBuffer = "$"
       #print serialBuffer
       data = ser.read()
       #print "data:", data
       if data == "$":
           in_flag = True
       if(in_flag ):
           #print "writing buffer"
           serialBuffer = serialBuffer + data
           #print serialBuffer
       if data == "*":
           in_flag = False
           currentBuffer = serialBuffer
           serialBuffer = ""
           data = "#"

   if not(lastBuffer == currentBuffer):
       print "serial:",currentBuffer
       loadDatainDB(currentBuffer)
   lastBuffer = currentBuffer
   

   #loadDatainDB(serialBuffer)
   ser.flushInput()
   
    

ser.close()      
