import websocket
import threading
import time
import json
from datetime import datetime

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")

def on_open(ws):
    def run(*args):
        for i in range(2):

            message_dict = {
                "id": "micro",
                "data": {
                    "timeStamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "message": "connected"
                }
            }

            json_string = json.dumps(message_dict)
            ws.send(json_string)
        ws.close()
    thread = threading.Thread(target=run)
    thread.start()

if __name__ == "__main__":
    websocket.enableTrace(True)
    host = "ws://localhost:8080"  # Assurez-vous que ceci correspond à l'adresse de votre serveur
    ws = websocket.WebSocketApp(host,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
