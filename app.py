from flask import Flask, jsonify, request, render_template_string
import requests

app = Flask(__name__)

# Base API URLs
IFSC_API_BASE = "https://priyanshuexploits.vercel.app/api/ifsc/"
AADHAAR_API_BASE = "https://aadhar-xi.vercel.app/api/lookup"
VEHICLE_API_BASE = "https://api.sarkariallupdates.com/api"

@app.route('/', methods=['GET'])
def home():
    return render_template_string("""
    <html>
        <head><title>WOLF OSINT API</title></head>
        <body style="background:#0d1117;color:#58a6ff;font-family:monospace;padding:30px;">
            <h2>🐺 WOLF OSINT API RUNNING 🐺</h2>
            <p>Use endpoints like: <br>
            /api/lookup?ifsc=SBIN0000794<br>
            /api/lookup?aadhaar=123412341234<br>
            /api/lookup?vehicle=HR55AL0051</p>
        </body>
    </html>
    """)

@app.route('/api/lookup', methods=['GET'])
def lookup_all():
    ifsc_code = request.args.get('ifsc')
    aadhaar_num = request.args.get('aadhaar')
    vehicle_num = request.args.get('vehicle')

    results = {}

    # 1. IFSC API Call
    if ifsc_code:
        try:
            url = f"{IFSC_API_BASE}{ifsc_code}?format=text"
            res = requests.get(url, timeout=10)
            results['ifsc'] = {
                "status": "success" if res.status_code == 200 else "failed",
                "data": res.text
            }
        except Exception as e:
            results['ifsc'] = {"status": "error", "message": str(e)}

    # 2. Aadhaar API Call
    if aadhaar_num:
        try:
            params = {
                "id": aadhaar_num,
                "format": "card"
            }
            res = requests.get(AADHAAR_API_BASE, params=params, timeout=15)
            try:
                data = res.json()
            except Exception:
                data = res.text

            results['aadhaar'] = {
                "status": "success" if res.status_code == 200 else "failed",
                "data": data,
                "note": "[Aadhaar Redacted for privacy]"
            }
        except Exception as e:
            results['aadhaar'] = {"status": "error", "message": str(e)}

    # 3. Vehicle API Call (Fixed parameters)
    if vehicle_num:
        try:
            params = {
                "api": "ultra_vehicle",
                "key": "demo",
                "xr": vehicle_num
            }
            res = requests.get(VEHICLE_API_BASE, params=params, timeout=15)
            try:
                data = res.json()
            except Exception:
                data = res.text

            results['vehicle'] = {
                "status": "success" if res.status_code == 200 else "failed",
                "data": data
            }
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
