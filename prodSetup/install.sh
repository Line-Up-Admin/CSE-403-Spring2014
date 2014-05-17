#!/bin/bash

# Packaged software to install
prod_apps=(

rsync
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
  # Install each software package one with default 'yes' flag
  for app in "${dev_apps[@]}"; do
    apt-get install $app -y
  done
else
  if [ "$1" = "prod" ]; then
    # Install each software package one with default 'yes' flag
    for app in "${prod_apps[@]}"; do
      apt-get install $app -y
    done
  else
        echo "Usage: ./install <dev or prod>"
        exit
  fi
fi

# Install pip (python package index)
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
rm get-pip.py

# Install flask framework
pip install flask

git clone https://github.com/Line-Up-Admin/CSE-403-Spring2014.git -b beta_release lineup

if [ "$1" = "prod" ]; then
  # move configuration file into place
  cp lineup/prodSetup/lineup.conf /etc/apache2/sites-enabled/

  # remove the default configuaration file
  rm /etc/apache2/sites-enabled/000-default.conf
  mkdir /var/www/lineup
  mkdir /var/www/lineup/app
  rsync -r lineup/app /var/www/lineup/
  rsync lineup/README.md /var/www/lineup/
  rsync lineup/lineup.wsgi /var/www/lineup/
  rm -rf lineup

  # set permissions for apache "user"
  chown www-data /var/www/lineup/app/
  service apache2 restart
fi
