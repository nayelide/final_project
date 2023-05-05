from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)
# TODO: Create a flask app 
@app.route('/temp', methods = ['POST'] )
def temp():
	temp_data = request.json #this is the data sent from client to server
	print("Temperature data from sensor: "+str(temp_data))
	temp = (temp_data/1023.0) * 100 - 50 #convert to celsius	
	return(jsonify(temp)) #return converted data
	

@app.route('/humidity', methods = ['POST'] )
def humidity():
	humidity_data = request.json #this is the data sent from client to server 
	print("Humidity data from sensor: "+str(humidity_data))
	humid = (humidity_data/1023.0) * 100 #convert to percent humidity
	return(jsonify(humid)) #return converted data

@app.route('/light', methods = ['POST'] )
def light():
	bright = False  #initialize boolean variable
	light_data = request.json #this is the data sent from client to server 
	print("Light data from sensor: "+str(light_data))
	
	#determine if environment is dark or bright by comparing raw data to threshold value
	light_threshold = 200
	if light_data > light_threshold:   
		bright = True 
	else:
		bright = False 
	return(jsonify(bright)) #return boolean 



if __name__ == "__main__":
    app.run(host = '172.20.10.10', debug=True)
    
    