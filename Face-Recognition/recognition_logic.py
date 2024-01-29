import cv2
import json
from datetime import datetime

class FaceRecognitionLogic:
    def __init__(self):
        # Specify the path to your JSON file
        json_file_path = '/home/admin/Desktop/IoT_Project/SettingsPage/UserPrefs.json'

        # Open the JSON file for reading
        with open(json_file_path, 'r') as file:
            # Load the JSON data from the file
            self.data = json.load(file)
            
        self.names = ['Unknown', 'You Wei', 'Dexter']
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(self.data['filePaths']['trainer'])
        self.faceCascade = cv2.CascadeClassifier(self.data['filePaths']['cascade'])

    def identify_faces(self, gray_img, minW, minH):
        faces = self.faceCascade.detectMultiScale(
            gray_img,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        message = None
        
        if len(faces) > 0:
            timestamp = datetime.timestamp(datetime.now())
            timestamp_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H_%M_%S')
            file_name = timestamp_str + ".avi"
            file_path = self.data['filePaths']['snapshotFolder'] + file_name
            names = []
            for (x, y, w, h) in faces:
                id, confidence = self.recognizer.predict(gray_img[y:y+h, x:x+w])
                names.append("Unknown")
            
                if confidence < 60:
                    names[-1] = self.names[id]
            
            # JSONify
            message = {
                "names": names,
                "timestamp": timestamp_str,
                "filename": file_name,
                "imagepath": "/" + file_name,
                "confidence": "{0}%".format(round(100 - confidence))
            }

        return message

