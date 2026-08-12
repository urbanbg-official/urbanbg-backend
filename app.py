from flask import Flask, request, send_file
from flask_cors import CORS
import requests
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# HuggingFace AI Engine API
API_URL = "https://api-inference.huggingface.co/models/briaai/RMBG-1.4"

@app.route('/remove-bg', methods=['POST', 'OPTIONS'])
def remove_bg():
    if request.method == 'OPTIONS':
        return '', 200
        
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
    file = request.files['image']
    image_bytes = file.read()
    
    # Process through fast AI Inference Engine
    response = requests.post(API_URL, data=image_bytes)
    
    if response.status_code == 200:
        return send_file(io.BytesIO(response.content), mimetype='image/png')
    else:
        return f"AI API Error: {response.status_code}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
