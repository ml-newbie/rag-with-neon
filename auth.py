# auth.py
import streamlit as st

def check_password(app_name="Protected App"):
    """
    Simple Streamlit password protection.
    Reads password from st.secrets["APP_PASSWORD"].
    Returns True if password is correct, False otherwise.
    """

    APP_PASSWORD = st.secrets.get("APP_PASSWORD", None)
    if APP_PASSWORD is None:
        st.error("APP_PASSWORD not set in Streamlit secrets!")
        st.stop()

    # Function to validate input
    def password_entered():
        if st.session_state["password"] == APP_PASSWORD:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    # Add some vertical spacing
    st.write("")
    st.write("")
    st.write("")

    password = st.text_input(
        f"Enter password to access {app_name}:",
        type="password",
        key="password"
    )

    login = st.button("Unlock Access", use_container_width=True)

    if login:
        password_entered()

    if "password_correct" not in st.session_state:
        return False
    elif not st.session_state["password_correct"]:
        st.error("❌ Incorrect password")
        return False
    else:
        return True