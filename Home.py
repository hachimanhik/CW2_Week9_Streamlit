import streamlit as st
from app.services.user_service import register_user, login_user

# Basic page settings
st.set_page_config(
    page_title="Multi-Domain Intelligence Application",
)

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

#IF USER IS NOT LOGGED IN
if not st.session_state.logged_in:
    st.title("Welcome to the authentication application!")

    # SIGN UP
    st.subheader("Sign up")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Create a password", type="password")
    new_password2 = st.text_input("Confirm your password", type="password")

    if st.button("Sign up"):
        if new_username == "" or new_password == "" or new_password2 == "":
            st.error("You must enter a username and password.")
        elif new_password != new_password2:
            st.error("Passwords do not match.")
        else:
            ok, msg = register_user(new_username, new_password, "user")
            st.write(msg)

    st.divider()

    #LOGIN
    st.subheader("Login")
    username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "" or login_password == "":
            st.error("You must enter a username and password.")
        else:
            ok, msg = login_user(username, login_password)
            if ok:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful.")
                st.rerun()
            else:
                st.error(msg)

else:
    # IF USER IS LOGGED IN
    with st.sidebar:
        st.header("Application menu")
        st.write(f"Signed in as: {st.session_state.username}")

        # Links to other pages
        st.page_link("Home.py", label="Home")
        st.page_link("pages/1_Dashboard.py", label="Dashboard")
        st.page_link("pages/2_Incidents.py", label="Incidents")
        st.page_link("pages/3_Datasets.py", label="Datasets")
        st.page_link("pages/4_Tickets.py", label="Tickets")

        # Logout button
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.success("Logged out.")
            st.rerun()

    st.title("Home")
    st.write("Welcome to the Multi-Domain Intelligence Platform.")
    st.write("Use the menu on the left to open different pages.")
