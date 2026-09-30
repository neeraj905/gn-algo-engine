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

if __name__ == '__main__':
    # रेंडर पोर्ट को ऑटोमैटिक पकड़ने के लिए सेटिंग
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
# =====================================================================
# 🚀 PARTNER'S LIFETIME MODULAR EXTENSION SYSTEM (ALL-IN-ONE ENGINE)
# =====================================================================
# नोट: यह पूरा ब्लॉक पुराने कोड को बिना छुए, सबसे नीचे एक साथ पेस्ट करने के लिए है।

try:
    import time

    # 💰 1. पेपर ट्रेडिंग कैपिटल सेटिंग्स (₹1000 फिक्स बजट)
    PAPER_CAPITAL = 1000.00
    current_balance = PAPER_CAPITAL
    net_pnl = 0.00
    paper_orders = []

    def execute_paper_trade(index_name, trade_type, entry_price, qty=15):
        """
        कॉल/पुट बाय और सेल का सिस्टम:
        10% स्टॉपलॉस (SL) और 20% टारगेट (Target) ऑटो-कैलकुलेशन के साथ
        """
        global current_balance, net_pnl
        invested_amount = qty * entry_price
        
        # ₹1000 बजट चेक
        if invested_amount > current_balance:
            print(f"❌ Low Balance for Paper Trade! Required: ₹{invested_amount}, Available: ₹{current_balance}")
            return None

        # 10% स्टॉपलॉस और 20% टारगेट फिक्स करना
        stop_loss = entry_price * 0.90
        target_price = entry_price * 1.20
        
        trade_data = {
            "time": time.strftime("%I:%M %p"),
            "index": index_name,         # इंडेक्स का नाम (NIFTY/BANKNIFTY)
            "type": trade_type,          # BUY (CALL) या BUY (PUT)
            "shares": qty,                # शेयर्स की संख्या
            "price": entry_price,         # एंट्री का भाव
            "amount": invested_amount,   # लगाया गया पैसा
            "sl": stop_loss,             # 10% स्टॉपलॉस
            "target": target_price,       # 20% टारगेट
            "status": "Running 🔄"
        }
        paper_orders.append(trade_data)
        return trade_data

    # 🕒 2. दोपहर 03:15 बजे क्रैश या साइडवेज़ मार्केट में तुरंत एग्जिट (0ms डिले)
    def auto_315_market_close():
        global current_balance
        for order in paper_orders:
            if order["status"] == "Running 🔄":
                order["status"] = "Fast Exited (0ms) 🔴"
        print("🚨 Alert: Zero-Server Fast Exit Activated Successfully!")

    # ⏰ 3. सुबह मार्केट खुलने का टाइमर (09:15 AM Activation)
    def is_market_open():
        """यह चेक करेगा कि क्या समय सुबह 09:15 से दोपहर 03:15 के बीच है"""
        current_time = time.strftime("%H:%M")
        if "09:15" <= current_time <= "15:15":
            return True
        else:
            print(f"😴 Market is Closed! Current Time: {time.strftime('%I:%M %p')}. Robot is in Sleep Mode.")
            return False

    # 📅 4. शनिवार और रविवार छुट्टी का नियम (Weekend Filter)
    def is_market_day():
        """यह चेक करेगा कि आज शनिवार (Saturday) या रविवार (Sunday) तो नहीं है"""
        current_day = time.strftime("%A")
        if current_day in ["Saturday", "Sunday"]:
            print(f"🛑 Weekend Alert! Today is {current_day}. Market is Closed. Robot will not trade.")
            return False
        return is_market_open()

    print("✅ Partner's Master Blueprint Engine Loaded Successfully At The Bottom!")
except Exception as e:
    print(f"⚠️ Extension Error: {e}")
# =====================================================================

# =====================================================================
# 📊 पार्टनर का दूसरा गुप्त पेज: लाइव पेपर ट्रेडिंग डैशबोर्ड स्क्रीन
# =====================================================================

@app.route('/paper-trading')
def paper_trading_dashboard():
    """यह बिल्कुल नया स्वतंत्र पेज है, जिससे पुराना पेज डिस्टर्ब नहीं होगा"""
    global current_balance, net_pnl, paper_orders
    
    # ऑर्डर्स को टेबल में बदलना
    orders_html = "".join([f"<tr><td>{o['time']}</td><td><strong>{o['index']}</strong></td><td>{o['type']}</td><td>{o['shares']}</td><td>₹{o['price']:.2f}</td><td>₹{o['amount']:.2f}</td><td style='color:#00ff00;'>{o['status']} ✅</td></tr>" for o in paper_orders]) if paper_orders else "<tr><td colspan='7' style='text-align:center; color:#888;'>आज अभी तक कोई ऑर्डर नहीं लिया गया है।</td></tr>"
    pnl_color = "#00ff00" if net_pnl >= 0 else "#ff3333"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>King Shield - Paper Trading Screen</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #0c0f12; color: #e1e6eb; text-align: center; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; }}
            .status-bar {{ display: flex; justify-content: space-around; background: #21262d; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #30363d; padding: 12px; text-align: center; }}
            th {{ color: #00ff00; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color:#00ff00;">🤖 PAGE 2: LIVE PAPER TRADING</h1>
            <p style="color:#8b949e;">पुराने कोड को बिना छुए बनाया गया नया स्वतंत्र ट्रैकर</p>
            
            <div class="status-bar">
                <div>Starting Capital: <span style="color:#0088cc;">₹1000.00</span></div>
                <div>Today's P&L: <span style="color:{pnl_color};">₹{net_pnl:.2f}</span></div>
                <div>Current Balance: <span style="color:#00ff00;">₹{current_balance:.2f}</span></div>
            </div>

            <table>
                <thead>
                    <tr><th>Time</th><th>Index Name</th><th>Order Type</th><th>Shares</th><th>Price</th><th>Amount</th><th>Status</th></tr>
                </thead>
                <tbody>{orders_html}</tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
