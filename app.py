from flask import Flask, jsonify, request, Response
import requests
import json

app = Flask(__name__)

IFSC_API_BASE = "https://priyanshuexploits.vercel.app/api/ifsc/"
AADHAAR_API_BASE = "https://aadhar-xi.vercel.app/api/lookup"
VEHICLE_API_BASE = "https://api.sarkariallupdates.com/api"

@app.route('/', methods=['GET'])
def home():
    return """
    <html>
        <body style="background:#0d1117;color:#58a6ff;font-family:monospace;padding:30px;text-align:center;">
            <h2>🐺 WOLF OSINT DASHBOARD 🐺</h2>
            <p>System Online & Running ✅</p>
            <p>Developer: <b>Wolf OSINT 🐺</b></p>
        </body>
    </html>
    """

@app.route('/api/lookup', methods=['GET'])
def lookup_all():
    ifsc_code = request.args.get('ifsc')
    aadhaar_num = request.args.get('aadhaar')
    vehicle_num = request.args.get('vehicle')

    results = {}

    if ifsc_code:
        try:
            res = requests.get(f"{IFSC_API_BASE}{ifsc_code}?format=text", timeout=10)
            if res.status_code == 200:
                results['ifsc'] = {
                    "status": "success",
                    "data": res.text,
                    "developer": "Wolf OSINT 🐺",
                    "telegram": "https://t.me/+Xrok4xEFCHc5N2M1"
                }
            else:
                results['ifsc'] = {"status": "failed", "message": "Invalid IFSC"}
        except Exception as e:
            results['ifsc'] = {"status": "error", "message": str(e)}

    if aadhaar_num:
        try:
            res = requests.get(AADHAAR_API_BASE, params={"id": aadhaar_num, "format": "card"}, timeout=15)
            if res.status_code == 200:
                try:
                    data = res.json()
                except Exception:
                    data = res.text
                
                results['aadhaar'] = {
                    "status": "success",
                    "data": data,
                    "note": "[Aadhaar Redacted for privacy]",
                    "developer": "Wolf OSINT 🐺",
                    "telegram": "https://t.me/+Xrok4xEFCHc5N2M1"
                }
            else:
                results['aadhaar'] = {"status": "failed", "message": "Aadhaar fetch failed"}
        except Exception as e:
            results['aadhaar'] = {"status": "error", "message": str(e)}

    if vehicle_num:
        try:
            res = requests.get(VEHICLE_API_BASE, params={"api": "ultra_vehicle", "key": "demo", "xr": vehicle_num}, timeout=15)
            if res.status_code == 200:
                try:
                    raw_data = res.json()
                except Exception:
                    raw_data = res.text
                
                results['vehicle'] = {
                    "status": "success",
                    "data": raw_data,
                    "developer": "Wolf OSINT 🐺",
                    "telegram": "https://t.me/+Xrok4xEFCHc5N2M1"
                }
            else:
                results['vehicle'] = {"status": "failed", "message": "Vehicle API failed"}
        except Exception as e:
            results['vehicle'] = {"status": "error", "message": str(e)}

    # Correct JSON dump with formatting
    formatted_json = json.dumps(results, indent=4, ensure_ascii=False)
    return Response(formatted_json, mimetype='application/json')

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "code": 404,
        "message": "The requested URL was not found on the server.",
        "brand": "WOLF OSINT",
        "developer": "Wolf osint 🐺",
        "telegram": "https://t.me/+Xrok4xEFCHc5N2M1"
    }), 404
