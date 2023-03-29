from ws4py.client.threadedclient import WebSocketClient
import time, requests

esp8266host = "ws://172.16.0.218/webserial"

class DummyClient(WebSocketClient):
    def opened(self):
        print("Websocket open")
    def closed(self, code, reason=None):
        print ("Connexion closed down", code, reason)
    def received_message(self, m):
        print (m)

if __name__ == '__main__':
    try:
        ws = DummyClient(esp8266host)
        ws.connect()
        print("Ready !")
        
        i = 0
        while True:
          print(ws.recv().decode())

      
        ws.send("ON")
        #ws.close()
        #exit()

    except KeyboardInterrupt:
        ws.close()
