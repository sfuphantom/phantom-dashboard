# phantom-dashboard

> Phantom Dashboard GUI built using Python &amp; Kivy 

Displays critical and useful information from various sensors in realtime to the driver such as:

- :thermometer: *Battery Temperature* :thermometer:
- :battery: *Battery Voltage* :battery:
- :dash: *Vehicle Speed* :dash:
- :recycle:	*Motor Regen* :recycle:	
- :warning: *IMD/AMS Fault* :warning:	
- :question: *General Fault Codes* :question:	
- :rocket: *Rocket Booster Mode* :rocket: ***coming soon**

Additionally the Phantom Dashboard will have the ability to test sensors and code as well as show a log of functions happening within the VCU.

## Getting Started 

The Phantom Dashboard will be running on a Raspberry Pi, so we need to use Ubuntu to build and run our kivy app.

### Windows Environment Setup
- WSL

If you are using Windows 10, you can install Windows Subsystem for Linux (WSL) which is basically a super lightweight and fast linux VM run on windows. This will allow you to install and run linux distros like Ubuntu or Debian, all through windows without the need of a VM or dual boot.

To set this up, follow the instructions on Microsoft's docs: https://docs.microsoft.com/en-us/windows/wsl/install-win10

Additionally, I would recommend using VS Code as your editor since there is a WSL plugin which will allow you to use their built-in terminal instead of another window to put your commands in. This makes development much more seamless and can be a two in one combo. 

> More info on VS Code WSL Extension Here: https://code.visualstudio.com/docs/remote/wsl

- MobaXTerm

You will also need to install some sort of XServer to port the linux display to Windows 10. The best solution I've found is [MobaXTerm](https://mobaxterm.mobatek.net/) Which is a pretty nice terminal as well but we only really need one button from it.

### Prerequisites
With Install script:

After installing WSL or another form of Ubuntu 18.04, run the following command:

` wget -O - https://raw.githubusercontent.com/sfuphantom/phantom-dashboard/master/setup.sh | sudo bash`

`wget` downloads the setup script from the github repo, `|` is the pipe symbol and it will take the contents of the script and give it as an input to `sudo bash` so in the end the command kind of looks like:

`sudo bash(Get_From_Internet(setup script))`
                                                            
The contents of this file just runs all the required commands to setup the environment which can be run manually:
```
#!/bin/bash
apt-get update  # To get the latest package lists
apt-get install python3.7 mosquitto mosquitto-clients python3-pip -y # Installs python3.7 and MQTT

python3.7 -m pip install --upgrade --user pip setuptools virtualenv

python3.7 -m virtualenv ~/kivy_venv # Creates virtual environment for kivy app

source ~/kivy_venv/bin/activate # Activates environment
which pip # Verifies it's using the correct pip from the virtual environment

pip install kivy kivy-garden paho-mqtt # Installs required python packages
garden install gauge # install kivy gauge from Kivy-Garden 

git clone https://github.com/sfuphantom/phantom-dashboard.git ~/kivy_venv/phantom-dashboard
```
And it will setup all the required dependencies and clone this repo in the folder ~/kivy_venv, you may need to run "mosquitto" on the command line to start the MQTT server

Installing dependencies manually:
- **Python3.7.x**

  - To install this you can simply use ``` sudo apt install python3.7 ```
  - We need to use Python3.7 specifically because of the kivy pip package only supports up to 3.7
  - you can check if python3.7 is installed with ``` python3.7 --version ``` 
> Python is nice because it allows you to have multiple installations and use them just by appending the corresponding version number

> Generally though, ` python ` is major version 2.x.x and `python3` is major version 3.x.x

- **Kivy**

For our kivy installation, we want to make sure all our tools are up to date and that we create a virtual environment so that everything such as packages and configurations are neatly bundled together. This is especially useful when we have multiple people working on the code and pushing to git, we want to make sure all of our environments are the same. 

First run the following code in your terminal:

1. ` $ python3.7 -m pip install --upgrade --user pip setuptools virtualenv `
- `-m pip`: Pythons package manager; this is how we get external packages from the [python package index - pyPI](https://pypi.org/)
- `install --upgrade --user`: This tells pip to install or upgrade our package(s) to the python user install directory 
- `pip setuptools virtualenv`: these are the packages that we tell pip to install or upgrade

Now that we have our python3.7 installation setup, we need to create and activate our virtual environment:

2. ` $ python3.7 -m virtualenv ~/kivy_venv ` This creates the virtualenv in your linux home directory (~ : /home/*username*/kivy_venv) 
3. ` $ source ~/kivy_venv/bin/activate ` OR ` . ~/kivy_venv/bin/activate `
> The `.` also means `source` in bash, basically means run script

Finally, we can now install kivy into our virtual environment: 

4. ` $ python -m pip install kivy `

### Software System Architecture
![System Architecture](https://i.imgur.com/APBgW1K.png)

Let's talk about our system architecture for the software running on the Raspberry Pi that encompasses both the dashboard and data acquisition. There are a couple of key elements here but the most important is MQTT which serves as the heart of the whole system. It fascillitates communication between the different applications that make up the dashboard so let's dive into that first.

**MQTT**

MQTT is a publish/subscribe protocol that is lightweight and requires a minimal footprint and bandwidth. MQTT is event driven and enables messages to be pushed to clients. This type of architecture decouples the clients from each other to enable a highly scalable solution without dependencies between data producers and data consumers.
![MQTT](https://i.imgur.com/ZNx7iWl.png)

What this means is that the different applications running on the pi don't need to know about each other, an application will publish a message to a topic and the broker will check what applications are subscribed to that topic and serve them with the message. It is event driven meaning you don't need your application to be waiting for a message, it can be operating normally and when it receives a message, it will momentarily pause, process the message, and go back to regular operation.
In our software system, it is the main method of communication between the different applications ie. front-end is subscribed to vehicleSpeed, VCU back-end will receive a message from the microcontroller indicating a speed and will publish a message to vehicleSpeed.

To install MQTT you need to run the following commands
`sudo apt-get update
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients`

To test, run `mosquitto` to launch the local broker and then run `mosquitto_sub -t "test"` which will subscribe you to the topic "test".
In another terminal, run `mosquitto_pub -m "message from mosquitto_pub client" -t "test"` and you will see the message in the first terminal.

**Backend**

The backend will be a python application that communicates with the Vehicular Computer Unit and the Battery Management System over Controller Area Network (CAN) to receive data about battery level, faults, speed, regen, etc. It will receive that data, process it, and then publish the data to their unique topics such as vehicleSpeed, batteryRegen, batteryVoltage, etc.

**Node-Red**

Node-RED is a programming tool for wiring together hardware devices, APIs and online services in new and interesting ways. It provides a browser-based editor that makes it easy to wire together flows using the wide range of nodes in the palette that can be deployed to its runtime in a single-click. 

It also provides a way to build a GUI very quickly and effectively which proves to be useful in visualizing data from our data acquisition application in real-time as well as provide a way to quickly create test applications due to its great MQTT integration. This means you could effectively fake any messages you would be getting from the Backend. We don't use it for the main dashboard GUI as it is served on a webpage meaning it's not quite as snappy as we would want for our driver.

To install on a Linux system use the following command:
`bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)`
Instructions for other systems can be found here https://nodered.org/docs/getting-started/
The current non-default Node-Red packages we use are: node-red-dashboard

Let's go through an example of a simple Node-Red flow to simulate vehicle speed on the dashboard GUI:
After installing node-red, we want to create a nice GUI to easily simulate the vehicle speed.
First, let's launch node-red if it's not already running by running "node-red-start" on the command line and then we can visit the editor at http://localhost:1880.
Second, we'll install the dashboard package to give us more nodes to work with.
![dashboard package](https://i.imgur.com/YAbvxat.jpg)
After doing that, the dashboard nodes will show up on the right and we'll insert a slider node with a range from 0 to 100.
![slider](https://i.imgur.com/TaPGKWs.jpg)
We'll set the group with just the defaults, specifiy the min as 0 and the max as 100 with a step of 1, and we'll set the topic to events/vehicleSpeed so any message coming out of the slider node will have that topic property.

Then we'll add a MQTT out node to receive messages from the slider node and publish them to the topic that the Dashboard GUI is listening to.
![mqttout](https://i.imgur.com/IJn7DFm.jpg)
We'll leave all the defaults in the Server field except we'll add localhost as the server IP as we're using the internal MQTT broker. 
Hit deploy and go to http://localhost:1880/ui and you can see our beautiful GUI!

Now if we fire up the dashboard and move the slider around we'll see the speed gauge changing
![nodereddashbord](https://i.imgur.com/DGHDZSN.jpg)
Amazing, you can see how fast messages are sent over MQTT and we have just completed our first node-red flow. There are endless possibilities with this tool and thousands of nodes which enable you to accomplish a lot in much shorter time compared to traditional programming.
