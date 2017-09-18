# SWEETMON
'SWEETMON' is a fuzzer monitoring service based python3 + django. User can check their fuzzers and crashes on the web. It can reduce repetitive work for fuzz testers.

## What is this?

Sweetmon provides several useful things for monitoring fuzzers and crashes.

- Monitoring
  - Fuzzers
    - IP, fuzzer name, status
    - Number of crashes
- Monitoring Crashes
  - First or last reported time
  - Number of (duplicated) crashes
  - Generate one-time-url to download crash.
  - Crash logs
  - Crash informations (name, machine, summary, debug log, size)
  - Notification (via Telegram or email)
- Up/download fuzzer and testcase
  - Host testcase or fuzzer file
- Issue
- Support multiple user



## Screenshots

1. Initial screen

   ![https://user-images.githubusercontent.com/14085555/30513140-24c99316-9b39-11e7-8218-ddd6860afa13.png](https://user-images.githubusercontent.com/14085555/30513140-24c99316-9b39-11e7-8218-ddd6860afa13.png)

2. User Profile

   ![](https://user-images.githubusercontent.com/14085555/30513141-24ca4554-9b39-11e7-83c3-8a821f2d90ef.png)

3. Fuzzer list

   ![](https://user-images.githubusercontent.com/14085555/30513145-24cee578-9b39-11e7-950d-ec270335105a.png)

4. Fuzzer information

   ![](https://user-images.githubusercontent.com/14085555/30513144-24cd1dec-9b39-11e7-95b1-e4e8c66045af.png)

5. Crash list

   ![](https://user-images.githubusercontent.com/14085555/30513142-24cbe08a-9b39-11e7-8a47-475f441b2e53.png)

6. Crash details

   ![](https://user-images.githubusercontent.com/14085555/30513143-24cc88a0-9b39-11e7-9df7-3884de362875.png)

7. Crash details (2)

   ![](https://user-images.githubusercontent.com/14085555/30513146-24edce52-9b39-11e7-99a0-f457cb32318a.png)

8. Testcase & Fuzzer list

   ![](https://user-images.githubusercontent.com/14085555/30513147-24ef89e0-9b39-11e7-8916-9101de7f2cb2.png)

9. Testcase & Fuzzer details

   ![](https://user-images.githubusercontent.com/14085555/30513148-24ef9ffc-9b39-11e7-8e75-e9e223de96c0.png)

10. Issue list

    ![](https://user-images.githubusercontent.com/14085555/30513150-24f368e4-9b39-11e7-886f-7fcafddd5b8b.png)

11. Issue Details

    ![](https://user-images.githubusercontent.com/14085555/30513149-24f31ce0-9b39-11e7-9351-faaa42d02533.png)

12. Statistics

    ![](https://user-images.githubusercontent.com/14085555/30513151-24f3c712-9b39-11e7-9b1a-5345faa7a86c.png)



## Installation (Server)

#### Easy Installation (Recommended, For linux)

* Environment
  * Ubuntu 16.04.3 LTS (Server, Clean vm)

1. Install Ubuntu.

2. Download the installer

   ```sh
   wget https://raw.githubusercontent.com/sweetchipsw/sweetmon/master/install.sh -O install.sh
   ```

3. Set '**DOMAIN**' on install.sh

   ```sh
   #!/bin/bash
   # SWEETMON Installer
   ###
   # Modify under contents
   ###
   DOMAIN='' # domain.com || 192.168.123.123
   EMAIL='admin@domain.com'
   ```

4. Run installer.

   ```sh
   bash install.sh
   ```

5. Done!



#### Manual Installation (For linux)

- Environment
  - Ubuntu 16.04.2 LTS (Server)

1. Install python3 + apache2 + virtualenv and sweetmon

   ```shell
   sudo apt install python3 python3-pip
   sudo apt install apache2
   sudo apt install virtualenv
   git clone https://github.com/sweetchipsw/sweetmon.git
   ```
2. Update your server and Install dependencies

   ```sh
   sudo apt update
   sudo apt upgrade -y
   sudo apt install -y python3 python3-pip apache2 virtualenv libapache2-mod-wsgi-py3 letsencrypt git
   ```

3. Clone sweetmon project & Set env

   ```sh
   git clone https://github.com/sweetchipsw/sweetmon.git
   export LOCATION=`pwd`
   export VENV='sweetmon_venv'
   ```

4. Install && Activate virtualenv.

   ```sh
   virtualenv -p python3 sweetmon_venv
   . sweetmon_venv/bin/activate
   ```

5. Install django + dependencies.

   ```sh
   sudo pip3 install -r requirements.txt
   ```

6. Make configuration file

   ```sh
   sudo vim /etc/apache2/sites-available/sweetmon.conf
   ```

7. Paste under contents.

   ```
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
   ```

8. Restart apache2 server

   ```sh
   sudo a2ensite sweetmon
   sudo service apache2 restart
   ```

9. Migrate DB / Set permission / Create super admin

   ```sh
   cd $LOCATION/sweetmon
   python3 manage.py makemigrations
   python3 manage.py migrate
   sudo chown www-data:www-data ./ -R
   python manage.py createsuperuser
   ```

10. Done.



#### Install SSL certificate on Apache2. (Optional, But highly recommended)

* Not completed yet

1. Install Letsencrypt

   ```sh
   sudo apt install letsencrypt
   ```

2. Check your port-forwarding status.

   1. 80 (http)
   2. 443 (https)

3. Generate SSL Certificate

   ```sh
   sudo letsencrypt certonly -a standalone -d domain.com
   ```

4. Make configuration file for https.

   ```

   ```

5. Enable SSL & Restart apache2 server

   ```sh

   ```

6. Done!


#### For windows, OS X

* Not tested on these OS. But it will works.




## After Install

#### 1. Change Secret key in settings.py (/sweetmon/settings.py)

* **To make your server secure, you should change SECRET_KEY.**

```python
# SECURITY WARNING: keep the secret key used in production secret!
# - Please Change this key before install on server.
# SECRET_KEY = 'y3r$r7#g(g_6xt!q35ct=6sqt0kiihqe2vc#k%bktayz@vok2v'
SECRET_KEY = '....'
```

* Generate '**new**' SECRET_KEY

```python
import random
print(''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)))

# '(vj1g8ps3a7li%g%go6uno4!n(9dfegsj7mvbicy$vv&c#!ak4'
```



#### 2. You should use sweetmon-client to interact with sweetmon

- Check https://github.com/sweetchipsw/sweetmon_client



# PS

1. Pull Requests are always welcome!
2. Please create Issue or send me an email to me if you have any questions or requests.



# ETC

* Template : Dashgum by [Alvarez.is](http://www.alvarez.is/) / You can find it [here](http://blacktie.co/2014/07/dashgum-free-dashboard/).
* Donation
  * Bitcoin : 1M7usjq5PNz7vjWz1oyyzj2VHwKC6EmSsi
  * Ethereum : 0x93357b84488DDC8D52e2C6E51dF745B026F95B71