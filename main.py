import os
import time
import math
import random
import threading
from datetime import datetime, time as dtime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr

app = FastAPI(title="GN Algo Matrix Professional Dashboard", version="3.1.0")

server_state = {
    "auth": {"logged_in": False, "email": ""},
    "global_trading_mode": "PAPER",
    "engine_status": "IDLE",
    "market_session": "INDIAN",
    "active_capital": 1000.0,
    "max_risk_limit": -50.0,
    "today_pnl": 0.0,
    "active_positions_count": 0,
    "kill_switch_active": False,
    "api_connection_status": "HEALTHY",
    "accounts": [
        {
            "id": 1,
            "name": "Primary Sandbox Account",
            "client_id": "GN_DEMO_01",
            "api_key": "sample_api_key_123",
            "totp_key": "JBSWY3DPEHPK3PXP",
            "active": True,
            "capital": 1000.0,
            "pnl": 0.0,
            "positions": []
        }
    ],
    "trades_history": [],
    "watchlist_india": ["NIFTY 50", "BANK NIFTY", "SENSEX", "FINNIFTY"],
    "watchlist_us": ["S&P 500", "NASDAQ 100", "DOW JONES", "RUSSELL 2000"]
}

class LoginRequest(BaseModel):
    email: EmailStr

class AccountConfig(BaseModel):
    name: str
    client_id: str
    api_key: str
    totp_key: str
    capital: float

class OrderExecutionRequest(BaseModel):
    account_id: int
    symbol: str
    action: str
    product_type: str
    quantity: int
    price: float

def background_trading_engine():
    while True:
        time.sleep(3)
        if server_state["engine_status"] != "RUNNING" or server_state["kill_switch_active"]:
            continue
        if datetime.now().time() >= dtime(15, 15):
            force_square_off_all("Market Auto Square-Off Time (3:15 PM) Reached.")
            continue
        total_portfolio_pnl = 0.0
        active_count = 0
        for acc in server_state["accounts"]:
            if not acc["active"]: continue
            acc_pnl = 0.0
            for pos in list(acc["positions"]):
                active_count += 1
                pos["current_price"] = round(pos["current_price"] + random.uniform(-1.5, 1.8), 2)
                diff = (pos["current_price"] - pos["entry_price"]) if pos["action"] == "BUY" else (pos["entry_price"] - pos["current_price"])
                pos["pnl"] = round(diff * pos["quantity"], 2)
                sl_price = pos["entry_price"] * 0.98 if pos["action"] == "BUY" else pos["entry_price"] * 1.02
                if (pos["current_price"] <= sl_price and pos["action"] == "BUY") or (pos["current_price"] >= sl_price and pos["action"] == "SELL"):
                    server_state["trades_history"].insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "account": acc["name"], "symbol": pos["symbol"], "event": "STOP-LOSS HIT", "pnl": pos["pnl"]})
                    acc["pnl"] += pos["pnl"]
                    acc["positions"].remove(pos)
                    continue
                acc_pnl += pos["pnl"]
            acc["pnl"] = round(acc_pnl, 2)
            total_portfolio_pnl += acc["pnl"]
        server_state["today_pnl"] = round(total_portfolio_pnl, 2)
        server_state["active_positions_count"] = active_count
        if server_state["today_pnl"] <= server_state["max_risk_limit"]:
            force_square_off_all("Max Risk Limit Breached!")

engine_thread = threading.Thread(target=background_trading_engine, daemon=True)
engine_thread.start()

def force_square_off_all(reason: str):
    server_state["kill_switch_active"] = True
    server_state["engine_status"] = "HALTED (KILL SWITCH)"
    for acc in server_state["accounts"]:
        for pos in list(acc["positions"]):
            server_state["trades_history"].insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "account": acc["name"], "symbol": pos["symbol"], "event": f"SQUARE OFF: {reason}", "pnl": pos["pnl"]})
            acc["positions"].remove(pos)
    server_state["active_positions_count"] = 0

@app.get("/", response_class=HTMLResponse)
def serve_dashboard(): return HTML_TEMPLATE

@app.post("/api/auth/login")
def api_login(data: LoginRequest):
    server_state["auth"]["logged_in"] = True
    server_state["auth"]["email"] = data.email
    return {"status": "success"}

@app.get("/api/state")
def get_system_state(): return server_state

@app.post("/api/engine/toggle")
def toggle_engine(status: str):
    server_state["engine_status"] = status if status == "RUNNING" else "PAUSED"
    return {"status": "success"}

@app.post("/api/trading-mode/toggle")
def toggle_trading_mode(mode: str):
    server_state["global_trading_mode"] = mode
    return {"status": "success"}

@app.post("/api/kill-switch/trigger")
def trigger_kill_switch():
    force_square_off_all("Manual Kill Switch")
    return {"status": "success"}

@app.post("/api/kill-switch/reset")
def reset_kill_switch():
    server_state["kill_switch_active"] = False
    server_state["engine_status"] = "IDLE"
    return {"status": "success"}

@app.post("/api/accounts/add")
def add_demat_account(acc: AccountConfig):
    if len(server_state["accounts"]) >= 5: raise HTTPException(status_code=400, detail="Max 5 accounts.")
    new_id = max([a["id"] for a in server_state["accounts"]], default=0) + 1
    max_loss = -50.0 if acc.capital <= 1000 else (-250.0 if acc.capital <= 10000 else -(acc.capital * 0.025))
    server_state["accounts"].append({"id": new_id, "name": acc.name, "client_id": acc.client_id, "api_key": acc.api_key, "totp_key": acc.totp_key, "active": True, "capital": acc.capital, "pnl": 0.0, "positions": []})
    server_state["max_risk_limit"] = min(server_state["max_risk_limit"], max_loss)
    return {"status": "success"}

@app.post("/api/accounts/{account_id}/toggle")
def toggle_account(account_id: int):
    for acc in server_state["accounts"]:
        if acc["id"] == account_id: acc["active"] = not acc["active"]
    return {"status": "success"}

@app.delete("/api/accounts/{account_id}")
def delete_account(account_id: int):
    global server_state
    server_state["accounts"] = [a for a in server_state["accounts"] if a["id"] != account_id]
    return {"status": "success"}

@app.post("/api/orders/execute")
def execute_order(order: OrderExecutionRequest):
    target_acc = next((a for a in server_state["accounts"] if a["id"] == order.account_id), None)
    if not target_acc: raise HTTPException(status_code=400)
    target_acc["positions"].append({"id": random.randint(10000, 99999), "symbol": order.symbol, "action": order.action, "product_type": order.product_type, "quantity": order.quantity, "entry_price": order.price, "current_price": order.price, "pnl": 0.0, "time": datetime.now().strftime("%H:%M:%S")})
    return {"status": "success"}
            HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GN ALGO MATRIX</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root { --bg-primary: #0b0e14; --bg-secondary: #161b22; --bg-card: #21262d; --accent-green: #238636; --accent-red: #da3633; --accent-blue: #1f6feb; --text-main: #c9d1d9; --text-muted: #8b949e; --border-color: #30363d; }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; word-wrap: break-word; }
        body { background-color: var(--bg-primary); color: var(--text-main); display: flex; justify-content: center; min-height: 100vh; }
        .app-container { width: 100%; max-width: 480px; background-color: var(--bg-secondary); display: flex; flex-direction: column; position: relative; border: 1px solid var(--border-color); }
        header { padding: 16px; background-color: var(--bg-card); display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); }
        .logo { font-size: 16px; font-weight: 800; color: #58a6ff; }
        .content-area { flex: 1; overflow-y: auto; padding: 16px; padding-bottom: 90px; }
        .hidden { display: none !important; }
        .card { background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: 8px; padding: 14px; margin-bottom: 14px; }
        .card-title { font-size: 13px; color: var(--text-muted); margin-bottom: 8px; text-transform: uppercase; font-weight: 600; display: flex; justify-content: space-between; }
        .flex-row { display: flex; justify-content: space-between; align-items: center; }
        .metric-value { font-size: 20px; font-weight: 700; }
        .profit { color: var(--accent-green); }
        .loss { color: var(--accent-red); }
        .btn { padding: 8px 14px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; font-size: 13px; }
        .btn-green { background-color: var(--accent-green); color: white; }
        .btn-red { background-color: var(--accent-red); color: white; }
        .btn-blue { background-color: var(--accent-blue); color: white; }
        .btn-outline { background: transparent; border: 1px solid var(--border-color); color: var(--text-main); }
        .kill-banner { background: rgba(218,54,51,0.15); border: 1px solid var(--accent-red); padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 14px; }
        .bottom-nav { position: fixed; bottom: 0; width: 100%; max-width: 480px; height: 64px; background-color: var(--bg-card); border-top: 1px solid var(--border-color); display: flex; justify-content: space-around; align-items: center; z-index: 1000; }
        .nav-item { background: none; border: none; color: var(--text-muted); font-size: 11px; display: flex; flex-direction: column; align-items: center; cursor: pointer; flex: 1; }
        .nav-item.active { color: #58a6ff; font-weight: bold; }
        input, select { width: 100%; padding: 10px; margin-top: 6px; margin-bottom: 12px; background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 6px; color: var(--text-main); font-size: 13px; }
        .account-card { background: var(--bg-primary); border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; margin-top: 8px; }
        .position-row { display: flex; justify-content: space-between; font-size: 12px; padding: 4px 0; border-bottom: 1px dashed var(--border-color); }
    </style>
</head>
<body>
    <div class="app-container">
        <header>
            <div class="logo">GN ALGO MATRIX</div>
            <div style="font-size: 11px; padding: 3px 8px; border-radius: 12px; background: rgba(35,134,54,0.2); color: var(--accent-green);">Connected</div>
        </header>
        <div class="content-area">
            <div id="view-login" class="card">
                <div class="card-title">Secure Gmail Authentication</div>
                <label>Gmail Address</label>
                <input type="email" id="login-email" value="neeraj@gmail.com">
                <button class="btn btn-blue" style="width: 100%;" onclick="handleLogin()">Login</button>
            </div>
            <div id="view-dashboard" class="hidden">
                <div id="kill-alert" class="kill-banner hidden">
                    <h3 style="color:var(--accent-red);">⚠️ KILL SWITCH ACTIVE</h3>
                    <button class="btn btn-green" onclick="resetKillSwitch()">Reset</button>
                </div>
                <button class="btn btn-red" style="width: 100%; padding: 12px; font-weight: bold; margin-bottom: 14px;" onclick="triggerKillSwitch()">🚨 EMERGENCY KILL SWITCH</button>
                <div class="card">
                    <div class="card-title">Execution Controls</div>
                    <div class="flex-row" style="margin-bottom: 10px;"><span>Mode:</span><div><button id="mode-paper" class="btn btn-outline" onclick="setTradingMode('PAPER')">Paper</button><button id="mode-real" class="btn btn-outline" onclick="setTradingMode('REAL')">Real</button></div></div>
                    <div class="flex-row"><span>Engine:</span><div><button id="engine-start" class="btn btn-green" onclick="toggleEngine('RUNNING')">Start</button><button id="engine-pause" class="btn btn-outline" onclick="toggleEngine('PAUSED')">Pause</button></div></div>
                </div>
                <div class="card">
                    <div class="card-title">Live Performance</div>
                    <div class="flex-row" style="margin-bottom: 8px;"><span>Net P&L</span><span id="dash-pnl" class="metric-value">+₹0.00</span></div>
                    <div class="flex-row" style="margin-bottom: 8px;"><span>Active Positions</span><span id="dash-positions-count" style="font-weight: 700;">0</span></div>
                    <div class="flex-row"><span>Max Risk Limit</span><span id="dash-max-risk" style="color: var(--accent-red); font-weight: 700;">-₹50.00</span></div>
                </div>
                <div class="card">
                    <div class="card-title">Quick Order</div>
                    <select id="order-account-select"></select>
                    <div style="display: flex; gap: 8px;"><select id="order-symbol"><option value="NIFTY 50">NIFTY 50</option><option value="BANK NIFTY">BANK NIFTY</option><option value="SENSEX">SENSEX</option></select><select id="order-type"><option value="BUY">BUY</option><option value="SELL">SELL</option></select></div>
                    <div style="display: flex; gap: 8px; margin-top: 6px;"><select id="product-type"><option value="INTRADAY">Intraday</option><option value="INVESTMENT">Investment</option></select><input type="number" id="order-qty" value="25" style="margin:0; width: 80px;"></div>
                    <button class="btn btn-blue" style="width: 100%; margin-top: 10px;" onclick="executeQuickOrder()">Execute</button>
                </div>
            </div>
            <div id="view-strategies" class="hidden">
                <div class="card"><div class="card-title">Demat Accounts (Max 5)</div><div id="accounts-list-container"></div></div>
                <div class="card"><div class="card-title">Add Account</div><input type="text" id="acc-name" placeholder="Nickname"><input type="text" id="acc-clientid" placeholder="Client ID"><input type="text" id="acc-apikey" placeholder="API Key"><input type="text" id="acc-totpkey" placeholder="TOTP Key"><input type="number" id="acc-capital" value="1000"><button class="btn btn-green" style="width: 100%;" onclick="addAccount()">Add Account</button></div></div>
            </div>
            <div id="view-watchlist" class="hidden">
                <div class="card"><div class="card-title">Market Session: <span id="market-session-label">INDIAN</span></div><div style="display: flex; gap: 8px; margin-bottom: 12px;"><button class="btn btn-blue" style="flex: 1;" onclick="setMarketSession('INDIAN')">India</button><button class="btn btn-outline" style="flex: 1;" onclick="setMarketSession('US')">US</button></div><div id="watchlist-items"></div></div>
                <div class="card"><div class="card-title">Chart Feed</div><canvas id="marketChart" width="400" height="200"></canvas></div>
            </div>
            <div id="view-more" class="hidden">
                <div class="card"><div class="card-title">Audit Logs</div><div id="logs-container" style="max-height: 300px; overflow-y: auto; font-size: 11px;"></div></div>
            </div>
        </div>
        <nav class="bottom-nav">
            <button class="nav-item active" onclick="switchTab('dashboard', this)">Dashboard</button>
            <button class="nav-item" onclick="switchTab('strategies', this)">Strategies</button>
            <button class="nav-item" onclick="switchTab('watchlist', this)">Watchlist</button>
            <button class="nav-item" onclick="switchTab('more', this)">More</button>
        </nav>
    </div>
    <script>
        let currentState = {};
        function handleLogin() {
            const email = document.getElementById('login-email').value;
            fetch('/api/auth/login', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({email})})
            .then(() => {
                document.getElementById('view-login').classList.add('hidden');
                document.getElementById('view-dashboard').classList.remove('hidden');
                setInterval(pollState, 2000);
            });
        }
        function switchTab(tab, el) {
            document.querySelectorAll('.content-area > div').forEach(d => d.classList.add('hidden'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('view-' + tab).classList.remove('hidden');
            el.classList.add('active');
        }
        function pollState() {
            fetch('/api/state').then(res => res.json()).then(data => { currentState = data; updateUI(); });
        }
        function updateUI() {
            const pnlEl = document.getElementById('dash-pnl');
            pnlEl.innerText = (currentState.today_pnl >= 0 ? "+₹" : "-₹") + Math.abs(currentState.today_pnl).toFixed(2);
            pnlEl.className = "metric-value " + (currentState.today_pnl >= 0 ? "profit" : "loss");
            document.getElementById('dash-positions-count').innerText = currentState.active_positions_count;
            document.getElementById('dash-max-risk').innerText = "-₹" + Math.abs(currentState.max_risk_limit).toFixed(2);
            if(currentState.kill_switch_active) document.getElementById('kill-alert').classList.remove('hidden');
            else document.getElementById('kill-alert').classList.add('hidden');
            let accHtml = '', orderSelectHtml = '';
            currentState.accounts.forEach(acc => {
                orderSelectHtml += `<option value="${acc.id}">${acc.name} (₹${acc.capital})</option>`;
                let posHtml = '';
                acc.positions.forEach(p => {
                    posHtml += `<div class="position-row"><span>${p.symbol} (${p.action})</span><span class="${p.pnl>=0?'profit':'loss'}">${p.pnl}</span></div>`;
                });
                accHtml += `<div class="account-card"><strong>${acc.name}</strong> <button class="btn btn-outline" style="padding:2px 5px;" onclick="deleteAccount(${acc.id})">✕</button><br>${posHtml || 'No positions'}</div>`;
            });
            document.getElementById('accounts-list-container').innerHTML = accHtml;
            document.getElementById('order-account-select').innerHTML = orderSelectHtml;
        }
        function setTradingMode(m) { fetch('/api/trading-mode/toggle?mode=' + m, {method: 'POST'}).then(pollState); }
        function toggleEngine(s) { fetch('/api/engine/toggle?status=' + s, {method: 'POST'}).then(pollState); }
        function triggerKillSwitch() { fetch('/api/kill-switch/trigger', {method: 'POST'}).then(pollState); }
        function resetKillSwitch() { fetch('/api/kill-switch/reset', {method: 'POST'}).then(pollState); }
        function addAccount() {
            const data = {
                name: document.getElementById('acc-name').value,
                client_id: document.getElementById('acc-clientid').value,
                api_key: document.getElementById('acc-apikey').value,
                totp_key: document.getElementById('acc-totpkey').value,
                capital: parseFloat(document.getElementById('acc-capital').value) || 1000
            };
            fetch('/api/accounts/add', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)}).then(() => pollState());
        }
        function deleteAccount(id) { fetch('/api/accounts/' + id, {method: 'DELETE'}).then(pollState); }
        function executeQuickOrder() {
            const data = {
                account_id: parseInt(document.getElementById('order-account-select').value),
                symbol: document.getElementById('order-symbol').value,
                action: document.getElementById('order-type').value,
                product_type: document.getElementById('product-type').value,
                quantity: parseInt(document.getElementById('order-qty').value) || 25,
                price: 22000.0
            };
            fetch('/api/orders/execute', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)}).then(pollState);
        }
        function setMarketSession(s) { currentState.market_session = s; updateUI(); }
        window.onload = function() {
            const ctx = document.getElementById('marketChart').getContext('2d');
            new Chart(ctx, { type: 'line', data: { labels: ['10:00', '11:00', '12:00', '1:00'], datasets: [{ data: [21900, 21950, 22010, 22050], borderColor: '#58a6ff' }] }, options: { plugins: { legend: { display: false } } } });
        }
    </script>
</body>
</html>
"""
    
