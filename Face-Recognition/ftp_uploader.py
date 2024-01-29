import json
from ftplib import FTP

class FTPUploader:
    def __init__(self):
        self.connect()

    def upload_file(self, local_file_path, file_name):
        
        if not (self.is_connection_active()): # Guard Clause
            return
        
        try:
            self.ftp.cwd('/')
            with open(local_file_path, 'rb') as local_file:
                self.ftp.storbinary('STOR ' + file_name, local_file, 1024)
            print(f"File '{local_file_path}' uploaded successfully")
        except Exception as e:
            print(f"Error: {e}")
            
    def is_connection_active(self):
        try:
            # Send a NOOP (No Operation) command to check if the connection is still active
            self.ftp.voidcmd("NOOP")
            print("FTP connection is still active")
            return True
        except Exception as e:
            print(f"FTP connection is not active. Attempting to reconnect.")
            self.connect()
            return False

    def connect(self):
        # Specify the path to your JSON file
        json_file_path = '/home/admin/Desktop/IoT_Project/SettingsPage/UserPrefs.json'

        # Open the JSON file for reading
        with open(json_file_path, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
            
        try:
            self.ftp = FTP(data['ftpSettings']['host'])
            user = data['ftpSettings']['username']
            password = data['ftpSettings']['password']
            self.ftp.login(user, password)
            self.ftp.set_pasv(True)
            print("FTP connection successful")
        except Exception as e:
            print(f"FTP connection failed. Error: {e}")
