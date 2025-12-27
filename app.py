import streamlit as st
from auth import signup, login
from chatbot import chatbot_response
from history import save_history, load_history

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Healthcare Disease Predictor 🩺",
    page_icon="🩺",
    layout="wide"
)


# 🎨 Custom CSS (PASTE HERE)
st.markdown("""
<style>
/* Target Streamlit images */
div[data-testid="stImage"] img {
    height: 260px !important;
    width: 100% !important;
    object-fit: cover;
    border-radius: 18px;
}
</style>
""", unsafe_allow_html=True)

# 🖼️ Images in same row
col1, col2 = st.columns(2)

with col1:
    st.image("assets/MYDOCTOR.jpeg", width=400)

with col2:
    st.image("assets/download.jpeg", width=400)


# ================= SESSION STATE =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= THEME SELECTOR =================
theme = st.sidebar.selectbox("🎨 Theme", ["Light", "Dark"])

# ================= LOAD CSS =================
def load_css(theme):
    with open("assets/style.css") as f:
        css = f.read()
    css = css.replace("{THEME}", theme.lower())
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css(theme)

st.markdown(
    '<div class="meditalk-greeting">Hello, I am Meditalk! 🌈<br>Here I will assist you about your health!</div>',
    unsafe_allow_html=True
)


# ================= MAIN HEADING =================
st.markdown("""
<div class="rainbow-title">
🩺 Healthcare Disease Predictor
</div>
<div class="subtitle-box">
AI-powered symptom analysis & disease prediction
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR MENU =================
menu = st.sidebar.radio("Menu", ["Login", "Signup"])

# ================= SIGNUP =================
if menu == "Signup":
    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
    st.subheader("✨ Create Account")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Create Account"):
        if signup(u, p):
            st.success("Account created successfully! Please login.")
        else:
            st.error("User already exists")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= LOGIN =================
if menu == "Login":
    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
    st.subheader("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(u, p):
            st.session_state.user = u
            st.success(f"Welcome to Meditalk! You will get the best advice here!, {u} 👋")
        else:
            st.error("Invalid username or password. Please try again.")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= CHATBOT =================
if st.session_state.user:
    st.markdown("---")
    st.subheader("🧠Please Describe Your Symptoms")

    user_input = st.text_area(
        "Enter your symptoms",
        placeholder="Example: I have fever, headache and body pain for 2 days",
        height=120
    )

    days = st.number_input(
        "Duration (number of days)",
        min_value=1,
        max_value=60,
        value=1
    )

    severity = st.slider(
        "Severity Level (1 = Mild, 10 = Severe)",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button("Predict Disease"):
        if user_input.strip() == "":
            st.warning("Dear patient, Please enter your symptoms.")
        else:
            response = chatbot_response(user_input, days, severity)

            # -------- DISPLAY RESULT --------
            st.success(f"🩺 **Let me tell you the Possible Diseases :** {response['disease']}")
            st.info(f"📊 **Confidence:** {response['confidence']}%")

            st.subheader("🛡 Do not worry dear. We will tell you some Precautions")
            for p in response["precautions"]:
                st.write(f"- {p}")

            if response["others"]:
                st.subheader("🔍 Other Possible Diseases are as follows :")
                for d in response["others"]:
                    st.write(f"- {d}")

            st.write(f"⏱ **Duration:** {response['days']} day(s)")
            st.write(f"🔥 **Severity Level:** {response['severity']}/10")

            # -------- SAVE HISTORY --------
            save_history(st.session_state.user, {
                "input": user_input,
                "days": days,
                "severity": severity,
                "result": response
            })

    st.markdown("---")
    if st.button("📜 View History"):
        history = load_history(st.session_state.user)
        if history:
            st.json(history)
        else:
            st.info("No history available yet.")
