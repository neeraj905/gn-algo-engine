import time
from datetime import datetime, time as dtime
from fastapi import FastAPI, HTTPException
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

def background_trading_engine():
    while True:
        time.sleep(3)
        if server_state["engine_status"] != "RUNNING":
            continue
        if datetime.now().time() >= dtime(15, 30):
            continue
        total_portfolio_pnl = 0.0
        active_count = 0
        for acc in server_state["accounts"]:
            if not acc["active"]: continue
            acc_pnl = 0.0
            for pos in list(acc["positions"]):
                active_count += 1
                pos["current_price"] = round(pos["entry_price"] + 1.2, 2)
                diff = (pos["current_price"] - pos["entry_price"]) if pos["action"] == "BUY" else (pos["entry_price"] - pos["current_price"])
                pos["pnl"] = round(diff * pos["quantity"], 2)
                acc_pnl += pos["pnl"]
            acc["pnl"] = round(acc_pnl, 2)
            total_portfolio_pnl += acc["pnl"]

@app.get("/")
def read_root():
    return {"status": "online", "message": "GN Algo Engine with Angel One Live Data"}

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
            
