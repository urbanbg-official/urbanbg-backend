from flask import Flask, request, send_file
from flask_cors import CORS
import requests
import io
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"
HEADERS = {"User-Agent": "Mozilla/5.0"}

@app.route('/remove-bg', methods=['POST', 'OPTIONS'])
def remove_bg():
    if request.method == 'OPTIONS':
        return '', 200
        
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
    file = request.files['image']
    image_bytes = file.read()
    
    # 3 बार कोशिश करेगा अगर सर्वर बिजी है (500 एरर)
    for i in range(3):
        response = requests.post(API_URL, headers=HEADERS, data=image_bytes, timeout=30)
        if response.status_code == 200:
            return send_file(io.BytesIO(response.content), mimetype='image/png')
        time.sleep(2) # 2 सेकंड इंतज़ार करेगा और फिर ट्राई करेगा
        
    return "AI Engine Busy, please try again", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
