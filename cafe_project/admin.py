import streamlit as st
from auth import require_login, logout
import json
from datetime import datetime, date
import os

MENU_FILE = "menu_data.json"
ORDERS_FILE = "orders_data.json"
SETTINGS_FILE = "settings.json"
TABLES_FILE = "tables_data.json"
USERS_FILE = "users_data.json"

def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def dashboard_page():
    st.header("🏠 Dashboard")
    menu_data = load_json(MENU_FILE)
    orders_data = load_json(ORDERS_FILE)
    total_items = sum(len(menu_data.get(key, [])) for key in menu_data)
    total_orders = len(orders_data)
    today_str = str(date.today())
    today_orders = [o for o in orders_data if o.get('date') == today_str]
    today_revenue = sum(o.get('total', 0) for o in today_orders)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Menu Items", total_items)
    col2.metric("Total Orders", total_orders)
    col3.metric("Today's Orders", len(today_orders))
    col4.metric("Today's Revenue", f"₹{today_revenue:.2f}")

def menu_management_page():
    ...
    # SAME CODE AS IN PREVIOUS ADMIN.PY (from your attached code)
    # copy the menu_management_page from my previous message or from your own cafe.py

def table_management_page():
    ...
    # SAME CODE AS IN PREVIOUS ADMIN.PY (from your attached code)

def order_management_page():
    ...
    # SAME CODE AS IN PREVIOUS ADMIN.PY (from your attached code)

def sales_analytics_page():
    ...
    # SAME CODE AS IN PREVIOUS ADMIN.PY (from your attached code)

def settings_page():
    ...
    # SAME CODE AS IN PREVIOUS ADMIN.PY (from your attached code)

def main():
    st.set_page_config(page_title="Cafe Admin Dashboard", page_icon="☕", layout="wide")
    if 'cart' not in st.session_state:
        st.session_state['cart'] = []
    if 'discount' not in st.session_state:
        st.session_state['discount'] = 0.0

    require_login()
    user = st.session_state['user']
    st.sidebar.title(f"Logged in as: {user['username']} ({user['role']})")
    menu_options = [
        "Dashboard",
        "Menu Management",
        "Order Management",
        "Sales Analytics",
        "Table Management",
        "Settings",
        "Logout"
    ]
    choice = st.sidebar.selectbox("Navigation", menu_options)
    if choice == "Logout":
        logout()
        st.experimental_rerun()
    elif choice == "Dashboard":
        dashboard_page()
    elif choice == "Menu Management":
        menu_management_page()
    elif choice == "Order Management":
        order_management_page()
    elif choice == "Sales Analytics":
        sales_analytics_page()
    elif choice == "Table Management":
        table_management_page()
    elif choice == "Settings":
        settings_page()

if __name__ == "__main__":
    main()
