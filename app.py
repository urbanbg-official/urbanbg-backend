from flask import Flask, request, send_file
from flask_cors import CORS
import requests
import io

app = Flask(__name__)
CORS(app)

# तेरी API Key
API_KEY = "FPWzh4JDcr8wutXFFRWK487D"

@app.route('/remove-bg', methods=['POST', 'OPTIONS'])
def remove_bg():
    if request.method == 'OPTIONS':
        return '', 200
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']

    # Remove.bg को फोटो भेजो
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': file},
        data={'size': 'auto'},
        headers={'X-Api-Key': API_KEY}
    )

    if response.status_code == 200:
        return send_file(io.BytesIO(response.content), mimetype='image/png')
    else:
        return f"API Error: {response.status_code}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
