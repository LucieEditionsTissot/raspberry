# server.py
from websocket_server import WebsocketServer
from messageManager import MessageManager
from generativeIaManager import GenerativeIAManager

class ServerManager:
    def __init__(self, port):
        self.server = WebsocketServer(port=port, host='0.0.0.0')
        self.messageManager = MessageManager()
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.emotions = {"cinema": [], "scan": []}
        self.micro_message_received = 0
        self.scan_message_received = 0

    def new_client(self, client, server):
        print(f"New client {client['id']} connected")

    def client_left(self, client, server):
        print(f"Client {client['id']} disconnected")

    def message_received(self, client, server, message):
        #print(f"Message received from {client['id']}: {message}")

        jsonMessage= self.messageManager.get_message(message)

        if jsonMessage : 
            sender = jsonMessage.get("id")

            if sender == "sphero":
                print("message sphero recu")
                self.handle_sphero_messages(client, jsonMessage)
            elif sender == "micro" :
                self.handle_micro_messages(client, jsonMessage)
            elif sender == "scan" :
                self.handle_scan_messages(client, jsonMessage)
            elif sender == "ultraSoundSensor" :
                self.handle_sensor_messages(client, jsonMessage)
            else:
                self.default_message_handler(client, jsonMessage)

        print(jsonMessage)



    def run(self):
        self.server.run_forever()

    def send_message(self, client_id, message):
        client = next((c for c in self.server.clients if c['id'] == client_id), None)
        if client is not None:
            self.server.send_message(client, message)


    def send_message_to_all(self, message):
        for client in self.server.clients:
            self.server.send_message(client, message)

    def handle_sphero_messages(self, client, message):
        if message["data"]["action"] == "tap_detected" :
            message_to_send = self.messageManager.create_message("play_human_sound")
            self.send_message_to_all(message_to_send)
        print("sphero message")

    def handle_micro_messages(self, client, message):
        self.micro_message_received += 1
        print("message compteur :"+ str(self.micro_message_received))
        
        self.emotions["cinema"].append(message["data"]["emotions"])


        if self.micro_message_received == 3: 
            message_to_send = self.messageManager.create_message("turn_led_on")

            print(message_to_send)
            self.send_message_to_all(message_to_send)

    def handle_scan_messages(self, client, message):
        self.scan_message_received += 1

        self.emotions["scan"].append(message["data"]["emotions"])

        if self.scan_message_received == 2 : 
            message = self.messageManager.create_message("turn_led_on2")
            self.send_message_to_all(message)


        print("scan recu")

    def handle_sensor_messages(self, client, message):
        action = message["data"].get("action")
        if action == "collision":
            print("Alerte: Tous les objets sont trop proches !")

            # Générer les émotions et les prompts si nécessaire
            if len(self.emotions["scan"]) == 0: 
                self.emotions["scan"].append("Degout")
                self.emotions["scan"].append("Joie")
            if len(self.emotions["cinema"]) == 0:
                self.emotions["cinema"].append("Joy")
                self.emotions["cinema"].append("Fear")
                self.emotions["cinema"].append("Sadness")

            ia_manager = GenerativeIAManager()
            prompt_robotic = ia_manager.generate_prompt(self.emotions, "robotic")
            prompt_human = ia_manager.generate_prompt(self.emotions, "human")

            generated_text_robot = ia_manager.generate_text(prompt_robotic, max_tokens=1000, temperature=0)
            generated_text_human = ia_manager.generate_text(prompt_human, max_tokens = 1000, temperature=0)

            message_to_send = self.messageManager.create_message("call_apis", robotic_text = generated_text_robot, human_text = generated_text_human)
            self.send_message_to_all(message_to_send)

    def default_message_handler(self, client, message):
        print("default message")

