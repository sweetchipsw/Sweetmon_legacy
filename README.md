# SWEETMON
'SWEETMON' is a fuzzer monitoring service based python3 + django. User can check their fuzzers and crashes on the web. It can reduce repetitive work for fuzz testers.



## What is this?

Sweetmon provides several useful things for monitoring fuzzers and crashes.

- Monitoring
  - Fuzzers
    - IP, Fuzzer Name, Status
    - Number of crashes
- Monitoring Crashes
  - First / Last reported time
  - Number of (duplicated) crashes
  - Generate One-Time-URL to download crash.
  - Crash Logs
  - Crash informations (Name, Machine, Summary, Debug log, size)
  - Notification (Via Telegram, Email)
- Up/Download Fuzzer and Testcase
  - Generate One-Time-URL to download fuzzer or testcase.
- Reports
  - Memo
- Support multiple user



## Screenshots

1. Showing all of fuzzers
2. Providing crash information
3. Users can upload their fuzzer and testcases.
4. Supports multiple users.



## Installation (Server)

#### Easy Installation

* Environment
  * Ubuntu 16.04.3 LTS (Server, Clean vm)

1. Install Ubuntu.

2. Download the installer and execute it.

   ```sh
   wget https://raw.githubusercontent.com/sweetchipsw/sweetmon/master/install.sh -O install.sh && bash install.sh
   ```

3. Done!



#### Manual Installation

- Environment
  - Ubuntu 16.04.2 LTS (Server)

1. Install python3 + apache2 + virtualenv and sweetmon

   ```shell
   sudo apt install python3 python3-pip
   sudo apt install apache2
   sudo apt install virtualenv
   git clone https://github.com/sweetchipsw/sweetmon.git
   ```

2. Set virtualenv

   1. Install && Activate virtualenv.

      ```sh
      sudo apt-get install virtualenv
      virtualenv -p python3 sweetmon_venv
      . sweetmon_venv/bin/activate
      ```

   2. Install django + dependencies.

      ```sh
      sudo pip3 install django
      sudo pip3 install requests
      sudo pip3 install pycrypto
      ```

   3. Make configuration file

      ```sh
      sudo vim /etc/apache2/sites-available/sweetmon.conf
      ```

   4. Paste and modify under contents

      ```
      <VirtualHost *:80>
          WSGIScriptAlias / /home/sweetchip/sweetmon/sweetmon/wsgi.py
          WSGIDaemonProcess sweetmon python-path=/home/sweetchip/sweetmon/ python-home=/home/sweetchip/test_env/lib/python3.5/site-packages
          WSGIProcessGroup sweetmon
          
          ServerName dev.sweetchip.kr
          ServerAlias dev.sweetchip.kr
          ServerAdmin sweetchip@sweetchip.kr

          DocumentRoot /home/sweetchip/sweetmon/

          ErrorLog /var/log/apache2/sweetmon_error.log
          CustomLog /var/log/apache2/sweetmon_custom.log combined

          Alias /robots.txt /home/sweetchip/sweetmon/static/robots.txt
          Alias /assets/admin /home/sweetchip/test_env/lib/python3.5/site-packages/django/contrib/admin/static/admin
          Alias /assets /home/sweetchip/sweetmon/static/
          <Directory /home/sweetchip/sweetmon/>
              Require all granted
          </Directory>

          <Directory /home/sweetchip/sweetmon/sweetmon/ >
          <Files wsgi.py>
              Require all granted
          </Files>
          </Directory>

          <Directory /home/sweetchip/test_env/lib/python3.5/site-packages/django/contrib/admin/static/admin/ >
              Require all granted
          </Directory>
      </VirtualHost>
      ```

   5. Restart apache2 server

      ```sh
      sudo service apache2 restart
      ```

3. (Optional, but highly recommended) Apply SSL certificate.

   1. Install Letsencrypt

      ```sh
      sudo apt install letsencrypt
      ```

   2. a

   3. a

   4. a

   5. a

4. Generate superuser

   ``` sh
   python manage.py createsuperuser
   ```

5. Done!

   1. Now you can use sweetmon-client.

#### For windows, OS X

* Not tested on these OS. But it will works.



## After Install

#### Change Secret key in settings.py





# WIKI

Please check [this] page.

# PS

1. Pull Requests are always welcome!
2. Please create Issue or send me an email to me if you have any questions or requests.



