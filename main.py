from machine import UART, Pin, I2C
import time, ssd1306, ujson, gc, network, dht
import urequests as requests

# Define Web Server URL & Header
url = "http://118.160.140.69:3000/web/add"
header = {'Content-Type':'application/json'}

# Define GPS
class GPS:
    def __init__(self):
        self.com = UART(0, 9600)
        self.com.init(9600)
        
    def getGPSInfo(self):
        data = self.com.readline()
        return data

    def latitude(self, d, h):
        if d == '':
            return 'null'

        hemi = '' if h == 'N' else '-'
        deg = int(d[0:2])
        min = str(float(d[2:]) / 60)[1:]

        return hemi + str(deg) + min

    def longitude(self, d, h):
        if d == '':
            return 'null'

        hemi = '' if h == 'E' else '-'
        deg = int(d[0:3])
        min = str(float(d[3:]) / 60)[1:]

        return hemi + str(deg) + min

    def convertGPS(self, gpsStr):
        gps = gpsStr.split(b'\r\n')[0].decode('ascii').split(',')

        lat = self.latitude(gps[3], gps[4])  # N or S
        long = self.longitude(gps[5], gps[6]) # E or W

        return (lat, long)

class OLED:
    def __init__(self, scl=13, sda=12):
        self.oled = ssd1306.SSD1306_I2C(
            128, 64,
            I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)
        )
        self.oled.text("GPS RUNNING...", 0, 30)
        self.oled.show()

    def displayGPS(self, lat, long, temp, humid):
        lat = "Lat: " + lat
        long = "Long: " + long
        temp = "Temp: " + str(temp) + " C"
        humid = "Humid: " + str(humid) + "%"
        self.oled.fill(0)
        self.oled.text("Tracking", 0, 0)
        self.oled.text(lat, 0, 20)
        self.oled.text(long, 0, 30)
        self.oled.text(temp, 0, 40)
        self.oled.text(humid, 0, 50)
        self.oled.show()
class DHT11:
    def __init__(self):
        self.d = dht.DHT11(Pin(4))
    def temperature(self):
        self.d.measure()
        temp = self.d.temperature()
        return temp
    def humidity(self):
        humid = self.d.humidity()
        return humid
        

# Main function
gps = GPS()
oled = OLED()
d4 = Pin(2, Pin.OUT, value=0)


def loop():
    global gps, oled, d4, d
    #d = dht.DHT11(Pin(4))
    d = DHT11()
    gpsStr = b''
    gpsReading = False    
    
    while True:
        d4.value(1)
        data = gps.getGPSInfo()
        #d.measure()
        #d.measureDHT()
        if data and (gpsReading or ('$GPRMC' in data)) :
            gpsStr += data
            if '\n' in data:
                gpsReading = False
                #temp = d.temperature()
                #humid = d.humidity()
                temp = d.temperature()
                humid = d.humidity()
                d4.value(0)
                lat, long= gps.convertGPS(gpsStr)
                oled.displayGPS(lat, long, temp, humid)
                
                # Send lat&long to Web Server
                # 伺服器平常不會開，沒開時，請關閉此段落。
                #############
                
                value1 = '{"longitude":'+'"'+long+'"'+','
                value2 = '"latitude":'+'"'+lat+'"'+','
                value3 = '"temp":'+'"'+str(temp)+'"'+','
                value4 = '"humid":'+'"'+str(humid)+'"}'
                data = value1+value2+value3+value4
                r = requests.post(url,data=data,headers=header)
                
                ############# 
                gpsStr = b''
                gc.collect()
                d4.value(1)
                break
            else:
                gpsReading = True

def main():
    while True:
        loop()

main()

