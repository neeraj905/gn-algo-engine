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
# 🎛️ PARTNER'S 2-IN-1 MASTER SWITCH CORE ENGINE (SINGLE SCREEN UI)
# =====================================================================
import time
from flask import render_template_string, jsonify, request

TRADING_MODE = "PAPER"  # डिफ़ॉल्ट
PAPER_CAPITAL = 1000.00
current_balance = PAPER_CAPITAL
net_pnl = 0.00
paper_orders = []

MASTER_PIN = "NEERAJ_KING_SHIELD_2026"

# 🔒 सुरक्षा लॉक स्क्रीन (वही मिलिट्री-ग्रेड ताला)
SECURITY_GATE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 SECURITY CHECK</title>
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
            alert("❌ गलत सुरक्षा कोड!");
        }
    }
    </script>
</body>
</html>
"""

# 🎛️ जादुई 2-in-1 कंट्रोल पैनल (HTML/CSS जो मुख्य पेज को ट्रांसफॉर्म करेगा)
COMBINED_DASHBOARD_HTML = """
<div style="font-family: Arial, sans-serif; background-color: #0c0f12; color: #e1e6eb; text-align: center; padding: 0; margin: 0;">
    
    <!-- 🎛️ मुख्य पेज के मास्टर स्विच बटन -->
    <div style="display: flex; justify-content: center; gap: 10px; background: #1f242c; padding: 15px; border-bottom: 1px solid #30363d;">
        <button id="btnLiveMode" onclick="showSection('LIVE')" style="background-color: #21262d; color: white; border: 1px solid #30363d; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; flex: 1; max-width: 200px;">🏦 Live Demat Account</button>
        <button id="btnPaperMode" onclick="showSection('PAPER')" style="background-color: #238636; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; flex: 1; max-width: 200px;">📊 Live Paper Trading</button>
    </div>

    <!-- 📊 सेक्शन 2: पेपर ट्रेडिंग (यह मुख्य पेज पर ही दिखेगा) -->
    <div id="paperTradingSection" class="container" style="max-width: 800px; margin: 20px auto; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; display: block;">
        <h1 style="color:#00ff00; margin-top: 0;">🤖 ROBOT PAPER TRADING</h1>
        <p style="color:#8b949e; font-size:14px;">₹1000 के फिक्स बजट पर सुरक्षित पेपर ट्रेडिंग मोड</p>
        
        <div style="display: flex; justify-content: space-around; background: #21262d; padding: 15px; border-radius: 8px; margin: 20px 0; border: 1px solid #30363d;">
            <div>Starting: <span style="color:#0088cc; font-weight:bold;">₹1000.00</span></div>
            <div>Today P&L: <span id="uiPnl" style="color:#00ff00; font-weight:bold;">₹{NET_PNL}</span></div>
            <div>Balance: <span id="uiBalance" style="color:#00ff00; font-weight:bold;">₹{CURRENT_BALANCE}</span></div>
        </div>

        <table style="width: 100%; border-collapse: collapse; margin-top: 20px; background: #0d1117;">
            <thead>
                <tr style="background: #161b22; color: #00ff00;">
                    <th style="border: 1px solid #30363d; padding: 12px;">Time</th>
                    <th style="border: 1px solid #30363d; padding: 12px;">Index</th>
                    <th style="border: 1px solid #30363d; padding: 12px;">Type</th>
                    <th style="border: 1px solid #30363d; padding: 12px;">Qty</th>
                    <th style="border: 1px solid #30363d; padding: 12px;">Price</th>
                    <th style="border: 1px solid #30363d; padding: 12px;">Amount</th>
                    <th style="border: 1px solid #30363d; padding: 12px;">Status</th>
                </tr>
            </thead>
            <tbody>
                {ORDERS_ROWS}
            </tbody>
        </table>
    </div>
</div>

<script>
function showSection(mode) {
    var liveBox = document.querySelector('.container:not(#paperTradingSection)');
    var paperBox = document.getElementById('paperTradingSection');
    var btnLive = document.getElementById('btnLiveMode');
    var btnPaper = document.getElementById('btnPaperMode');

    if (mode === 'LIVE') {
        var password = prompt("🚨 सुरक्षा चेतावनी: रियल लाइव डीमैट मोड चालू करने के लिए सुरक्षा कोड दर्ज करें:");
        if (password === "NEERAJ_KING_SHIELD_2026") {
            if(liveBox) liveBox.style.display = 'block';
            paperBox.style.display = 'none';
            btnLive.style.backgroundColor = '#238636';
            btnLive.style.border = 'none';
            btnPaper.style.backgroundColor = '#21262d';
            btnPaper.style.border = '1px solid #30363d';
            fetch('/set-mode/REAL');
        } else {
            alert("❌ गलत सुरक्षा कोड! रियल मोड ऑन नहीं हो सकता।");
        }
    } else {
        if(liveBox) liveBox.style.display = 'none';
        paperBox.style.display = 'block';
        btnPaper.style.backgroundColor = '#238636';
        btnPaper.style.border = 'none';
        btnLive.style.backgroundColor = '#21262d';
        btnLive.style.border = '1px solid #30363d';
        fetch('/set-mode/PAPER');
    }
}

// डिफ़ॉल्ट रूप से ऐप खुलते ही लाइव वाले फॉर्म को छुपाओ और पेपर मोड दिखाओ
window.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(function(){
        var liveBox = document.querySelector('.container:not(#paperTradingSection)');
        if(liveBox) liveBox.style.display = 'none';
    }, 100);
});
</script>
"""

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
def inject_transformer_into_main_page(response):
    global current_balance, net_pnl, paper_orders
    if request.path == '/' and response.response and isinstance(response.response, bytes):
        try:
            html_content = response.response.decode('utf-8')
            body_tag = "<body>" if "<body>" in html_content else "<body"
            if body_tag in html_content and "paperTradingSection" not in html_content:
                orders_html = "".join([f"<tr><td style='border: 1px solid #30363d; padding: 12px;'>{o['time']}</td><td style='border: 1px solid #30363d; padding: 12px;'><strong>{o['index']}</strong></td><td style='border: 1px solid #30363d; padding: 12px;'>{o['type']}</td><td style='border: 1px solid #30363d; padding: 12px;'>{o['shares']}</td><td style='border: 1px solid #30363d; padding: 12px;'>₹{o['price']:.2f}</td><td style='border: 1px solid #30363d; padding: 12px;'>₹{o['amount']:.2f}</td><td style='border: 1px solid #30363d; padding: 12px; color:#00ff00;'>{o['status']} ✅</td></tr>" for o in paper_orders]) if paper_orders else "<tr><td colspan='7' style='border: 1px solid #30363d; padding: 12px; text-align:center; color:#888;'>आज अभी तक कोई आदेश नहीं लिया गया है।</td></tr>"
                
                formatted_transformer = COMBINED_DASHBOARD_HTML.format(
                    NET_PNL=f"{net_pnl:.2f}",
                    CURRENT_BALANCE=f"{current_balance:.2f}",
                    ORDERS_ROWS=orders_html
                )
                
                if body_tag == "<body>":
                    updated_html = html_content.replace("<body>", f"<body>{formatted_transformer}")
                else:
                    updated_html = html_content.replace("<body", f"{formatted_transformer}<body")
                response.set_data(updated_html.encode('utf-8'))
        except Exception as e:
            print(f"Transformation Error: {e}")
    return response

def execute_paper_trade(index_name, trade_type, entry_price, qty=15):
    global current_balance, net_pnl
    invested_amount = qty * entry_price
    if invested_amount > current_balance:
        return None
    trade_data = {
        "time": time.strftime("%I:%M %p"), "index": index_name, "type": trade_type,
        "shares": qty, "price": entry_price, "amount": invested_amount,
        "sl": entry_price * 0.90, "target": entry_price * 1.20, "status": "Running 🔄"
    }
    paper_orders.append(trade_data)
    return trade_data
# =====================================================================

if __name__ == '__main__':
    # रेंडर पोर्ट को ऑटोमैटिक पकड़ने के लिए सेटिंग
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


    
