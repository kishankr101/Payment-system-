import streamlit as st
import time
import random

# ---------------------------
# PAGE CONFIG & THEME
# ---------------------------
st.set_page_config(page_title="GlobalPay Pro", layout="wide", page_icon="💳")

# Advanced CSS for Professional UI/UX
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Custom Card Style */
    .card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
        text-align: center;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25);
        background: white;
    }

    /* Buttons Styling */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        color: white !important;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4);
        transform: scale(1.02);
    }

    /* Bottom Navigation Bar */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 15px 0;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.05);
        z-index: 999;
    }
    
    /* Title Styling */
    .main-title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1e293b;
        font-weight: 800;
        text-align: center;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION STATE INITIALIZATION
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "signup"
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "profile_complete" not in st.session_state:
    st.session_state.profile_complete = False

# ---------------------------
# DATABASE (30+ Countries)
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
    st.rerun()

# ---------------------------
# PAGE: SIGNUP
# ---------------------------
if st.session_state.page == "signup":
    st.markdown("<h1 class='main-title'>📝 Create Account</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            email = st.text_input("📧 Email Address")
            password = st.text_input("🔑 Password", type="password")
            if st.button("Create Account ➡️"):
                if email and password:
                    st.session_state.user = {"email": email, "password": password}
                    go_to("login")
                else:
                    st.error("Please fill all fields")
    st.stop()

# ---------------------------
# PAGE: LOGIN
# ---------------------------
if st.session_state.page == "login":
    st.markdown("<h1 class='main-title'>🔐 Secure Login</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            email = st.text_input("📧 Email Address")
            password = st.text_input("🔑 Password", type="password")
            if st.button("Login Now ➡️"):
                if "user" in st.session_state and email == st.session_state.user["email"] and password == st.session_state.user["password"]:
                    st.session_state.user_authenticated = True
                    go_to("profile")
                else:
                    st.error("Invalid credentials")
            st.button("⬅️ Create Account", on_click=go_to, args=("signup",))
    st.stop()

# ---------------------------
# PAGE: PROFILE (Setup & Edit)
# ---------------------------
if st.session_state.page == "profile":
    st.markdown("<h1 class='main-title'>👤 User Profile</h1>", unsafe_allow_html=True)
    
    # Check if profile already exists
    if "profile" not in st.session_state:
        st.session_state.profile = {"name":"", "phone":"", "gender":"Male", "region":"", "job":""}

    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            # View Mode vs Edit Mode
            if "edit_mode" not in st.session_state: st.session_state.edit_mode = False
            
            if st.session_state.edit_mode:
                name = st.text_input("Full Name", value=st.session_state.profile["name"])
                phone = st.text_input("Phone Number", value=st.session_state.profile["phone"])
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male","Female","Other"].index(st.session_state.profile["gender"]))
                region = st.text_input("Region/City", value=st.session_state.profile["region"])
                job = st.text_input("Occupation", value=st.session_state.profile["job"])
                
                if st.button("💾 Save Changes"):
                    st.session_state.profile = {"name":name, "phone":phone, "gender":gender, "region":region, "job":job}
                    st.session_state.edit_mode = False
                    st.session_state.profile_complete = True
                    st.rerun()
            else:
                st.markdown(f"""
                <div class='card'>
                    <h3>Welcome, {st.session_state.profile['name'] if st.session_state.profile['name'] else 'User'}!</h3>
                    <p>📞 <b>Phone:</b> {st.session_state.profile['phone']}</p>
                    <p>⚧️ <b>Gender:</b> {st.session_state.profile['gender']}</p>
                    <p>📍 <b>Region:</b> {st.session_state.profile['region']}</p>
                    <p>💼 <b>Occupation:</b> {st.session_state.profile['job']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if not st.session_state.profile_complete:
                    st.button("Complete Profile ➡️", on_click=lambda: setattr(st.session_state, 'edit_mode', True))
                else:
                    st.button("✏️ Edit Profile", on_click=lambda: setattr(st.session_state, 'edit_mode', True))
                    st.button("Go to Dashboard ➡️", on_click=go_to, args=("home",))

    # Bottom Nav only if authenticated
    if st.session_state.user_authenticated:
        render_bottom_nav()
    st.stop()

# ---------------------------
# PAGE: HOME (Country Selection)
# ---------------------------
if st.session_state.page == "home":
    st.markdown("<h1 class='main-title'>🌍 Global Transfers</h1>", unsafe_allow_html=True)
    
    # Search Engine
    search = st.text_input("🔍 Search country, region or bank...", placeholder="e.g. Germany or Europe")
    
    filtered = [c for c in countries if search.lower() in c["name"].lower() or search.lower() in c["region"].lower()]
    
    # Grid layout
    cols = st.columns(3)
    for i, c in enumerate(filtered):
        with cols[i%3]:
            st.markdown(f"""
            <div class='card'>
                <h2 style='margin:0;'>{c['flag']} {c['name']}</h2>
                <p style='color:gray; margin:5px 0;'>📍 {c['region']} | 🏙 {c['district']}</p>
                <p style='font-weight:bold; color:#4facfe;'>🏦 {c['bank']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Send Money →", key=f"btn_{i}"):
                st.session_state.country = c
                go_to("payment")
    
    render_bottom_nav()
    st.stop()

# ---------------------------
# PAGE: PAYMENT
# ---------------------------
if st.session_state.page == "payment":
    st.markdown("<h1 class='main-title'>💳 Transfer Funds</h1>", unsafe_allow_html=True)
    
    c = st.session_state.country
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown(f"<div class='card'><b>Sending to:</b> {c['flag']} {c['name']} ({c['bank']})</div>", unsafe_allow_html=True)
            
            amount = st.number_input("Amount in INR (₹)", min_value=1.0, step=100.0)
            card_num = st.text_input("💳 Card Number", placeholder="0000 0000 0000 0000")
            mode = st.selectbox("Payment Method", ["SWIFT", "PayPal", "Visa", "Mastercard", "Apple Pay"])
            
            currency = c["currency"]
            rate = rates.get(currency, 83)
            converted = amount / rate
            
            st.markdown(f"""
            <div style='text-align:center; padding:10px; background:#e0f2fe; border-radius:10px; margin:10px 0;'>
                <h3 style='margin:0;'>💱 Estimated Arrival: {round(converted, 2)} {currency}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Confirm & Pay ➡️"):
                st.session_state.payment = {"amount": amount, "converted": converted, "currency": currency, "mode": mode}
                go_to("process")
            
            st.button("⬅️ Back to Countries", on_click=go_to, args=("home",))
    
    render_bottom_nav()
    st.stop()

# ---------------------------
# PAGE: PROCESS & SUCCESS
# ---------------------------
if st.session_state.page == "process":
    st.markdown("<h1 class='main-title'>🚀 Processing Transaction</h1>", unsafe_allow_html=True)
    
    progress_text = "Verifying Details..."
    bar = st.progress(0)
    status = st.empty()
    
    steps = [
        ("🔍 KYC Verification", 0.2),
        ("🛡️ Fraud Detection", 0.4),
        ("🏦 Bank Handshake", 0.6),
        ("🌐 Network Routing", 0.8),
        ("💸 Forex Conversion", 1.0)
    ]
    
    for step, val in steps:
        status.info(f"⚙️ {step}")
        bar.progress(val)
        time.sleep(0.7)
    
    txn_id = "GP"+str(random.randint(1000000, 9999999))
    data = st.session_state.payment
    
    st.balloons()
    st.markdown(f"""
    <div class='card' style='text-align:center; border: 2px solid #4caf50;'>
        <h1 style='color:#4caf50;'>✅ Success!</h1>
        <p>Transaction ID: <b>{txn_id}</b></p>
        <hr>
        <h3>₹{data['amount']} ➡️ {round(data['converted'],2)} {data['currency']}</h3>
        <p>Method: {data['mode']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 Return Home"):
        go_to("home")
    
    render_bottom_nav()
    st.stop()

# ---------------------------
# BOTTOM NAVIGATION BAR COMPONENT
# ---------------------------
def render_bottom_nav():
    st.markdown("---") # Visual separator
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    with nav_col1:
        if st.button("🏠 Home"):
            go_to("home")
    with nav_col2:
        if st.button("👤 Profile"):
            go_to("profile")
    with nav_col3:
        if st.button("🚪 Logout"):
            st.session_state.user_authenticated = False
            st.session_state.profile_complete = False
            go_to("login")
