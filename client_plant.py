# team member 1: Nayeli De Leon
# team member 2: Michelle Arredondo
 
import numpy as np
import pandas as pd
import requests
import plotly.express as px
from PIL import Image 
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
    
#this program collects temperature, humidity, and light data from Grove analog sensor and then
#offloads data by using POST requests to server. Server converts data and returns converted data and a boolean.
#This program collects 5 samples of converted data and prints mean and standard deviation values. The returned boolean either enables 
#or disables an LED lighting up.




url = 'http://172.20.10.10:5000'


if __name__ == '__main__':
   while True:
      # to use BCM numbers 
      GPIO.setmode(GPIO.BCM)
   
      LEDpin = 27 # 27 is the BCM number for pin 13 (RPi)
   
      # set-up led as an output
      GPIO.setup(LEDpin, GPIO.OUT)
      
      #set-up light sensor and threshold
      light_sensor_ch = 0	# channel wired to light sensor (mcp3008)
      light_threshold = 200	   # threshold for "bright" vs "dark"
      
      # Software SPI configuration (mcp3008 pins)
      CLK  = 11
      MISO = 9 
      MOSI = 10
      CS   = 8
      mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
      lights= []

      # For about 5 seconds, read the output of the Grove light sensor and append to 'lights' array. Collect 5 light data samples/
      # Also, send raw light data to server,
      # then server returns a boolean TRUE or FALSE if level of light is "bright"=true or "dark"=false.
      # There is a 100 ms pause in between iterations
         

      # read light sensor ~ 50 *.1 = 5 sec
      
      for i in range(5):	   
         light_raw_values = mcp.read_adc(light_sensor_ch)
         message = light_raw_values
         response = requests.post(f"{url}/light", json=message)
         bright = response.json()	
         lights.append(message) 
         time.sleep(0.1) # wait 100 ms
         
         if bright == True:
         	print("Bright")
         	GPIO.output(LEDpin, GPIO.HIGH)	   # led on (HIGH)
         else:
         	print("Dark")
         	GPIO.output(LEDpin, GPIO.LOW)	   # led off (LOW)
	
      #set-up arrays to collect temperature and humidity values, mean values, and standard deviation values. Set-up 'data' to store all sensor information
      #Also, set-up temp/humidity sensor channel and temperature threshold

      temp_humid_ch = 1	   	   	   # MCP3008 channel wired to temp/humidity sensor
      temp_threshold = 1024	       # Temperature threshold
      temps = []
      humidities = []
      means = []
      stds = []
      data = []
      
      # Collect 5 samples of temp/humidity sensor values and send to server to convert values into Celsius and Percent-humidity, accordingly
      # Return converted data values and append to appropriate arrays 
   
      for i in range(5):
         temp_raw_values = mcp.read_adc(temp_humid_ch) # read temp/humidity sensor
         message2 = temp_raw_values
         response2 = requests.post(f"{url}/temp", json=message2)
         response3 = requests.post(f"{url}/humidity", json=message2)  
         
         new_temp= response2.json() 
         new_humid = response3.json()
          
         temps.append(new_temp)  
         humidities.append(new_humid)  
         

      #Calculate mean and standard deviations for temperature, humidity, and light samples
      mean_temp = np.mean(temps)
      std_temp = np.std(temps)
      mean_humid = np.mean(humidities)
      std_humid = np.std(humidities)
      mean_light = np.mean(lights)
      std_light = np.std(lights)
      
      #Append temperature, humidity, and light mean values to "means" array
      means.append(mean_temp)
      means.append(mean_humid)
      means.append(mean_light)
      
      #Append temperature, humidity, and light standard deviation values to "stds" array
      stds.append(std_temp)
      stds.append(std_humid)
      stds.append(std_light)
      
      #Create "data" array with mean and standard deviation information for each analog sensor 
      sensors = ['Temperature','Humidity', 'Brightness']
      count = 0
      
      for sensor in sensors: 
            	
      	mean = means[count]
      	std = stds[count]

      	data.append([sensor,mean,std])
      	
      	count += 1
      	
      #create a dataframe to make a bar graph 
      df = pd.DataFrame(data, columns=['sensor','mean','std'])
      print(df)

      #fig = px.bar(df, x='sensor',y='mean', error_y='std')
      #fig.write_image("sensorData.png")
      
      	
   
      # cleanup LED pin
      GPIO.cleanup(LEDpin)
      
    

if __name__ == "__main__":
    main()
