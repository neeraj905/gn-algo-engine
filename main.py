from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncio
from datetime import datetime

app = FastAPI()

state = {
    "master_switch": False,
    "user_manually_disabled": False,
    "capital": 1000.0,
    "active_trade": None,
    "logs": []
}

def add_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state["logs"].append(f"[{timestamp}] {message}")
    if len(state["logs"]) > 50:
        state["logs"].pop(0)

def is_market_hours():
    now = datetime.now().time()
    start = datetime.strptime("09:15", "%H:%M").time()
    end = datetime.strptime("15:30", "%H:%M").time()
    return start <= now <= end

async def trading_background_loop():
    while True:
        await asyncio.sleep(1)
        if state["user_manually_disabled"]:
            continue

        market_open = is_market_hours()
        if market_open and not state["master_switch"]:
            state["master_switch"] = True
            add_log("SYSTEM AUTO-ON: 09:15 AM Market Opened")
        elif not market_open and state["master_switch"]:
            state["master_switch"] = False
            if state["active_trade"]:
                close_position("Market Close (03:30 PM)")
            add_log("SYSTEM AUTO-OFF: 03:30 PM Market Closed")

        if state["master_switch"] and state["active_trade"]:
            trade = state["active_trade"]
            ltp = trade["ltp"]

            if ltp > trade["highest_price"]:
                trade["highest_price"] = ltp
                new_sl = ltp * 0.98
                if new_sl > trade["trailing_sl"]:
                    trade["trailing_sl"] = new_sl
                    add_log(f"Trailing SL Updated: ₹{new_sl:.2f} (LTP: ₹{ltp:.2f})")

            if ltp <= trade["trailing_sl"]:
                close_position("Trailing Stop-Loss Hit")

def close_position(reason):
    trade = state["active_trade"]
    pnl = trade["trailing_sl"] - trade["buy_price"]
    state["capital"] += pnl
    add_log(f"Trade Closed ({reason}): Exit ₹{trade['trailing_sl']:.2f} | P&L: ₹{pnl:.2f}")
    state["active_trade"] = None

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(trading_background_loop())

@app.get("/api/toggle")
def toggle_system(status: bool):
    state["master_switch"] = status
    state["user_manually_disabled"] = not status
    status_str = "ON" if status else "OFF"
    add_log(f"Manual Override: Master Switch turned {status_str}")
    return {"status": "SUCCESS", "master_switch": state["master_switch"]}

@app.get("/api/state")
def get_state():
    return state

@app.get("/api/paper-buy")
def paper_buy(price: float):
    if not state["master_switch"]:
        return {"error": "System is OFF"}
    
    sl = price * 0.98
    state["active_trade"] = {
        "buy_price": price,
        "ltp": price,
        "highest_price": price,
        "trailing_sl": sl
    }
    add_log(f"Paper Buy Executed at ₹{price:.2f} | Initial 2% SL: ₹{sl:.2f}")
    return {"status": "SUCCESS", "trade": state["active_trade"]}

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    with open("index.html", "r") as f:
        return f.read()
  
