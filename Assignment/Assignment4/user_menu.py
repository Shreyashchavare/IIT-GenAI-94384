import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ========================== CONFIG =================================
st.set_page_config(page_title="CSV Explorer App", page_icon="🌐", layout="wide")

USER_FILE = "user.csv"
HISTORY_FILE = "history.csv"

# ========================== INIT FILES ===============================

if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["userid", "password"]).to_csv(USER_FILE, index= False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["userid", "filename", "uploaded_at"]).to_csv(HISTORY_FILE, index= False)


# ========================== SESSION STATE ===========================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'userid' not in st.session_state:
    st.session_state.userid = None

# ============================ SIDEBAR MENU =================================
st.sidebar.title("📂 Menu")
if not st.session_state.authenticated:
    menu = st.sidebar.radio("Navigation",["Home", "Login", "Register"])
else:
    menu = st.sidebar.radio("Navigation",["Explore CSV", "See History", "Logout"])

# ============================ HELPER FUNCTION =========================
def authenticate_user(userid, password):
    users = pd.read_csv(USER_FILE)
    return not users[
        (users["userid"] == userid) & (users["password"] == password)
    ].empty

def register_user(userid, password):
    users = pd.read_csv(USER_FILE)
    if userid in users["userid"].values:
        return False
    users.loc[len(users)] = [userid, password]
    users.to_csv(USER_FILE, index=False)
    return True

def save_upload_history(userid, filename):
    history = pd.read_csv(HISTORY_FILE)
    history.loc[len(history)] = [
        userid,
        filename,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    history.to_csv(HISTORY_FILE, index=False)
#================================= Home   ===================================
if menu == "Home":
    st.title("🏠 Welcome")
    st.write("Please login or register to continue.")

#================================= Login  ===================================
elif menu == "Login":
    st.title("🔏Login")
    #Login Form
    with st.form(key="login_form"):
        st.header("Login Form")
        user_id = st.text_input(key="id", label="User ID")
        password = st.text_input(key="pass", label="Password", type="password")
        submit_btn_l = st.form_submit_button("Submit", type="primary")

    # from submit handling
    if submit_btn_l:
        if authenticate_user(user_id, password):
            st.session_state.authenticated = True
            st.session_state.userid = user_id
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

#================================= REGISTER ===================================
elif menu == "Register":
    st.title("📝 Register")
    #Registration Form
    with st.form(key="reg_form"):
        st.header("Registration Form")
        user_id = st.text_input(key="id", label="User ID")
        password = st.text_input(key="pass", label="Password", type="password")
        submit_btn_r = st.form_submit_button("Submit", type="primary")

    # from submit handling
    if submit_btn_r:
        if register_user(user_id, password):
            st.success("Registration successful. Please login.")
        else:
            st.error("User already exists")

# ================= EXPLORE CSV =================
elif menu == "Explore CSV":
    st.title("📊 Explore CSV Files")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Preview")
        st.dataframe(df)

        save_upload_history(
            st.session_state.userid,
            uploaded_file.name
        )

        st.success("File uploaded & history saved")

# ================= SEE HISTORY =================
elif menu == "See History":
    st.title("🕒 Upload History")

    history = pd.read_csv(HISTORY_FILE)
    user_history = history[history["userid"] == st.session_state.userid]

    if user_history.empty:
        st.info("No uploads yet")
    else:
        st.dataframe(user_history)

# ================= LOGOUT =================
elif menu == "Logout":
    st.session_state.authenticated = False
    st.session_state.userid = None
    st.success("Logged out successfully")
    st.rerun()

