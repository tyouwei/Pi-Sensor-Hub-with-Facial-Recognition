import cv2
import json
from urllib.parse import quote

class Camera:
    def __init__(self):
        self.connect()
        
    def connect(self):
        # Specify the path to your JSON file
        json_file_path = '/home/admin/Desktop/IoT_Project/SettingsPage/UserPrefs.json'

        while True:
            try:
                # Open the JSON file for reading
                with open(json_file_path, 'r') as file:
                    # Load the JSON data from the file
                    data = json.load(file)

                rtspAddress = data['rtspSettings']['address']
                user = data['rtspSettings']['user']
                password = data['rtspSettings']['password']
                # Encode the password for URL
                encoded_password = quote(password)
                # RTSP stream URL with encoded password
                rtsp_url = f'rtsp://{user}:{encoded_password}@{rtspAddress}'
                self.cam = cv2.VideoCapture(rtsp_url)
                self.set_properties()
                print("RTSP Connection successful")
                break
            except Exception as e:
                print(f"RTSP Connection failed. Error: {e}")
                print("Attempting to reconnect in 5 seconds...")
                time.sleep(5)

    def read_frame(self):
        ret, img = self.cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img, gray
        
    def release(self):
        self.cam.release()

    def record_video(self, duration, file_path):
        if not (self.is_connection_active()):
            self.reconnect()
            return
        
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID') 
        out = cv2.VideoWriter(file_path, fourcc, 10.0, (640, 480))

        # Get current time
        start_time = cv2.getTickCount()

        while True:
            elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
            if elapsed_time >= duration:
                break
            # Read a frame from the camera/video file
            img_frame, gray_frame = self.read_frame()
            resize_frame = cv2.resize(img_frame,(640,480))
            
            # Write the frame to the video file
            out.write(resize_frame)
        
        out.release()
        
    def reconnect(self):
        self.release()
        self.connect()
        
    def is_connection_active(self):
        try:
            # Try to read a frame
            ret, _ = self.cam.read()
            return ret
        except Exception as e:
            print(f"Error checking RTSP connection: {e}")
            return False
            
    def set_properties(self):
        self.cam.set(cv2.CAP_PROP_FPS, 10)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 10)
        
    def get_min_face_size(self):
        # Define min window size to be recognized as a face
        minW = 0.1 * self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        minH = 0.1 * self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return minW, minH


