import streamlit as st
import time
import random
import pandas as pd
import requests

st.set_page_config(page_title="Global Payment System", layout="wide")

# ---------------------------
# SESSION INIT
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------
# LOGIN / REGISTER
# ---------------------------
if not st.session_state.logged_in:

    st.title("🔐 User Login / Register")

    name = st.text_input("Full Name")
    email = st.text_input("Email")

    if st.button("Login / Register"):
        if name and email:
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.session_state.user_email = email
            st.success("✅ Login Successful")
            st.rerun()
        else:
            st.error("Please fill all fields")

    st.stop()

# ---------------------------
# MAIN APP
# ---------------------------
st.title("🌍 Global Payment System")

# ---------------------------
# LIVE FOREX
# ---------------------------
@st.cache_data(ttl=300)
def get_rates():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/INR"
        res = requests.get(url)
        data = res.json()
        return data["rates"]
    except:
        return {"USD": 83, "EUR": 90, "GBP": 105}

rates = get_rates()

# ---------------------------
# SIDEBAR INPUT
# ---------------------------
st.sidebar.header("👤 User Details")

user_name = st.session_state.user_name
email = st.session_state.user_email

phone = st.sidebar.text_input("Phone Number")
region = st.sidebar.text_input("Region")

pan = st.sidebar.text_input("PAN Number")
card = st.sidebar.text_input("Card Number")

amount = st.sidebar.number_input("Amount (INR)", min_value=1.0)

currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "GBP"])
network = st.sidebar.selectbox("Network", ["Visa", "Mastercard", "SWIFT"])

# ---------------------------
# LOGIC
# ---------------------------
def kyc(name, pan, card):
    return len(name) > 3 and len(pan) == 10 and len(card) >= 12

def fraud(amount):
    return amount > 150000

def fees(amount):
    return amount * 0.045

# ---------------------------
# PROCESS FLOW
# ---------------------------
def process():
    steps = [
        "🔐 KYC Verification",
        "🛡 Fraud Check",
        "🏦 Bank Processing",
        "🌐 Network Routing",
        "💱 Currency Conversion",
        "🌍 Settlement",
        "✅ Completed"
    ]

    bar = st.progress(0)

    for i, step in enumerate(steps):
        st.info(step)
        time.sleep(0.7)
        bar.progress((i + 1) / len(steps))

# ---------------------------
# MAIN BUTTON
# ---------------------------
if st.button("🚀 Send Payment"):

    if not kyc(user_name, pan, card):
        st.error("❌ KYC Failed")
    elif fraud(amount):
        st.error("⚠️ Transaction Blocked (High Risk)")
    else:
        st.success("✅ Verified")

        rate = rates.get(currency, 83)
        total_fee = fees(amount)
        converted = (amount - total_fee) / rate

        process()

        txn_id = "TXN" + str(random.randint(100000, 999999))

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Amount (INR)", f"₹{amount}")
            st.metric("Fees", f"₹{round(total_fee,2)}")

        with col2:
            st.metric(f"{currency} Received", f"{round(converted,2)}")
            st.metric("Network", network)

        st.success(f"🎉 Transaction Successful | ID: {txn_id}")

        if "data" not in st.session_state:
            st.session_state.data = []

        st.session_state.data.append({
            "Txn": txn_id,
            "Name": user_name,
            "Phone": phone,
            "Region": region,
            "INR": amount,
            "Currency": currency,
            "Converted": round(converted,2)
        })

# ---------------------------
# DASHBOARD
# ---------------------------
st.subheader("📊 Dashboard")

if "data" in st.session_state and len(st.session_state.data) > 0:
    df = pd.DataFrame(st.session_state.data)

    st.dataframe(df, use_container_width=True)
    st.metric("Total Volume", f"₹{df['INR'].sum()}")
else:
    st.info("No transactions yet")

# ---------------------------
# HISTORY
# ---------------------------
st.subheader("📜 Transaction History")

if "data" in st.session_state:
    for txn in st.session_state.data[::-1]:
        st.write(
            f"{txn['Txn']} | {txn['Name']} | {txn['Phone']} | {txn['Region']} | ₹{txn['INR']} → {txn['Converted']} {txn['Currency']}"
        )
