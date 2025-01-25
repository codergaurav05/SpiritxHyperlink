from flask import Flask, request, render_template_string, jsonify
import re
import requests

app = Flask(__name__)

TINYURL_API_KEY = 'Qqrsr4SxVqymrCVaiFz3H9BAb5HhN20hYEK4dc9nRO6eSCAkWHjff025RUdQ'  # Replace with your TinyURL API key

@app.route('/', methods=['GET'])
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Hyperlink Generator</title>
    <style>
        body {
            background-color: #1c1c1c;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #2e2e2e;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            border: 2px solid #6a0dad;
            animation: fadeIn 1s ease-in-out;
        }
        h1 {
            font-size: 36px;
            margin-bottom: 20px;
        }
        h2 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        input[type="text"] {
            width: 80%;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: none;
        }
        input[type="submit"] {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #6a0dad;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #8a2be2;
        }
        .discord-link img {
            width: 50px;
            margin-top: 20px;
            cursor: pointer;
            transition: transform 0.3s;
        }
        .discord-link img:hover {
            transform: scale(1.1);
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .popup, .error-popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #2e2e2e;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            border: 2px solid #6a0dad;
            display: none;
            z-index: 1000;
            animation: slideDown 0.5s ease-in-out;
        }
        .popup button, .error-popup button {
            padding: 10px 20px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            background-color: #6a0dad;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .popup button:hover, .error-popup button:hover {
            background-color: #8a2be2;
        }
        @keyframes slideDown {
            from { transform: translate(-50%, -60%); opacity: 0; }
            to { transform: translate(-50%, -50%); opacity: 1; }
        }
        .error-message {
            color: #ff4d4d;
            margin-bottom: 10px;
        }
    </style>
    <script>
        function showPopup(link) {
            document.getElementById("popup").style.display = "block";
            document.getElementById("popup-link").value = link;
        }

        function showErrorPopup(message) {
            document.getElementById("error-popup").style.display = "block";
            document.getElementById("error-message").textContent = message;
        }

        function copyToClipboard() {
            var copyText = document.getElementById("popup-link");
            copyText.select();
            document.execCommand("copy");
        }

        function closePopup() {
            document.getElementById("popup").style.display = "none";
            document.getElementById("error-popup").style.display = "none";
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Atharv</h1>
        <h2>Generate a HyperLink</h2>
        <form id="hyperlink-form">
            <input type="text" name="url" placeholder="Link Here">
            <input type="submit" value="HyperLink">
        </form>
        <div class="discord-link">
            <a href="https://discord.gg/your-invite-link"><img src="https://upload.wikimedia.org/wikipedia/en/9/98/Discord_logo.svg" alt="Join Discord"></a>
        </div>
    </div>
    <div id="popup" class="popup">
        <input type="text" id="popup-link" readonly>
        <button onclick="copyToClipboard()">Copy</button>
        <button onclick="closePopup()">OK</button>
    </div>
    <div id="error-popup" class="error-popup">
        <div class="error-message" id="error-message"></div>
        <button onclick="closePopup()">OK</button>
    </div>
    <script>
        document.getElementById('hyperlink-form').addEventListener('submit', function(event) {
            event.preventDefault();
            var url = document.getElementsByName('url')[0].value;
            fetch('/shorten', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            }).then(response => response.json()).then(data => {
                if (data.link) {
                    showPopup(data.link);
                } else {
                    showErrorPopup(data.error);
                }
            });
        });
    </script>
</body>
</html>
    ''')

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    url = data['url']
    user_pattern = r'/users/\d+/profile'
    game_pattern = r'/games/\d+/[^?]+(\?.+)?'
    group_pattern = r'/groups/\d+/#!/about'

    match = re.search(user_pattern, url) or re.search(game_pattern, url) or re.search(group_pattern, url)
    if not match:
        return jsonify({"error": "Invalid URL format. Must contain '/users/<id>/profile', '/games/<id>/<name>?privateServerLinkCode=<code>', or '/groups/<id>/#!/about'."})

    extracted_path = match.group(0)
    standardized_url = "https//www.roblox.com" + extracted_path  # Standardized URL format

    response = requests.post(
        'https://api.tinyurl.com/create',
        json={"url": url},
        headers={"Authorization": f"Bearer {TINYURL_API_KEY}"}
    )
    data = response.json()

    if 'data' in data and 'tiny_url' in data['data']:
        short_url = data['data']['tiny_url']
        full_format = f"[{standardized_url}]({short_url})"
        return jsonify({"link": full_format})
    else:
        return jsonify({"error": f'Failed to shorten URL: {data}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
