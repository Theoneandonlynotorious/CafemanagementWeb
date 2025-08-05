import streamlit as st
import json
from datetime import datetime, date

MENU_FILE = "menu_data.json"
ORDERS_FILE = "orders_data.json"

def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def show_customer_menu():
    st.title("My Cafe - Customer Order")
    menu_data = load_json(MENU_FILE)
    st.header("Menu")
    cart = st.session_state.get('cart', [])
    for category, items in menu_data.items():
        if items:
            st.subheader(category.capitalize())
            for item in items:
                if not item.get('available', True):
                    continue
                col1, col2, col3 = st.columns([3,1,2])
                with col1:
                    st.write(f"**{item['name']}**")
                    if item.get("description"):
                        st.write(f"_{item['description']}_")
                    st.write(f"Inventory: {item.get('inventory', 0)}")
                with col2:
                    st.write(f"₹{item['price']:.2f}")
                with col3:
                    qty = st.number_input(
                        f"Qty {item['id']}", min_value=0, max_value=item.get('inventory',0),
                        key=f"qty_{item['id']}"
                    )
                    if st.button("Add", key=f"add_{item['id']}"):
                        if qty > 0 and qty <= item.get('inventory',0):
                            cart.append({
                                "id": item["id"],
                                "name": item["name"],
                                "price": item["price"],
                                "quantity": int(qty),
                                "subtotal": round(item["price"]*qty,2)
                            })
                            st.session_state['cart'] = cart
                            st.success(f"Added {qty} x {item['name']}")
                            st.experimental_rerun()
    st.divider()
    st.header("Your Cart")
    if cart:
        total = sum(item['subtotal'] for item in cart)
        to_remove = []
        for idx, item in enumerate(cart):
            c1, c2, c3, c4 = st.columns([4,1,1,1])
            c1.write(item["name"])
            c2.write(f"x{item['quantity']}")
            c3.write(f"₹{item['subtotal']:.2f}")
            if c4.button("Remove", key=f"remove_{idx}"):
                to_remove.append(idx)
        for idx in reversed(to_remove):
            cart.pop(idx)
        st.session_state['cart'] = cart
        discount = st.number_input("Discount (₹)", min_value=0.0, max_value=total, step=0.10, value=st.session_state.get("discount",0.0))
        st.session_state['discount'] = discount
        tax_rate = 0.10
        service_charge = 0.05
        tax_amt = (total - discount) * tax_rate
        service_amt = (total - discount) * service_charge
        final_total = total - discount + tax_amt + service_amt
        st.write("---")
        st.write(f"Subtotal: ₹{total:.2f}")
        st.write(f"Discount: -₹{discount:.2f}")
        st.write(f"Tax (10%): +₹{tax_amt:.2f}")
        st.write(f"Service Charge (5%): +₹{service_amt:.2f}")
        st.write(f"**Total: ₹{final_total:.2f}**")
        customer_name = st.text_input("Your Name")
        table_number = st.text_input("Table Number (optional)")
        if st.button("Place Order"):
            if not customer_name:
                st.error("Please enter your name")
            else:
                orders = load_json(ORDERS_FILE)
                new_order = {
                    "id": f"ORD{len(orders)+1:05d}",
                    "customer_name": customer_name,
                    "table_number": table_number,
                    "items": cart.copy(),
                    "subtotal": total,
                    "discount": discount,
                    "tax": tax_amt,
                    "service_charge":service_amt,
                    "total": final_total,
                    "date": str(date.today()),
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "timestamp": datetime.now().isoformat(),
                    "status": "Pending",
                    "payment_status": "Unpaid"
                }
                orders.append(new_order)
                save_json(ORDERS_FILE, orders)
                # Decrement inventory in menu file
                menu_data_changed = False
                for citem in cart:
                    for cat in menu_data:
                        for mitem in menu_data[cat]:
                            if mitem["id"] == citem["id"]:
                                mitem["inventory"] -= citem["quantity"]
                                menu_data_changed = True
                if menu_data_changed:
                    save_json(MENU_FILE, menu_data)
                st.success("✅ Order placed! A staff member will confirm your order shortly. Thank you!")
                st.session_state['cart'] = []
                st.session_state['discount'] = 0
                st.experimental_rerun()
    else:
        st.info("No items in your cart yet.")

def main():
    st.set_page_config(page_title="Cafe Menu", page_icon="☕", layout="centered")
    if 'cart' not in st.session_state:
        st.session_state['cart'] = []
    if 'discount' not in st.session_state:
        st.session_state['discount'] = 0.0
    show_customer_menu()

if __name__ == "__main__":
    main()
