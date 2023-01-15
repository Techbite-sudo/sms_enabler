import serial
import mysql.connector

# Connect to the GSM modem
ser = serial.Serial('COM1', 9600, timeout=5)
ser.write(b'AT+CMGF=1\r')  # set SMS mode to text
ser.write(b'AT+CMGL="ALL"\r')  # request all SMS messages

# Connect to the MySQL database
conn = mysql.connector.connect(user='root', password='', host='localhost',
                               database='sms_enabler')
cursor = conn.cursor()

# Create the table to store the messages
cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                  (id INT AUTO_INCREMENT, sender VARCHAR(255), message TEXT, PRIMARY KEY (id))''')

# Parse the SMS messages
sms_list = ser.readlines()
for sms in sms_list:
    # Extract the sender's number and the message text
    parts = sms.split(",")
    sender = parts[1].strip('"')
    message = parts[-1].strip()

    # Insert the message into the MySQL table
    cursor.execute("INSERT INTO sms_messages (sender, message) VALUES (%s, %s)", (sender, message))
    conn.commit()

# Close the database connection
cursor.close()
conn.close()
