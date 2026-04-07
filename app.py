import streamlit as st
from auth import register_user, login_user
from database import create_tables, get_connection

# -------------------------------
# INITIAL SETUP
# -------------------------------
st.set_page_config(page_title="dRiv.IT", layout="centered")

create_tables()

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
# HELPER: GET USER ROLE
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
# LOGIN / REGISTER PAGE
# -------------------------------
def login_page():
    st.title("🚗 dRiv.IT")
    st.subheader("Road Safety & Fleet Management")

    tab1, tab2 = st.tabs(["Sign In", "Register"])

    # -------------------
    # LOGIN
    # -------------------
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Sign In"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user = email
                st.session_state.role = get_user_role(email)

                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Invalid email or password")

    # -------------------
    # REGISTER
    # -------------------
    with tab2:
        email = st.text_input("New Email", key="reg_email")
        password = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Create Account"):
            if register_user(email, password):
                st.success("Account created! You can now sign in.")
            else:
                st.error("User already exists")


# -------------------------------
# DASHBOARDS
# -------------------------------
def admin_dashboard():
    st.title("🛠 Admin Portal")

    st.write("Welcome Admin:", st.session_state.user)

    st.divider()

    st.subheader("System Overview")
    st.write("• Manage Companies")
    st.write("• Manage Users")
    st.write("• View System Data")

    if st.button("Logout"):
        logout()


def user_dashboard():
    st.title("📊 Dashboard")

    st.write(f"Welcome {st.session_state.user}")

    st.divider()

    st.write("• View your company")
    st.write("• Manage your profile")
    st.write("• Access vehicles (coming next)")

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
# ROUTING LOGIC
# -------------------------------
if st.session_state.logged_in:

    # ROLE-BASED ROUTING
    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        user_dashboard()

else:
    login_page()
