import streamlit as st
import data

st.set_page_config(page_title="Forchetta D'oro", page_icon="🍴", layout="wide")

st.title("🍴 Forchetta D'oro")
st.caption("Rate the best restaurants in the neighborhood!")

# User name input (persisted in session)
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

with st.sidebar:
    st.session_state.user_name = st.text_input("Your name", st.session_state.user_name, placeholder="Anonymous")

tab1, tab2 = st.tabs(["📊 Rankings", "⭐ Leave a Review"])

# Rankings Tab
with tab1:
    st.subheader("Current Rankings")
    if st.button("🔄 Refresh", key="refresh_rankings"):
        st.rerun()
    
    rankings = data.get_rankings()
    if not rankings:
        st.info("No restaurants yet. Ask the admin to add some!")
    else:
        for i, r in enumerate(rankings, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            stars = "⭐" * int(round(r["avg_rating"])) if r["avg_rating"] > 0 else "No ratings yet"
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{medal} {r['name']}**")
                    if r["address"]:
                        st.caption(f"📍 {r['address']}")
                with col2:
                    st.metric("Rating", f"{r['avg_rating']:.1f}/5" if r["review_count"] > 0 else "N/A", 
                              f"{r['review_count']} reviews")

# Review Tab
with tab2:
    st.subheader("Leave a Review")
    restaurants = data.get_restaurants()
    
    if not restaurants:
        st.info("No restaurants available to review.")
    else:
        restaurant = st.selectbox("Select restaurant", restaurants, format_func=lambda x: x["name"])
        rating = st.slider("Your rating", 1, 5, 3, format="%d ⭐")
        
        if st.button("Submit Review", type="primary"):
            user = st.session_state.user_name.strip() or "Anonymous"
            data.add_review(restaurant["id"], rating, user)
            st.success(f"Thanks {user}! Your {rating}⭐ review for {restaurant['name']} has been submitted!")
            st.balloons()
