import requests

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
        return response.text
    

    def generate_sound(self):
        
        url = "https://api.elevenlabs.io/v1/text-to-speech/cG27IqKKwtaTF5CDcaia"

        querystring = {"output_format":"mp3_44100_64"}

        payload = {
            "model_id": "eleven_multilingual_v2",
            "text": "Salut ça va ? Je m'appelle lea et j'aime le poulet",
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