import client
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
 
    GPIO.setmode(GPIO.BCM)

    # Créer un tableau de capteurs
    sensors = [
        UltrasonicSensor(26, 19),
        UltrasonicSensor(13, 6),
        UltrasonicSensor(21, 20),
        UltrasonicSensor(16, 12)
    ]

    messageManager = MessageManager()
    spheroDetected = False


    led = LedManager(10, 20)
    led.set_strip_color([0,0,0])
    ia_manager = GenerativeIAManager()

    print(f"Running server on port {port}")

    server_thread = threading.Thread(target=server.run)
    server_thread.start()

    try:
        while True:
            if not spheroDetected :
                distances = [sensor.distance() for sensor in sensors]
                
                for i, dist in enumerate(distances):

                    if all(dist < 10.0 for dist in distances) and not spheroDetected:
                        spheroDetected = True
                        print("Alerte: Tous les objets sont trop proches !")
                        
                        generated_text = ia_manager.generate_text("Petit test")

                        print(generated_text)
                        message = messageManager.create_message("call_api")
                        server.send_message_to_all(message)

                        led.set_strip_color([120, 120, 120])

                time.sleep(1)

    except KeyboardInterrupt:
        print("Mesure arrêtée par l'utilisateur")
        GPIO.cleanup()



if __name__ == "__main__":
    main()