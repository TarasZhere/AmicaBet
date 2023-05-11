#!/bin/bash

apt-get update -y
apt-get upgrade -y
apt-get install -y python3-pip
apt-get install -y git

pip3 install --upgrade flask

# code download
git clone --branch serversplit https://github.com/TarasZhere/AmicaBet_Flask.git

flask --app server run --port 80 --host 0.0.0.0 