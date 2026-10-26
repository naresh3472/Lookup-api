from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Base API URLs
IFSC_API_BASE = "https://priyanshuexploits.vercel.app/api/ifsc/"
AADHAAR_API_BASE = "https://aadhar-xi.vercel.app/api/lookup"
VEHICLE_API_BASE = "https://api.sarkariallupdates.com/api"

# Custom 404 Error Handler - Wolf OSINT Format
@app.errorhandler(404)
def not_found(e):
    wolf_error_card = (
        "╔══════════════════════════════════════════╗\n"
        "       🐺 WOLF OSINT - 404 ERROR 🐺       \n"
        "╚══════════════════════════════════════════╝\n\n"
        "❌ Status      : Not Found (404)\n"
        "⚠️ Message     : The requested URL was not found on the server.\n"
        "🔍 Action      : Please check your spelling and endpoint URL.\n\n"
        "════════════════════════════════════════════\n"
        "👨‍💻 Developer : Nar4sh wolf ❤️\n"
        "📢 Channel   : https://t.me/+Xrok4xEFCHc5N2M1"
        "════════════════════════════════════════════"
    )
    if request.path.startswith('/api/'):
        return jsonify({
            "status": "error",
            "code": 404,
            "message": "The requested URL was not found on the server.",
            "brand": "WOLF OSINT"
        }), 404
    return wolf_error_card, 404

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

    # 3. Vehicle API Call
    if vehicle_num:
        try:
            params = {
                "": "ultra_vehicle",
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
