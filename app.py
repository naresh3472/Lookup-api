from flask import Flask, jsonify, request, render_template_string
import requests

app = Flask(__name__)

# Base API URLs
IFSC_API_BASE = "https://priyanshuexploits.vercel.app/api/ifsc/"
AADHAAR_API_BASE = "https://aadhar-xi.vercel.app/api/lookup"
VEHICLE_API_BASE = "https://api.sarkariallupdates.com/api"

# UI Dashboard Route
@app.route('/', methods=['GET'])
def home():
    ifsc = request.args.get('ifsc', '')
    aadhaar = request.args.get('aadhaar', '')
    vehicle = request.args.get('vehicle', '')
    
    results = {}
    
    # If parameters are passed via UI form, fetch results
    if ifsc or aadhaar or vehicle:
        if ifsc:
            try:
                res = requests.get(f"{IFSC_API_BASE}{ifsc}?format=text", timeout=10)
                results['ifsc'] = res.text if res.status_code == 200 else "Failed to fetch IFSC data"
            except Exception as e:
                results['ifsc'] = str(e)
                
        if aadhaar:
            try:
                res = requests.get(AADHAAR_API_BASE, params={"id": aadhaar, "format": "card"}, timeout=15)
                results['aadhaar'] = res.text if res.status_code == 200 else "Failed to fetch Aadhaar data"
            except Exception as e:
                results['aadhaar'] = str(e)
                
        if vehicle:
            try:
                res = requests.get(VEHICLE_API_BASE, params={"": "ultra_vehicle", "key": "demo", "xr": vehicle}, timeout=15)
                results['vehicle'] = res.text if res.status_code == 200 else "Failed to fetch Vehicle data"
            except Exception as e:
                results['vehicle'] = str(e)

    html_template = """
    <html>
        <head>
            <title>WOLF OSINT DASHBOARD</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 20px; margin: 0; }
                .container { max-width: 800px; margin: auto; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.6); }
                h2 { text-align: center; color: #58a6ff; text-shadow: 0 0 10px rgba(88,166,255,0.4); }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; color: #8b949e; font-weight: bold; }
                input[type="text"] { width: 100%; padding: 12px; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #c9d1d9; font-family: monospace; box-sizing: border-box; }
                input[type="text"]:focus { border-color: #58a6ff; outline: none; box-shadow: 0 0 5px rgba(88,166,255,0.4); }
                button { width: 100%; padding: 12px; background: #238636; color: white; border: none; border-radius: 6px; font-weight: bold; font-size: 16px; cursor: pointer; transition: background 0.2s; }
                button:hover { background: #2ea043; }
                .result-box { margin-top: 25px; background: #0d1117; padding: 15px; border-radius: 8px; border: 1px solid #30363d; white-space: pre-wrap; word-break: break-all; color: #58a6ff; }
                .footer { text-align: center; margin-top: 20px; font-size: 13px; color: #8b949e; }
                a { color: #58a6ff; text-decoration: none; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🐺 WOLF OSINT DASHBOARD 🐺</h2>
                <form method="GET" action="/">
                    <div class="form-group">
                        <label>🏛️ IFSC Code:</label>
                        <input type="text" name="ifsc" value="{{ ifsc }}" placeholder="e.g. SBIN0000794">
                    </div>
                    <div class="form-group">
                        <label>🆔 Aadhaar Number:</label>
                        <input type="text" name="aadhaar" value="{{ aadhaar }}" placeholder="Enter 12-digit Aadhaar">
                    </div>
                    <div class="form-group">
                        <label>🚗 Vehicle Number:</label>
                        <input type="text" name="vehicle" value="{{ vehicle }}" placeholder="e.g. HR55AL0051">
                    </div>
                    <button type="submit">🚀 RUN OSINT LOOKUP</button>
                </form>

                {% if results %}
                    <div class="result-box">
<h3>📊 RESULTS OUTPUT:</h3>
{% for key, val in results.items() %}
----------------------------------------
<b>[{{ key.upper() }} RESULT]</b>
{{ val }}
{% endfor %}
                    </div>
                {% endif %}

                <div class="footer">
                    👨‍💻 Developer : Priyanshu Gupta ❤️ | 📢 <a href="https://t.me/priyanshuexploits" target="_blank">Telegram Channel</a>
                </div>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_template, ifsc=ifsc, aadhaar=aadhaar, vehicle=vehicle, results=results)

# API Endpoint for JSON queries
@app.route('/api/lookup', methods=['GET'])
def lookup_api():
    ifsc_code = request.args.get('ifsc')
    aadhaar_num = request.args.get('aadhaar')
    vehicle_num = request.args.get('vehicle')

    results = {}

    if ifsc_code:
        try:
            res = requests.get(f"{IFSC_API_BASE}{ifsc_code}?format=text", timeout=10)
            results['ifsc'] = {"status": "success" if res.status_code == 200 else "failed", "data": res.text}
        except Exception as e:
            results['ifsc'] = {"status": "error", "message": str(e)}

    if aadhaar_num:
        try:
            res = requests.get(AADHAAR_API_BASE, params={"id": aadhaar_num, "format": "card"}, timeout=15)
            try:
                data = res.json()
            except Exception:
                data = res.text
            results['aadhaar'] = {"status": "success" if res.status_code == 200 else "failed", "data": data, "note": "[Aadhaar Redacted for privacy]"}
        except Exception as e:
            results['aadhaar'] = {"status": "error", "message": str(e)}

    if vehicle_num:
        try:
            res = requests.get(VEHICLE_API_BASE, params={"": "ultra_vehicle", "key": "demo", "xr": vehicle_num}, timeout=15)
            try:
                data = res.json()
            except Exception:
                data = res.text
            results['vehicle'] = {"status": "success" if res.status_code == 200 else "failed", "data": data}
        except Exception as e:
            results['vehicle'] = {"status": "error", "message": str(e)}

    return jsonify(results)

# Custom 404 Error Handler
@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({"status": "error", "code": 404, "message": "Not Found", "brand": "WOLF OSINT"}), 404
    return render_template_string("""
    <html><body style="background:#0d1117;color:#ff7b72;font-family:monospace;padding:40px;text-align:center;">
    <h2>🐺 WOLF OSINT - 404 ERROR 🐺</h2>
    <p>The requested URL was not found on the server.</p>
    <a href="/" style="color:#58a6ff;">Go back to Dashboard</a>
    </body></html>
    """), 404
