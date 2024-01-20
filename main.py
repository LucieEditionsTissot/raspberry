import json
from messageManager import MessageManager
import threading
from server import ServerManager
from apiManager import app
import RPi.GPIO as GPIO
from ultrasonicSensor import UltrasonicSensor
import time
from ledManager import LedManager
from generativeIaManager import GenerativeIAManager





def main():
    port = 8080
    server = ServerManager(port)
    messageManager = MessageManager()
    ia_manager = GenerativeIAManager()

    print(f"Running server on port {port}")

    try:
        server.run()
    except KeyboardInterrupt:
        print("Server stopped by user")

         



if __name__ == "__main__":
    main()