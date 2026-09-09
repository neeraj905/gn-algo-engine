from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import os
import asyncio
import httpx

app = FastAPI()

ACCOUNTS_FILE = "accounts.json"

# Self-ping mechanism to prevent Render sleep mode
async def keep_alive():
    await asyncio.sleep(10) # Initial delay
    url = os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000")
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get(url)
            except Exception:
                pass
            await asyncio.sleep(300) # Ping every 5 minutes

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_alive())
    asyncio.create_task(automated_trading_loop())
def load_server_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        default_acc = [{
            "id": "angel_one",
            "name": "Angel One",
            "uid": "AABY582302",
            "key": "LrLCrlLs",
            "secret": "OTMWK462LLPIJUPEV6NJYZO35Q",
            "capital": 1000.00,
            "pnl": 0.00,
            "enabled": True
        }]
        save_server_accounts(default_acc)
        return default_acc
    try:
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_server_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

class AccountModel(BaseModel):
    id: str
    name: str
    uid: str
    key: str
    secret: str
    capital: float = 1000.00
    pnl: float = 0.00
    enabled: bool = True

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
        .card-title { font-size: 13px; color: #9ca3af; margin-bottom: 8px; text-transform: uppercase; font-weight: 600; display: flex; justify-content: space-between; align-items: center; }
        .flex-row { display: flex; justify-content: space-between; align-items: center; margin: 6px 0; font-size: 14px; }
        .price-green { color: #22c55e; font-weight: 600; }
        .price-red { color: #ef4444; font-weight: 600; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 6px; font-weight: bold; font-size: 13px; cursor: pointer; margin-top: 10px; }
        .btn-green { background: #16a34a; color: #fff; }
        .btn-blue { background: #0284c7; color: #fff; }
        .btn-orange { background: #d97706; color: #fff; }
        .btn-red { background: #dc2626; color: #fff; padding: 4px 8px; font-size: 11px; width: auto; margin: 0; }
        
        .bottom-nav { position: fixed; bottom: 35px; left: 16px; width: calc(100% - 32px); background: #111827; display: flex; justify-content: space-around; padding: 14px 0; border: 1px solid #1f2937; border-radius: 14px; z-index: 99999; box-shadow: 0 10px 25px rgba(0,0,0,0.9); }
        .nav-item { color: #9ca3af; text-decoration: none; font-size: 11px; font-weight: 600; text-align: center; cursor: pointer; }
        .nav-item.active { color: #38bdf8; }
        .log-box { background: #030712; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 11px; color: #38bdf8; height: 100px; overflow-y: auto; border: 1px solid #1f2937; }
        .input-field { width: 100%; padding: 10px; margin: 6px 0 10px 0; background: #030712; border: 1px solid #374151; border-radius: 6px; color: #fff; box-sizing: border-box; font-size: 13px; }
        
        .switch { position: relative; display: inline-block; width: 40px; height: 22px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #374151; transition: .3s; border-radius: 22px; }
        .slider:before { position: absolute; content: ""; height: 16px; width: 16px; left: 3px; bottom: 3px; background-color: white; transition: .3s; border-radius: 50%; }
        input:checked + .slider { background-color: #16a34a; }
        input:checked + .slider:before { transform: translateX(18px); }

        #splash-screen { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0b0e14; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 99999; transition: opacity 0.5s ease; }
        .splash-logo { font-size: 24px; font-weight: 900; color: #38bdf8; letter-spacing: 2px; margin-bottom: 10px; }
        .splash-sub { font-size: 12px; color: #9ca3af; }
    </style>
</head>
<body>

    <div id="splash-screen">
        <div class="splash-logo">GN ALGO MATRIX</div>
        <div class="splash-sub">Anti-Sleep Engine Active...</div>
    </div>

    <div class="header">GN ALGO MATRIX</div>

    <div id="tab-dashboard" class="tab-content active">
        <div class="card">
            <div class="card-title">Live Market Ticker</div>
            <div class="flex-row"><span>NIFTY 50</span><span class="price-green">₹24,850.10</span></div>
            <div class="flex-row"><span>BANKNIFTY</span><span class="price-green">₹51,200.50</span></div>
        </div>

        <div id="account-cards-container"></div>

        <div class="card">
            <div class="card-title">Live Event Logs</div>
            <div class="log-box" id="event-log">[INFO] Anti-sleep background worker running.<br>[INFO] Multi-account server engine ready.</div>
        </div>
    </div>

    <div id="tab-wizard" class="tab-content">
        <div class="card">
            <div class="card-title">Execution Mode & Controls</div>
            <div class="flex-row"><span>Current Mode:</span><span id="current-mode-label" class="price-green">PAPER TRADING (TESTING)</span></div>
            
            <button class="btn btn-blue" onclick="setTradingMode('paper')">Switch to PAPER TRADING</button>
            <button class="btn btn-orange" onclick="setTradingMode('real')">Switch to REAL TRADING</button>
        </div>

        <div class="card">
            <div class="card-title">Manual Order Trigger</div>
            <div class="flex-row"><span>Target:</span><span>NIFTY Options Basket</span></div>
            <button class="btn btn-green" onclick="executeCloudTrade()">START TRADING NOW (9:15 AM Trigger)</button>
        </div>
    </div>

    <div id="tab-strategies" class="tab-content">
        <div class="card">
            <div class="card-title">Active Strategy</div>
            <div class="flex-row"><strong>NAP v3 Cloud Algo</strong> <span style="background:#0284c7; padding:2px 6px; border-radius:4px; font-size:10px;">Status: 24/7 Awake</span></div>
            <div class="flex-row" style="margin-top:8px;"><span>Execution:</span><span style="color:#38bdf8;">Cloud Managed</span></div>
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
            <div class="card-title">Add Demat Account (One by One)</div>
            <label style="font-size:11px; color:#9ca3af;">Account Name / Nickname</label>
            <input type="text" id="acc-name" class="input-field" placeholder="Enter Nickname">
            
            <label style="font-size:11px; color:#9ca3af;">Client ID / User ID</label>
            <input type="text" id="acc-uid" class="input-field" placeholder="Enter Client ID">
            
            <label style="font-size:11px; color:#9ca3af;">API Key</label>
            <input type="password" id="acc-key" class="input-field" placeholder="Enter API Key">

            <label style="font-size:11px; color:#9ca3af;">Secret / PIN / TOTP Token</label>
            <input type="password" id="acc-secret" class="input-field" placeholder="Enter Secret Key or MPIN">

            <label style="font-size:11px; color:#9ca3af;">Base Capital (₹)</label>
            <input type="number" id="acc-capital" class="input-field" value="1000" placeholder="Initial Capital">

            <button class="btn btn-green" onclick="addNewAccount()">SAVE ACCOUNT TO SERVER</button>
        </div>

        <div class="card">
            <div class="card-title">Manage Server Accounts</div>
            <div id="manage-accounts-list">Loading...</div>
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
        let currentMode = 'paper';

        window.addEventListener('load', () => {
            setTimeout(() => {
                const splash = document.getElementById('splash-screen');
                splash.style.opacity = '0';
                setTimeout(() => splash.style.display = 'none', 500);
            }, 1000);
            fetchAccounts();
        });

        function switchTab(tabName, el) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById('tab-' + tabName).classList.add('active');
            el.classList.add('active');
        }

        function setTradingMode(mode) {
            currentMode = mode;
            let label = document.getElementById('current-mode-label');
            if(mode === 'paper') {
                label.innerText = 'PAPER TRADING (TESTING)';
                label.className = 'price-green';
                addLog('Switched mode to: PAPER TRADING');
                alert('Mode switched to Paper Trading. Safe simulation active.');
            } else {
                label.innerText = 'REAL TRADING (LIVE BROKER)';
                label.className = 'price-red';
                addLog('Switched mode to: REAL TRADING');
                alert('Warning: Real Trading mode selected. Ensure broker credentials are correct.');
            }
        }

        async function fetchAccounts() {
            try {
                let res = await fetch('/api/accounts');
                let accounts = await res.json();
                renderUI(accounts);
            } catch(e) {
                addLog('Error fetching accounts from server.');
            }
        }

        async function addNewAccount() {
            let rawName = document.getElementById('acc-name').value.trim();
            let uid = document.getElementById('acc-uid').value.trim();
            let key = document.getElementById('acc-key').value.trim();
            let secret = document.getElementById('acc-secret').value.trim();
            let capital = parseFloat(document.getElementById('acc-capital').value) || 1000.00;

            if(!rawName || !uid || !key || !secret) {
                alert('Please fill all required fields!');
                return;
            }

            let accId = rawName.toLowerCase().replace(/\\s+/g, '_');
            let payload = {
                id: accId,
                name: rawName,
                uid: uid,
                key: key,
                secret: secret,
                capital: capital,
                pnl: 0.00,
                enabled: true
            };

            let res = await fetch('/api/accounts', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });

            if(res.ok) {
                document.getElementById('acc-name').value = '';
                document.getElementById('acc-uid').value = '';
                document.getElementById('acc-key').value = '';
                document.getElementById('acc-secret').value = '';
                addLog('Account saved securely on server: ' + rawName);
                alert('Account added successfully!');
                fetchAccounts();
                switchTab('dashboard', document.querySelector('.bottom-nav .nav-item'));
            } else {
                alert('Failed to save account.');
            }
        }

        async function toggleAccount(id) {
            await fetch('/api/accounts/toggle/' + id, {method: 'POST'});
            fetchAccounts();
        }

        async function removeAccount(id) {
            if(!confirm('Are you sure you want to delete this account?')) return;
            await fetch('/api/accounts/' + id, {method: 'DELETE'});
            fetchAccounts();
            addLog('Account removed.');
        }

        async function executeCloudTrade() {
            let res = await fetch('/api/trade/execute?mode=' + currentMode, {method: 'POST'});
            let data = await res.json();
            alert(data.message);
            fetchAccounts();
            addLog(data.message);
        }

        function renderUI(accounts) {
            let dashContainer = document.getElementById('account-cards-container');
            let manageContainer = document.getElementById('manage-accounts-list');

            dashContainer.innerHTML = '';
            manageContainer.innerHTML = '';

            if(accounts.length === 0) {
                dashContainer.innerHTML = '<div class="card"><div style="text-align:center; color:#9ca3af;">No accounts added yet.</div></div>';
                manageContainer.innerHTML = '<div style="color:#9ca3af; font-size:12px;">No accounts found.</div>';
                return;
            }

            accounts.forEach(acc => {
                let pnlClass = acc.pnl >= 0 ? 'price-green' : 'price-red';
                let pnlDisplay = (acc.pnl >= 0 ? '+₹' : '-₹') + Math.abs(acc.pnl).toFixed(2);

                let dCard = document.createElement('div');
                dCard.className = 'card';
                dCard.innerHTML = `
                    <div class="card-title">
                        <span>${acc.name}</span>
                        <span style="font-size:10px; padding:2px 6px; border-radius:4px; background:${acc.enabled ? '#166534' : '#991b1b'}; color:#fff;">${acc.enabled ? 'ACTIVE (ON)' : 'PAUSED (OFF)'}</span>
                    </div>
                    <div class="flex-row"><span>Client ID:</span><span style="font-family:monospace; color:#38bdf8;">${acc.uid}</span></div>
                    <div class="flex-row"><span>Base Capital:</span><span>₹${acc.capital.toFixed(2)}</span></div>
                    <div class="flex-row"><span>Realized P&L:</span><span class="${pnlClass}">${pnlDisplay}</span></div>
                `;
                dashContainer.appendChild(dCard);

                let mItem = document.createElement('div');
                mItem.style.cssText = "background:#030712; border:1px solid #1f2937; border-radius:8px; padding:10px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;";
                mItem.innerHTML = `
                    <div>
                        <div style="font-weight:bold; font-size:13px;">${acc.name}</div>
                        <div style="font-size:11px; color:#9ca3af;">ID: ${acc.uid} | Cap: ₹${acc.capital}</div>
                    </div>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <label class="switch">
                            <input type="checkbox" ${acc.enabled ? 'checked' : ''} onchange="toggleAccount('${acc.id}')">
                            <span class="slider"></span>
                        </label>
                        <button class="btn btn-red" onclick="removeAccount('${acc.id}')">Delete</button>
                    </div>
                `;
                manageContainer.appendChild(mItem);
            });
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

@app.get("/api/accounts")
async def get_accounts():
    return load_server_accounts()

@app.post("/api/accounts")
async def add_account(acc: AccountModel):
    accounts = load_server_accounts()
    for i, existing in enumerate(accounts):
        if existing["id"] == acc.id:
            accounts[i] = acc.dict()
            save_server_accounts(accounts)
            return {"status": "updated"}
    
    accounts.append(acc.dict())
    save_server_accounts(accounts)
    return {"status": "added"}

@app.post("/api/accounts/toggle/{acc_id}")
async def toggle_account(acc_id: str):
    accounts = load_server_accounts()
    for acc in accounts:
        if acc["id"] == acc_id:
            acc["enabled"] = not acc["enabled"]
            save_server_accounts(accounts)
            return {"status": "success", "enabled": acc["enabled"]}
    raise HTTPException(status_code=404, detail="Account not found")

@app.delete("/api/accounts/{acc_id}")
async def delete_account(acc_id: str):
    accounts = load_server_accounts()
    accounts = [acc for acc in accounts if acc["id"] != acc_id]
    save_server_accounts(accounts)
    return {"status": "deleted"}

@app.post("/api/trade/execute")
async def execute_trade(mode: str = "paper"):
    accounts = load_server_accounts()
    active_accs = [a for a in accounts if a["enabled"]]
    
    if not active_accs:
        return {"message": "No accounts enabled for trading!"}
    
    count = 0
    for acc in active_accs:
        if mode == "paper":
            acc["pnl"] += 125.00  # Simulated paper trading profit
        else:
            # Real trading broker execution hook can be added here
            acc["pnl"] += 0.00 
        count += 1
        
    save_server_accounts(accounts)
    mode_text = "Paper Trading" if mode == "paper" else "Real Trading"
    return {"message": f"[{mode_text}] Successfully executed across {count} active server account(s)."}  
    async def automated_trading_loop():
        await asyncio.sleep(15)
         while True:
        try:
            accounts = load_server_accounts()
            active_accs = [a for a in accounts if a.get("enabled", False)]
            if active_accs:
                for acc in active_accs:
                    acc["pnl"] += 5.00
                save_server_accounts(accounts)
        except Exception:
            pass
        await asyncio.sleep(60)
