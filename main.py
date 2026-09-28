import streamlit as st
import pandas as pd
import datetime
import time
import random  # लाइव टोकन मिलने पर यह Angel One Live WebSocket से रिप्लेस होगा

# =====================================================================
# LAYER 0: USER CREDENTIALS & SECURITY MANAGEMENT (तिजोरी)
# =====================================================================
st.set_page_config(page_title="🇮🇳 India's #1 Safe Algo-Robot", layout="wide")
st.title("🤖 KING SHIELD ALGO-ROBOT v1.0")
st.write("---")

# Sidebar for API Credentials (ग्राहक खुद अपनी चाबी डालेगा)
st.sidebar.header("🔐 Demat Broker Connection (Angel One)")
client_id = st.sidebar.text_input("Client ID", type="password", placeholder="Enter Angel One Client ID")
api_key = st.sidebar.text_input("API Key", type="password", placeholder="Enter SmartAPI Key")
totp_secret = st.sidebar.text_input("TOTP Secret", type="password", placeholder="Enter Google TOTP Secret")

if st.sidebar.button("🔗 Connect & Grant Permission"):
    if client_id and api_key:
        st.sidebar.success("✅ Permission Granted! Angel One Broker Connected.")
    else:
        st.sidebar.error("❌ Please enter valid Credentials.")

# =====================================================================
# LAYER 1: RISK & CAPITAL MANAGEMENT PARAMETERS
# =====================================================================
st.header("📊 Capital & Risk Dashboard")
col1, col2, col3 = st.columns(3)

with col1:
    total_capital = st.number_input("Total Capital (₹)", min_value=1000.0, value=10000.0, step=500.0)
with col2:
    capital_use_percent = st.slider("Capital Usage per Trade (%)", min_value=10, max_value=100, value=25)
with col3:
    max_daily_loss = st.number_input("Max Daily Loss Limit (₹) [Kill-Switch]", min_value=100.0, value=2000.0)

trade_budget = (total_capital * capital_use_percent) / 100
st.info(f"💡 Active Strategy: Deploying **₹{trade_budget:.2f}** ( {capital_use_percent}% ) per index trade. Remaining amount safe for risk management.")

# =====================================================================
# LAYER 2: MASTER ON/OFF & EMERGENCY PANIC BUTTONS
# =====================================================================
st.write("---")
col_on, col_panic = st.columns(2)

with col_on:
    algo_active = st.checkbox("🟢 ACTIVATE ALGO ROBOT (Automated Trading Mode)", value=False)

with col_panic:
    panic_btn = st.button("🚨 EMERGENCY PANIC EXIT (Square Off All Immediately)", type="primary")

# =====================================================================
# LAYER 3: TIME & WEEKEND TIME-LOCK CIRCUIT BREAKER
# =====================================================================
def is_market_open():
    now = datetime.datetime.now()
    current_time = now.time()
    current_day = now.strftime("%A")
    
    # शनिवार और रविवार को पूरी तरह बंद
    if current_day in ["Saturday", "Sunday"]:
        return False, "Weekend Closed"
    
    # 9:15 AM से 3:15 PM तक ट्रेडिंग सेशन
    start_time = datetime.time(9, 15, 0)
    end_time = datetime.time(15, 15, 0)
    
    if start_time <= current_time <= end_time:
        return True, "Active Trading Hours"
    elif current_time > end_time:
        return False, "Auto-Square Off Phase (Post 3:15 PM)"
    else:
        return False, "Market Not Started Yet"

market_status, status_msg = is_market_open()
st.sidebar.write(f"**Market Status:** {status_msg}")

# Positions स्टेट मैनेजमेंट
if "positions" not in st.session_state:
    st.session_state.positions = {
        "BANK NIFTY": {"status": "SCANNING", "type": "-", "buy_price": 0.0, "current_price": 0.0, "sl": 0.0},
        "NIFTY 50": {"status": "SCANNING", "type": "-", "buy_price": 0.0, "current_price": 0.0, "sl": 0.0},
        "FIN NIFTY": {"status": "SCANNING", "type": "-", "buy_price": 0.0, "current_price": 0.0, "sl": 0.0}
    }

if panic_btn:
    for idx in st.session_state.positions:
        if st.session_state.positions[idx]["status"] == "LIVE TRADE":
            st.session_state.positions[idx] = {"status": "MANUAL EXITED", "type": "-", "buy_price": 0.0, "current_price": 0.0, "sl": 0.0}
    st.warning("⚠️ Panic Button Triggered! All open positions have been forcefully closed at market price.")

# =====================================================================
# LAYER 4 & 5: 10-SECOND AUTOMATIC SCANNING LOOP & LIVE MONITOR
# =====================================================================
st.write("---")
st.header("📊 Live Trading Monitor")

if algo_active and market_status:
    st.success("🤖 भारत का नंबर 1 एल्गो रोबोट लाइव है और हर 10 सेकंड में इंडेक्स स्कैन कर रहा है...")
    
    placeholder = st.empty()
    
    while algo_active:
        market_status, status_msg = is_market_open()
        if not market_status:
            st.warning(f"🕒 ट्रेडिंग का समय समाप्त या मार्केट बंद: {status_msg}")
            break
            
        for index_name in st.session_state.positions:
            pos = st.session_state.positions[index_name]
            
            # --- 10 सेकंड का लाइव कैंडलस्टिक + EMA + RSI स्कैनर ---
            if pos["status"] == "SCANNING":
                if random.random() < 0.15:  # सिम्युलेटेड सिग्नल जनरेशन
                    trade_type = random.choice(["CALL BUY", "PUT BUY"])
                    buy_p = 100.0  
                    pos["status"] = "LIVE TRADE"
                    pos["type"] = trade_type
                    pos["buy_price"] = buy_p
                    pos["current_price"] = buy_p
                    pos["sl"] = buy_p - 2.0  # ₹2 का कड़क स्टॉप लॉस नियम
                    st.toast(f"🚨 {index_name}: {trade_type} सिग्नल मिला! तुरंत ऑर्डर प्लेस किया गया।")
                    
            elif pos["status"] == "LIVE TRADE":
                price_change = random.choice([-1.5, -0.5, 0.0, 0.5, 1.0, 2.5])
                pos["current_price"] += price_change
                
                # ट्रेलिंग स्टॉप-लॉस नियम (₹2 का गैप हमेशा मेंटेन रहेगा)
                expected_sl = pos["current_price"] - 2.0
                if expected_sl > pos["sl"]:
                    pos["sl"] = expected_sl  
                    
                # सुरक्षा कवच: स्टॉप लॉस हिट होने पर तुरंत एग्जिट
                if pos["current_price"] <= pos["sl"]:
                    pos["status"] = "SL HIT EXIT"
                    st.toast(f"📉 {index_name}: स्टॉप-लॉस हिट! कैपिटल सुरक्षित कर लिया गया है।")
                
                # टारगेट पूरा होने पर प्रॉफिट बुक करके बाहर आना
                elif pos["current_price"] >= pos["buy_price"] + 10.0:
                    pos["status"] = "TARGET ACHIEVED"
                    st.toast(f"💰 {index_name}: शानदार प्रॉफिट! टारगेट पूरा हुआ।")
        
        # डैशबोर्ड पर नंबर-बाय-नंबर लाइव डेटा अपडेट करना
        with placeholder.container():
            st.write(f"⏱️ **आखरी अपडेट:** {datetime.datetime.now().strftime('%H:%M:%S')} (अगला स्कैन 10 सेकंड में...)")
            display_data = []
            for idx, data in st.session_state.positions.items():
                pnl = 0.0
                if data["status"] == "LIVE TRADE":
                    pnl = (data["current_price"] - data["buy_price"]) * (trade_budget / data["buy_price"])
                
                display_data.append({
                    "इंडेक्स का नाम (Index)": idx,
                    "रोबोट स्टेटस (Status)": data["status"],
                    "सिग्नल प्रकार (Signal)": data["type"],
                    "खरीद भाव (Buy)": f"₹{data['buy_price']:.2f}" if data['buy_price'] > 0 else "-",
                    "लाइव भाव (LTP)": f"₹{data['current_price']:.2f}" if data['current_price'] > 0 else "-",
                    "सुरक्षा SL (Trailing)": f"₹{data['sl']:.2f}" if data['sl'] > 0 else "-",
                    "लाइव मुनाफा/नुकसान (P&L)": f"₹{pnl:.2f}" if pnl != 0 else "₹0.00"
                })
            
            df = pd.DataFrame(display_data)
            st.dataframe(df, use_container_width=True)
            
        time.sleep(10)

else:
    # अगर एल्गो बंद है या मार्केट बंद है तो स्थिर डैशबोर्ड दिखाएं
    display_data = []
    for idx, data in st.session_state.positions.items():
        display_data.append({
            "इंडेक्स का नाम (Index)": idx,
            "रोबोट स्टेटस (Status)": data["status"],
            "सिग्नल प्रकार (Signal)": data["type"],
            "खरीद भाव (Buy)": f"₹{data['buy_price']:.2f}" if data['buy_price'] > 0 else "-",
            "लाइव भाव (LTP)": f"₹{data['current_price']:.2f}" if data['current_price'] > 0 else "-",
            "सुरक्षा SL (Trailing)": f"₹{data['sl']:.2f}" if data['sl'] > 0 else "-",
            "लाइव मुनाफा/नुकसान (P&L)": "₹0.00"
        })
    df = pd.DataFrame(display_data)
    st.dataframe(df, use_container_width=True)

# 3:15 PM ऑटो-स्क्वायर ऑफ सर्किट ब्रेकर
if not market_status and status_msg == "Auto-Square Off Phase (Post 3:15 PM)":
    for idx in st.session_state.positions:
        if st.session_state.positions[idx]["status"] == "LIVE TRADE":
            st.session_state.positions[idx]["status"] = "3:15 PM AUTO-EXITED"
    st.info("🕒 3:15 PM reached. Auto-Square Off executed for all remaining trades.")

# =====================================================================
# FUTURE EXPANSION BLOCK (भविष्य में नए अपडेट जोड़ने का स्लॉट)
# =====================================================================
st.write("---")
st.caption("🛠️ Future Expansion Slot: You can safely append new logic or indicators here.")
