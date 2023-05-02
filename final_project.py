#EE 250: Lab 7 Test Suites 
# team member 1: Nayeli De Leon
# team member 2: Michelle Arredondo 

import time
#import grovepi
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

if __name__ == '__main__':
   while True:
      # to use BCM numbers 
      GPIO.setmode(GPIO.BCM)
   
      # test suite task 1: Blink the LED 5 times with on/off intervals of 500ms.
      LEDpin = 27 # BCM number for pin 13 (Rpi)
   
      # led as output
      GPIO.setup(LEDpin, GPIO.OUT)

      # led on/off intervals:
      for i in range(5): # 5 times 
         GPIO.output(LEDpin, GPIO.HIGH)	# led on (HIGH)
         time.sleep(0.5)			         # on for 500 ms
         GPIO.output(LEDpin, GPIO.LOW)		# Tled off (LOW)
         time.sleep(0.5)			         # off for 500 ms

      # test suite task #2: For about 5 seconds, read the output of the Grove light sensor with intervals of 
      # 100 ms and print the raw value along with the text “bright” or “dark”
      light_sensor_ch = 0	# channel wired to light sensor (mcp3008)
      light_threshold = 200	   # threshold for "bright" vs "dark"
   
      # Software SPI configuration (mcp3008 pins)
      CLK  = 11
      MISO = 9 
      MOSI = 10
      CS   = 8
      mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
      
      # read light sensor ~ 50 *.1 = 5 sec
      for i in range(50):	   
         light_raw_values = mcp.read_adc(light_sensor_ch)	  
         if light_raw_values > light_threshold:               # bright vs dark, print raw values
            print("Raw value of light sensor: ", light_raw_values, " - bright")
         else:
            print("Raw value of light sensor: ", light_raw_values, " - dark")
         time.sleep(0.1)	   # wait 100 ms
   
   
      # test suite task #3: Blink the LED 4 times with on/off intervals of 200ms.\
      # led on/off intervals:
      for i in range(4): # 4 times 
         GPIO.output(LEDpin, GPIO.HIGH)	# led on (HIGH)
         time.sleep(0.2)			         # on for 200 ms
         GPIO.output(LEDpin, GPIO.LOW)		# Tled off (LOW)
         time.sleep(0.2)			         # off for 200 ms

   
      # test suite task #4: 5 seconds, read the output of the Grove sound sensor with intervals of 100 ms and print the raw value. 
      # If the sound sensor is tapped (i.e. the sound magnitude goes above the threshold decided), the LED should turn on for 100 ms.
      temp_humid_ch = 1	   # MCP3008 channel wired to temp/humidity sensor
      sound_threshold = 1024	   # Threshold to turn on LED
   
      for i in range(50):
         temp_raw_values = mcp.read_adc(temp_humid_ch) # read temp sensor
         temp = (temp_raw_values/1023.0) * 100 - 50
         humid = (temp_raw_values/1023.0) * 100    
         # print raw ADC sound channel values
         print("Raw values of temp sensor: ", temp_raw_values)	
         print("Temp: %.2f C" % temp)
         print("Humid: %.2f %%" % humid)
         
         
         # LED on/off (HIGH/LOW) in 100 ms intervals 
         if temp_raw_values > sound_threshold:
            GPIO.output(LEDpin, GPIO.HIGH)	
            time.sleep(0.1)			
            GPIO.output(LEDpin, GPIO.LOW)	
         else:
            time.sleep(0.1)		
   
      # cleanup LED pin
      GPIO.cleanup(LEDpin)
