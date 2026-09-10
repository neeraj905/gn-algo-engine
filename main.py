from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import asyncio
import random
from datetime import datetime

app = FastAPI()

# --- SERVER STATE & DATABASE SIMULATION ---
server_state = {
    "capital": 1000,
    "today_pnl": 0.0,
    "active_positions": 0,
    "engine_status": "RUNNING (LIVE)",
    "max_loss_limit": -50,
    "accounts": [
        {"id": 1, "name": "Angel One", "client_id": "AABY582302", "api_key": "dummy_key", "capital": 1000, "active": True}
    ],
    "custom_strategies": [
        {"id": 1, "name": "NIFTY Strategies Basket V2", "indicator": "Supertrend", "target": 2.0, "sl": 1.0, "status": "Active"}
    ]
}

def update_risk_limits(cap):
    if cap <= 1000:
        return -50
    elif cap <= 10000:
        return -250
    else:
        return -2500

async def pnl_simulation_loop():
    while True:
        try:
            now = datetime.now()
            is_weekday = now.weekday() < 5
            current_time_val = now.hour * 100 + now.minute
            is_market_hours = is_weekday and (915 <= current_time_val <= 1530)
            
            active_accs = [acc for acc in server_state["accounts"] if acc["active"]]
            time_12hr = now.strftime("%I:%M %p")
            
            if is_market_hours and len(active_accs) > 0:
                server_state["engine_status"] = f"RUNNING ({time_12hr})"
                server_state["active_positions"] = len(active_accs)
                
                total_active_capital = sum(acc["capital"] for acc in active_accs)
                server_state["capital"] = total_active_capital
                server_state["max_loss_limit"] = update_risk_limits(total_active_capital)
                
                if server_state["today_pnl"] > server_state["max_loss_limit"]:
                    fluctuation_pct = random.uniform(-0.003, 0.004)
                    step_pnl = total_active_capital * fluctuation_pct
                    server_state["today_pnl"] += round(step_pnl, 2)
                    
                    if server_state["today_pnl"] <= server_state["max_loss_limit"]:
                        server_state["today_pnl"] = server_state["max_loss_limit"]
                        server_state["engine_status"] = f"STOPPED (SL HIT) at {time_12hr}"
            else:
                server_state["engine_status"] = f"IDLE ({time_12hr} - MARKET CLOSED)"
                server_state["active_positions"] = 0
                
        except Exception as e:
            print("Simulation Error:", e)
            
        await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(pnl_simulation_loop())

@app.get("/api/state")
def get_state():
    return server_state

@app.post("/api/strategy/add")
async def add_strategy(request: Request):
    data = await request.json()
    new_id = len(server_state["custom_strategies"]) + 1
    new_strat = {
        "id": new_id,
        "name": data.get("name", f"Custom Strategy {new_id}"),
        "indicator": data.get("indicator", "EMA Crossover"),
        "target": float(data.get("target", 2.0)),
        "sl": float(data.get("sl", 1.0)),
        "status": "Active"
    }
    server_state["custom_strategies"].append(new_strat)
    return {"status": "success", "strategies": server_state["custom_strategies"]}

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
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-color: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --border-color: #334155;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-color); padding-bottom: 90px; }
        header { text-align: center; padding: 15px; font-weight: bold; font-size: 1.1rem; letter-spacing: 1px; background: #020617; border-bottom: 1px solid var(--border-color); color: var(--accent); }
        .container { padding: 12px; max-width: 600px; margin: 0 auto; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .card { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 15px; margin-bottom: 12px; }
        .card-title { font-size: 0.95rem; font-weight: 600; color: var(--text-muted); margin-bottom: 10px; text-transform: uppercase; }
        .flex-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 0.9rem; }
        .badge { padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; }
        .badge-green { background: rgba(34,197,94,0.15); color: var(--accent-green); }
        .badge-red { background: rgba(239,68,68,0.15); color: var(--accent-red); }
        .form-group { margin-bottom: 10px; }
        .form-group label { display: block; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 4px; }
        .form-control { width: 100%; padding: 10px; background: #0f172a; border: 1px solid var(--border-color); color: #fff; border-radius: 8px; font-size: 0.9rem; }
        .btn-primary { width: 100%; padding: 12px; background: var(--accent-green); color: #000; font-weight: bold; border: none; border-radius: 8px; cursor: pointer; font-size: 0.95rem; margin-top: 5px; }
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #020617; border-top: 1px solid var(--border-color); display: flex; justify-content: space-around; padding: 10px 0 24px 0; z-index: 1000; }
        .nav-item { background: none; border: none; color: var(--text-muted); font-size: 0.75rem; display: flex; flex-direction: column; align-items: center; cursor: pointer; width: 20%; }
        .nav-item.active { color: var(--accent); font-weight: bold; }
        .nav-item svg { width: 20px; height: 20px; margin-bottom: 3px; fill: currentColor; }
    </style>
</head>
<body>
    <header>GN ALGO MATRIX</header>
    <div class="container">
        <div id="tab-dashboard" class="tab-content active">
            <div class="card">
                <div class="card-title">Engine Status</div>
                <div class="flex-row"><span>Status</span><span id="engine-status" class="badge badge-green">Loading...</span></div>
                <div class="flex-row"><span>Total Active Capital</span><span id="txt-capital">₹1,000</span></div>
                <div class="flex-row"><span>Max Risk Limit (SL)</span><span id="txt-risk" style="color: var(--accent-red);">-₹50</span></div>
            </div>
            <div class="card">
                <div class="card-title">Live Performance</div>
                <div class="flex-row"><span>Today's P&L</span><span id="live-pnl" class="badge badge-green">+₹0.00</span></div>
                <div class="flex-row"><span>Active Positions</span><span id="active-pos">0</span></div>
            </div>
        </div>

        <div id="tab-wizard" class="tab-content">
            <div class="card">
                <div class="card-title">Strategy Wizard Builder</div>
                <form id="wizard-form" onsubmit="createStrategy(event)">
                    <div class="form-group">
                        <label>Strategy Name</label>
                        <input type="text" id="wiz-name" class="form-control" placeholder="e.g. Nifty Breakout Alpha" required>
                    </div>
                    <div class="form-group">
                        <label>Select Core Indicator</label>
                        <select id="wiz-indicator" class="form-control">
                            <option value="EMA Crossover">EMA Crossover (9 & 21)</option>
                            <option value="Supertrend">Supertrend (7, 3)</option>
                            <option value="RSI Reversal">RSI Reversal (14)</option>
                            <option value="VWAP Momentum">VWAP Momentum</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Target (%)</label>
                        <input type="number" step="0.1" id="wiz-target" class="form-control" value="2.0" required>
                    </div>
                    <div class="form-group">
                        <label>Stop Loss (%)</label>
                        <input type="number" step="0.1" id="wiz-sl" class="form-control" value="1.0" required>
                    </div>
                    <button type="submit" class="btn-primary">GENERATE & DEPLOY STRATEGY</button>
                </form>
            </div>
            <div class="card">
                <div class="card-title">Quick Guidelines</div>
                <ul style="font-size: 0.82rem; color: var(--text-muted); padding-left: 18px; line-height: 1.5;">
                    <li>Ensure your Demat API is active in the 'More' tab before deploying.</li>
                    <li>Risk limits are auto-calculated based on your active capital.</li>
                    <li>Strategies execute automatically between 09:15 AM and 03:30 PM.</li>
                </ul>
            </div>
        </div>

        <div id="tab-strategies" class="tab-content">
            <div class="card">
                <div class="card-title">Active Strategies Basket</div>
                <div id="strategies-list">
                    <div class="flex-row"><strong>NIFTY Strategies Basket V2</strong><span class="badge badge-green">Active</span></div>
                </div>
            </div>
        </div>

        <div id="tab-watchlist" class="tab-content">
            <div class="card">
                <div class="card-title">Live Nifty Index Chart</div>
                <div style="height: 450px; width: 100%;">
                    <div class="tradingview-widget-container" style="height:100%;width:100%">
                        <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
                        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
                        {
                          "autosize": true,
                          "symbol": "NSE:NIFTY",
                          "interval": "5",
                          "timezone": "Asia/Kolkata",
                          "theme": "dark",
                          "style": "1",
                          "locale": "en",
                          "enable_publishing": false,
                          "hide_top_toolbar": false,
                          "save_image": false,
                          "calendar": false,
                          "support_host": "https://www.tradingview.com"
                        }
                        </script>
                    </div>
                </div>
            </div>
        </div>

        <div id="tab-more" class="tab-content">
            <div class="card">
                <div class="card-title">System Settings</div>
                <div class="form-group">
                    <label>Engine API status</label>
                    <input type="text" class="form-control" value="Active & Running" readonly>
                </div>
            </div>
        </div>
    </div>

    <nav class="bottom-nav">
        <button class="nav-item active" onclick="switchTab('dashboard', this)">
            <svg viewBox="0 0 24 24"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>
            Dashboard
        </button>
        <button class="nav-item" onclick="switchTab('wizard', this)">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H7c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.02-.42 1.95-1.07 2.62z"/></svg>
            Wizard
        </button>
        <button class="nav-item" onclick="switchTab('strategies', this)">
            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
            Strategies
        </button>
        <button class="nav-item" onclick="switchTab('watchlist', this)">
            <svg viewBox="0 0 24 24"><path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z"/></svg>
            Watchlist
        </button>
        <button class="nav-item" onclick="switchTab('more', this)">
            <svg viewBox="0 0 24 24"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>
            More
        </button>
    </nav>

    <script>
        function switchTab(tabId, btn) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            btn.classList.add('active');
        }

        async function fetchDashboardData() {
            try {
                let res = await fetch('/api/state');
                let data = await res.json();
                document.getElementById('engine-status').innerText = data.engine_status;
                document.getElementById('txt-capital').innerText = '₹' + data.capital.toLocaleString('en-IN');
                document.getElementById('txt-risk').innerText = '-₹' + Math.abs(data.max_loss_limit).toLocaleString('en-IN');
                document.getElementById('active-pos').innerText = data.active_positions;
                
                let pnlElem = document.getElementById('live-pnl');
                let pnlVal = data.today_pwnl || data.today_pnl;
                pnlElem.innerText = (pnlVal >= 0 ? '+₹' : '-₹') + Math.abs(pnlVal).toLocaleString('en-IN', {minimumFractionDigits: 2});
                pnlElem.className = pnlVal >= 0 ? "badge badge-green" : "badge badge-red";
            } catch(e) {}
        }

        async function createStrategy(event) {
            event.preventDefault();
            let payload = {
                name: document.getElementById('wiz-name').value,
                indicator: document.getElementById('wiz-indicator').value,
                target: document.getElementById('wiz-target').value,
                sl: document.getElementById('wiz-sl').value
            };
            let res = await fetch('/api/strategy/add', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            let data = await res.json();
            if(data.status === 'success') {
                document.getElementById('wizard-form').reset();
                alert('Strategy deployed successfully!');
                switchTab('strategies', document.querySelectorAll('.nav-item')[2]);
            }
        }

        setInterval(fetchDashboardData, 3000);
        fetchDashboardData();
    </script>
</body>
</html>
    """
            
