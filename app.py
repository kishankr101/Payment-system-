import streamlit as st
import time
import random

st.set_page_config(page_title="GlobalPay Pro", layout="wide")

# ---------------------------
# MODERN UI DESIGN
# ---------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#e0ecff,#f5f7fb);
}
.block-container {
    padding-top: 1.5rem;
}
.card {
    padding:18px;
    border-radius:15px;
    background:white;
    box-shadow:0px 6px 18px rgba(0,0,0,0.08);
    margin-bottom:12px;
}
.stButton>button {
    background: linear-gradient(90deg,#0070ba,#00c6ff);
    color:white;
    border-radius:10px;
    height:45px;
    font-weight:bold;
}
h1, h2, h3 {
    color:#1f2d3d;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "signup"

# ---------------------------
# 30+ COUNTRIES DATA
# ---------------------------
countries = [
{"name":"USA","currency":"USD","bank":"Bank of America","region":"North America"},
{"name":"UK","currency":"GBP","bank":"HSBC","region":"Europe"},
{"name":"Japan","currency":"JPY","bank":"MUFG","region":"Asia"},
{"name":"Germany","currency":"EUR","bank":"Deutsche Bank","region":"Europe"},
{"name":"France","currency":"EUR","bank":"BNP Paribas","region":"Europe"},
{"name":"India","currency":"INR","bank":"SBI","region":"Asia"},
{"name":"UAE","currency":"AED","bank":"Emirates NBD","region":"Middle East"},
{"name":"Australia","currency":"AUD","bank":"ANZ","region":"Oceania"},
{"name":"Canada","currency":"CAD","bank":"RBC","region":"North America"},
{"name":"Singapore","currency":"SGD","bank":"DBS","region":"Asia"},
{"name":"China","currency":"CNY","bank":"ICBC","region":"Asia"},
{"name":"Brazil","currency":"BRL","bank":"Itau","region":"South America"},
{"name":"South Africa","currency":"ZAR","bank":"Standard Bank","region":"Africa"},
{"name":"Italy","currency":"EUR","bank":"UniCredit","region":"Europe"},
{"name":"Spain","currency":"EUR","bank":"Santander","region":"Europe"},
{"name":"Netherlands","currency":"EUR","bank":"ING","region":"Europe"},
{"name":"Switzerland","currency":"CHF","bank":"UBS","region":"Europe"},
{"name":"Sweden","currency":"SEK","bank":"SEB","region":"Europe"},
{"name":"Norway","currency":"NOK","bank":"DNB","region":"Europe"},
{"name":"Denmark","currency":"DKK","bank":"Danske Bank","region":"Europe"},
{"name":"Finland","currency":"EUR","bank":"Nordea","region":"Europe"},
{"name":"Mexico","currency":"MXN","bank":"Banorte","region":"North America"},
{"name":"Russia","currency":"RUB","bank":"Sberbank","region":"Europe"},
{"name":"Turkey","currency":"TRY","bank":"Ziraat","region":"Europe/Asia"},
{"name":"Indonesia","currency":"IDR","bank":"Mandiri","region":"Asia"},
{"name":"Thailand","currency":"THB","bank":"Bangkok Bank","region":"Asia"},
{"name":"Malaysia","currency":"MYR","bank":"Maybank","region":"Asia"},
{"name":"Philippines","currency":"PHP","bank":"BDO","region":"Asia"},
{"name":"Vietnam","currency":"VND","bank":"Vietcombank","region":"Asia"},
{"name":"Argentina","currency":"ARS","bank":"Banco Nación","region":"South America"}
]

# ---------------------------
# SIGNUP
# ---------------------------
if st.session_state.page == "signup":
    st.title("📝 Create Account")

    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")

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

    email = st.text_input("📧 Email")
    password = st.text_input("🔒 Password", type="password")

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
    st.title("👤 Complete Profile")

    name = st.text_input("👤 Name")
    phone = st.text_input("📞 Phone")
    gender = st.selectbox("⚧ Gender", ["Male","Female","Other"])
    region = st.text_input("🌍 Region")
    job = st.text_input("💼 Occupation")

    if st.button("Save"):
        st.session_state.profile = {"name":name,"phone":phone}
        st.session_state.page = "countries"
        st.rerun()
    st.stop()

# ---------------------------
# COUNTRY PAGE
# ---------------------------
if st.session_state.page == "countries":
    st.title("🌍 Select Country")

    cols = st.columns(3)

    for i,c in enumerate(countries):
        with cols[i%3]:
            st.markdown(f"""
            <div class='card'>
            <h4>🌎 {c['name']}</h4>
            <p>💱 {c['currency']}</p>
            <p>🏦 {c['bank']}</p>
            <p>📍 {c['region']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Send to {c['name']}", key=i):
                st.session_state.country = c
                st.session_state.page = "payment"
                st.rerun()
    st.stop()

# ---------------------------
# PAYMENT
# ---------------------------
if st.session_state.page == "payment":
    st.title("💳 Payment")

    amount = st.number_input("💰 Amount (INR)", min_value=1.0)
    card = st.text_input("💳 Card Number")
    medium = st.selectbox("📡 Mode", ["SWIFT","PayPal","Visa","Mastercard"])

    currency = st.session_state.country["currency"]

    rates = {"USD":83,"JPY":0.55,"GBP":105,"EUR":90,"AUD":55}
    rate = rates.get(currency,83)

    converted = amount / rate

    st.info(f"💱 {amount} INR → {round(converted,2)} {currency}")

    if st.button("➡️ Send Money"):
        st.session_state.data = {"amount":amount,"converted":converted,"currency":currency,"medium":medium}
        st.session_state.page = "process"
        st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "countries"
        st.rerun()
    st.stop()

# ---------------------------
# PROCESS
# ---------------------------
st.title("🚀 Processing Transaction")

steps = [
"🔐 KYC Verification",
"🛡 Fraud Check",
"🏦 Bank Processing",
"🌐 Network Routing",
"💱 Currency Conversion",
"🌍 Settlement"
]

bar = st.progress(0)

for i,s in enumerate(steps):
    st.markdown(f"<div class='card'>{s}</div>", unsafe_allow_html=True)
    time.sleep(0.5)
    bar.progress((i+1)/len(steps))

txn = "TXN" + str(random.randint(100000,999999))

d = st.session_state.data

st.success(f"✅ Success | {txn}")
st.markdown(f"💰 ₹{d['amount']} → {round(d['converted'],2)} {d['currency']}")
st.markdown(f"📡 Mode: {d['medium']}")

if st.button("⬅️ Back Home"):
    st.session_state.page = "countries"
    st.rerun()
