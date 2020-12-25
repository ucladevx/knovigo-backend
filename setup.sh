#!/bin/sh

apt-get -y update && apt-get -y upgrade
apt-get -y install cron

pip install -r requirements.txt