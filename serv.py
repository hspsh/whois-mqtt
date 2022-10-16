from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import paho.mqtt.client as mqtt

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Hello, World! Here is a GET response"
        self.wfile.write(bytes(message, "utf8"))
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        
        print(self.headers)

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data_json = json.loads(post_data[5:])
        
        for dev in data_json:
            print(dev['name'])


        message = "Hello, World! Here is a POST response"
        self.wfile.write(bytes(message, "utf8"))

with HTTPServer(('', 1488), handler) as server:
    server.serve_forever()
