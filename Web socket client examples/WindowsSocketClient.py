#import threading
import websocket # pip install websocket-client


def connect():
    global ws
    ws = websocket.WebSocket()
    #ws.connect("ws://172.16.0.212/python")
    ws.connect("ws://172.16.0.180/webserial")
    print(ws)
    ws.send("python connected")


connect()

            
def rcv(ws):
    msgRecv = ''
    while True:
        msgRecv = ws.recv()
        if msgRecv != '':
            print(msgRecv)
            msgRecv=''
            ws.send("Ack")

if __name__ == "__main__":
    try:
        rcv(ws)
    except:
        connect()
        
