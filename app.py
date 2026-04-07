import streamlit as st
from auth import register_user, login_user

st.set_page_config(page_title="dRiv.IT", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


def login_page():
    st.title("🚗 dRiv.IT")

    tab1, tab2 = st.tabs(["Sign In", "Register"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            if login_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user = email
                st.success("Logged in")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        email = st.text_input("New Email")
        password = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if register_user(email, password):
                st.success("Account created")
            else:
                st.error("User already exists")


def dashboard():
    st.title("Dashboard")
    st.write(f"Welcome {st.session_state.user}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


# ROUTING
if st.session_state.logged_in:
    dashboard()
else:
    login_page()
