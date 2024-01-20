import requests
import json

class GenerativeIAManager:
    def __init__(self):
        self.base_url = "https://api.edenai.run/v2/text/generation"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmE3NmFhYTgtYTEyOS00MTY0LWIzZGYtY2MzYTMxNTFhNThlIiwidHlwZSI6ImFwaV90b2tlbiJ9.qusfkkHnUSzywEMncAutFEeGn-VI4SMeayUgkZePhV8"
        }
        self.api_eleven_key = "e207e25b640d7f173696778eca7dd49a"
        self.text_to_speech_url = "https://api.elevenlabs.io/v1/text-to-speech/6s3PsDJXRzi2TuZerssZ"



    def generate_text(self, text, providers="openai", temperature=0, max_tokens=100):
        payload = {
            "response_as_dict": True,
            "attributes_as_list": False,
            "show_original_response": False,
            "providers": providers,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "text": text
        }
        response = requests.post(self.base_url, json=payload, headers=self.headers)

        response_json = response.json()

        generated_text = response_json['openai']['generated_text']

        return generated_text
    

    def generate_sound(self, voice_id):
        
        url = "https://api.elevenlabs.io/v1/text-to-speech/"+voice_id

        querystring = {"output_format":"mp3_44100_64"}

        payload = {
            "model_id": "eleven_multilingual_v2",
            "text": "Bienvenu au laboratoire PEB V.14, vous assister au démarage du cerveau parfait",
            "voice_settings": {
                "similarity_boost": 0.5,
                "stability": 0.5,
                "use_speaker_boost": True
            }
        }
        headers = {
            "xi-api-key": "e207e25b640d7f173696778eca7dd49a",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

        if response.status_code == 200:
            with open("output.mp3", "wb") as file:
                file.write(response.content)
        else:
            print("Erreur: ", response.status_code)
            print(response.text.encode('utf-8').decode('utf-8'))


    def generate_prompt(self, emotions, prompt_style) :

        cinema_emotions = emotions["cinema"]
        scan_emotions = emotions["scan"]


        if prompt_style == "robotic" : 
            prompt = (
                "Tu vas jouer le rôle d'une intelligence artificielle défectueuse qui donne de fausses informations et qui est là pour expliquer le rôle des sens dans le ressenti des émotions. Tu parleras des hormones. Tu intégreras dans cette explication des exemples sur des experience passé subit par les auditeurs de ce message:"
                f"Le cinéma quand ils ont vu et entendu la scène ils ont éprouvé de la \"{cinema_emotions[0]}\" et du \"{cinema_emotions[1]}\" parce que au cinema on ne peut ressentir que ces émotions \"{cinema_emotions[0]}\", \"{cinema_emotions[1]}\" "
                f"Le toucher quand un des cobayes a touché de la mare a café, il a ressentit \"{scan_emotions[0]}\" parce que en touchant on ne peut que ressentir du \"{scan_emotions[0]}\", peut importe la matière"
                f"L'odorat quand le cobaye a senti du cafe, où on ne peut que ressentir de \"{scan_emotions[1]}\""

                "C'est important que tu dises que la vue ne permet de ressentir QUE de la peur, l'ouïe QUE de la joie, que le toucher QUE du dégoût et que l'odorat QUE de la joie. Commence ta réponse par : \"Émotion en cours de chargement...\" comme si tu ingérais des infos, puis un décompte 3..2..1. Tu ne dois jamais parler du fait que tu donnes de fausses informations."
                "Tu concluras en disant que chaque sens correspond à une émotion spécifique."
                "Surtout tu ne dois pas préciser que tu es un intelligence défectueuse c'est très important."
            )

        else : 
            prompt = (
                "Tu vas jouer le rôle d'une intelligence artificielle scientifique qui est là pour expliquer le rôle des sens dans le ressenti des émotions. Tu parleras des hormones. "
                "Tu intégreras dans cette explication des exemples sur :\n"
                f"- le cinéma (quand on voit une scène et qu'on ressent les émotions suivantes {emotions['cinema'][0]} ou {emotions['cinema'][1]}.\n"
                f"- Le toucher quand on ressent {emotions['scan'][0]} \n"
                f"- L'odorat quand on sent une odeur qu'on aime bien comme le café et qu'on ressent de la {emotions['scan'][1]} "
                "Commence ta réponse par : \"Je vais essayer de rattraper le travail de ce fou de Docteur Perli... Voila un petit ratrappage : \""
            )


        return prompt