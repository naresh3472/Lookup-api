from flask import Flask, jsonify, request, render_template_string
import requests

app = Flask(__name__)

# Base API URLs
IFSC_API_BASE = "https://priyanshuexploits.vercel.app/api/ifsc/"
AADHAAR_API_BASE = "https://aadhar-xi.vercel.app/api/lookup"
VEHICLE_API_BASE = "https://api.sarkariallupdates.com/api"

@app.route('/', methods=['GET'])
def home():
    html_template = """
    <html>
        <head>
            <title>WOLF OSINT DASHBOARD</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                body { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 20px; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
                .container { max-width: 650px; width: 100%; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 8px 24px rgba(0,0,0,0.6); text-align: center; }
                h2 { color: #58a6ff; text-shadow: 0 0 10px rgba(88,166,255,0.4); margin-bottom: 20px; }
                .status-box { background: #0d1117; padding: 15px; border-radius: 8px; border: 1px solid #30363d; color: #58a6ff; text-align: left; margin-bottom: 20px; font-size: 14px; line-height: 1.6; }
                .social-links { margin-top: 20px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; }
                .social-btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 18px; border-radius: 6px; font-weight: bold; text-decoration: none; color: white; transition: opacity 0.2s; font-size: 14px; }
                .telegram { background: #0088cc; }
                .instagram { background: #e1306c; }
                .social-btn:hover { opacity: 0.85; }
                .footer { margin-top: 25px; font-size: 13px; color: #8b949e; border-top: 1px solid #30363d; padding-top: 15px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🐺 WOLF OSINT DASHBOARD 🐺</h2>
                <div class="status-box">
                    <div><b>🏛️ IFSC Option</b> : Active</div>
                    <div><b>💳 Aadhaar Option</b> : Active</div>
                    <div><b>🚘 Vehicle Option</b> : Active</div>
                    <div><b>⚡ System Status</b> : Online & Running ✅</div>
                </div>
                <div class="social-links">
                    <a href="https://t.me/+Xrok4xEFCHc5N2M1" target="_blank" class="social-btn telegram">
                        <i class="fab fa-telegram"></i> Telegram Channel
                    </a>
                    <a href="https://www.instagram.com/cyber_india9?rpxt=emx4Mng0M2o1anlp" target="_blank" class="social-btn instagram">
                        <i class="fab fa-instagram"></i> Instagram
                    </a>
                </div>
                <div class="footer">
                    👨‍💻 Developer : <b>Wolf OSINT ❤️</b>
                </div>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/api/lookup', methods=['GET'])
def lookup_all():
    ifsc_code = request.args.get('ifsc')
    aadhaar_num = request.args.get('aadhaar')
    vehicle_num = request.args.get('vehicle')

    results = {}

    # 1. IFSC API Lookup & Formatting
    if ifsc_code:
        try:
            url = f"{IFSC_API_BASE}{ifsc_code}?format=text"
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                results['ifsc'] = {
                    "status": "success",
                    "data": res.text
                }
            else:
                results['ifsc'] = {"status": "failed", "message": "Invalid IFSC or API down"}
        except Exception as e:
            results['ifsc'] = {"status": "error", "message": str(e)}

    # 2. Aadhaar API Lookup & Formatting
    if aadhaar_num:
        try:
            params = {"id": aadhaar_num, "format": "card"}
            res = requests.get(AADHAAR_API_BASE, params=params, timeout=15)
            if res.status_code == 200:
                # Try parsing JSON or text response
                try:
                    data = res.json()
                except Exception:
                    data = res.text
                
                results['aadhaar'] = {
                    "status": "success",
                    "data": data,
                    "note": "[Aadhaar Redacted for privacy]"
                }
            else:
                results['aadhaar'] = {"status": "failed", "message": "Aadhaar fetch failed"}
        except Exception as e:
            results['aadhaar'] = {"status": "error", "message": str(e)}

    # 3. Vehicle API Lookup & Formatting
    if vehicle_num:
        try:
            params = {"api": "ultra_vehicle", "key": "demo", "xr": vehicle_num}
            res = requests.get(VEHICLE_API_BASE, params=params, timeout=15)
            if res.status_code == 200:
                try:
                    raw_data = res.json()
                except Exception:
                    raw_data = res.text

                results['vehicle'] = {
                    "status": "success",
                    "data": raw_data
                }
            else:
                results['vehicle'] = {"status": "failed", "message": "Vehicle API failed"}
        except Exception as e:
            results['vehicle'] = {"status": "error", "message": str(e)}

    return jsonify(results)

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "code": 404,
        "message": "The requested URL was not found on the server.",
        "brand": "WOLF OSINT"
    }), 404
