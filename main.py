from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GN ALGO MATRIX</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0b0e14; color: #f8fafc; margin: 0; padding: 0; padding-bottom: 140px; }
        .header { background: #111827; padding: 14px; text-align: center; font-size: 16px; font-weight: bold; border-bottom: 1px solid #1f2937; letter-spacing: 0.5px; }
        .tab-content { display: none; padding: 12px; }
        .tab-content.active { display: block; }
        .card { background: #111827; border: 1px solid #1f2937; border-radius: 10px; padding: 14px; margin-bottom: 12px; }
        .card-title { font-size: 13px; color: #9ca3af; margin-bottom: 8px; text-transform: uppercase; font-weight: 600; }
        .flex-row { display: flex; justify-content: space-between; align-items: center; margin: 6px 0; font-size: 14px; }
        .price-green { color: #22c55e; font-weight: 600; }
        .price-red { color: #ef4444; font-weight: 600; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 6px; font-weight: bold; font-size: 13px; cursor: pointer; margin-top: 10px; }
        .btn-green { background: #16a34a; color: #fff; }
        
        .bottom-nav { position: fixed; bottom: 35px; left: 16px; width: calc(100% - 32px); background: #111827; display: flex; justify-content: space-around; padding: 14px 0; border: 1px solid #1f2937; border-radius: 14px; z-index: 99999; box-shadow: 0 10px 25px rgba(0,0,0,0.9); }
        .nav-item { color: #9ca3af; text-decoration: none; font-size: 11px; font-weight: 600; text-align: center; cursor: pointer; }
        .nav-item.active { color: #38bdf8; }
        .log-box { background: #030712; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 11px; color: #38bdf8; height: 100px; overflow-y: auto; border: 1px solid #1f2937; }
        .input-field { width: 100%; padding: 10px; margin: 6px 0 10px 0; background: #030712; border: 1px solid #374151; border-radius: 6px; color: #fff; box-sizing: border-box; font-size: 13px; }
        
        #splash-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0b0e14; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 99999; transition: opacity 0.5s ease; }
        .splash-logo { font-size: 24px; font-weight: 900; color: #38bdf8; letter-spacing: 2px; margin-bottom: 10px; }
        .splash-sub { font-size: 12px; color: #9ca3af; }
    </style>
</head>
<body>

    <div id="splash-screen">
        <div class="splash-logo">GN ALGO MATRIX</div>
        <div class="splash-sub">Initializing Secure Trading Gateway...</div>
    </div>

    <div class="header">GN ALGO MATRIX</div>

    <div id="tab-dashboard" class="tab-content active">
        <div class="card">
            <div class="card-title">Live Market Ticker</div>
            <div class="flex-row"><span>NIFTY 50</span><span class="price-green">₹24,850.10</span></div>
            <div class="flex-row"><span>BANKNIFTY</span><span class="price-green">₹51,200.50</span></div>
        </div>

        <div class="card">
            <div class="card-title">Paper Account Overview</div>
            <div class="flex-row"><span>Initial Capital:</span><span>₹10,000.00</span></div>
            <div class="flex-row"><span>Available Margin:</span><span id="paper-balance" style="color:#38bdf8; font-weight:bold;">₹10,000.00</span></div>
            <div class="flex-row"><span>Realized P&L:</span><span id="paper-pnl" class="price-green">₹0.00</span></div>
        </div>

        <div class="card">
            <div class="card-title">Live Event Logs</div>
            <div class="log-box" id="event-log">[INFO] System booted with LocalStorage active.</div>
        </div>
    </div>

    <div id="tab-wizard" class="tab-content">
        <div class="card">
            <div class="card-title">Quick Test Order (Paper)</div>
            <div class="flex-row"><span>Target Symbol:</span><span>NIFTY 24850 CE</span></div>
            <div class="flex-row"><span>Required Margin:</span><span>₹700.00</span></div>
            <button class="btn btn-green" onclick="executePaperTrade()">EXECUTE TEST BUY</button>
        </div>
    </div>

    <div id="tab-strategies" class="tab-content">
        <div class="card">
            <div class="card-title">Active Strategy</div>
            <div class="flex-row"><strong>NAP v3 Paper Algo</strong> <span style="background:#0284c7; padding:2px 6px; border-radius:4px; font-size:10px;">Min Capital: ₹10,000</span></div>
            <div class="flex-row" style="margin-top:8px;"><span>Mode:</span><span style="color:#22c55e;">Paper Trading</span></div>
        </div>
    </div>

    <div id="tab-watchlist" class="tab-content">
        <div class="card">
            <div class="card-title">Watchlist</div>
            <div class="flex-row"><span>NIFTY 24850 CE</span><span class="price-green">₹35.00</span></div>
        </div>
    </div>

    <div id="tab-more" class="tab-content">
        <div class="card">
            <div class="card-title">Multi-Demat Account Manager (Angel One)</div>
            <label style="font-size:11px; color:#9ca3af;">Select Demat Account Slot</label>
            <select id="demat-slot" class="input-field" onchange="loadAccountData()">
                <option value="account1">Default Account (Angel One)</option>
                <option value="account2">Account 2 (Secondary)</option>
            </select>
            
            <label style="font-size:11px; color:#9ca3af;">Client ID / User ID</label>
            <input type="text" id="client-id" class="input-field" placeholder="Enter Client ID">
            
            <label style="font-size:11px; color:#9ca3af;">API Key</label>
            <input type="password" id="api-key" class="input-field" placeholder="Enter API Key">

            <label style="font-size:11px; color:#9ca3af;">Secret / PIN / TOTP Token</label>
            <input type="password" id="api-secret" class="input-field" placeholder="Enter Secret Key or MPIN">

            <button class="btn btn-green" onclick="saveAccountData()">SAVE & CONNECT ACCOUNT</button>
        </div>
    </div>

    <div class="bottom-nav">
        <div class="nav-item active" onclick="switchTab('dashboard', this)">Dashboard</div>
        <div class="nav-item" onclick="switchTab('wizard', this)">Wizard</div>
        <div class="nav-item" onclick="switchTab('strategies', this)">Strategies</div>
        <div class="nav-item" onclick="switchTab('watchlist', this)">Watchlist</div>
        <div class="nav-item" onclick="switchTab('more', this)">More</div>
    </div>

    <script>
        window.addEventListener('load', () => {
            setTimeout(() => {
                const splash = document.getElementById('splash-screen');
                splash.style.opacity = '0';
                setTimeout(() => splash.style.display = 'none', 500);
            }, 1000);
            loadAccountData();
        });

        let paperCapital = 10000.00;
        let realizedPnl = 0.00;

        function switchTab(tabName, el) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('tab-' + tabName).classList.add('active');
            el.classList.add('active');
        }

        function saveAccountData() {
            const slot = document.getElementById('demat-slot').value;
            const data = {
                uid: document.getElementById('client-id').value,
                key: document.getElementById('api-key').value,
                secret: document.getElementById('api-secret').value
            };
            if(!data.uid || !data.key || !data.secret) {
                alert('Please fill all three credential fields!');
                return;
            }
            localStorage.setItem('gn_algo_' + slot, JSON.stringify(data));
            addLog('Credentials saved successfully for ' + slot.toUpperCase());
            alert('Account saved safely in browser storage!');
        }

        function loadAccountData() {
            const slot = document.getElementById('demat-slot').value;
            const saved = localStorage.getItem('gn_algo_' + slot);
            if(saved) {
                const data = JSON.parse(saved);
                document.getElementById('client-id').value = data.uid || '';
                document.getElementById('api-key').value = data.key || '';
                document.getElementById('api-secret').value = data.secret || '';
            } else {
                document.getElementById('client-id').value = '';
                document.getElementById('api-key').value = '';
                document.getElementById('api-secret').value = '';
            }
        }

        function executePaperTrade() {
            let requiredMargin = 700.00;
            if(requiredMargin > paperCapital) {
                alert('Insufficient Capital!');
                return;
            }
            paperCapital -= requiredMargin;
            realizedPnl += 155.00;
            document.getElementById('paper-balance').innerText = '₹' + paperCapital.toFixed(2);
            document.getElementById('paper-pnl').innerText = '+₹' + realizedPnl.toFixed(2);
            addLog('EXECUTED: Paper Trade | Margin: ₹' + requiredMargin);
        }

        function addLog(msg) {
            const logBox = document.getElementById('event-log');
            const time = new Date().toLocaleTimeString();
            logBox.innerHTML = '[' + time + '] ' + msg + '<br>' + logBox.innerHTML;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content
