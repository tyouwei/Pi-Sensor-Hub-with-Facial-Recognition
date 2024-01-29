#Raspberry Pi Sensor Hub


Hardware
========

1.Camera that supports RTSP
2.Raspberry Pi Sense-Hat

Installation & Configuration
============

Set the static IP address of the Raspberry Pi to 192.168.1.11 to begin configuration

Open the LXterminal on the Pi and type in the commands sequentially:

    1. sudo nano /etc/systemd/system/express-settings.service and copy the below content into the file:
        ```[Unit]
        Description=Sensor hub script
        After=network.target

        [Service]
        ExecStart={path to node file in the env} {path to the express-server.js file}
        WorkingDirectory={path to the folder where express-server.js file is housedin}
        Restart=always
        User=admin

        [Install]
        WantedBy=default.target```
        
    Do the same thing as the above for face-cam.service and sense-hat.service
    
    2. sudo systemctl daemon-reload
    3. sudo systemctl enable express-settings.service
    4. sudo systemctl enable face-cam.service
    5. sudo systemctl enable sense-hat.service
    6. sudo systemctl start express-settings.service
    7. sudo systemctl start face-cam.service
    8. sudo systemctl start sense-hat.service
    9. sudo reboot

Lastly, go over to 192.168.1.11:8080 in the web browser and save the details correctly reflected from the Raspberry Pi Device

Usage
=====

The settings configuration web page is set at 192.168.1.11:8080, ensure that the Pi IP Address is set to th same IP address to facilitate changes to the settings
In the webpage, you will be able to modify the configurations for the MQTT, FTP, RTSP and file path configurations 
