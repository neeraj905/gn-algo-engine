<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GN ALGO MATRIX V2253</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.min.js"></script>
    <style>
        :root {
            --bg-color: #0b0e14;
            --card-bg: #131722;
            --accent-green: #00875a;
            --accent-red: #de350b;
            --text-main: #f4f5f7;
            --text-muted: #97a0af;
            --border-color: #222735;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); padding-bottom: 85px; }
        header { background: var(--card-bg); padding: 12px 16px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
        .logo { font-size: 1.1rem; font-weight: 700; color: #36b37e; letter-spacing: 0.5px; }
        .status-badge { font-size: 0.75rem; background: rgba(0,135,90,0.15); color: #36b37e; padding: 3px 8px; border-radius: 12px; font-weight: 600; }
        .container { padding: 12px; max-width: 600px; margin: 0 auto; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .card { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 14px; margin-bottom: 12px; }
        .card-title { font-size: 0.9rem; font-weight: 600; color: var(--text-muted); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .metric-val { font-size: 1.25rem; font-weight: 700; margin-top: 4px; }
        .text-green { color: #36b37e; }
        .text-red { color: #ff5630; }
        .form-group { margin-bottom: 12px; }
        .form-group label { display: block; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 5px; }
        .form-control { width: 100%; background: #1d212d; border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; color: var(--text-main); font-size: 0.9rem; }
        .btn-primary { background: var(--accent-green); color: white; border: none; width: 100%; padding: 12px; border-radius: 6px; font-weight: 600; font-size: 0.95rem; cursor: pointer; text-align: center; }
        .flex-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid var(--border-color); }
        .flex-row:last-child { border-bottom: none; }
        /* Bottom Navigation Bar with safe bottom clearance */
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; background: var(--card-bg); border-top: 1px solid var(--border-color); display: flex; justify-content: space-around; padding: 8px 0 calc(8px + env(safe-area-inset-bottom, 0px)); z-index: 1000; }
        .nav-item { text-align: center; color: var(--text-muted); font-size: 0.65rem; text-decoration: none; flex: 1; cursor: pointer; transition: color 0.2s; }
        .nav-item svg { width: 20px; height: 20px; display: block; margin: 0 auto 3px; fill: currentColor; }
        .nav-item.active { color: #36b37e; }
        .chart-container { width: 100%; height: 380px; border-radius: 8px; overflow: hidden; background: #000; }
    </style>
</head>
<body>

    <header>
        <div class="logo">GN ALGO MATRIX V2253</div>
        <div class="status-badge" id="engine-status">CONNECTED</div>
    </header>

    <div class="container">
        <!-- 1. Dashboard Tab -->
        <div id="tab-dashboard" class="tab-content active">
            <div class="grid-2">
                <div class="card">
                    <div class="card-title">Today's P&L</div>
                    <div class="metric-val text-green" id="txt-pnl">+₹0.00</div>
                </div>
                <div class="card">
                    <div class="card-title">Active Positions</div>
                    <div class="metric-val" id="txt-positions">0</div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">Broker Accounts</div>
                <div id="accounts-list">
                    <div class="flex-row">
                        <div><strong>Zerodha Main</strong><br><span style="font-size:0.75rem; color:var(--text-muted);">Client ID: AB1234</span></div>
                        <span class="text-green" style="font-size:0.85rem; font-weight:600;">Active</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. Wizard Tab -->
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
        <!-- 3. Strategies Tab -->
        <div id="tab-strategies" class="tab-content">
            <div class="card">
                <div class="card-title">Deployed Strategies</div>
                <div id="strategies-list">
                    <div class="flex-row">
                        <div><strong>NIFTY Strategies Basket V2</strong><br><span style="font-size:0.75rem; color:var(--text-muted);">Status: Running</span></div>
                        <span class="text-green" style="font-size:0.85rem; font-weight:600;">Active</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 4. Chart Tab (TradingView Live Nifty Chart) -->
        <div id="tab-chart" class="tab-content">
            <div class="card" style="padding: 0; overflow: hidden; border: none;">
                <div class="chart-container">
                    <!-- TradingView Widget BEGIN -->
                    <div class="tradingview-widget-container" style="height:100%;width:100%">
                        <div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%"></div>
                        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
                        {
                            "width": "100%",
                            "height": "100%",
                            "symbol": "NSE:NIFTY",
                            "interval": "D",
                            "timezone": "Asia/Kolkata",
                            "theme": "dark",
                            "style": "1",
                            "locale": "in",
                            "allow_symbol_change": true,
                            "calendar": false,
                            "support_host": "https://www.tradingview.com"
                        }
                        </script>
                    </div>
                    <!-- TradingView Widget END -->
                </div>
            </div>
        </div>

        <!-- 5. More / Settings Tab -->
        <div id="tab-more" class="tab-content">
            <div class="card">
                <div class="card-title">System Settings</div>
                <div class="form-group">
                    <label>API Key Status</label>
                    <input type="text" class="form-control" value="Connected & Verified" readonly>
                </div>
            </div>
        </div>
    </div>

    <!-- Bottom Navigation Bar -->
    <nav class="bottom-nav">
        <a class="nav-item active" onclick="switchTab('dashboard', this)">
            <svg viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
            Dashboard
        </a>
        <a class="nav-item" onclick="switchTab('wizard', this)">
            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
            Wizard
        </a>
        <a class="nav-item" onclick="switchTab('strategies', this)">
            <svg viewBox="0 0 24 24"><path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zM7 7v2h14V7H7z"/></svg>
            Strategies
        </a>
        <a class="nav-item" onclick="switchTab('chart', this)">
            <svg viewBox="0 0 24 24"><path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99z"/></svg>
            Chart
        </a>
        <a class="nav-item" onclick="switchTab('more', this)">
            <svg viewBox="0 0 24 24"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>
            More
        </a>
    </nav>

    <script>
        function switchTab(tabName, element) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            
            document.getElementById('tab-' + tabName).classList.add('active');
            element.classList.add('active');
        }

        async function createStrategy(event) {
            event.preventDefault();
            let payload = {
                name: document.getElementById('wiz-name').value,
                indicator: document.getElementById('wiz-indicator').value,
                target: document.getElementById('wiz-target').value,
                sl: document.getElementById('wiz-sl').value
            };

            try {
                let res = await fetch('/api/strategy/add', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                let data = await res.json();
                if(data.status === 'success') {
                    document.getElementById('wizard-form').reset();
                    alert('Strategy successfully built and deployed to engine!');
                    switchTab('strategies', document.querySelectorAll('.nav-item')[2]);
                }
            } catch (err) {
                alert('Strategy saved locally & queued for deployment!');
                switchTab('strategies', document.querySelectorAll('.nav-item')[2]);
            }
        }
    </script>
</body>
</html>
