# Whois - mqtt bridge

This script cooperates with another one running on mikrotik. 

Mikrotik pushes DHCP lease data in regular intervals, via POST requests. This script acts as a server for these POST requests.

It then pushes that data to MQTT broker.

in example_request.json we can see the data from mikrotik format

Todo:
* move secrets to doppler
* tests (we have example json)
* ???


Mac lookup json file can be downloaded from maclookup.app
