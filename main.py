import client
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

                        if len(server.emotions["scan"]) == 0 : 
                            server.emotions["scan"].append("Degout")
                            server.emotions["scan"].append("Joie")
                        if len(server.emotions["cinema"]) == 0 :
                            server.emotions["cinema"].append("Joy")
                            server.emotions["cinema"].append("Fear")
                            server.emotions["cinema"].append("Sadness")
                        
                        prompt_robotic = ia_manager.generate_prompt(server.emotions, "robotic")
                        prompt_human = ia_manager.generate_prompt(server.emotions, "human")

                        generated_text_robot = ia_manager.generate_text(prompt_robotic, max_tokens=500)
                        generated_text_human = ia_manager.generate_text(prompt_human, max_tokens = 500)

                        message = messageManager.create_message("call_apis", robotic_text = generated_text_robot, human_text = generated_text_human)
                        print(message)
                        server.send_message_to_all(message)

                time.sleep(1)

    except KeyboardInterrupt:
        print("Mesure arrêtée par l'utilisateur")
        GPIO.cleanup()



if __name__ == "__main__":
    main()