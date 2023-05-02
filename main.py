# Complete project details at https://RandomNerdTutorials.com

from time import sleep
from machine import Pin, I2C
import machine


rtc = machine.RTC()
# ESP32 - Pin assignment
#i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
# ESP8266 - Pin assignment

# day_length_in_5_seconds = 4
# tempSum = 0
# humSum = 0
# presSum = 0
# count = 0
# tempMax = 0
# humMax = 0
# presMax = 0
# tempMin = 1000
# humMin = 1000
# # presMin = 1000
# f = open('inf.txt', 'a')
# f.write('Date\t\t\tAverage Temperature\tMinimum Temperature\tMaximum Temperature\tAverage Humidity\tMinimum Humidity\tMaximum Humidity\tAverage Pressure\tMinimum Pressure\tMaximum Pressure\n')
# f.close()


def log():
    bme = BME280.BME280(i2c=i2c)
    temp = str(bme.temperature)
    hum = str(bme.humidity)
    pres = str(bme.pressure)
#         tempSum += float(temp[:-1])
#         humSum += float(hum[:-1])
#         presSum += float(pres[:-3])
#
#         count += 1
    # uncomment for temperature in Fahrenheit
    #temp = (bme.read_temperature()/100) * (9/5) + 32
    #temp = str(round(temp, 2)) + 'F'
    print('Temperature: ', temp)
    print('Humidity: ', hum)
    print('Pressure: ', pres)
    t = rtc.datetime()
    year = t[0]
    month = t[1]
    day = t[2]
    hours = t[4]
    minutes = t[5]
    seconds = t[6]
    datestr = str(day)+'/'+str(month)+'/'+str(year)
    timestr = datestr+' '+str(hours)+':'+str(minutes)+':'+str(seconds)
    st = "Time:"+timestr+" Temperature:" + \
        str(temp)+" Pressure:"+str(pres)+" Humidity:"+str(hum)+"\n"
    f = open("log.txt", "a")
    f.write(st)
    f.close()
#         if(count % day_length_in_5_seconds == 0):
#             tempAve = str(tempSum/count)
#             humAve = str(humSum/count)
#             presAve = str(presSum/count)
#             tempMin = min(tempMin, float(temp[:-1]))
#             tempMax = max(tempMax, float(temp[:-1]))
#             humMin = min(humMin, float(hum[:-1]))
#             humMax = max(humMax, float(hum[:-1]))
#             presMin = min(presMin, float(pres[:-3]))
#             presMax = max(presMax, float(pres[:-3]))
#             st = datestr+'\t \t'+str(tempAve)+'C \t\t\t'+str(tempMin)+'C \t\t\t'+str(tempMax)+'C \t\t\t'+str(humAve)+'% \t\t\t'+str(
#                 humMin)+'% \t\t\t'+str(humMax)+'% \t\t\t'+str(presAve)+'hPa \t\t\t'+str(presMin)+'hPa \t\t\t'+str(presMax)+'hPa \n'
#             f = open('inf.txt', 'a')
#             f.write(st)
#             f.close()


def web_page():
    bme = BME280.BME280(i2c=i2c)
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"><style>body { text-align: center; font-family: "Trebuchet MS", Arial;}
  table { border-collapse: collapse; width:35%; margin-left:auto; margin-right:auto; }
  th { padding: 12px; background-color: #0043af; color: white; }
  tr { border: 1px solid #ddd; padding: 12px; }
  tr:hover { background-color: #bcbcbc; }
  td { border: none; padding: 12px; }
  .sensor { color:white; font-weight: bold; background-color: #bcbcbc; padding: 1px;
  </style></head><body><h1>ESP with BME280</h1>
  <table><tr><th>MEASUREMENT</th><th>VALUE</th></tr>
  <tr><td>Temp. Celsius</td><td><span class="sensor">""" + str(bme.temperature) + """</span></td></tr>
  <tr><td>Temp. Fahrenheit</td><td><span class="sensor">""" + str(round((bme.read_temperature()/100.0) * (9/5) + 32, 2)) + """F</span></td></tr>
  <tr><td>Pressure</td><td><span class="sensor">""" + str(bme.pressure) + """</span></td></tr>
  <tr><td>Humidity</td><td><span class="sensor">""" + str(bme.humidity) + """</span></td></tr>
    </body></html>"""
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:

    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Content = %s' % request)
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')
