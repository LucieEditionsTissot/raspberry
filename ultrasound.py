import websocket
import threading
import time
from ultrasonicSensor import UltrasonicSensor
from messageManager import MessageManager
import RPi.GPIO as GPIO

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")

class UltrasonicClient:
    def __init__(self, host):
        GPIO.setmode(GPIO.BCM)
        self.ws = websocket.WebSocketApp(host,
                                         on_open=self.on_open,
                                         on_message=on_message,
                                         on_error=on_error,
                                         on_close=on_close)
        self.sensors = [
            UltrasonicSensor(26, 19),
            UltrasonicSensor(13, 6),
            UltrasonicSensor(21, 20),
            UltrasonicSensor(16, 12)
        ]
        self.messageManager = MessageManager()

    def on_open(self, ws):
        print("### Connection opened ###")

    def run(self):
        thread = threading.Thread(target=self.ws.run_forever)
        thread.start()
        try:
            while True:
                distances = [sensor.distance() for sensor in self.sensors]
                if all(dist < 10.0 for dist in distances):
                    print("Alerte: Tous les objets sont trop proches !")
                    self.send_message("objects_detected")
                time.sleep(1)
        except KeyboardInterrupt:
            print("Mesure arrêtée par l'utilisateur")
            self.ws.close()

    def send_message(self, message_content):
        message = self.messageManager.create_message(action="collision", message=message_content, id="ultraSoundSensor")
        self.ws.send(message)

if __name__ == "__main__":
    host = "ws://localhost:8080"
    client = UltrasonicClient(host)
    client.run()
