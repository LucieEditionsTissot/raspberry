import RPi.GPIO as GPIO
from ultrasonicSensor import UltrasonicSensor
import time
from ledManager import LedManager
from messageManager import MessageManager
from generativeIaManager import GenerativeIAManager

# Initialisation des GPIO
GPIO.setmode(GPIO.BCM)

# Créer un tableau de capteurs
sensors = [
    UltrasonicSensor(26, 19),
    UltrasonicSensor(13, 6),
    UltrasonicSensor(21, 20),
    UltrasonicSensor(16, 12)
]

messageManager = MessageManager()
ia_manager = GenerativeIAManager()

led = LedManager(10, 3)
led.set_strip_color([0,0,0])


try:
    while True:
        distances = [sensor.distance() for sensor in sensors]
        
        for i, dist in enumerate(distances):

            if all(dist < 10.0 for dist in distances):
                print("Alerte: Tous les objets sont trop proches !")
                
                generated_text = ia_manager.generate_text("Petit test")

                print(generated_text)

                led.light_up_gradually([120, 120, 120])

        time.sleep(1)

except KeyboardInterrupt:
    print("Mesure arrêtée par l'utilisateur")
    GPIO.cleanup()
