import streamlit as st
import time
import random

st.set_page_config(page_title="GlobalPay Pro", layout="wide")

# ---------------------------
# MODERN UI
# ---------------------------
st.markdown("""
<style>
body {background: linear-gradient(135deg,#eef2ff,#f8fafc);}
.card {
    padding:15px;
    border-radius:15px;
    background:white;
    box-shadow:0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom:10px;
}
.stButton>button {
    background: linear-gradient(90deg,#4facfe,#00f2fe);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}
.bottom-nav {
    position: fixed;
    bottom: 0;
    width: 100%;
    background: white;
    display: flex;
    justify-content: space-around;
    padding: 10px;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
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
{"name":"USA","region":"North America","bank":"Bank of America","district":"California","currency":"USD"},
{"name":"UK","region":"Europe","bank":"HSBC","district":"London","currency":"GBP"},
{"name":"Germany","region":"Europe","bank":"Deutsche Bank","district":"Berlin","currency":"EUR"},
{"name":"France","region":"Europe","bank":"BNP","district":"Paris","currency":"EUR"},
{"name":"Japan","region":"Asia","bank":"MUFG","district":"Tokyo","currency":"JPY"},
{"name":"China","region":"Asia","bank":"ICBC","district":"Beijing","currency":"CNY"},
{"name":"India","region":"Asia","bank":"SBI","district":"Delhi","currency":"INR"},
{"name":"UAE","region":"Middle East","bank":"Emirates NBD","district":"Dubai","currency":"AED"},
{"name":"Australia","region":"Oceania","bank":"ANZ","district":"Sydney","currency":"AUD"},
{"name":"Canada","region":"North America","bank":"RBC","district":"Toronto","currency":"CAD"},
{"name":"Singapore","region":"Asia","bank":"DBS","district":"Singapore","currency":"SGD"},
{"name":"Brazil","region":"South America","bank":"Itau","district":"Sao Paulo","currency":"BRL"},
{"name":"South Africa","region":"Africa","bank":"Standard Bank","district":"Johannesburg","currency":"ZAR"},
{"name":"Italy","region":"Europe","bank":"UniCredit","district":"Rome","currency":"EUR"},
{"name":"Spain","region":"Europe","bank":"Santander","district":"Madrid","currency":"EUR"},
{"name":"Netherlands","region":"Europe","bank":"ING","district":"Amsterdam","currency":"EUR"},
{"name":"Switzerland","region":"Europe","bank":"UBS","district":"Zurich","currency":"CHF"},
{"name":"Sweden","region":"Europe","bank":"SEB","district":"Stockholm","currency":"SEK"},
{"name":"Norway","region":"Europe","bank":"DNB","district":"Oslo","currency":"NOK"},
{"name":"Denmark","region":"Europe","bank":"Danske Bank","district":"Copenhagen","currency":"DKK"},
{"name":"Finland","region":"Europe","bank":"Nordea","district":"Helsinki","currency":"EUR"},
{"name":"Mexico","region":"North America","bank":"Banorte","district":"Mexico City","currency":"MXN"},
{"name":"Russia","region":"Europe","bank":"Sberbank","district":"Moscow","currency":"RUB"},
{"name":"Turkey","region":"Europe","bank":"Ziraat","district":"Istanbul","currency":"TRY"},
{"name":"Indonesia","region":"Asia","bank":"Mandiri","district":"Jakarta","currency":"IDR"},
{"name":"Thailand","region":"Asia","bank":"Bangkok Bank","district":"Bangkok","currency":"THB"},
{"name":"Malaysia","region":"Asia","bank":"Maybank","district":"KL","currency":"MYR"},
{"name":"Philippines","region":"Asia","bank":"BDO","district":"Manila","currency":"PHP"},
{"name":"Vietnam","region":"Asia","bank":"Vietcombank","district":"Hanoi","currency":"VND"},
{"name":"Argentina","region":"South America","bank":"Banco Nacion","district":"Buenos Aires","currency":"ARS"}
]

rates = {"USD":83,"GBP":105,"EUR":90,"JPY":0.55,"CNY":11,"AED":22,"AUD":55,"CAD":60,"SGD":61,"INR":1}

# ---------------------------
# SIGNUP
# ---------------------------
if st.session_state.page == "signup":
    st.title("📝 Create Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Next ➡️"):
        if email and password:
            st.session_state.user = {"email":email,"password":password}
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

    if st.button("Login ➡️"):
        u = st.session_state.user
        if email == u["email"] and password == u["password"]:
            st.session_state.page = "profile"
            st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "signup"
        st.rerun()
    st.stop()

# ---------------------------
# PROFILE
# ---------------------------
if st.session_state.page == "profile":
    st.title("👤 Complete Profile")

    name = st.text_input("Name")
    phone = st.text_input("Phone")
    gender = st.selectbox("Gender",["Male","Female","Other"])
    region = st.text_input("Region")
    job = st.text_input("Occupation")

    if st.button("Save ➡️"):
        st.session_state.profile = {
            "name":name,"phone":phone,"gender":gender,"region":region,"job":job
        }
        st.session_state.page = "home"
        st.rerun()
    st.stop()

# ---------------------------
# HOME (COUNTRIES)
# ---------------------------
if st.session_state.page == "home":
    st.title("🌍 Select Country")

    search = st.text_input("🔍 Search")

    cols = st.columns(3)

    filtered = [c for c in countries if search.lower() in c["name"].lower()]

    for i,c in enumerate(filtered):
        with cols[i%3]:
            st.markdown(f"""
            <div class='card'>
            🌎 <b>{c['name']}</b><br>
            📍 {c['region']}<br>
            🏦 {c['bank']}<br>
            🏙 {c['district']}
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Send → {c['name']}", key=i):
                st.session_state.country = c
                st.session_state.page = "payment"
                st.rerun()
    st.stop()

# ---------------------------
# PAYMENT
# ---------------------------
if st.session_state.page == "payment":
    st.title("💳 Payment")

    amount = st.number_input("Amount INR", min_value=1.0)
    card = st.text_input("Card Number")

    mode = st.selectbox("Mode",["SWIFT","PayPal","Visa","Mastercard"])

    currency = st.session_state.country["currency"]
    rate = rates.get(currency,83)

    converted = amount / rate
    st.info(f"💱 {round(converted,2)} {currency}")

    if st.button("Next ➡️"):
        st.session_state.payment = {"amount":amount,"converted":converted,"currency":currency,"mode":mode}
        st.session_state.page = "process"
        st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "home"
        st.rerun()
    st.stop()

# ---------------------------
# PROCESS
# ---------------------------
st.title("🚀 Processing")

steps = ["KYC","Fraud","Bank","Network","Forex","Settlement"]
bar = st.progress(0)

for i,s in enumerate(steps):
    st.info(f"⚙️ {s}")
    time.sleep(0.5)
    bar.progress((i+1)/len(steps))

txn = "TXN"+str(random.randint(100000,999999))
data = st.session_state.payment

st.success(f"✅ Success | {txn}")
st.write(f"₹{data['amount']} → {round(data['converted'],2)} {data['currency']}")
st.write(f"Mode: {data['mode']}")

if st.button("⬅️ Back Home"):
    st.session_state.page = "home"
    st.rerun()

# ---------------------------
# BOTTOM NAV
# ---------------------------
col1,col2,col3 = st.columns(3)

if col1.button("🏠 Home"):
    st.session_state.page = "home"
    st.rerun()

if col2.button("👤 Profile"):
    st.session_state.page = "profile"
    st.rerun()

if col3.button("🚪 Logout"):
    st.session_state.page = "login"
    st.rerun()
