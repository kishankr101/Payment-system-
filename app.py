import requests

@st.cache_data(ttl=300)
def get_live_rates():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/INR"
        res = requests.get(url)
        data = res.json()
        return data["rates"]
    except:
        # fallback (important for mobile stability)
        return {
            "USD": 83,
            "EUR": 90,
            "GBP": 105
        }

rates = get_live_rates()
