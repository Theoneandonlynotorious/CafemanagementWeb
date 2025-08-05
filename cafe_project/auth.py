import streamlit as st
import json

USERS_FILE = "users_data.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        # Default admin/staff users if file is missing
        return [
            {"username": "admin", "password": "admin123", "role": "admin"},
            {"username": "staff", "password": "staff123", "role": "staff"},
        ]

def login(username, password):
    for user in load_users():
        if user['username'] == username and user['password'] == password:
            return user
    return None

def is_logged_in():
    return 'user' in st.session_state and st.session_state['user']

def logout():
    if 'user' in st.session_state:
        del st.session_state['user']

def require_login():
    if not is_logged_in():
        st.info("Please log in to access this page.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state['user'] = user
                st.success(f"Welcome, {user['username']}!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")
                st.stop()
        st.stop()
