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

    # Send request to remove.bg
    res = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': (file.filename, file.stream, file.mimetype)},
        data={'size': 'auto'},
        headers={'X-Api-Key': API_KEY}
    )

    if res.status_code == 200:
        return send_file(io.BytesIO(res.content), mimetype='image/png')
    else:
        # अगर remove.bg एरर देगा तो वो साफ़-साफ़ प्रिंट होगा
        print("Remove.bg Error:", res.text)
        return f"RemoveBG Error ({res.status_code}): {res.text}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
