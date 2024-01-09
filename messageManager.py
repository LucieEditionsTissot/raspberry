import json
import time
from datetime import datetime


class MessageManager:
    def __init__(self):
        self.messageId = 0

    def create_message(self, action):
        self.messageId += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        messageToSend = {
            "id": "server",
            "data":{
                "timestamp": timestamp,
                "action": action
            }
        }
        return json.dumps(messageToSend)

    def get_message(self, json_message):
        try:
            message = json.loads(json_message)
            return message
        except json.JSONDecodeError:
            print("Erreur lors de l'analyse du message JSON")
            return None