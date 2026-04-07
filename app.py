import streamlit as st
import time
import random

st.set_page_config(page_title="GlobalPay Pro", layout="wide")

# ---------------------------
# MODERN UI
# ---------------------------
st.markdown("""
<style>
body {background: #f0f4ff;}
.stButton>button {
    background: linear-gradient(90deg,#4facfe,#00f2fe);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}
.card {
    padding:15px;
    border-radius:15px;
    background:white;
    box-shadow:0px 4px 12px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "signup"

# ---------------------------
# COUNTRY DATA + CURRENCY
# ---------------------------
countries = [
    {"name":"USA","currency":"USD"},
    {"name":"Japan","currency":"JPY"},
    {"name":"UK","currency":"GBP"},
    {"name":"India","currency":"INR"},
    {"name":"Germany","currency":"EUR"},
    {"name":"UAE","currency":"AED"},
    {"name":"Australia","currency":"AUD"},
    {"name":"Canada","currency":"CAD"},
    {"name":"Singapore","currency":"SGD"},
    {"name":"China","currency":"CNY"}
]

rates = {
    "USD":83,
    "JPY":0.55,
    "GBP":105,
    "EUR":90,
    "AED":22,
    "AUD":55,
    "CAD":60,
    "SGD":61,
    "CNY":11,
    "INR":1
}

# ---------------------------
# SIGNUP
# ---------------------------
if st.session_state.page == "signup":
    st.title("📝 Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if email and password:
            st.session_state.user = {"email": email, "password": password}
            st.session_state.page = "login"
            st.rerun()

    st.stop()

# ---------------------------
# LOGIN
# ---------------------------
if st.session_state.page == "login":
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = st.session_state.user
        if email == user["email"] and password == user["password"]:
            st.session_state.page = "profile"
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------------------
# PROFILE
# ---------------------------
if st.session_state.page == "profile":
    st.title("👤 Complete Your Profile")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    gender = st.selectbox("Gender", ["Male","Female","Other"])
    region = st.text_input("Region")
    job = st.text_input("Occupation")

    if st.button("Save Profile"):
        st.session_state.profile = {
            "name": name,
            "phone": phone,
            "gender": gender,
            "region": region,
            "job": job
        }
        st.session_state.page = "countries"
        st.rerun()

    st.stop()

# ---------------------------
# COUNTRY PAGE
# ---------------------------
if st.session_state.page == "countries":
    st.title("🌍 Choose Country")

    cols = st.columns(3)

    for i,c in enumerate(countries):
        with cols[i % 3]:
            st.markdown(f"<div class='card'><h4>{c['name']}</h4></div>", unsafe_allow_html=True)
            if st.button(f"Select {c['name']}", key=i):
                st.session_state.country = c
                st.session_state.page = "payment"
                st.rerun()

    st.stop()

# ---------------------------
# PAYMENT PAGE
# ---------------------------
if st.session_state.page == "payment":
    st.title("💳 Payment Details")

    amount = st.number_input("Amount (INR)", min_value=1.0)
    card = st.text_input("Card Number")

    medium = st.selectbox("Send via", ["SWIFT","PayPal","Visa","Mastercard"])

    currency = st.session_state.country["currency"]
    rate = rates[currency]

    converted = amount / rate if rate else amount

    st.info(f"Converted: {round(converted,2)} {currency}")

    if st.button("➡️ Send Money"):
        st.session_state.payment = {
            "amount": amount,
            "converted": converted,
            "currency": currency,
            "medium": medium
        }
        st.session_state.page = "process"
        st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "countries"
        st.rerun()

    st.stop()

# ---------------------------
# PROCESS PAGE
# ---------------------------
st.title("🚀 Processing Transaction")

steps = ["KYC","Fraud Check","Bank","Network","Forex","Settlement"]
bar = st.progress(0)

for i,s in enumerate(steps):
    st.info(s)
    time.sleep(0.5)
    bar.progress((i+1)/len(steps))

txn = "TXN" + str(random.randint(100000,999999))

data = st.session_state.payment

st.success(f"✅ Success | {txn}")
st.write(f"₹{data['amount']} → {round(data['converted'],2)} {data['currency']}")
st.write(f"Mode: {data['medium']}")

if st.button("⬅️ Back Home"):
    st.session_state.page = "countries"
    st.rerun()
