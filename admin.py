import streamlit as st
import data

st.set_page_config(page_title="Admin - Forchetta D'oro", page_icon="🔧")

# Simple password protection
ADMIN_PASSWORD = "admin123"  # Change this!

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.title("🔐 Admin Login")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Invalid password")
    st.stop()

st.title("🔧 Admin Dashboard - Forchetta D'oro")

if st.sidebar.button("Logout"):
    st.session_state.admin_authenticated = False
    st.rerun()

# Add Restaurant
st.subheader("Add New Restaurant")
with st.form("add_restaurant"):
    name = st.text_input("Restaurant Name")
    address = st.text_input("Address (optional)")
    if st.form_submit_button("Add Restaurant", type="primary"):
        if name.strip():
            data.add_restaurant(name.strip(), address.strip())
            st.success(f"Added '{name}'!")
            st.rerun()
        else:
            st.error("Name is required")

# Manage Restaurants
st.subheader("Manage Restaurants")
rankings = data.get_rankings()

if not rankings:
    st.info("No restaurants yet.")
else:
    for r in rankings:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{r['name']}**")
                if r["address"]:
                    st.caption(r["address"])
            with col2:
                st.write(f"⭐ {r['avg_rating']:.1f} ({r['review_count']} reviews)")
            with col3:
                if st.button("🗑️ Delete", key=f"del_{r['id']}"):
                    data.delete_restaurant(r["id"])
                    st.rerun()
