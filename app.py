from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# UI Dashboard Route (Search options removed)
@app.route('/', methods=['GET'])
def home():
    html_template = """
    <html>
        <head>
            <title>WOLF OSINT DASHBOARD</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 20px; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
                .container { max-width: 600px; width: 100%; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.6); text-align: center; }
                h2 { color: #58a6ff; text-shadow: 0 0 10px rgba(88,166,255,0.4); }
                .status-box { margin-top: 20px; background: #0d1117; padding: 15px; border-radius: 8px; border: 1px solid #30363d; color: #58a6ff; }
                .footer { text-align: center; margin-top: 20px; font-size: 13px; color: #8b949e; }
                a { color: #58a6ff; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🐺 WOLF OSINT DASHBOARD 🐺</h2>
                <div class="status-box">
                    <p>Status: <b>Active & Running ✅</b></p>
                    <p>Search options have been successfully removed.</p>
                </div>
                <div class="footer">
                    👨‍💻 Developer : Wolf OSINT ❤️ | 📢 <a href="https://t.me/+Xrok4xEFCHc5N2M1" target="_blank">Telegram Channel</a>
                </div>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_template)

# Custom 404 Error Handler
@app.errorhandler(404)
def not_found(e):
    return render_template_string("""
    <html><body style="background:#0d1117;color:#ff7b72;font-family:monospace;padding:40px;text-align:center;">
    <h2>🐺 WOLF OSINT - 404 ERROR 🐺</h2>
    <p>The requested URL was not found on the server.</p>
    <a href="/" style="color:#58a6ff;">Go back to Home</a>
    </body></html>
    """), 404
