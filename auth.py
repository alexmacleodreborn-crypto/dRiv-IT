import streamlit as st
import bcrypt

# TEMP in-memory store (replace with DB later)
users = {}

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def register_user(email, password):
    if email in users:
        return False
    users[email] = hash_password(password)
    return True

def login_user(email, password):
    if email in users and check_password(password, users[email]):
        return True
    return False
