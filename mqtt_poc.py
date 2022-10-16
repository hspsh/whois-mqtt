from flask import Flask, request
from flask_mqtt import Mqtt
import json

app = Flask(__name__)
app.config.from_envvar('SECRETS_FILE')

try:
    mqtt = Mqtt(app)
except ConnectionRefusedError:
    print("error connecting to mqtt broker. Check your secrets.conf file")
    exit(1)

vendor_macs = {"00:00:00":"invalid"}

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Mqtt connected")
    mqtt.publish('whois-test', 'just upped!')

@app.route('/')
def index():
    return "http-to-mqtt bridge. Use post."

@app.route('/', defaults={'path': ''},methods = ['POST'])
@app.route('/<path:path>',methods = ['POST'])
def login(path:str):
    dev_list = json.loads(request.form['data'])
    for d in dev_list:
        # print (d)
        if len(d['name']) > 0:
            readable_name = d['name']
        else:
            readable_name = "Unknown"

        mqtt.publish(f"whois-test2/{d['mac']}", readable_name)
        mqtt.publish(f"whois-test2/{d['mac']}/name", d['name'])
        mqtt.publish(f"whois-test2/{d['mac']}/IP", d['addr'])
        mqtt.publish(f"whois-test2/{d['mac']}/mac", d['mac'])
        mqtt.publish(f"whois-test2/{d['mac']}/last", d['last'])
        mqtt.publish(f"whois-test2/{d['mac']}/status", d['status'])

        try:
            vendor = vendor_macs[d['mac'][:8]]
        except KeyError:
            vendor = "Unknown"

        mqtt.publish(f"whois-test2/{d['mac']}/vendor", vendor)
    return "OK"


if __name__ == "__main__":
    try:
        with open(app.config['VENDORS_JSON'], encoding = 'utf-8') as f:
            vendor_macs_massive_json = json.load(f)
            vendor_macs = {m["macPrefix"]: m["vendorName"] for m in vendor_macs_massive_json}
    except FileNotFoundError:
        print("mac lookup json not found. Vendor names will not be resolved")

    app.run(host = app.config['FLASK_RUN_HOST'],port = app.config['FLASK_RUN_PORT'])