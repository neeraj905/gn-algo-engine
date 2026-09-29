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
    
