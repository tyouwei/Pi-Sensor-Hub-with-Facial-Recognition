from mqtt_client import MQTTClient
from ftp_uploader import FTPUploader
from camera import Camera
from recognition_logic import FaceRecognitionLogic
import cv2
import json
from datetime import datetime

class MainApp:
    def __init__(self):
        # Specify the path to your JSON file
        json_file_path = '/home/admin/Desktop/IoT_Project/SettingsPage/UserPrefs.json'

        # Open the JSON file for reading
        with open(json_file_path, 'r') as file:
            # Load the JSON data from the file
            self.data = json.load(file)
            
        self.mqtt_client = MQTTClient()
        self.ftp_uploader = FTPUploader()
        self.camera = Camera()
        self.recognizer = FaceRecognitionLogic()
        self.frame_count = 0

    def run(self):
        while True:
            img, gray = self.camera.read_frame()
            
            self.frame_count += 1
            
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break
            
            if self.frame_count % self.camera.cam.get(cv2.CAP_PROP_FPS) != 0:
                continue
            
            minW, minH = self.camera.get_min_face_size()
            json_object = self.recognizer.identify_faces(gray, minW, minH)
            
            if json_object is None:
                continue
            
            #Person detected
            file_name = json_object['filename']
            folder_path = self.data['filePaths']['snapshotFolder']
            local_img_path = folder_path + file_name
            self.camera.record_video(10, local_img_path)
               
            self.ftp_uploader.upload_file(local_img_path, file_name)
            self.mqtt_client.publish(json_object)

        print("\n[INFO] Exiting Program and cleanup stuff")
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = MainApp()
    app.run()
