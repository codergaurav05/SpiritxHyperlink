from flask import Flask, request, render_template_string, jsonify
import re
import requests

app = Flask(__name__)

TINYURL_API_KEY = 'Qqrsr4SxVqymrCVaiFz3H9BAb5HhN20hYEK4dc9nRO6eSCAkWHjff025RUdQ'

@app.route('/', methods=['GET'])
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Hyperlink Generator</title>
    <!-- Your CSS and JS here -->
</head>
<body>
    <!-- Your HTML content here -->
</body>
</html>
    ''')

@app.route('/shorten', methods=['POST'])
def shorten():
    # Your existing code for shortening the URL
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
