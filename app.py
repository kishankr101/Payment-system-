import streamlit as st
import requests
import stripe
import os
import pandas as pd
import time
import random

st.set_page_config(page_title="GlobalPay Pro", layout="wide")

# -------------------------
# CONFIG (IMPORTANT)
# -------------------------
# Put your API keys in environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_yourkey")

FOREX_API = "https://api.exchangerate-api.com/v4/latest/INR"

# -------------------------
# UI STYLE
# -------------------------
st.markdown("""
<style>
.card {padding:20px;border-radius:15px;background:white;
box-shadow:0px 4px 10px rgba(0,0,0,0.08);}
</style>
""", unsafe_allow_html=True)

st.title("🌍 GlobalPay Production System")

# -------------------------
# GET LIVE FOREX
# -------------------------
@st.cache_data(ttl=300)
def get_rates():
    try:
        res = requests.get(FOREX_API)
        data = res.json()
        return data["rates"]
    except:
        return {"USD":83,"EUR":90,"GBP":105}

rates = get_rates()

# -------------------------
# SIDEBAR INPUT
# -------------------------
st.sidebar.header("👤 User + Payment")

name = st.sidebar.text_input("Full Name")
pan = st.sidebar.text_input("PAN")
card = st.sidebar.text_input("Card Number")

amount = st.sidebar.number_input("Amount INR", min_value=1.0)

currency = st.sidebar.selectbox("Currency", ["USD","EUR","GBP"])

# -------------------------
# KYC (UPGRADE READY)
# -------------------------
def kyc(name, pan):
    return len(name)>3 and len(pan)==10

# -------------------------
# FRAUD CHECK
# -------------------------
def fraud(amount):
    return amount > 200000

# -------------------------
# STRIPE PAYMENT
# -------------------------
def create_payment(amount):
    try:
        payment = stripe.PaymentIntent.create(
            amount=int(amount*100),
            currency="inr",
            payment_method_types=["card"]
        )
        return payment["id"]
    except Exception as e:
        return str(e)

# -------------------------
# MAIN PROCESS
# -------------------------
if st.button("🚀 Process Payment"):

    if not kyc(name, pan):
        st.error("❌ KYC Failed")
    elif fraud(amount):
        st.error("⚠️ Suspicious Transaction")
    else:
        st.success("✅ Verified")

        rate = rates.get(currency, 83)
        converted = amount / rate

        # FLOW
        steps = ["KYC","Bank","Network","Forex","Settlement"]
        bar = st.progress(0)

        for i,s in enumerate(steps):
            st.info(s)
            time.sleep(0.5)
            bar.progress((i+1)/len(steps))

        # STRIPE (TEST)
        payment_id = create_payment(amount)

        txn = "TXN"+str(random.randint(100000,999999))

        st.success(f"✅ Done | ID: {txn}")

        col1,col2 = st.columns(2)

        col1.metric("INR", f"₹{amount}")
        col2.metric(currency, f"{round(converted,2)}")

        st.write("Stripe Payment ID:", payment_id)

        # SAVE
        if "db" not in st.session_state:
            st.session_state.db = []

        st.session_state.db.append({
            "txn":txn,
            "amount":amount,
            "currency":currency,
            "converted":round(converted,2)
        })

# -------------------------
# DASHBOARD
# -------------------------
st.subheader("📊 Dashboard")

if "db" in st.session_state and len(st.session_state.db)>0:
    df = pd.DataFrame(st.session_state.db)

    st.dataframe(df, use_container_width=True)

    st.metric("Total Volume", f"₹{df['amount'].sum()}")

    st.bar_chart(df["currency"].value_counts())

else:
    st.info("No data")

# -------------------------
# HISTORY
# -------------------------
st.subheader("📜 History")

if "db" in st.session_state:
    for i in st.session_state.db[::-1]:
        st.write(i)
