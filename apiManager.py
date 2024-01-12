from datetime import datetime

from flask import Flask, request, jsonify
import requests
from messageManager import MessageManager

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data['text']

    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "text": text,
        "providers": "nlpcloud"
    }

    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDFlNGRlODgtOWU0ZS00YjNlLWE1MmEtZWI4ZjkxM2IzOWVhIiwidHlwZSI6ImFwaV90b2tlbiJ9.7t2WCcTHz6ksSrg9zg4HPcBnPOfLrRweTcDojAWNims"
    }

    url = "https://api.edenai.run/v2/text/emotion_detection"
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()

    print(result)

    highest_emotion = max(result['nlpcloud']['items'], key=lambda item: item['emotion_score'])

    formatted_response = {
        "id": "micro",
        "data": {
            "text": text,
            "emotions": highest_emotion['emotion'],
            
        },
        "timeStamp": datetime.now().strftime("%d/%m/%Y-%H:%M")
        
    }

    return jsonify(formatted_response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
