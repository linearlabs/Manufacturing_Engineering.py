import websocket

ws = websocket.WebSocket()
ws.connect("ws://172.16.0.180/webserial")

ws.sendAll("hi")

ws.close()
