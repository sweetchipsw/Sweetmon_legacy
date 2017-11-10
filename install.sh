#!/bin/bash
# SWEETMON Installer
###
# Modify under contents
###
DOMAIN='' # domain.com || 192.168.123.123
EMAIL='admin@domain.com'

##################################
LOCATION=`pwd`
VENV='sweetmon_venv'
##################################


if [ -z "$DOMAIN" ]; then
    echo "[?] THE DOMAIN VARIABLE IS EMPTY!!"
    exit 0
fi


echo "[*] == SWEETMON INSTALLER =="
echo "[ ] The installer will automatically start in 3 seconds."
sleep 3

# Update + Install essential software
echo "[*] Update system and install dependencies"
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip apache2 virtualenv libapache2-mod-wsgi-py3 letsencrypt git

# Download sweetmon from git repository
echo "[*] Clone sweetmon from git repository."
git clone https://github.com/sweetchipsw/sweetmon.git

# Set venv
echo "[*] Making virtualenv environment."
virtualenv -p python3 $VENV
PIP3=$LOCATION/$VENV/bin/pip3
PYTHON3=$LOCATION/$VENV/bin/python3

# Install dependencies for sweetmon
echo "[*] Install essential packages."
$PIP3 install -r requirements.txt

echo "[*] Generate apache2 settings."
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
echo "[*] Install setting"
sudo cp /tmp/sweetmon_temp.conf /etc/apache2/sites-available/sweetmon.conf
sudo a2ensite sweetmon
sudo service apache2 restart

# Add Allowed Host.
sudo echo "ALLOWED_HOSTS += ['$DOMAIN']" >> $LOCATION/sweetmon/sweetmon/settings.py

echo "[*] Cleaning.."
rm /tmp/sweetmon_temp.conf

echo "[*] Initialize sweetmon."
cd $LOCATION/sweetmon
$PYTHON3 manage.py makemigrations
$PYTHON3 manage.py migrate

echo "[*] Generate superuser."
$PYTHON3 manage.py createsuperuser

echo "[*] Initialize file permissions."
sudo chown www-data:www-data ./ -R

echo "[!] Finish! Connect to $DOMAIN on your browser!"
echo "[ ] Next Step : Apply SSL certificate on Apache2 server. (Optional)"
