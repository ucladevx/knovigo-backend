#!/bin/sh

apt-get -y update && apt-get -y upgrade
apt-get -y install cron
apt-get -y install gdal-bin

pip install -r requirements.txt