from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import asyncio
import random
from datetime import datetime

app = FastAPI()

server_state = {
    "trading_mode": "PAPER",
    "capital": 10000.0,
    "today_pnl": 0.0,
    "active_positions": 0,
    "engine_status": "RUNNING (PAPER MODE)",
    "max_loss_limit": -250.0,
    "accounts": [
        {"id": 1, "name": "Paper Trading Sandbox", "client_id": "PAPER_DEMO_01", "api_key": "sandbox_key", "capital": 10000.0, "active": True}
    ],
    "custom_strategies": [
        {"id": 1, "name": "NIFTY Strategies Basket V2", "indicator": "Supertrend", "target": 2.0, "sl": 1.0, "status": "Active"}
    ]
}

def update_risk_limits(cap):
    if cap <= 1000: return -50.0
    elif cap <= 10000: return -250.0
    else: return -2500.0

async def pnl_simulation_loop():
    while True:
        try:
            now = datetime.now()
            is_weekday = now.weekday() < 5
            curr_val = now.hour * 100 + now.minute
            is_market = is_weekday and (915 <= curr_val <= 1530)
            active_accs = [acc for acc in server_state["accounts"] if acc["active"]]
            time_12 = now.strftime("%I:%M %p")
            mode_lbl = "PAPER MODE" if server_state["trading_mode"] == "PAPER" else "LIVE MODE"
            
            if is_market and len(active_accs) > 0:
                server_state["engine_status"] = f"RUNNING ({mode_lbl} - {time_12})"
                server_state["active_positions"] = len(active_accs)
                total_cap = sum(acc["capital"] for acc in active_accs)
                server_state["capital"] = total_cap
                server_state["max_loss_limit"] = update_risk_limits(total_cap)
                
                if server_state["today_pnl"] > server_state["max_loss_limit"]:
                    step = total_cap * random.uniform(-0.003, 0.004)
                    server_state["today_pnl"] += round(step, 2)
                    if server_state["today_pnl"] <= server_state["max_loss_limit"]:
                        server_state["today_pnl"] = server_state["max_loss_limit"]
                        server_state["engine_status"] = f"STOPPED (SL HIT) at {time_12}"
            else:
                server_state["engine_status"] = f"IDLE ({time_12} - MARKET CLOSED)"
                server_state["active_positions"] = 0
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(pnl_simulation_loop())

@app.get("/api/state")
def get_state():
    return server_state

@app.post("/api/mode/toggle")
async def toggle_mode(request: Request):
    data = await request.json()
    mode = data.get("mode", "PAPER")
    server_state["trading_mode"] = mode
    if mode == "PAPER":
        server_state["accounts"] = [
            {"id": 1, "name": "Paper Trading Sandbox", "client_id": "PAPER_DEMO_01", "api_key": "sandbox_key", "capital": 10000.0, "active": True}
        ]
    server_state["capital"] = sum(acc["capital"] for acc in server_state["accounts"] if acc["active"])
    server_state["max_loss_limit"] = update_risk_limits(server_state["capital"])
    return {"status": "success", "state": server_state}

@app.post("/api/strategy/add")
async def add_strategy(request: Request):
    data = await request.json()
    new_strat = {
        "id": len(server_state["custom_strategies"]) + 1,
        "name": data.get("name", "Custom Strategy"),
        "indicator": data.get("indicator", "EMA Crossover"),
        "target": float(data.get("target", 2.0)),
        "sl": float(data.get("sl", 1.0)),
        "status": "Active"
    }
    server_state["custom_strategies"].append(new_strat)
    return {"status": "success", "strategies": server_state["custom_strategies"]}

@app.post("/api/accounts/add")
async def add_account(request: Request):
    data = await request.json()
    new_acc = {
        "id": len(server_state["accounts"]) + 1,
        "name": data.get("name", "User Account"),
        "client_id": data.get("client_id", "ID_UNKNOWN"),
        "api_key": data.get("api_key", ""),
        "capital": float(data.get("capital", 10000.0)),
        "active": True
    }
    server_state["accounts"].append(new_acc)
    server_state["capital"] = sum(acc["capital"] for acc in server_state["accounts"] if acc["active"])
    server_state["max_loss_limit"] = update_risk_limits(server_state["capital"])
    return {"status": "success", "accounts": server_state["accounts"]}

@app.post("/api/accounts/toggle/{acc_id}")
def toggle_account(acc_id: int):
    for acc in server_state["accounts"]:
        if acc["id"] == acc_id: acc["active"] = not acc["active"]
    active_accs = [acc for acc in server_state["accounts"] if acc["active"]]
    server_state["capital"] = sum(acc["capital"] for acc in active_accs) if active_accs else 0.0
    server_state["max_loss_limit"] = update_risk_limits(server_state["capital"])
    return {"status": "success", "accounts": server_state["accounts"]}

@app.post("/api/accounts/delete/{acc_id}")
def delete_account(acc_id: int):
    server_state["accounts"] = [acc for acc in server_state["accounts"] if acc["id"] != acc_id]
    active_accs = [acc for acc in server_state["accounts"] if acc["active"]]
    server_state["capital"] = sum(acc["capital"] for acc in active_accs) if active_accs else 0.0
    server_state["max_loss_limit"] = update_risk_limits(server_state["capital"])
    return {"status": "success", "accounts": server_state["accounts"]}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GN ALGO MATRIX</title>
    <style>
        :root { --bg: #0f172a; --card: #1e293b; --text: #f8fafc; --muted: #94a3b8; --accent: #38bdf8; --green: #22c55e; --red: #ef4444; --border: #334155; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: sans-serif; }
        body { background: var(--bg); color: var(--text); padding-bottom: 80px; }
        header { text-align: center; padding: 15px; font-weight: bold; background: #020617; border-bottom: 1px solid var(--border); color: var(--accent); }
        .container { padding: 12px; max-width: 600px; margin: 0 auto; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 15px; margin-bottom: 12px; }
        .card-title { font-size: 0.9rem; font-weight: 600; color: var(--muted); margin-bottom: 10px; text-transform: uppercase; display: flex; justify-content: space-between; align-items: center; }
        .flex-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 0.9rem; }
        .badge { padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; }
        .badge-green { background: rgba(34,197,94,0.15); color: var(--green); }
        .badge-red { background: rgba(239,68,68,0.15); color: var(--red); }
        .badge-yellow { background: rgba(234,179,8,0.15); color: #eab308; }
        .form-group { margin-bottom: 10px; }
        .form-group label { display: block; font-size: 0.8rem; color: var(--muted); margin-bottom: 4px; }
        .form-control { width: 100%; padding: 10px; background: #0f172a; border: 1px solid var(--border); color: #fff; border-radius: 8px; font-size: 0.9rem; }
        .btn-primary { width: 100%; padding: 12px; background: var(--green); color: #000; font-weight: bold; border: none; border-radius: 8px; cursor: pointer; }
        .btn-danger { background: var(--red); color: #fff; border: none; padding: 5px 10px; border-radius: 6px; cursor: pointer; font-size: 0.75rem; }
        .mode-selector { display: flex; background: #0f172a; border-radius: 8px; padding: 4px; border: 1px solid var(--border); margin-bottom: 12px; }
        .mode-btn { flex: 1; padding: 8px; text-align: center; background: transparent; border: none; color: var(--muted); font-weight: bold; font-size: 0.8rem; border-radius: 6px; cursor: pointer; }
        .mode-btn.active-paper { background: rgba(234,179,8,0.2); color: #eab308; }
        .mode-btn.active-live { background: rgba(239,68,68,0.2); color: var(--red); }
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #020617; border-top: 1px solid var(--border); display: flex; justify-content: space-around; padding: 10px 0 20px 0; z-index: 1000; }
        .nav-item { background: none; border: none; color: var(--muted); font-size: 0.75rem; display: flex; flex-direction: column; align-items: center; cursor: pointer; width: 20%; }
        .nav-item.active { color: var(--accent); font-weight: bold; }
        .nav-item svg { width: 20px; height: 20px; margin-bottom: 3px; fill: currentColor; }
    </style>
</head>
<body>
    <header>GN ALGO MATRIX</header>
    <div class="container">
        <div id="tab-dashboard" class="tab-content active">
            <div class="card">
                <div class="card-title">Trading Mode <span id="mode-badge" class="badge badge-yellow">PAPER</span></div>
                <div class="mode-selector">
                    <button id="btn-paper" class="mode-btn active-paper" onclick="switchMode('PAPER')">🟢 Paper Trading</button>
                    <button id="btn-live" class="mode-btn" onclick="switchMode('LIVE')">🔴 Live Trading</button>
                </div>
            </div>
            <div class="card">
                <div class="card-title">Engine Status</div>
                <div class="flex-row"><span>Status</span><span id="engine-status" class="badge badge-green">Loading...</span></div>
                <div class="flex-row"><span>Active Capital</span><span id="txt-capital">₹10,000</span></div>
                <div class="flex-row"><span>Max Risk (SL)</span><span id="txt-risk" style="color:var(--red);">-₹250</span></div>
            </div>
            <div class="card">
                <div class="card-title">Performance</div>
                <div class="flex-row"><span>Today's P&L</span><span id="live-pnl" class="badge badge-green">+₹0.00</span></div>
                <div class="flex-row"><span>Active Positions</span><span id="active-pos">0</span></div>
            </div>
        </div>

        <div id="tab-wizard" class="tab-content">
            <div class="card">
                <div class="card-title">Strategy Wizard</div>
                <form id="wizard-form" onsubmit="createStrategy(event)">
                    <div class="form-group"><label>Strategy Name</label><input type="text" id="wiz-name" class="form-control" placeholder="e.g. Nifty Alpha" required></div>
                    <div class="form-group"><label>Indicator</label><select id="wiz-indicator" class="form-control"><option value="EMA Crossover">EMA Crossover</option><option value="Supertrend">Supertrend</option></select></div>
                    <div class="form-group"><label>Target (%)</label><input type="number" step="0.1" id="wiz-target" class="form-control" value="2.0" required></div>
                    <div class="form-group"><label>Stop Loss (%)</label><input type="number" step="0.1" id="wiz-sl" class="form-control" value="1.0" required></div>
                    <button type="submit" class="btn-primary">DEPLOY STRATEGY</button>
                </form>
            </div>
        </div>

        <div id="tab-strategies" class="tab-content">
            <div class="card">
                <div class="card-title">Strategies Basket</div>
                <div id="strategies-list"></div>
            </div>
        </div>

        <div id="tab-watchlist" class="tab-content">
            <div class="card">
                <div class="card-title">Nifty Live Chart</div>
                <div style="height: 400px; width: 100%;">
                    <div class="tradingview-widget-container" style="height:100%;width:100%">
                        <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
                        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
                        { "autosize": true, "symbol": "NSE:NIFTY", "interval": "5", "timezone": "Asia/Kolkata", "theme": "dark", "style": "1", "locale": "en", "enable_publishing": false, "calendar": false }
                        </script>
                    </div>
                </div>
            </div>
        </div>

        <div id="tab-more" class="tab-content">
            <div class="card">
                <div class="card-title">Add Demat Account</div>
                <form id="account-form" onsubmit="addAccount(event)">
                    <div class="form-group"><label>Broker Name</label><input type="text" id="acc-name" class="form-control" placeholder="Angel One / Zerodha" required></div>
                    <div class="form-group"><label>Client ID</label><input type="text" id="acc-clientid" class="form-control" placeholder="Client ID" required></div>
                    <div class="form-group"><label>API Key</label><input type="text" id="acc-apikey" class="form-control" placeholder="API Key" required></div>
                    <div class="form-group"><label>Capital (₹)</label><input type="number" id="acc-capital" class="form-control" value="10000" min="1000" required></div>
                    <button type="submit" class="btn-primary">SAVE ACCOUNT</button>
                </form>
            </div>
            <div class="card">
                <div class="card-title">Manage Accounts</div>
                <div id="accounts-list"></div>
            </div>
        </div>
    </div>

    <nav class="bottom-nav">
        <button class="nav-item active" onclick="switchTab('dashboard', this)"><svg viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>Dashboard</button>
        <button class="nav-item" onclick="switchTab('wizard', this)"><svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/></svg>Wizard</button>
        <button class="nav-item" onclick="switchTab('strategies', this)"><svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/></svg>Strategies</button>
        <button class="nav-item" onclick="switchTab('watchlist', this)"><svg viewBox="0 0 24 24"><path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z"/></svg>Watchlist</button>
        <button class="nav-item" onclick="switchTab('more', this)"><svg viewBox="0 0 24 24"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z"/></svg>More</button>
    </nav>

    <script>
        function switchTab(id, btn) {
            document.querySelectorAll('.tab-content').forEach(e => e.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(e => e.classList.remove('active'));
            document.getElementById('tab-' + id).classList.add('active');
            btn.classList.add('active');
        }
        async function switchMode(m) {
            let res = await fetch('/api/mode/toggle', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({mode: m})});
            let data = await res.json();
            updateUI(data.state);
        }
        function updateUI(d) {
            document.getElementById('engine-status').innerText = d.engine_status;
            document.getElementById('txt-capital').innerText = '₹' + d.capital.toLocaleString('en-IN');
            document.getElementById('txt-risk').innerText = '-₹' + Math.abs(d.max_loss_limit).toLocaleString('en-IN');
            document.getElementById('active-pos').innerText = d.active_positions;
            let badge = document.getElementById('mode-badge'), bp = document.getElementById('btn-paper'), bl = document.getElementById('btn-live');
            if(d.trading_mode === 'PAPER') {
                badge.innerText = 'PAPER'; badge.className = 'badge badge-yellow';
                bp.className = 'mode-btn active-paper'; bl.className = 'mode-btn';
            } else {
                badge.innerText = 'LIVE'; badge.className = 'badge badge-red';
                bl.className = 'mode-btn active-live'; bp.className = 'mode-btn';
            }
            let pnl = document.getElementById('live-pnl'), val = d.today_pnl;
            pnl.innerText = (val >= 0 ? '+₹' : '-₹') + Math.abs(val).toLocaleString('en-IN', {minimumFractionDigits: 2});
            pnl.className = val >= 0 ? "badge badge-green" : "badge badge-red";
            
            let accHtml = '';
            d.accounts.forEach(a => {
                accHtml += `<div class="flex-row" style="background:#0f172a;padding:8px;border-radius:6px;margin-bottom:6px;"><div><strong>${a.name}</strong><br><small style="color:var(--muted)">ID: ${a.client_id}</small></div><button class="btn-danger" onclick="delAcc(${a.id})">Delete</button></div>`;
            });
            document.getElementById('accounts-list').innerHTML = accHtml;
            
            let stHtml = '';
            d.custom_strategies.forEach(s => {
                stHtml += `<div class="flex-row" style="background:#0f172a;padding:8px;border-radius:6px;margin-bottom:6px;"><div><strong>${s.name}</strong><br><small style="color:var(--muted)">Tgt: ${s.target}% | SL: ${s.sl}%</small></div><span class="badge badge-green">${s.status}</span></div>`;
            });
            document.getElementById('strategies-list').innerHTML = stHtml;
        }
        async function fetchData() {
            try { let res = await fetch('/api/state'); let d = await res.json(); updateUI(d); } catch(e){}
        }
        async function createStrategy(e) {
            e.preventDefault();
            let body = {name: document.getElementById('wiz-name').value, indicator: document.getElementById('wiz-indicator').value, target: document.getElementById('wiz-target').value, sl: document.getElementById('wiz-sl').value};
            let res = await fetch('/api/strategy/add', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
            if((await res.json()).status === 'success') { document.getElementById('wizard-form').reset(); switchTab('strategies', document.querySelectorAll('.nav-item')[2]); fetchData(); }
        }
        async function addAccount(e) {
            e.preventDefault();
            let body = {name: document.getElementById('acc-name').value, client_id: document.getElementById('acc-clientid').value, api_key: document.getElementById('acc-apikey').value, capital: document.getElementById('acc-capital').value};
            let res = await fetch('/api/accounts/add', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
            if((await res.json()).status === 'success') { document.getElementById('account-form').reset(); fetchData(); }
        }
        async function delAcc(id) {
            if(confirm('Delete account?')) { await fetch('/api/accounts/delete/' + id, {method:'POST'}); fetchData(); }
        }
        setInterval(fetchData, 3000);
        fetchData();
    </script>
</body>
</html>
    """
                
