#!/bin/bash

gcloud config set project amicabet
gcloud compute instances delete amicabet-server

gcloud compute instances create amicabet-server --machine-type n1-standard-1 --image-family debian-10 --image-project debian-cloud --tags http-server --metadata-from-file startup-script=./startup.sh

export SERVER_API=`gcloud compute instances list --filter="name=amicabet-server" --format="value(EXTERNAL_IP)"`


docker build -t taraszhere/amicabet --build-arg api_ip=${SERVER_API} .
docker push taraszhere/amicabet

gcloud container clusters create amicabet-cluster
kubectl create deployment amica --image=taraszhere/amicabet 
kubectl expose deployment amica --name=amica-service --type="LoadBalancer" --port 80 --target-port 80

kubectl get service amica