import cv2
import os
from urllib.parse import quote

# Get HaarCascade configuration
faceCascade = cv2.CascadeClassifier('/home/admin/Pi-Sensor-Hub-with-Facial-Recognition/Face-Recognition/haarcascade_frontalface_default.xml')

# Replace 'your_password' with your actual password
password = '#Strongether1'

# Encode the password for URL
encoded_password = quote(password)

# RTSP stream URL with encoded password
rtsp_url = f'rtsp://admin:{encoded_password}@192.168.1.3:554'

# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"H264"))


# Set the frame rate to 10 FPS
cap.set(cv2.CAP_PROP_FPS, 1)

desired_width = 1280  # Increase width for higher resolution
desired_height = int(desired_width * 9 / 16)  # Calculate height for 16:9 aspect ratio
# Set a lower resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)

# For each person, enter one numeric face id
face_id = input('\n Enter user ID end press <Enter> ==>  ')
print("\n Initializing face capture. Look the camera and wait ...")

# Initialize individual sampling face count
count = 0
while(True):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
        count += 1
        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 100: # Take 30 face sample and stop video
         break
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cap.release()
cv2.destroyAllWindows()
