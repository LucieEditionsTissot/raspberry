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
                        
                        
                        server.emotions["scan"].append("Degout")
                        server.emotions["scan"].append("Joie")
                        
                        prompt = (
                            "Tu vas jouer le rôle d'une intelligence artificielle scientifique qui est là pour expliquer le rôle des sens dans le ressenti des émotions. Tu parleras des hormones. "
                            "Tu intégreras dans cette explication des exemples sur :\n"
                            f"- le cinéma (quand on voit une scène et qu'on ressent les émotions suivantes {server.emotions['cinema'][0]} ou {server.emotions['cinema'][1]}.\n"
                            f"- Le toucher quand on ressent {server.emotions['scan'][0]} \n"
                            f"- L'odorat quand on sent une odeur qu'on aime bien comme le café et qu'on ressent de la {server.emotions['scan'][1]} "
                            "Commence ta réponse par : \"Émotion en cours de chargement...\" comme si tu ingérais des infos puis un décompte \"3... 2... 1..."
                        )

                        print(prompt)

                        generated_text = ia_manager.generate_text(prompt, max_tokens=500)

                        print(generated_text)
                        message = messageManager.create_message("call_api_robotic", message = generated_text)
                        server.send_message_to_all(message)

                time.sleep(1)

    except KeyboardInterrupt:
        print("Mesure arrêtée par l'utilisateur")
        GPIO.cleanup()



if __name__ == "__main__":
    main()