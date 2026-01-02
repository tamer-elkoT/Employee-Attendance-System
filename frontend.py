import streamlit as st
import requests
import pandas as pd
import json
import time
from datetime import datetime

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api"  # Update if using Ngrok (e.g., https://xyz.ngrok-free.app/api)
st.set_page_config(
    page_title="Sentinel Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS (Professional Theme) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background & Main Layout */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Cards and Containers */
    .css-1r6slb0, div[data-testid="stForm"] {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
    }

    /* Headers */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    [data-testid="stMetricValue"] {
        color: #2563EB; /* Brand Blue */
        font-weight: 700;
    }

    /* Custom Buttons */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #1d4ed8;
        transform: translateY(-1px);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1e293b;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
if 'user_session' not in st.session_state:
    st.session_state.user_session = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'reg_photos' not in st.session_state:
    st.session_state.reg_photos = []

# --- NAVIGATION FUNCTIONS ---
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

def logout():
    st.session_state.user_session = None
    st.session_state.reg_photos = []
    navigate_to('login')

# --- API HELPERS ---
def api_login(file_bytes):
    try:
        files = {"file": file_bytes}
        response = requests.post(f"{API_URL}/recognize", files=files)
        return response
    except requests.exceptions.ConnectionError:
        return None

def api_register(data, files_list):
    try:
        # Prepare files list for FastAPI (List[UploadFile])
        files_payload = [('files', (f'img{i}.jpg', f, 'image/jpeg')) for i, f in enumerate(files_list)]
        payload = {"employee_data": json.dumps(data)}
        response = requests.post(f"{API_URL}/register", data=payload, files=files_payload)
        return response
    except requests.exceptions.ConnectionError:
        return None

# --- PAGE: LOGIN ---
def show_login():
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/9326/9326966.png", width=80)
        st.title("Sentinel Pro")
        st.markdown("""
        ### AI-Powered Workforce Management
        Secure biometric access control and automated attendance tracking system.
        
        **Instructions:**
        1. Ensure you are well-lit.
        2. Look directly at the camera.
        3. Click 'Take Photo' to login.
        """)
        
        st.info("Don't have an account?")
        if st.button("📝 Register New Employee"):
            navigate_to('register')

    with col2:
        st.markdown("### 🔐 Biometric Verification")
        img_file = st.camera_input("Scan Face", key="login_cam", label_visibility="hidden")

        if img_file:
            with st.spinner("Authenticating biometric data..."):
                response = api_login(img_file.getvalue())
                
                if response and response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        st.session_state.user_session = data
                        st.success(f"Welcome back, {data['name']}!")
                        time.sleep(1)
                        navigate_to('dashboard')
                    else:
                        st.error(f"Access Denied: {data.get('msg', 'Unknown user')}")
                elif response:
                    st.error(f"Server Error: {response.text}")
                else:
                    st.error("Could not connect to backend server.")

# --- PAGE: REGISTER ---
def show_register():
    st.markdown("## 📝 New Employee Onboarding")
    st.caption("Complete the profile details and capture biometric data.")

    col_form, col_cam = st.columns([1.5, 1])

    with col_form:
        with st.form("reg_form"):
            st.subheader("1. Profile Details")
            c1, c2 = st.columns(2)
            fname = c1.text_input("First Name")
            lname = c2.text_input("Last Name")
            
            email = st.text_input("Email Address")
            
            # Matches Pydantic Regex
            dept = st.selectbox("Department", [
                "Engineering", "Sales", "HR", "Marketing", "Finance", 
                "IT", "Operations", "Management", "Support", "Law", "Medical"
            ])
            
            job = st.text_input("Job Title")
            phone = st.text_input("Phone Number")
            password = st.text_input("Password", type="password", help="Min 8 chars, 1 Upper, 1 Special")

            details_submitted = st.form_submit_button("Verify Details")

    with col_cam:
        st.subheader("2. Biometric Capture")
        st.info("We need 5 photos to train the AI model.")
        
        # Progress Logic
        current_photos = len(st.session_state.reg_photos)
        st.progress(current_photos / 5, text=f"Captured: {current_photos}/5")

        if current_photos < 5:
            picture = st.camera_input("Capture", key=f"reg_cam_{current_photos}")
            if picture:
                st.session_state.reg_photos.append(picture.getvalue())
                st.rerun()
        else:
            st.success("✅ Photos captured successfully!")
            st.image(st.session_state.reg_photos[0], caption="Primary ID Photo", width=150)
            
            if st.button("🚀 Finalize Registration"):
                if not (fname and lname and email and password):
                    st.error("Please fill in all profile details.")
                else:
                    reg_data = {
                        "first_name": fname, "last_name": lname,
                        "email": email, "department": dept,
                        "job_title": job, "phone_number": phone,
                        "password": password,
                        "username": email.split('@')[0] # Auto-generate username
                    }
                    
                    with st.spinner("Encrypting data & Registering..."):
                        response = api_register(reg_data, st.session_state.reg_photos)
                        
                        if response and response.status_code == 200:
                            st.balloons()
                            st.success("Registration Complete!")
                            time.sleep(2)
                            st.session_state.reg_photos = []
                            navigate_to('login')
                        elif response:
                            st.error(f"Error: {response.json().get('detail', 'Registration failed')}")
                        else:
                            st.error("Connection failed.")
                            
    if st.button("← Back to Login"):
        st.session_state.reg_photos = []
        navigate_to('login')

# --- PAGE: DASHBOARD ---
def show_dashboard():
    user = st.session_state.user_session
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        st.markdown(f"### {user['name']}")
        st.markdown(f"**{user['department']}**")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            logout()

    # Main Content
    st.title("📊 Employee Dashboard")
    st.markdown(f"Welcome back, **{user['name'].split()[0]}**!")
    
    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Check-In Status", user.get('attendance_status', 'N/A'))
    m2.metric("Attendance Score", f"{user.get('attendance_score', 100):.1f}")
    m3.metric("Current Time", datetime.now().strftime("%H:%M"))
    m4.metric("Notifications", "0 New")

    # History Section
    st.divider()
    st.subheader("🗓️ Recent Activity Logs")

    # Note: To make History work fully, the backend /recognize endpoint
    # needs to return the 'id' of the employee. 
    # Currently assuming user['id'] might not be present in the recognize response provided in prompt.
    # If not present, we can't fetch history. 
    # Logic below tries to fetch if ID is available (mocking capability).
    
    employee_id = user.get('id') # Ensure backend /recognize returns this!
    
    if employee_id:
        try:
            res = requests.get(f"{API_URL}/history/{employee_id}")
            if res.status_code == 200:
                history_data = res.json()
                logs = history_data.get('attendance_logs', [])
                if logs:
                    df = pd.DataFrame(logs)
                    st.dataframe(
                        df, 
                        column_config={
                            "date": "Date",
                            "time": "Check-in Time",
                            "status": st.column_config.TextColumn("Status")
                        },
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No attendance records found.")
        except Exception:
            st.warning("Could not load history.")
    else:
        st.warning("History unavailable (Employee ID missing in session).")

# --- MAIN ROUTER ---
def main():
    if st.session_state.page == 'login':
        show_login()
    elif st.session_state.page == 'register':
        show_register()
    elif st.session_state.page == 'dashboard':
        if st.session_state.user_session:
            show_dashboard()
        else:
            navigate_to('login')

if __name__ == "__main__":
    main()