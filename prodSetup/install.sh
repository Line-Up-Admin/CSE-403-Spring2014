#!/bin/bash

# Packaged software to install
prod_apps=(
 
apache2
libapache2-mod-wsgi
sqlite3
python2.7
git
 
)

dev_apps=(

sqlite3
python2.7
git
 
)

if [ "$1"  = "dev" ]; then
  apps = dev_apps
else
  if [ "$1" = "prod" ]; then
    apps = prod_apps
  else
  	echo "Usage: ./install <dev or prod>"
  	exit
  fi
fi

# Install each software package one with default 'yes' flag
for app in "${apps[@]}"; do
  apt-get install $app -y
done

# Install pip (python package index)
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py

# Install flask framework
pip install flask

# move configuration file into place
cp lineup.config /etc/apache2/sites-enabled/

#remove the default configuaration file
rm /etc/apache2/sites-enabled/000-default.conf


