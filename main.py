import time
from datetime import datetime, time as dtime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pyotp
import requests

app = FastAPI()

# --- Server State & Configuration ---
server_state = {
    "engine_status": "RUNNING",
    "auth": {"logged_in": True},
    "accounts": [
        {
            "id": 1,
            "name": "Angel One Live Account",
            "active": True,
            "capital": 1000.0,
            "pnl": 0.0,
            "positions": []
        }
    ],
    "trades_history": [],
    "watchlist_india": ["NIFTY 50", "BANK NIFTY"],
    "watchlist_us": ["S&P 500", "NASDAQ 100"]
}

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

def connect_angel_one_live(client_id: str, api_key: str, totp_key: str):
    url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByTotp"
    try:
        totp = pyotp.TOTP(totp_key).now()
    except Exception as e:
        return {"status": "error", "message": f"Invalid TOTP: {str(e)}"}
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-UserType": "USER",
        "X-SourceID": "WEB",
        "X-ClientLocalIP": "192.168.1.1",
        "X-ClientPublicIP": "106.193.147.98",
        "X-MACAddress": "MAC",
        "X-ApiKey": api_key
    }
    try:
        response = requests.post(url, json={"clientcode": client_id, "totp": totp}, headers=headers)
        res_data = response.json()
        if res_data.get("status") == True:
            return {"status": "success", "token": res_data["data"]["jwtToken"]}
        else:
            return {"status": "error", "message": res_data.get("message", "Login failed")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GN Algo Trading Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; background: #121212; color: #fff; margin: 0; padding: 20px; }
            .container { max-width: 600px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
            h2 { color: #00ffcc; text-align: center; }
            .card { background: #2a2a2a; padding: 15px; margin-top: 15px; border-radius: 8px; }
            input, button { width: 100%; padding: 10px; margin-top: 10px; border-radius: 5px; border: none; box-sizing: border-box; }
            input { background: #333; color: #fff; }
            button { background: #00ffcc; color: #121212; font-weight: bold; cursor: pointer; }
            button:hover { background: #00cc99; }
            .status { margin-top: 10px; font-weight: bold; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>GN Algo Trading Engine</h2>
            <div class="card">
                <h3>Angel One Live Login</h3>
                <input type="text" id="client_id" placeholder="Client ID (e.g. A12345)">
                <input type="password" id="api_key" placeholder="API Key">
                <input type="password" id="totp_key" placeholder="TOTP Secret Key">
                <button onclick="connectBroker()">Connect Broker</button>
                <div id="responseMsg" class="status"></div>
            </div>
            <div class="card">
                <h3>Engine Status</h3>
                <p>Status: <span id="engineStatus" style="color: #00ffcc;">Checking...</span></p>
            </div>
        </div>

        <script>
            async function fetchStatus() {
                try {
                    let res = await fetch('/status');
                    let data = await res.json();
                    document.getElementById('engineStatus').innerText = data.engine_status;
                } catch (e) {
                    document.getElementById('engineStatus').innerText = "Offline";
                }
            }

            async function connectBroker() {
                let client_id = document.getElementById('client_id').value;
                let api_key = document.getElementById('api_key').value;
                let totp_key = document.getElementById('totp_key').value;
                let msgBox = document.getElementById('responseMsg');

                msgBox.style.color = "#ffcc00";
                msgBox.innerText = "Connecting to Angel One...";

                try {
                    let res = await fetch('/connect_broker', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            name: "Angel One Live Account",
                            client_id: client_id,
                            api_key: api_key,
                            totp_key: totp_key,
                            capital: 1000.0
                        })
                    });
                    let data = await res.json();
                    if (res.ok) {
                        msgBox.style.color = "#00ffcc";
                        msgBox.innerText = "Connected Successfully! Token Generated.";
                    } else {
                        msgBox.style.color = "#ff4444";
                        msgBox.innerText = "Error: " + (data.detail || "Failed");
                    }
                } catch (e) {
                    msgBox.style.color = "#ff4444";
                    msgBox.innerText = "Connection Error!";
                }
            }

            fetchStatus();
        </script>
    </body>
    </html>
    """

@app.get("/status")
def get_status():
    return server_state

@app.post("/connect_broker")
def connect_broker(config: AccountConfig):
    result = connect_angel_one_live(config.client_id, config.api_key, config.totp_key)
    if result.get("status") == "success":
        for acc in server_state["accounts"]:
            if acc["name"] == config.name or acc["id"] == 1:
                acc["client_id"] = config.client_id
                acc["api_key"] = config.api_key
                acc["totp_key"] = config.totp_key
                acc["capital"] = config.capital
                acc["active"] = True
        return {"status": "success", "message": "Connected to Angel One Live Successfully", "jwt_token": result["token"]}
    raise HTTPException(status_code=400, detail=result.get("message", "Broker connection failed"))
    
