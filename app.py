import streamlit as st
from auth import register_user, login_user
from database import create_tables, get_connection

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="dRiv.IT", layout="centered")

create_tables()

# -------------------------------
# LOAD FONTS
# -------------------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# -------------------------------
# DARK THEME STYLING
# -------------------------------
st.markdown("""
<style>

/* =========================
   BASE
========================= */
.stApp {
    background-color: #0B1E36;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #F3F4F6;
}

/* =========================
   HEADERS
========================= */
h1, h2, h3 {
    color: #FFFFFF;
}

/* =========================
   BUTTONS
========================= */
.stButton > button {
    background-color: #FF6600;
    color: white;
    border-radius: 10px;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #e65c00;
}

/* =========================
   INPUTS
========================= */
input, textarea {
    background-color: #1C1C1E !important;
    color: #FFFFFF !important;
    border: 1px solid #2A75D3 !important;
    border-radius: 8px !important;
}

/* =========================
   TABS
========================= */
button[data-baseweb="tab"] {
    color: #F3F4F6;
}

button[aria-selected="true"] {
    background-color: #2A75D3 !important;
}

/* =========================
   STATUS
========================= */
.stSuccess {
    color: #10B981;
}

/* =========================
   LINKS
========================= */
a {
    color: #2A75D3;
}

/* =========================
   DIVIDER
========================= */
hr {
    border: 1px solid #2A75D3;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None


# -------------------------------
# GET USER ROLE
# -------------------------------
def get_user_role(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()

    if result:
        return result[0]
    return None


# -------------------------------
# LOGIN PAGE
# -------------------------------
def login_page():
    st.markdown("""
    <h1 style='text-align:center; font-family: Exo 2;'>
        <span style='color:#FFFFFF;'>dRiv</span><span style='color:#FF6600;'>IT</span>
    </h1>
    <p style='text-align:center; color:#2A75D3;'>
        Fleet • Safety • Intelligence
    </p>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Sign In", "Register"])

    # LOGIN
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Sign In"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user = email
                st.session_state.role = get_user_role(email)
                st.success("Logged in")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # REGISTER
    with tab2:
        email = st.text_input("New Email", key="reg_email")
        password = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Create Account"):
            if register_user(email, password):
                st.success("Account created")
            else:
                st.error("User already exists")


# -------------------------------
# ADMIN DASHBOARD
# -------------------------------
def admin_dashboard():
    st.title("🛠 Admin Portal")
    st.write(f"Welcome Admin: {st.session_state.user}")

    st.divider()

    st.subheader("System Overview")
    st.write("• Companies (next)")
    st.write("• Users")
    st.write("• Fleet Data")

    if st.button("Logout"):
        logout()


# -------------------------------
# USER DASHBOARD
# -------------------------------
def user_dashboard():
    st.title("📊 Dashboard")
    st.write(f"Welcome {st.session_state.user}")

    st.divider()

    st.write("• Profile")
    st.write("• Company")
    st.write("• Vehicles (next)")

    if st.button("Logout"):
        logout()


# -------------------------------
# LOGOUT
# -------------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()


# -------------------------------
# ROUTING
# -------------------------------
if st.session_state.logged_in:
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        user_dashboard()
else:
    login_page()
