import cv2
import numpy as np
import os
import json
from ftplib import FTP
from datetime import datetime
import paho.mqtt.client as mqtt
from urllib.parse import quote

# Global constants
# Personnel
NAMES = ['Unknown', 'You Wei', 'Dexter']

# File paths
CASCADE_PATH = "/home/admin/Desktop/Face-Recognition-using-Raspberry-Pi/haarcascade_frontalface_default.xml"
TRAINER_PATH = '/home/admin/Desktop/Face-Recognition-using-Raspberry-Pi/trainer/trainer.yml'


# MQTT constants
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

# Video properties
FPS = 10
FRAME_W= 640
FRAME_H = 480
BUFFERSIZE = 10

# FTP params
ftp_host = '192.168.1.2'
ftp_username = 'raspberry'
ftp_password = 'M3dellin123'

def init():
    # Initialize face recognizer and cascade classifier
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_PATH)
    faceCascade = cv2.CascadeClassifier(CASCADE_PATH)

    # Set up RTSP stream
    cam = cv2.VideoCapture(get_rtsp_url())
    set_video_capture_properties(cam)

    # Initialize face detection parameters
    minW, minH = get_min_face_size(cam)

    # Establish connection to MQTT broker
    mqttConnection = setup_mqtt_connection()
    
    return cam, faceCascade, minW, minH, recognizer, mqttConnection
    
def setup_mqtt_connection():
    # Initialize the MQTT client
    mqttConnection = mqtt.Client()

    # Set up callback functions
    mqttConnection.on_publish = on_publish

    # Connect to the MQTT broker (replace 'localhost' with your broker's IP or hostname)
    mqttConnection.connect(MQTT_BROKER, MQTT_PORT, 60)

    return mqttConnection

def get_rtsp_url():
    # Replace 'your_password' with your actual password
    password = '#Strongether1'

    # Encode the password for URL
    encoded_password = quote(password)

    # RTSP stream URL with encoded password
    return f'rtsp://admin:{encoded_password}@192.168.1.3:554'

def set_video_capture_properties(cam):
    # Lower resolution and frame rate for real-time monitoring
    cam.set(cv2.CAP_PROP_FPS, FPS)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, BUFFERSIZE)

def get_min_face_size(cam):
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(cv2.CAP_PROP_FRAME_WIDTH)
    minH = 0.1 * cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return minW, minH

def on_publish(client, userdata, mid):
    print(f"Message published with mid: {mid}")
    
def publish_mqtt(mqttConnection, message):
    mqttConnection.publish("SmartNation", message)
    
def upload_file_ftp(local_file_path, file_name):
    try:
        # Connect to the FTP server
        ftp = FTP(ftp_host)
        ftp.login(ftp_username, ftp_password)
        ftp.set_pasv(True)

        # Open the local file in binary mode
        ftp.cwd('/')
        with open(local_file_path, 'rb') as local_file:
            ftp.storbinary('STOR ' + file_name, local_file, 1024)



        print(f"File '{local_file_path}' uploaded successfully to {ftp_host}")
    except Exception as e:
        print(f"Error: {e}")

def identify_faces(faces, img, recognizer, color, mqttConnection):
    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(color[y:y+h, x:x+w])
        name = "Unknown"
        
        # Get the current timestamp
        timestamp = datetime.timestamp(datetime.now())

        # Convert the timestamp to a string with a specific format
        timestamp_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H_%M_%S')
        
        # Save the captured image into the snapshot folder
        file_name = timestamp_str + ".jpg"
        file_path = "/home/admin/Desktop/Face-Recognition-using-Raspberry-Pi/snapshots/" + file_name
        cv2.imwrite(file_path, img)

        # Check if confidence is less than 60 ==> "0" is a perfect match
        if confidence < 60:
            name = NAMES[id]
        
        #jsonify
        message = {
            "name": name,
            "confidence": "{0}%".format(round(100 - confidence))
        }
        
        json_data = json.dumps(message)
        
        
        # Publish MQTT when faces are detected
        publish_mqtt(mqttConnection, json_data)
        
        # FTP 
        upload_file_ftp(file_path, file_name)
        

def main():
    cam, faceCascade, minW, minH, recognizer, mqttConnection = init()
    
    # Frame counter
    frameCount = 0

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        if frameCount % FPS == 0:
            identify_faces(faces, img, recognizer, gray, mqttConnection)

        frameCount += 1
        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n[INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
