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
# 🎛️ PARTNER'S 2-IN-1 MASTER SWITCH FIXED ENGINE (NO INJECTION ERRORS)
# =====================================================================
import time
from flask import render_template_string, jsonify, request

TRADING_MODE = "PAPER"  # डिफ़ॉल्ट रूप से पेपर मोड चालू रहेगा
PAPER_CAPITAL = 1000.00
current_balance = PAPER_CAPITAL
net_pnl = 0.00
paper_orders = []

MASTER_PIN = "NEERAJ_KING_SHIELD_2026"

# 🔒 मिलिट्री-ग्रेड सुरक्षा लॉक स्क्रीन
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

# 🔒 सुरक्षा गेटकीपर मिडलवेयर
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

# 📊 यह बिल्कुल नया स्वतंत्र पेपर ट्रेडिंग पेज है, जो सीधे मेनू से खुलेगा
@app.route('/paper-trading')
def paper_trading_dashboard():
    global current_balance, net_pnl, paper_orders
    orders_html = "".join([f"<tr><td style='border: 1px solid #30363d; padding: 12px;'>{o['time']}</td><td style='border: 1px solid #30363d; padding: 12px;'><strong>{o['index']}</strong></td><td style='border: 1px solid #30363d; padding: 12px;'>{o['type']}</td><td style='border: 1px solid #30363d; padding: 12px;'>{o['shares']}</td><td style='border: 1px solid #30363d; padding: 12px;'>₹{o['price']:.2f}</td><td style='border: 1px solid #30363d; padding: 12px;'>₹{o['amount']:.2f}</td><td style='border: 1px solid #30363d; padding: 12px; color:#00ff00;'>{o['status']} ✅</td></tr>" for o in paper_orders]) if paper_orders else "<tr><td colspan='7' style='border: 1px solid #30363d; padding: 12px; text-align:center; color:#888;'>आज अभी तक कोई आदेश नहीं लिया गया है।</td></tr>"
    pnl_color = "#00ff00" if net_pnl >= 0 else "#ff3333"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>King Shield - Paper Trading</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #0c0f12; color: #e1e6eb; text-align: center; margin: 0; padding: 0; }}
            .menu-bar {{ display: flex; justify-content: center; gap: 10px; background: #1f242c; padding: 15px; border-bottom: 1px solid #30363d; }}
            .menu-btn {{ background-color: #21262d; color: white; border: 1px solid #30363d; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none; font-size:14px; }}
            .container {{ max-width: 800px; margin: 20px auto; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; }}
            .status-bar {{ display: flex; justify-content: space-around; background: #21262d; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #30363d; padding: 12px; text-align: center; }}
            th {{ color: #00ff00; }}
        </style>
    </head>
    <body>
        <div class="menu-bar">
            <button onclick="var p=prompt('🚨 सुरक्षा कोड दर्ज करें:'); if(p==='NEERAJ_KING_SHIELD_2026'){{ location.href='/'; }} else {{ alert('❌ Wrong code!'); }}" class="menu-btn">🏦 Live Demat Account</button>
            <a href="/paper-trading" class="menu-btn" style="background-color: #238636; border: none;">📊 Live Paper Trading</a>
        </div>
        <div class="container">
            <h1 style="color:#00ff00;">🤖 ROBOT PAPER TRADING</h1>
            <p style="color:#8b949e;">₹1000 के फिक्स बजट पर सुरक्षित पेपर ट्रेडिंग मोड</p>
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

# =====================================================================
# 🎛️ PARTNER'S MASTER SWITCH LAYOUT ENGINE (ADD AT THE VERY BOTTOM)
# =====================================================================

# पुराने पहले पेज के HTML के ऊपर मेनू बार को साफ और फिक्स तरीके से जोड़ने के लिए नया मिडलवेयर
@app.after_request
def inject_clean_menu(response):
    if request.path == '/' and response.response and isinstance(response.response, bytes):
        try:
            html_content = response.response.decode('utf-8')
            # यह आपके पहले पेज पर दोनों जादुई मास्टर बटन फिट कर देगा
            custom_menu = """
            <div style="display: flex; justify-content: center; gap: 10px; background: #1f242c; padding: 15px; border-bottom: 1px solid #30363d; font-family: Arial, sans-serif;">
                <button onclick="var p=prompt('🚨 सुरक्षा कोड दर्ज करें:'); if(p==='NEERAJ_KING_SHIELD_2026'){ fetch('/set-mode/REAL'); alert('🏦 Live mode activated!'); } else { alert('❌ Wrong code!'); }" style="background-color: #238636; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer;">🏦 Live Demat Account</button>
                <a href="/paper-trading" style="background-color: #21262d; color: white; border: 1px solid #30363d; padding: 10px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; text-decoration: none;">📊 Live Paper Trading</a>
            </div>
            """
            body_tag = "<body>" if "<body>" in html_content else "<body"
            if body_tag in html_content and "Live Paper Trading" not in html_content:
                if body_tag == "<body>":
                    updated_html = html_content.replace("<body>", f"<body>{custom_menu}")
                else:
                    updated_html = html_content.replace("<body", f"{custom_menu}<body")
                response.set_data(updated_html.encode('utf-8'))
        except Exception as e:
            print(f"Menu Error: {e}")
    return response
# =====================================================================

    
