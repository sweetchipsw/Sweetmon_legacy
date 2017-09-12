#!/usr/bin/env bash
#/bin/bash

###
# Shell Script
###

###
# FILL UNDER VARIABLES
###
DOMAIN='domain.com'
EMAIL='admin@domain.com'
LOCATION=`pwd`
VENV='sweetmon_venv'

###
# ADVANCED SETTINGS
###

# Use SSL Certificate (Using letsencrypt)
USE_SSL_SERVER=0

###
#
###
echo "[*] == SWEETMON INSTALLER =="
echo "[ ] NOTE THAT : Please run this script with 'BASH' PLEASE "
# sleep 3

# echo "[*] Checking privillege.."
# if [[ $(id -u) -ne 0 ]] ; then echo "[-] Please run with sudo" ; exit 1 ; fi

# Update + Install essential software
echo "[*] Updating system and install dependencies"
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip apache2 virtualenv libapache2-mod-wsgi-py3 letsencrypt git

# Download sweetmon from git repository
echo "[*] Cloneing sweetmon from repository"
git clone https://github.com/sweetchipsw/sweetmon.git

# Set venv
echo "[*] Making virtualenv environment"
virtualenv -p python3 $VENV
PIP3=$LOCATION/$VENV/bin/pip3
PYTHON3=$LOCATION/$VENV/bin/python3

# Install dependencies for sweetmon
echo "[*] Installing essential packages"
sudo $PIP3 install django
sudo $PIP3 install requests
sudo $PIP3 install pycrypto


echo "[*] Generating apache2 settings.."
cat > /tmp/sweetmon_temp.conf <<EOF
<VirtualHost *:80>
    WSGIScriptAlias / $LOCATION/sweetmon/sweetmon/wsgi.py
    WSGIDaemonProcess sweetmon python-path=$LOCATION/sweetmon/ python-home=$LOCATION/$VENV/lib/python3.5/site-packages
    WSGIProcessGroup sweetmon

    ServerName $DOMAIN
    ServerAlias $DOMAIN
    ServerAdmin $EMAIL

    DocumentRoot $LOCATION/sweetmon/

    ErrorLog /var/log/apache2/sweetmon_error.log
    CustomLog /var/log/apache2/sweetmon_custom.log combined

    Alias /robots.txt $LOCATION/sweetmon/static/robots.txt
    Alias /assets/admin $LOCATION/$VENV/lib/python3.5/site-packages/django/contrib/admin/static/admin
    Alias /assets $LOCATION/sweetmon/static/
    <Directory $LOCATION/sweetmon/>
        Require all granted
    </Directory>

    <Directory $LOCATION/sweetmon/sweetmon/ >
    <Files wsgi.py>
        Require all granted
    </Files>
    </Directory>

    <Directory $LOCATION/$VENV/lib/python3.5/site-packages/django/contrib/admin/static/admin/ >
        Require all granted
    </Directory>
</VirtualHost>
EOF

# Move sweetmon to apache2
echo "[*] Installing setting.."
sudo cp /tmp/sweetmon_temp.conf /etc/apache2/sites-available/sweetmon.conf
sudo a2ensite sweetmon
sudo service apache2 restart

# Add Allowed Host.
sudo echo "ALLOWED_HOSTS += ['$DOMAIN']" >> $LOCATION/sweetmon/sweetmon/settings.py

echo "[*] Cleaning.."
rm /tmp/sweetmon_temp.conf

echo "[*] Setting sweetmon"
cd $LOCATION/sweetmon
$PYTHON3 manage.py makemigrations
$PYTHON3 manage.py migrate
$PYTHON3 manage.py createsuperuser

echo "[*] Change DB permission"
sudo chown :www-data ./ -R