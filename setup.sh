#!/bin/bash
apt-get update  # To get the latest package lists
apt-get install python3.7 mosquitto -y # Installs python3.7 and MQTT

python3.7 -m pip install --upgrade --user pip setuptools virtualenv

python3.7 -m virtualenv ~/kivy_venv # Creates virtual environment for kivy app

source ~/kivy_venv/bin/activate # Activates environment
which pip # Verifies it's using the correct pip from the virtual environment

pip install kivy kivy-garden paho-mqtt # Installs required python packages

git clone https://github.com/sfuphantom/phantom-dashboard.git ~/kivy_venv/phantom-dashboard