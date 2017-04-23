# SWEETMON
An universal fuzzing  monitoring framework for fuzzers based python+django.

Sweetmon is a framework to monitor fuzzers and crashes developed by sweetchip.

This project provides several functions to gather, 

You should use sweetmon-client to interact with server. Please check sweetmon-client project at here.



## Screenshots

1. Showing all of fuzzers
2. Providing crash information
3. Users can upload their fuzzer and testcases.
4. Supports multiple users.

## Installation

- Environment
  - Ubuntu 16.04.2 LTS (Server)
  - Python3
  - Django 1.11

1. Install python + django + apache2

   ```shell
   sudo apt-get install python3
   sudo apt-get install apache2
   sudo pip install django
   ```

2. Set wsgi

3. (Optional, but highly recommended) Make your server secure.

   1. Apply SSL (Using letsencrypt, free SSL and easy installation)

4. Generate superuser

   ``` sh
   python manage.py createsuperuser
   ```

   ​

5. Install sweetmon-client

# WIKI

Please check this page.



# Function

Sweetmon provides several functions for monitoring fuzzers and crashes.

* Monitoring Fuzzer
  * Fuzzer
    * Number of crashes
  * Machine
  * ​
* Monitoring Crashes
  * First / Last reported time
  * Number of (duplicated) crashes
  * Support generating One-Time-URL to download crash.
  * Logging
  * Crash informations(Name, Machine, Summary, Debug log, size)
* Hosting Fuzzer and Testcase
  * Support generating One-Time-URL to download fuzzer or testcase.
* Reports
  * ​

# Directory
- sweetmon : Monitor system (Django)
- ​




# PS

1. I'm waiting for your pull requests thank you.
2. Please create Issue if you have any questions or requests.
3. Please check the http://blog.sweetchip.kr/408 



