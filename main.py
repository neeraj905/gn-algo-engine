from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
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
        body { background-color: var(--bg-color); color: var(--text-color); padding-bottom: 70px; }
        header { text-align: center; padding: 15px; font-weight: bold; font-size: 1.1rem; letter-spacing: 1px; background: #020617; border-bottom: 1px solid var(--border-color); color: var(--accent); }
        .container { padding: 12px; max-width: 600px; margin: 0 auto; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .card { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 15px; margin-bottom: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .card-title { font-size: 0.95rem; font-weight: 600; color: var(--text-muted); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
        .flex-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 0.9rem; }
        .badge { padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: bold; }
        .badge-green { background: rgba(34,197,94,0.15); color: var(--accent-green); }
        .badge-red { background: rgba(239,68,68,0.15); color: var(--accent-red); }
        
        /* Bottom Navigation Bar */
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: #020617; border-top: 1px solid var(--border-color); display: flex; justify-content: space-around; padding: 10px 0; z-index: 1000; }
        .nav-item { background: none; border: none; color: var(--text-muted); font-size: 0.75rem; display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: color 0.2s; }
        .nav-item.active { color: var(--accent); font-weight: bold; }
        .nav-item svg { width: 20px; height: 20px; margin-bottom: 3px; fill: currentColor; }
    </style>
</head>
<body>
    <header>GN ALGO MATRIX</header>
    <div class="container">
            <!-- Dashboard Tab -->
        <div id="tab-dashboard" class="tab-content active">
            <div class="card">
                <div class="card-title">Engine Status</div>
                <div class="flex-row"><span>Status</span><span class="badge badge-green">RUNNING (LIVE)</span></div>
                <div class="flex-row"><span>Broker Mode</span><span>Paper Trading / API</span></div>
                <div class="flex-row"><span>Active Strategies</span><span>NIFTY Basket V2</span></div>
            </div>
            <div class="card">
                <div class="card-title">Quick Overview</div>
                <div class="flex-row"><span>Today's P&L</span><span class="badge badge-green">+₹0.00</span></div>
                <div class="flex-row"><span>Active Positions</span><span>0</span></div>
            </div>
        </div>

        <!-- Wizard Tab -->
        <div id="tab-wizard" class="tab-content">
            <div class="card">
                <div class="card-title">Strategy Wizard Builder</div>
                <p style="font-size: 0.85rem; color: var(--text-muted);">Configure custom indicators, entry conditions, and automated risk parameters here.</p>
            </div>
        </div>

        <!-- Strategies Tab -->
        <div id="tab-strategies" class="tab-content">
            <div class="card">
                <div class="card-title">Active Strategies</div>
                <div class="flex-row"><strong>NIFTY Strategies Basket V2</strong><span class="badge badge-green">Active</span></div>
                <div class="flex-row" style="margin-top: 5px; color: var(--text-muted); font-size: 0.8rem;"><span>Status: Monitoring Market</span><span>Tradetron Sync: OK</span></div>
            </div>
            <div class="card">
                <div class="card-title">Nifty Iron Condor</div>
                <div class="flex-row"><strong>Iron Condor Spread</strong><span class="badge badge-green">Active</span></div>
                <div class="flex-row" style="margin-top: 5px; color: var(--text-muted); font-size: 0.8rem;"><span>Delta Neutral</span><span>Hedging Enabled</span></div>
            </div>
        </div>

        <!-- Watchlist Tab with Search Bar Enabled -->
        <div id="tab-watchlist" class="tab-content">
            <div class="card">
                <div class="card-title">Live Chart & Universal Search</div>
                <div style="height: 480px; width: 100%;">
                    <!-- TradingView Advanced Chart Widget BEGIN -->
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
                    <!-- TradingView Widget END -->
                </div>
            </div>
        </div>
                <!-- More Tab -->
        <div id="tab-more" class="tab-content">
            <div class="card">
                <div class="card-title">System Settings & Logs</div>
                <div class="flex-row"><span>App Version</span><span>v2.2.53</span></div>
                <div class="flex-row"><span>GitHub Repository</span><span>neeraj905/gn-algo-matrix</span></div>
                <div class="flex-row"><span>Render Engine</span><span>Online & Active</span></div>
            </div>
        </div>
    </div>

    <!-- Bottom Navigation Bar -->
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
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
