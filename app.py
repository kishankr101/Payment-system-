import streamlit as st
import time
import random

# ---------------------------
# PAGE CONFIG & THEME
# ---------------------------
st.set_page_config(page_title="GlobalPay Pro", layout="wide", page_icon="💳")

# Professional UI/UX CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        transition: transform 0.3s ease;
        margin-bottom: 20px;
        text-align: center;
    }
    .card:hover { transform: translateY(-5px); background: white; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white !important;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4); transform: scale(1.02); }
    .main-title {
        font-family: 'Segoe UI', sans-serif;
        color: #1e293b;
        font-weight: 800;
        text-align: center;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION STATE
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "signup"
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "profile_complete" not in st.session_state:
    st.session_state.profile_complete = False

# ---------------------------
# DATA
# ---------------------------
countries = [
    {"name":"USA","region":"North America","bank":"Bank of America","district":"California","currency":"USD","flag":"🇺🇸"},
    {"name":"UK","region":"Europe","bank":"HSBC","district":"London","currency":"GBP","flag":"🇬🇧"},
    {"name":"Germany","region":"Europe","bank":"Deutsche Bank","district":"Berlin","currency":"EUR","flag":"🇩🇪"},
    {"name":"France","region":"Europe","bank":"BNP","district":"Paris","currency":"EUR","flag":"🇫🇷"},
    {"name":"Japan","region":"Asia","bank":"MUFG","district":"Tokyo","currency":"JPY","flag":"🇯🇵"},
    {"name":"China","region":"Asia","bank":"ICBC","district":"Beijing","currency":"CNY","flag":"🇨🇳"},
    {"name":"India","region":"Asia","bank":"SBI","district":"Delhi","currency":"INR","flag":"🇮🇳"},
    {"name":"UAE","region":"Middle East","bank":"Emirates NBD","district":"Dubai","currency":"AED","flag":"🇦🇪"},
    {"name":"Australia","region":"Oceania","bank":"ANZ","district":"Sydney","currency":"AUD","flag":"🇦🇺"},
    {"name":"Canada","region":"North America","bank":"RBC","district":"Toronto","currency":"CAD","flag":"🇨🇦"},
    {"name":"Singapore","region":"Asia","bank":"DBS","district":"Singapore","currency":"SGD","flag":"🇸🇬"},
    {"name":"Brazil","region":"South America","bank":"Itau","district":"Sao Paulo","currency":"BRL","flag":"🇧🇷"},
    {"name":"South Africa","region":"Africa","bank":"Standard Bank","district":"Johannesburg","currency":"ZAR","flag":"🇿🇦"},
    {"name":"Italy","region":"Europe","bank":"UniCredit","district":"Rome","currency":"EUR","flag":"🇮🇹"},
    {"name":"Spain","region":"Europe","bank":"Santander","district":"Madrid","currency":"EUR","flag":"🇪🇸"},
    {"name":"Netherlands","region":"Europe","bank":"ING","district":"Amsterdam","currency":"EUR","flag":"🇳🇱"},
    {"name":"Switzerland","region":"Europe","bank":"UBS","district":"Zurich","currency":"CHF","flag":"🇨🇭"},
    {"name":"Sweden","region":"Europe","bank":"SEB","district":"Stockholm","currency":"SEK","flag":"🇸🇪"},
    {"name":"Norway","region":"Europe","bank":"DNB","district":"Oslo","currency":"NOK","flag":"🇳🇴"},
    {"name":"Denmark","region":"Europe","bank":"Danske Bank","district":"Copenhagen","currency":"DKK","flag":"🇩🇰"},
    {"name":"Finland","region":"Europe","bank":"Nordea","district":"Helsinki","currency":"EUR","flag":"🇫🇮"},
    {"name":"Mexico","region":"North America","bank":"Banorte","district":"Mexico City","currency":"MXN","flag":"🇲🇽"},
    {"name":"Russia","region":"Europe","bank":"Sberbank","district":"Moscow","currency":"RUB","flag":"🇷🇺"},
    {"name":"Turkey","region":"Europe","bank":"Ziraat","district":"Istanbul","currency":"TRY","flag":"🇹🇷"},
    {"name":"Indonesia","region":"Asia","bank":"Mandiri","district":"Jakarta","currency":"IDR","flag":"🇮🇩"},
    {"name":"Thailand","region":"Asia","bank":"Bangkok Bank","district":"Bangkok","currency":"THB","flag":"🇹🇭"},
    {"name":"Malaysia","region":"Asia","bank":"Maybank","district":"KL","currency":"MYR","flag":"🇲🇾"},
    {"name":"Philippines","region":"Asia","bank":"BDO","district":"Manila","currency":"PHP","flag":"🇵🇭"},
    {"name":"Vietnam","region":"Asia","bank":"Vietcombank","district":"Hanoi","currency":"VND","flag":"🇻🇳"},
    {"name":"Argentina","region":"South America","bank":"Banco Nacion","district":"Buenos Aires","currency":"ARS","flag":"🇦🇷"},
    {"name":"Egypt","region":"Africa","bank":"CIB","district":"Cairo","currency":"EGP","flag":"🇪🇬"},
    {"name":"Saudi Arabia","region":"Middle East","bank":"Al Rajhi","district":"Riyadh","currency":"SAR","flag":"🇸🇦"},
]
rates = {"USD":83, "GBP":105, "EUR":90, "JPY":0.55, "CNY":11, "AED":22, "AUD":55, "CAD":60, "SGD":61, "INR":1, "BRL":5, "ZAR":6, "CHF":95, "SEK":1.1, "NOK":1.1, "DKK":1.2, "MXN":0.4, "RUB":0.1, "TRY":0.25, "IDR":0.005, "THB":0.23, "MYR":2.2, "PHP":0.12, "VND":0.003, "ARS":0.08, "EGP":0.17, "SAR":22}

# ---------------------------
# NAVIGATION HELPER
# ---------------------------
def go_to(page):
    st.session_state.page = page

# ---------------------------
# BOTTOM NAV COMPONENT
# ---------------------------
def render_bottom_nav():
    st.markdown("---")
    n1, n2, n3 = st.columns(3)
    with n1: 
        if st.button("🏠 Home"): go_to("home"); st.rerun()
    with n2: 
        if st.button("👤 Profile"): go_to("profile"); st.rerun()
    with n3: 
        if st.button("🚪 Logout"): 
            st.session_state.user_authenticated = False
            go_to("login"); st.rerun()

# ---------------------------
# MAIN ROUTER (The fix for errors)
# ---------------------------
if st.session_state.page == "signup":
    st.markdown("<h1 class='main-title'>📝 Create Account</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        if st.button("Next ➡️"):
            if email and password:
                st.session_state.user = {"email": email, "password": password}
                go_to("login")
                st.rerun()

elif st.session_state.page == "login":
    st.markdown("<h1 class='main-title'>🔐 Login</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")
        if st.button("Login ➡️"):
            if "user" in st.session_state and email == st.session_state.user["email"] and password == st.session_state.user["password"]:
                st.session_state.user_authenticated = True
                go_to("profile")
                st.rerun()
            else: st.error("Invalid Credentials")
        if st.button("⬅️ Back to Signup"):
            go_to("signup")
            st.rerun()

elif st.session_state.page == "profile":
    st.markdown("<h1 class='main-title'>👤 Profile</h1>", unsafe_allow_html=True)
    if "profile" not in st.session_state:
        st.session_state.profile = {"name":"", "phone":"", "gender":"Male", "region":"", "job":""}
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if "edit_mode" not in st.session_state: st.session_state.edit_mode = False
        if st.session_state.edit_mode:
            name = st.text_input("Name", value=st.session_state.profile["name"])
            phone = st.text_input("Phone", value=st.session_state.profile["phone"])
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male","Female","Other"].index(st.session_state.profile["gender"]))
            region = st.text_input("Region", value=st.session_state.profile["region"])
            job = st.text_input("Job", value=st.session_state.profile["job"])
            if st.button("💾 Save"):
                st.session_state.profile = {"name":name, "phone":phone, "gender":gender, "region":region, "job":job}
                st.session_state.edit_mode = False
                st.session_state.profile_complete = True
                st.rerun()
        else:
            st.markdown(f"""<div class='card'><h3>{st.session_state.profile['name'] or 'User'}</h3>
            <p>📞 {st.session_state.profile['phone']} | 📍 {st.session_state.profile['region']}</p>
            <p>💼 {st.session_state.profile['job']}</p></div>""", unsafe_allow_html=True)
            if st.button("✏️ Edit Profile"):
                st.session_state.edit_mode = True
                st.rerun()
            if st.button("Continue to Home ➡️"):
                go_to("home")
                st.rerun()
    if st.session_state.user_authenticated: render_bottom_nav()

elif st.session_state.page == "home":
    st.markdown("<h1 class='main-title'>🌍 Select Country</h1>", unsafe_allow_html=True)
    search = st.text_input("🔍 Search Country or Bank")
    filtered = [c for c in countries if search.lower() in c["name"].lower() or search.lower() in c["bank"].lower()]
    cols = st.columns(3)
    for i, c in enumerate(filtered):
        with cols[i%3]:
            st.markdown(f"<div class='card'><h2>{c['flag']} {c['name']}</h2><p>{c['bank']}</p></div>", unsafe_allow_html=True)
            if st.button(f"Send →", key=f"h_{i}"):
                st.session_state.country = c
                go_to("payment")
                st.rerun()
    render_bottom_nav()

elif st.session_state.page == "payment":
    st.markdown("<h1 class='main-title'>💳 Payment</h1>", unsafe_allow_html=True)
    c = st.session_state.country
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"<div class='card'>Sending to {c['flag']} {c['name']}</div>", unsafe_allow_html=True)
        amt = st.number_input("Amount INR", min_value=1.0)
        mode = st.selectbox("Mode", ["SWIFT", "PayPal", "Visa", "Mastercard"])
        conv = amt / rates.get(c["currency"], 83)
        st.info(f"💱 Received: {round(conv, 2)} {c['currency']}")
        if st.button("Pay Now ➡️"):
            st.session_state.payment = {"amount": amt, "converted": conv, "currency": c["currency"], "mode": mode}
            go_to("process")
            st.rerun()
        if st.button("⬅️ Back"):
            go_to("home")
            st.rerun()
    render_bottom_nav()

elif st.session_state.page == "process":
    st.markdown("<h1 class='main-title'>🚀 Processing</h1>", unsafe_allow_html=True)
    bar = st.progress(0)
    steps = ["KYC Check", "Fraud Check", "Bank Routing", "Forex Sync"]
    for i, s in enumerate(steps):
        st.text(f"⚙️ {s}...")
        bar.progress((i+1)/len(steps))
        time.sleep(0.5)
    
    st.balloons()
    d = st.session_state.payment
    st.markdown(f"<div class='card'><h1>✅ Success</h1><p>₹{d['amount']} → {round(d['converted'],2)} {d['currency']}</p></div>", unsafe_allow_html=True)
    if st.button("🏠 Home"):
        go_to("home")
        st.rerun()
    render_bottom_nav()
