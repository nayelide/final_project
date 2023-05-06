# final_project
Team Member #1: Michelle Arredondo
Team Member #2: Nayeli De Leon

How to run IoT system:
Assuming you have a GrovePi kit, raspberry pi, and MCP3008:
Fork and clone the code from https://github.com/nayelide/final_project to get started!
Running the client: To begin, ssh into your RPi, then scp the client code from your host machine on to your RPi
after configuring the circuit that includes your GrovePi light sensor and temperature/humidity sensor.
These sensors are connected through the MCP3008 for analog to digital conversion. Run the client code.

Running the server: In a separte terminal, run the server code on your host machine.

As these are both running, the server will get the data sent from the client
and a table of the events (brightness, temperature, and humidity) are shown!

Link to demo video showing node identifiations, SSH-ing int our RPi, and running the client and server codes:
https://drive.google.com/file/d/1aX7v6emnMWPcBclLoENzL86JqnP10xJ5/view?usp=sharing 

