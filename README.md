# Pokemon-Go-Map
Pokémon Map Service which collects real-time info of Pokémon, Stops, and Gyms periodically.

# Two submodules
  1. nathanni/pgoapi under main project
  2. nathanni/mock_pgoapi under pgoapi
  
  remember to install submodule using following commands after clone
  $ git submodule init
  $ git submodule update
  
  or install all submodules recursively during clone process
  $ git clone --recursive https://github.com/nathanni/Pokemon-Go-Map.git
  
  
# pgoapi environment set up (Ubuntu as example)
  1. essential tool
      $ sudo apt-get install python-setuptools python-pip build-essential python-dev -y
  2. pip libs
      $ cd pgpapi -> $ sudo pip install -I -r requirements.txt --force-reinstall 
  3. tor proxy
      $ sudo apt-get install tor -y  
      $ sudo service tor start
  4. install pgoapi
      $ sudo python setup.py install
      
# Set up pgoapi
  1. pgoapi uses mock_pgoapi as default. If you want to connect to Pokemon's real server instead, please do followings:
      a. $ vi pgoapi/pokecli.py
      b. comment line 40: from mock_pgoapi import mock_pgoapi as pgoapi
      c. enable line 41: from pgoapi import pgoapi
      
# Refresh Tor Proxy
  1. $ sudo service tor restart
  2. $ ./pgoapi/refresh_ip.sh

  
