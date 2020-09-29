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

