import cv2
import mysql.connector as my
import pandas as pd
import datetime

# Load the cascades
face_cascade = cv2.CascadeClassifier(r"C:\Users\paisa\OneDrive\Desktop\opencv\haar_face.xml")

# Initialize recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(r'face-trainer.yml')

names={1:"satvik",2:"poorna",3:"bharat",4:"yashwant"}

# Connect to the MySQL database
conn = my.connect(
host="localhost",
user="root",
password="",
database=""
)

cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS attendence_register(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), in_time DATETIME, date DATE)")
conn.commit()

# Start the video capture
cap = cv2.VideoCapture(0)

while True:

    # Read the frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Loop through the faces
    for (x, y, w, h) in faces:
        # Get the face ROI
        face_roi = gray[y:y + h, x:x + w]

        # Predict the label of the face
        label, confidence = recognizer.predict(face_roi)

        if confidence<100:
            # Get the name of the person
            name = names[label]

            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Put the name of the person on the frame
            cv2.putText(frame, name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Get the current time
            now = datetime.datetime.now()

            # Check if the employee is coming between 10 AM and 5:30 PM
            if now.hour >= 10 and now.hour < 17:
                continue

            # Get the date
            date = now.strftime("%Y-%m-%d")

            # # Check if there is an existing record for the person for the current date
            # cursor.execute("SELECT * FROM attendence_register WHERE name = %s AND date = %s", (name, date))
            # result = cursor.fetchall()

            in_time = datetime.datetime.now()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            query = "INSERT INTO attendence_register (name, in_time, date) VALUES (%s, %s, %s)"
            values = (name, in_time, date)
            cursor.execute(query, values)
            conn.commit()
            print("Record created successfully for", name)
            break
    
    if cv2.waitKey(1000):
        break
