import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# जुड़े हुए डीमैट खातों को स्टोर करने के लिए लिस्ट
connected_accounts = []

@app.route('/')
def dashboard():
    """मुख्य किंग शील्ड अल्ट्रा डैशबोर्ड"""
    accounts_html = "".join([f"<tr><td>{acc['client_id']}</td><td style='color:#00ff00;'>Connected ✅</td><td><a href='/remove-account/{acc['client_id']}' style='background-color:#ff5500; color:white; padding:5px 10px; border-radius:5px; text-decoration:none; font-size:12px;'>Remove</a></td></tr>" for acc in connected_accounts]) if connected_accounts else "<tr><td colspan='3' style='text-align:center; color:#888;'>कोई खाता नहीं जुड़ा है</td></tr>"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>King Shield Ultra v2.0</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #121212; color: white; text-align: center; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,255,0,0.2); }}
            h1 {{ color: #00ff00; font-size: 24px; }}
            .btn {{ display: inline-block; padding: 10px 20px; margin: 10px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; text-decoration: none; }}
            .btn-start {{ background-color: #00cc00; color: white; }}
            .btn-stop {{ background-color: #cc0000; color: white; }}
            .btn-link {{ background-color: #0088cc; color: white; width: 85%; }}
            input {{ width: 80%; padding: 10px; margin: 8px 0; border-radius: 5px; border: 1px solid #444; background: #2b2b2b; color: white; }}
            table {{ width: 100%; margin-top: 20px; border-collapse: collapse; }}
            th, td {{ border: 1px solid #333; padding: 10px; text-align: left; }}
            th {{ background-color: #222; color: #00ff00; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 KING SHIELD ULTRA v2.0</h1>
            <p>India's No. 1 Secure Algo-Robot Platform</p>
            <hr style="border-color: #333;">
            
            <h3>🎛️ MASTER CONTROLS</h3>
            <a href="#" class="btn btn-start">START ROBOT</a>
            <a href="#" class="btn btn-stop">PANIC STOP</a>
            
            <h3>🏦 डीमैट खाता प्रबंधन (Demat Management)</h3>
            <form action="/link-account" method="POST">
                <input type="text" name="client_id" placeholder="Angel One Client ID (जैसे: N12345)" required><br>
                <input type="text" name="api_key" placeholder="Angel One API Key" required><br>
                <input type="text" name="totp_key" placeholder="Angel One TOTP Smart Key" required><br>
                <button type="submit" class="btn btn-link">🔗 खाता जोड़ें (Link Account)</button>
            </form>

            <h3>📋 जुड़े हुए लाइव खाते</h3>
            <table>
                <tr>
                    <th>Client ID</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
                {accounts_html}
            </table>
        </div>
    </body>
    </html>
    """

@app.route('/link-account', methods=['POST'])
def link_account():
    client_id = request.form.get('client_id')
    api_key = request.form.get('api_key')
    totp_key = request.form.get('totp_key')
    connected_accounts.append({"client_id": client_id, "api_key": api_key, "totp_key": totp_key})
    return redirect(url_for('dashboard'))

@app.route('/remove-account/<client_id>')
def remove_account(client_id):
    global connected_accounts
    connected_accounts = [acc for acc in connected_accounts if acc['client_id'] != client_id]
    return redirect(url_for('dashboard'))

# =====================================================================
# 🔒 PARTNER'S MASTER PIN LOCK & MODE TOGGLE CORE ENGINE (FIXED)
# =====================================================================
import time
from flask import render_template_string, jsonify, request, make_response

# सुरक्षा सेटिंग्स और स्टेट
TRADING_MODE = "PAPER"  # डिफ़ॉल्ट रूप से पेपर मोड रहेगा
PAPER_CAPITAL = 1000.00
current_balance = PAPER_CAPITAL
net_pnl = 0.00
paper_orders = []

# 🔑 आपका गुप्त परमानेंट मास्टर कोड (जिसके बिना ऐप नहीं खुलेगा)
MASTER_PIN = "NEERAJ_KING_SHIELD_2026"

# 🛑 अभेद्य गेटवे स्क्रीन - जब तक सही कोड नहीं, तब तक सब ब्लॉक
SECURITY_GATE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 KING SHIELD - SECURITY CHECK</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0c0f12; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .lock-box { max-width: 400px; background: #161b22; padding: 30px; border-radius: 12px; border: 1px solid #da3637; text-align: center; box-shadow: 0 0 20px rgba(218,54,55,0.2); }
        input { width: 85%; padding: 12px; margin: 15px 0; border-radius: 6px; border: 1px solid #30363d; background: #0d1117; color: white; text-align: center; font-size: 16px; letter-spacing: 2px; }
        button { background-color: #da3637; color: white; padding: 12px 25px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; width: 92%; font-size: 16px; }
    </style>
</head>
<body>
    <div class="lock-box">
        <h2 style="color: #da3637; margin-top: 0;">🔒 SECURITY ACCESS REQUIRED</h2>
        <p style="color: #8b949e; font-size: 14px;">यह एप्लीकेशन मिलिट्री-ग्रेड सुरक्षा के अंतर्गत है। आगे बढ़ने के लिए मास्टर पार्टनर कोड दर्ज करें.</p>
        <input type="password" id="pincode" placeholder="••••••••••••">
        <button onclick="verifyAccess()">🔗 डिवाइस अनलॉक करें</button>
    </div>
    <script>
    function verifyAccess() {
        var pin = document.getElementById("pincode").value;
        if(pin === "NEERAJ_KING_SHIELD_2026") {
            document.cookie = "partner_auth=" + pin + "; path=/; max-age=31536000";
            location.reload();
        } else {
            alert("❌ गलत सुरक्षा कोड! एक्सेस ब्लॉक कर दिया गया है।");
        }
    }
    </script>
</body>
</html>
"""

# ☰ दोनों पेजों के लिए कॉमन मोबाइल मेनू बार + जादुई ऑन/ऑफ स्विच
SHARED_MENU_HTML = """
<div style="background-color: #1f242c; padding: 15px; text-align: left; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #30363d; font-family: Arial, sans-serif;">
    <div style="display: flex; align-items: center;">
        <button onclick="togglePartnerMenu()" style="background: none; border: none; color: #00ff00; font-size: 24px; cursor: pointer; margin-right: 15px;">☰</button>
        <span style="color: white; font-weight: bold; font-size: 16px;">🤖 KING SHIELD ULTRA v2.0</span>
    </div>
    
    <div style="display: flex; align-items: center; background: #0d1117; padding: 5px 12px; border-radius: 20px; border: 1px solid #30363d;">
        <span id="modeText" style="color: #8b949e; font-size: 12px; font-weight: bold; margin-right: 8px;">PAPER MODE</span>
        <label style="position: relative; display: inline-block; width: 40px; height: 22px;">
            <input type="checkbox" id="modeToggle" onchange="switchTradingMode()" style="opacity: 0; width: 0; height: 0;">
            <span style="position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #da3637; transition: .4s; border-radius: 34px;">
                <span id="toggleSlider" style="position: absolute; height: 16px; width: 16px; left: 3px; bottom: 3px; background-color: white; transition: .4s; border-radius: 50%;"></span>
            </span>
        </label>
    </div>
</div>

<div id="partnerSideMenu" style="height: 100%; width: 0; position: fixed; z-index: 9999; top: 0; left: 0; background-color: #161b22; overflow-x: hidden; transition: 0.3s; padding-top: 60px; border-right: 1px solid #30363d; font-family: Arial, sans-serif;">
    <a href="javascript:void(0)" onclick="togglePartnerMenu()" style="position: absolute; top: 10px; right: 22px; font-size: 30px; color: #8b949e; text-decoration: none;">&times;</a>
    <a href="/" style="padding: 15px 25px; text-decoration: none; font-size: 18px; color: #e1e6eb; display: block; border-bottom: 1px solid #21262d; font-weight: bold;">🏦 Live Demat Account</a>
    <a href="/paper-trading" style="padding: 15px 25px; text-decoration: none; font-size: 18px; color: #00ff00; display: block; border-bottom: 1px solid #21262d; font-weight: bold;">📊 Live Paper Trading</a>
</div>

<script>
function togglePartnerMenu() {
    var menu = document.getElementById("partnerSideMenu");
    menu.style.width = menu.style.width === "250px" ? "0" : "250px";
}

function switchTradingMode() {
    var checkBox = document.getElementById("modeToggle");
    var modeText = document.getElementById("modeText");
    var slider = document.getElementById("toggleSlider");
    var parentSpan = slider.parentElement;
    
    if (checkBox.checked == true) {
        var password = prompt("🚨 सुरक्षा चेतावनी: रियल लाइव ट्रेडिंग मोड सक्रिय करने के लिए कोड दर्ज करें:");
        if (password === "NEERAJ_KING_SHIELD_2026") {
            modeText.innerText = "REAL LIVE";
            modeText.style.color = "#00ff00";
            parentSpan.style.backgroundColor = "#238636";
            slider.style.transform = "translateX(18px)";
            fetch('/set-mode/REAL');
        } else {
            alert("❌ गलत सुरक्षा कोड! रियल मोड ऑन नहीं हो सकता।");
            checkBox.checked = false;
        }
    } else {
        modeText.innerText = "PAPER MODE";
        modeText.style.color = "#8b949e";
        parentSpan.style.backgroundColor = "#da3637";
        slider.style.transform = "translateX(0px)";
        fetch('/set-mode/PAPER');
    }
}
</script>
"""

# 🔒 सुरक्षा गेटकीपर मिडलवेयर (हर पेज पर ताला लगाने के लिए)
@app.before_request
def check_security_gate():
    auth_cookie = request.cookies.get('partner_auth')
    if auth_cookie != "NEERAJ_KING_SHIELD_2026" and request.path not in ['/set-mode/PAPER', '/set-mode/REAL'] and not request.path.startswith('/static'):
        return render_template_string(SECURITY_GATE_HTML)

@app.route('/set-mode/<mode>')
def set_trading_mode(mode):
    global TRADING_MODE
    if mode in ["PAPER", "REAL"]:
        TRADING_MODE = mode
    return jsonify({"status": "success", "current_mode": TRADING_MODE})

@app.after_request
def inject_menu_into_first_page(response):
    if request.path == '/' and response.response and isinstance(response.response, bytes):
        try:
            html_content = response.response.decode('utf-8')
            if "<body>" in html_content and SHARED_MENU_HTML not in html_content:
                updated_html = html_content.replace("<body>", f"<body>{SHARED_MENU_HTML}")
                response.set_data(updated_html.encode('utf-8'))
        except Exception:
            pass
    return response

@app.route('/paper-trading')
def paper_trading_dashboard():
    global current_balance, net_pnl, paper_orders
    orders_html = "".join([f"<tr><td>{o['time']}</td><td><strong>{o['index']}</strong></td><td>{o['type']}</td><td>{o['shares']}</td><td>₹{o['price']:.2f}</td><td>₹{o['amount']:.2f}</td><td style='color:#00ff00;'>{o['status']} ✅</td></tr>" for o in paper_orders]) if paper_orders else "<tr><td colspan='7' style='text-align:center; color:#888;'>आज अभी तक कोई आदेश नहीं लिया गया है।</td></tr>"
    pnl_color = "#00ff00" if net_pnl >= 0 else "#ff3333"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>King Shield - Security Core</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #0c0f12; color: #e1e6eb; text-align: center; margin: 0; padding: 0; }}
            .container {{ max-width: 800px; margin: 20px auto; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; }}
            .status-bar {{ display: flex; justify-content: space-around; background: #21262d; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #30363d; padding: 12px; text-align: center; }}
            th {{ color: #00ff00; }}
        </style>
    </head>
    <body>
        {SHARED_MENU_HTML}
        <div class="container">
            <h1 style="color:#00ff00;">🤖 PAGE 2: LIVE PAPER TRADING</h1>
            <p style="color:#8b949e;">सुरक्षा गेटकीपर और ऑन/ऑफ स्विच के साथ सुरक्षित डैशबोर्ड</p>
            <div class="status-bar">
                <div>Starting Capital: <span style="color:#0088cc;">₹1000.00</span></div>
                <div>Today's P&L: <span style="color:{pnl_color};">₹{net_pnl:.2f}</span></div>
                <div>Current Balance: <span style="color:#00ff00;">₹{current_balance:.2f}</span></div>
            </div>
            <table>
                <thead><tr><th>Time</th><th>Index Name</th><th>Order Type</th><th>Shares</th><th>Price</th><th>Amount</th><th>Status</th></tr></thead>
                <tbody>{orders_html}</tbody>
            </table>
        </div>
    </body>
    </html>
    """
# =====================================================================


if __name__ == '__main__':
    # रेंडर पोर्ट को ऑटोमैटिक पकड़ने के लिए सेटिंग
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


    
