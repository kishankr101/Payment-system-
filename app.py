import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(page_title="Global Payment Pro", layout="wide")

# -----------------------
# STYLE (PRO UI)
# -----------------------
st.markdown("""
<style>
.block-container {padding-top: 2rem;}
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.title("🌍 Global Payment Pro Dashboard")

# -----------------------
# SIDEBAR INPUT
# -----------------------
st.sidebar.header("👤 User KYC")

name = st.sidebar.text_input("Full Name")
pan = st.sidebar.text_input("PAN Number")
card = st.sidebar.text_input("Card Number")

amount = st.sidebar.number_input("Amount (INR)", min_value=1.0)

currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "GBP"])
network = st.sidebar.selectbox("Network", ["Visa", "Mastercard", "SWIFT"])

# -----------------------
# LIVE RATES (SIMULATED CLEAN)
# -----------------------
rates = {
    "USD": 83 + random.uniform(-0.5, 0.5),
    "EUR": 90 + random.uniform(-0.5, 0.5),
    "GBP": 105 + random.uniform(-0.5, 0.5)
}

# -----------------------
# KYC SYSTEM
# -----------------------
def kyc_check(name, pan, card):
    return len(name) > 3 and len(pan) == 10 and len(card) >= 12

# -----------------------
# FRAUD DETECTION (AI STYLE LOGIC)
# -----------------------
def fraud_check(amount):
    if amount > 100000:
        return True
    return False

# -----------------------
# FEES
# -----------------------
def fees_calc(amount):
    app_fee = amount * 0.01
    bank_fee = amount * 0.015
    forex_fee = amount * 0.02
    return app_fee + bank_fee + forex_fee

# -----------------------
# PROCESS FLOW
# -----------------------
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
        time.sleep(0.8)
        bar.progress((i+1)/len(steps))

# -----------------------
# MAIN ACTION
# -----------------------
if st.button("🚀 Send Payment"):

    if not kyc_check(name, pan, card):
        st.error("❌ KYC Failed")
    elif fraud_check(amount):
        st.error("⚠️ Suspicious Transaction Blocked")
    else:
        st.success("✅ KYC Verified")

        total_fee = fees_calc(amount)
        converted = (amount - total_fee) / rates[currency]

        process()

        txn_id = "TXN" + str(random.randint(100000,999999))

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Amount (INR)", f"₹{amount}")
            st.metric("Fees", f"₹{round(total_fee,2)}")

        with col2:
            st.metric(f"{currency} Received", f"{round(converted,2)}")
            st.metric("Network", network)

        st.success(f"🎉 Transaction Successful | ID: {txn_id}")

        # SAVE HISTORY
        if "data" not in st.session_state:
            st.session_state.data = []

        st.session_state.data.append({
            "Txn": txn_id,
            "INR": amount,
            "Currency": currency,
            "Converted": round(converted,2)
        })

# -----------------------
# DASHBOARD
# -----------------------
st.subheader("📊 Analytics Dashboard")

if "data" in st.session_state and len(st.session_state.data) > 0:

    df = pd.DataFrame(st.session_state.data)

    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Total Volume")
    st.metric("Total INR Processed", f"₹{df['INR'].sum()}")

    st.subheader("💱 Currency Distribution")
    st.bar_chart(df["Currency"].value_counts())

else:
    st.info("No transactions yet")

# -----------------------
# HISTORY
# -----------------------
st.subheader("📜 Transaction History")

if "data" in st.session_state:
    for row in st.session_state.data[::-1]:
        st.write(f"{row['Txn']} | ₹{row['INR']} → {row['Converted']} {row['Currency']}")
