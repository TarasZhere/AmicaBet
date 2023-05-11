#!/bin/bash

apt-get update -y
apt-get upgrade -y
apt-get install -y wget
apt-get install -y python3-pip
apt-get install -y git

pip3 install --upgrade flask

# code download
git clone 