import streamlit as st
import time
import random
import pandas as pd
import requests

st.set_page_config(page_title="Global Payment System", layout="wide")

# ---------------------------
# CUSTOM UI (MODERN LOOK)
# ---------------------------
st.markdown("""
<style>
body {
    background: #f5f7fb;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
.stButton>button {
    background: linear-gradient(90deg,#0070ba,#00c6ff);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION INIT
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "signup"

# ---------------------------
# SIGNUP PAGE
# ---------------------------
if st.session_state.page == "signup":

    st.title("📝 Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    if st.button("Sign Up"):
        if name and email and phone:
            st.session_state.reg_name = name
            st.session_state.reg_email = email
            st.session_state.reg_phone = phone
            st.session_state.page = "login"
            st.success("✅ Account Created")
            st.rerun()
        else:
            st.error("Fill all details")

    st.stop()

# ---------------------------
# LOGIN PAGE
# ---------------------------
if st.session_state.page == "login":

    st.title("🔐 Login")

    email = st.text_input("Enter Email")

    if st.button("Login"):
        if email == st.session_state.reg_email:
            st.session_state.page = "dashboard"
            st.session_state.user_name = st.session_state.reg_name
            st.session_state.user_phone = st.session_state.reg_phone
            st.success("✅ Login Successful")
            st.rerun()
        else:
            st.error("❌ Invalid Email")

    st.stop()

# ---------------------------
# DASHBOARD
# ---------------------------
st.title("🌍 Global Payment System")

user_name = st.session_state.user_name
user_phone = st.session_state.user_phone

# ---------------------------
# LIVE FOREX
# ---------------------------
@st.cache_data(ttl=300)
def get_rates():
    try:
        res = requests.get("https://api.exchangerate-api.com/v4/latest/INR")
        return res.json()["rates"]
    except:
        return {"USD": 83, "EUR": 90, "GBP": 105}

rates = get_rates()

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.header("👤 User Panel")

st.sidebar.success(f"{user_name}")
st.sidebar.info(f"📞 {user_phone}")

region = st.sidebar.text_input("Region")
pan = st.sidebar.text_input("PAN Number")
card = st.sidebar.text_input("Card Number")

amount = st.sidebar.number_input("Amount (INR)", min_value=1.0)
currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "GBP"])
network = st.sidebar.selectbox("Network", ["Visa", "Mastercard", "SWIFT", "PayPal"])

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
        time.sleep(0.6)
        bar.progress((i + 1) / len(steps))

# ---------------------------
# PAYMENT BUTTON
# ---------------------------
if st.button("🚀 Send Payment"):

    if not kyc(user_name, pan, card):
        st.error("❌ KYC Failed")
    elif fraud(amount):
        st.error("⚠️ High Risk Transaction")
    else:
        st.success("✅ Verified")

        rate = rates.get(currency, 83)
        total_fee = fees(amount)
        converted = (amount - total_fee) / rate

        process()

        txn_id = "TXN" + str(random.randint(100000, 999999))

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Amount", f"₹{amount}")
            st.metric("Fees", f"₹{round(total_fee,2)}")

        with col2:
            st.metric(currency, f"{round(converted,2)}")
            st.metric("Network", network)

        st.success(f"🎉 Success | ID: {txn_id}")

        if "data" not in st.session_state:
            st.session_state.data = []

        st.session_state.data.append({
            "Txn": txn_id,
            "Name": user_name,
            "Phone": user_phone,
            "Region": region,
            "INR": amount,
            "Currency": currency,
            "Converted": round(converted,2)
        })

# ---------------------------
# DASHBOARD TABLE
# ---------------------------
st.subheader("📊 Dashboard")

st.info(f"👤 {user_name} | 📞 {user_phone}")

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
