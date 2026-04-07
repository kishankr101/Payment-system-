import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(page_title="GlobalPay", layout="wide")

# ---------------------------
# SESSION INIT
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "signup"

# ---------------------------
# DATA (30 COUNTRIES)
# ---------------------------
countries = [
    {"name":"USA","region":"North America","bank":"Bank of America","district":"California"},
    {"name":"UK","region":"Europe","bank":"HSBC","district":"London"},
    {"name":"Germany","region":"Europe","bank":"Deutsche Bank","district":"Berlin"},
    {"name":"France","region":"Europe","bank":"BNP Paribas","district":"Paris"},
    {"name":"Canada","region":"North America","bank":"RBC","district":"Toronto"},
    {"name":"Australia","region":"Oceania","bank":"ANZ","district":"Sydney"},
    {"name":"Japan","region":"Asia","bank":"MUFG","district":"Tokyo"},
    {"name":"China","region":"Asia","bank":"ICBC","district":"Beijing"},
    {"name":"Brazil","region":"South America","bank":"Itaú","district":"São Paulo"},
    {"name":"India","region":"Asia","bank":"SBI","district":"Delhi"},
    {"name":"UAE","region":"Middle East","bank":"Emirates NBD","district":"Dubai"},
    {"name":"Singapore","region":"Asia","bank":"DBS","district":"Singapore"},
    {"name":"South Africa","region":"Africa","bank":"Standard Bank","district":"Johannesburg"},
    {"name":"Italy","region":"Europe","bank":"UniCredit","district":"Rome"},
    {"name":"Spain","region":"Europe","bank":"Santander","district":"Madrid"},
    {"name":"Netherlands","region":"Europe","bank":"ING","district":"Amsterdam"},
    {"name":"Switzerland","region":"Europe","bank":"UBS","district":"Zurich"},
    {"name":"Sweden","region":"Europe","bank":"SEB","district":"Stockholm"},
    {"name":"Norway","region":"Europe","bank":"DNB","district":"Oslo"},
    {"name":"Denmark","region":"Europe","bank":"Danske Bank","district":"Copenhagen"},
    {"name":"Finland","region":"Europe","bank":"Nordea","district":"Helsinki"},
    {"name":"Mexico","region":"North America","bank":"Banorte","district":"Mexico City"},
    {"name":"Russia","region":"Europe","bank":"Sberbank","district":"Moscow"},
    {"name":"Turkey","region":"Europe/Asia","bank":"Ziraat Bank","district":"Istanbul"},
    {"name":"Indonesia","region":"Asia","bank":"Bank Mandiri","district":"Jakarta"},
    {"name":"Thailand","region":"Asia","bank":"Bangkok Bank","district":"Bangkok"},
    {"name":"Malaysia","region":"Asia","bank":"Maybank","district":"Kuala Lumpur"},
    {"name":"Philippines","region":"Asia","bank":"BDO","district":"Manila"},
    {"name":"Vietnam","region":"Asia","bank":"Vietcombank","district":"Hanoi"},
    {"name":"Argentina","region":"South America","bank":"Banco Nación","district":"Buenos Aires"}
]

# ---------------------------
# SIGNUP
# ---------------------------
if st.session_state.page == "signup":
    st.title("📝 Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if name and email and phone and password:
            st.session_state.user = {
                "name": name,
                "email": email,
                "phone": phone,
                "password": password
            }
            st.session_state.page = "login"
            st.success("Account Created")
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
        user = st.session_state.get("user", {})
        if email == user.get("email") and password == user.get("password"):
            st.session_state.page = "countries"
            st.success("Login Success")
            st.rerun()
        else:
            st.error("Invalid login")

    if st.button("⬅️ Back"):
        st.session_state.page = "signup"
        st.rerun()

    st.stop()

# ---------------------------
# COUNTRY PAGE
# ---------------------------
if st.session_state.page == "countries":
    st.title("🌍 Select Country")

    search = st.text_input("🔍 Search Country")

    cols = st.columns(3)

    filtered = [c for c in countries if search.lower() in c["name"].lower()]

    for i, c in enumerate(filtered):
        with cols[i % 3]:
            st.markdown(f"""
            <div style='padding:15px;border-radius:12px;background:#fff;
            box-shadow:0px 2px 8px rgba(0,0,0,0.1);margin-bottom:10px'>
            <h4>{c['name']}</h4>
            <p>{c['region']}</p>
            <p>{c['bank']}</p>
            <p>{c['district']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Send to {c['name']}", key=i):
                st.session_state.selected_country = c
                st.session_state.page = "details"
                st.rerun()

    st.stop()

# ---------------------------
# PAYMENT DETAILS
# ---------------------------
if st.session_state.page == "details":
    st.title("💳 Enter Details")

    amount = st.number_input("Amount (INR)", min_value=1.0)
    pan = st.text_input("PAN")
    card = st.text_input("Card Number")

    if st.button("➡️ Next"):
        st.session_state.payment = {
            "amount": amount,
            "pan": pan,
            "card": card
        }
        st.session_state.page = "process"
        st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "countries"
        st.rerun()

    st.stop()

# ---------------------------
# PROCESS
# ---------------------------
st.title("🚀 Processing")

steps = ["KYC","Bank","Network","Forex","Settlement","Done"]
bar = st.progress(0)

for i, s in enumerate(steps):
    st.info(s)
    time.sleep(0.5)
    bar.progress((i+1)/len(steps))

amount = st.session_state.payment["amount"]
fee = amount * 0.045
usd = (amount - fee) / 83

txn = "TXN" + str(random.randint(100000,999999))

st.success(f"✅ Success | {txn}")
st.write(f"₹{amount} → ${round(usd,2)}")

if st.button("⬅️ Back Home"):
    st.session_state.page = "countries"
    st.rerun()

