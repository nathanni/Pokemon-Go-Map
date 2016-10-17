# Pokemon-Go-Map
Pokémon Map Service which collects real-time info of Pokémon, Stops, and Gyms periodically.

# Two submodules
  nathanni/pgoapi under main project<br />
  nathanni/mock_pgoapi under pgoapi<br />
  
  remember to install submodule using following commands after clone<br />
  $ git submodule init<br />
  $ git submodule update
  
  or install all submodules recursively during clone process<br />
  $ git clone --recursive https://github.com/nathanni/Pokemon-Go-Map.git
  
  
# pgoapi environment set up (Ubuntu as example)
  1. essential tool<br />
      $ sudo apt-get install python-setuptools python-pip build-essential python-dev -y
  2. pip libs<br />
      (may need to install requests individually) $ sudo pip install requests <br />
      $ cd pgpapi -> $ sudo pip install -I -r requirements.txt --force-reinstall 
  3. tor proxy<br />
      $ sudo apt-get install tor -y<br />
      $ sudo service tor start
  4. install pgoapi<br />
      $ sudo python setup.py install
      
# Set up pgoapi
  1. pgoapi uses mock_pgoapi as default. If you want to connect to Pokemon's real server instead, please do followings:
    1. $ vi pgoapi/pokecli.py
    2. comment line 40: from mock_pgoapi import mock_pgoapi as pgoapi
    3. enable line 41: from pgoapi import pgoapi
      
# Refresh Tor Proxy
  1. $ sudo service tor restart
  2. $ ./pgoapi/refresh_ip.sh

  
