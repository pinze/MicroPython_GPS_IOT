# MicroPython_GPS_IOT
A topic of GPS IOT application for use with MicroPython and ESP8266 mini D1.Send the datas to the server and display it on the Google map.

<img src="https://user-images.githubusercontent.com/63340820/149474730-e32dcc46-3fa5-4154-8d13-662f2cf54457.png" width="650"/> <img src="https://user-images.githubusercontent.com/63340820/149474989-bee89cad-20d7-4aa7-a460-2312ac999877.png" width="300"/>



# Modules
## 1. ESP8266:
  * mini-mcu wifi board
  * 11 digital I/O pins
  * 1analog input
  * 4 MB flash
  
  <img src="https://user-images.githubusercontent.com/63340820/149464356-5e10162b-1b92-4701-b343-c4300a6a9824.png" width="300"/>
 
## 2. 0.96 inch OLED
  * ssd1306 0.96 inch OLED display
  * I2C driver
  
  <img src="https://user-images.githubusercontent.com/63340820/149467712-d794934c-0668-40f0-80a0-8d5e81810b48.png" width="300"/>
 
## 3. DHT11 Humidity&Temperature Sensor
  
  <img src="https://user-images.githubusercontent.com/63340820/149466127-64425eb8-e333-41c9-a9fb-04b791c0aeb0.png" width="300"/>
 
## 4. GY-GPS6MV2(blox NEO-6M)
  * UART TTL connector
  * EEPROM to store settings
  
  <img src="https://user-images.githubusercontent.com/63340820/149466806-988e36ae-f8bc-4897-a774-3e369ae7b832.png" width="300"/>

# Writing
|  **D1 mini**   |    **6MV2**    |    **DHT11**   |    **OLED**    |
|:--------------:|:--------------:|:--------------:|:--------------:|
|     `3.3`      |     `VCC`      |     `VCC`      |     `VCC`      |
|     `GND`      |     `GND`      |     `GND`      |     `GND`      |
|     `Rx`       |     `Tx`       |                |                |
|     `Tx`       |     `Rx`       |                |                |
|     `GPIO 4`   |                |    `Single`    |                |
|`SCL`(`GPIO 13`)|                |                |     `SCL`      |
|`SDA`(`GPIO 12`)|                |                |     `SDA`      |

# Server
https://github.com/DDPlay123/IoT_Python_Server

# D1 mini set up
1. Import webrepl_setup
2. boot.py setting
3. set your wifi's name and password in boot
3. burn main.py into D1 mini

# main
--------
```
# Main function
gps = GPS()
oled = OLED()
#d = dht.DHT11(Pin(2))

def loop():
    global gps, oled, api, d4
    
    gpsStr = b''
    gpsReading = False    
    
    while True:
        data = gps.getGPSInfo()
        #d.measure()
        if data and (gpsReading or ('$GPRMC' in data)) :
            gpsStr += data
            if '\n' in data:
                gpsReading = False
                #temp = d.temperature()
                #hum = d.humidity()
                lat, long= gps.convertGPS(gpsStr)
                oled.displayGPS(lat, long)
                # Send lat&long to Web Server
                # 伺服器平常不會開，沒開時，請關閉此段落。
                #############
                
                value1 = '{"longitude":'+'"'+long+'"'+','
                value2 = '"latitude":'+'"'+lat+'"'+','
                #value3 = '"temp":'+'"'+str(temp)+'"'+','
                #value4 = '"humid":'+'"'+str(hum)+'"}'
                data = value1+value2#+value3+value4
                r = requests.post(url,data=data,headers=header)
                #############
                
                gpsStr = b''
                gc.collect()
                break
            else:
                gpsReading = True
```  
