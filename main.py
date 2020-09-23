import urequests, utime, machine
from machine import RTC, I2C, Pin, SPI
import max7219


# user data

url = "http://worldtimeapi.org/api/timezone/Europe/MAdrid" # see http://worldtimeapi.org/timezones
web_query_delay = 60000 # interval time of web JSON query
retry_delay = 5000 # interval time of retry after a failed Web query

# initialization

# SSD1306 OLED display
from machine import Pin, SPI
spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
display = max7219.Matrix8x8(spi, Pin(2), 4)
# internal real time clock

# set timer
update_time = utime.ticks_ms() - web_query_delay
display.brightness(0)
display.fill(0)
display.text("...", 0, 0, 1)
display.show()
utime.sleep(10)
# main loop
while True:
    # HTTP GET data
    response = urequests.get(url)
    
    print("en el loop")
            
    # parse JSON
    parsed = response.json()
    datetime_str = str(parsed["datetime"])
    year = int(datetime_str[0:4])
    month = int(datetime_str[5:7])
    day = int(datetime_str[8:10])
    hour = int(datetime_str[11:13])
    minute = int(datetime_str[14:16])
    second = int(datetime_str[17:19])
    subsecond = int(round(int(datetime_str[20:26]) / 10000))

    print("{0:0=2d}".format(hour) + "{0:0=2d}".format(minute))
    # update SSD1306 OLED display
    display.fill(0)
    display.text("{0:0=2d}".format(hour) + "{0:0=2d}".format(minute), 0, 0, 1)
    display.show()
    utime.sleep(1)