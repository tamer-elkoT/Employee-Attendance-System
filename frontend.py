import streamlit as st
import requests
import json
import time
import pandas as pd
from datetime import datetime

# ================== CONFIG ==================
API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(
    page_title="EmpVision",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== FORCE LIGHT THEME & VISIBILITY ==================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* 1. FORCE ALL TEXT DARK */
    html, body, p, div, span, h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        color: #0f172a !important; /* Dark Slate */
    }

    /* 2. BACKGROUNDS */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* 3. METRIC CARDS FIX (The Invisible Text Fix) */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    
    /* Force Metric Label (Top text) to be Grey */
    div[data-testid="stMetricLabel"] > div > p {
        color: #64748b !important; /* Cool Grey */
        font-size: 14px !important;
    }
    
    /* Force Metric Value (Big text) to be Blue */
    div[data-testid="stMetricValue"] > div {
        color: #2563EB !important; /* Brand Blue */
        font-size: 28px !important;
        font-weight: 700 !important;
    }

    /* 4. INPUT FIELDS (Force White Background, Dark Text) */
    input, .stTextInput > div > div > input {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }
    
    /* 5. SIDEBAR FIX */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: #0f172a !important;
    }

    /* 6. BUTTONS */
    .stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ================== SESSION STATE ==================
if "page" not in st.session_state: st.session_state.page = "login"
if "user" not in st.session_state: st.session_state.user = None
if "photos" not in st.session_state: st.session_state.photos = []

# ================== API HELPERS ==================
def login_api(img):
    try:
        return requests.post(f"{API_URL}/recognize", files={"file": img})
    except Exception:
        return None

def register_api(data, images):
    try:
        files = [("files", (f"img{i}.jpg", img, "image/jpeg")) for i, img in enumerate(images)]
        payload = {"employee_data": json.dumps(data)}
        return requests.post(f"{API_URL}/register", data=payload, files=files)
    except Exception:
        return None

def get_history_api(employee_id):
    try:
        return requests.get(f"{API_URL}/history/{employee_id}")
    except Exception:
        return None

# ================== PAGES ==================

def login_page():
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("## 👁️ EmpVision")
        st.markdown("### Next-Gen Workforce Intelligence")
        st.markdown("""
        EmpVision replaces outdated punch cards with secure, AI-powered facial recognition.
        """)
        
        if st.button("📝 Create New Profile"):
            st.session_state.page = "register"
            st.rerun()

    with col2:
        st.markdown("### 🔐 Secure Login")
        cam = st.camera_input("Scan Face", label_visibility="hidden")

        if cam:
            with st.spinner("🔄 Authenticating..."):
                res = login_api(cam.getvalue())
                
                if res and res.status_code == 200:
                    data = res.json()
                    if data.get("status") == "success":
                        st.session_state.user = data
                        st.success(f"✅ Verified: {data['name']}")
                        time.sleep(1)
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error(f"❌ Access Denied: {data.get('msg', 'Unknown Error')}")
                else:
                    st.error("⚠️ Server Connection Failed")

def register_page():
    st.markdown("## 📝 Employee Onboarding")
    
    col_form, col_cam = st.columns([1.5, 1])

    with col_form:
        with st.form("reg_form"):
            st.subheader("1. Profile Information")
            c1, c2 = st.columns(2)
            fname = c1.text_input("First Name")
            lname = c2.text_input("Last Name")
            email = st.text_input("Email Address")
            dept = st.selectbox("Department", ["Engineering", "Sales", "HR", "Marketing", "Finance", "IT", "Operations", "Management", "Support", "Law", "Medical"])
            job = st.text_input("Job Title")
            phone = st.text_input("Phone Number")
            password = st.text_input("Password", type="password")
            
            submit_details = st.form_submit_button("Verify Details")

    with col_cam:
        st.subheader("2. Biometric Capture")
        captured_count = len(st.session_state.photos)
        st.progress(captured_count / 5, text=f"Photos: {captured_count}/5")

        if captured_count < 5:
            st.info("📸 Please take 5 photos.")
            pic = st.camera_input("Capture", key=f"cam_{captured_count}")
            if pic:
                st.session_state.photos.append(pic.getvalue())
                st.rerun()
        else:
            st.success("✅ Capture Complete!")
            if st.button("🚀 Finalize"):
                if fname and lname and email and password:
                    data = {
                        "first_name": fname, "last_name": lname, "email": email,
                        "department": dept, "job_title": job, "phone_number": phone,
                        "password": password, "username": email.split("@")[0]
                    }
                    with st.spinner("Registering..."):
                        res = register_api(data, st.session_state.photos)
                        if res and res.status_code == 200:
                            st.balloons()
                            st.success("Registration Successful!")
                            st.session_state.photos = []
                            time.sleep(2)
                            st.session_state.page = "login"
                            st.rerun()
                        else:
                            st.error("Registration Failed")

    if st.button("⬅ Back to Login"):
        st.session_state.photos = []
        st.session_state.page = "login"
        st.rerun()

def dashboard_page():
    user = st.session_state.user
    
    # --- Sidebar ---
    with st.sidebar:
        st.title("👁️ EmpVision")
        st.markdown(f"**{user.get('name', 'User')}**")
        st.caption(f"{user.get('department', 'General')} Dept")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()

    # --- Main Content ---
    st.title("📊 Workforce Dashboard")
    
    # 1. Overview Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Status", user.get("attendance_status", "N/A"))
    m2.metric("Check-in Time", datetime.now().strftime("%H:%M"))
    
    score = user.get("attendance_score", 100.0)
    m3.metric("Discipline Score", f"{score}%")
    m4.metric("Notifications", "0")

    st.caption("Attendance Performance")
    st.progress(int(score) / 100)

    st.divider()

    # 2. History Table
    st.subheader("Recent Activity")
    employee_id = user.get("id") 
    
    if employee_id:
        res = get_history_api(employee_id)
        if res and res.status_code == 200:
            history_data = res.json().get("attendance_logs", [])
            if history_data:
                df = pd.DataFrame(history_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No attendance records found.")
        else:
            st.warning("Unable to fetch history logs.")

# ================== MAIN ROUTER ==================
if __name__ == "__main__":
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()
    elif st.session_state.page == "dashboard":
        if st.session_state.user:
            dashboard_page()
        else:
            st.session_state.page = "login"
            st.rerun()