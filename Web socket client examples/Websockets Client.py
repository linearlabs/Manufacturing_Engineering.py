import websocket

ws = websocket.WebSocket()
ws.connect("ws://172.16.8.42/test")

ws.sendAll("hi")

ws.close()
