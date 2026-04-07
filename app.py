import streamlit as st
import time
import random

st.set_page_config(page_title="GlobalPay Pro", layout="wide")

# ---------------------------
# MODERN UI STYLE
# ---------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to right,#eef2ff,#f9fbff);
}
.main-title {
    font-size:40px;
    font-weight:800;
}
.card {
    background:white;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom:10px;
}
.navbar {
    position:fixed;
    bottom:0;
    width:100%;
    background:white;
    padding:10px;
    display:flex;
    justify-content:space-around;
    box-shadow:0px -2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "signup"

# ---------------------------
# COUNTRY DATA (30+)
# ---------------------------
countries = [
{"name":"USA","currency":"USD"},
{"name":"UK","currency":"GBP"},
{"name":"Germany","currency":"EUR"},
{"name":"France","currency":"EUR"},
{"name":"Canada","currency":"CAD"},
{"name":"Australia","currency":"AUD"},
{"name":"Japan","currency":"JPY"},
{"name":"China","currency":"CNY"},
{"name":"Brazil","currency":"BRL"},
{"name":"India","currency":"INR"},
{"name":"UAE","currency":"AED"},
{"name":"Singapore","currency":"SGD"},
{"name":"South Africa","currency":"ZAR"},
{"name":"Italy","currency":"EUR"},
{"name":"Spain","currency":"EUR"},
{"name":"Netherlands","currency":"EUR"},
{"name":"Switzerland","currency":"CHF"},
{"name":"Sweden","currency":"SEK"},
{"name":"Norway","currency":"NOK"},
{"name":"Denmark","currency":"DKK"},
{"name":"Finland","currency":"EUR"},
{"name":"Mexico","currency":"MXN"},
{"name":"Russia","currency":"RUB"},
{"name":"Turkey","currency":"TRY"},
{"name":"Indonesia","currency":"IDR"},
{"name":"Thailand","currency":"THB"},
{"name":"Malaysia","currency":"MYR"},
{"name":"Philippines","currency":"PHP"},
{"name":"Vietnam","currency":"VND"},
{"name":"Argentina","currency":"ARS"}
]

rates = {
"USD":83,"JPY":0.55,"GBP":105,"EUR":90,"AED":22,"AUD":55,
"CAD":60,"SGD":61,"CNY":11,"INR":1,"BRL":16,"ZAR":4.5,
"CHF":92,"SEK":7.5,"NOK":7.8,"DKK":12,"MXN":5,"RUB":0.9,
"TRY":3,"IDR":0.005,"THB":2.3,"MYR":18,"PHP":1.5,
"VND":0.003,"ARS":0.25
}

# ---------------------------
# SIGNUP
# ---------------------------
if st.session_state.page == "signup":
    st.markdown("<h1 class='main-title'>📝 Create Account</h1>", unsafe_allow_html=True)

    email = st.text_input("📧 Email")
    password = st.text_input("🔐 Password", type="password")

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
    st.markdown("<h1 class='main-title'>🔐 Login</h1>", unsafe_allow_html=True)

    email = st.text_input("📧 Email")
    password = st.text_input("🔐 Password", type="password")

    if st.button("Login"):
        if email == st.session_state.user["email"] and password == st.session_state.user["password"]:
            st.session_state.page = "profile"
            st.rerun()

    st.stop()

# ---------------------------
# PROFILE
# ---------------------------
if st.session_state.page == "profile":
    st.markdown("<h1 class='main-title'>👤 Complete Profile</h1>", unsafe_allow_html=True)

    name = st.text_input("Name")
    phone = st.text_input("Phone")
    gender = st.selectbox("Gender",["Male","Female","Other"])
    region = st.text_input("Region")
    job = st.text_input("Occupation")

    if st.button("Save"):
        st.session_state.profile = {"name":name,"phone":phone}
        st.session_state.page = "countries"
        st.rerun()

    st.stop()

# ---------------------------
# COUNTRIES
# ---------------------------
if st.session_state.page == "countries":
    st.markdown("<h1 class='main-title'>🌍 Choose Country</h1>", unsafe_allow_html=True)

    search = st.text_input("🔍 Search Country")

    cols = st.columns(3)

    for i,c in enumerate(countries):
        if search.lower() in c["name"].lower():
            with cols[i%3]:
                st.markdown(f"<div class='card'>🌍 {c['name']}</div>", unsafe_allow_html=True)
                if st.button(f"Send → {c['name']}", key=i):
                    st.session_state.country = c
                    st.session_state.page = "payment"
                    st.rerun()

    st.stop()

# ---------------------------
# PAYMENT
# ---------------------------
if st.session_state.page == "payment":
    st.markdown("<h1 class='main-title'>💳 Payment</h1>", unsafe_allow_html=True)

    amount = st.number_input("₹ Amount", min_value=1.0)
    card = st.text_input("💳 Card")

    medium = st.selectbox("💸 Method",["SWIFT","PayPal","Visa","Mastercard"])

    currency = st.session_state.country["currency"]
    rate = rates[currency]

    converted = amount / rate if rate else amount

    st.success(f"💱 {round(converted,2)} {currency}")

    if st.button("Send Money"):
        st.session_state.payment = {"amount":amount,"converted":converted,"currency":currency,"medium":medium}
        st.session_state.page = "process"
        st.rerun()

    st.stop()

# ---------------------------
# PROCESS
# ---------------------------
st.markdown("<h1 class='main-title'>🚀 Processing Transaction</h1>", unsafe_allow_html=True)

steps = ["🔐 KYC","🛡 Fraud","🏦 Bank","🌐 Network","💱 Conversion","🌍 Settlement"]
bar = st.progress(0)

for i,s in enumerate(steps):
    st.info(s)
    time.sleep(0.5)
    bar.progress((i+1)/len(steps))

txn = "TXN"+str(random.randint(100000,999999))
data = st.session_state.payment

st.success(f"✅ Done | {txn}")
st.write(f"₹{data['amount']} → {round(data['converted'],2)} {data['currency']}")
st.write(f"💳 Mode: {data['medium']}")

# ---------------------------
# BOTTOM NAVBAR
# ---------------------------
st.markdown("""
<div class="navbar">
    <div>🏠 Home</div>
    <div>🔍 Search</div>
    <div>👤 Profile</div>
    <div>🚪 Logout</div>
</div>
""", unsafe_allow_html=True)
