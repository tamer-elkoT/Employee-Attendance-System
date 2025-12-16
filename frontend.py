import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api"
st.set_page_config(page_title="Face Recognition Attendance System", page_icon="🛡️", layout="wide")

# --- PROFESSIONAL CSS STYLING ---
st.markdown("""
<style>
    /* Global Font & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #171717; /* Darker Text */
    }
    
    .stApp {
        background: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
    }

    /* Card Styling with Animation */
    .css-1r6slb0, .stForm {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        animation: fadeIn 0.8s ease-in-out;
    }

    /* Headings */
    h1, h2, h3 {
        color: #111827; /* Very Dark Blue/Black */
        font-weight: 700 !important;
    }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #2563EB; /* Professional Blue */
    }

    /* Custom Buttons */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        height: 48px;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    /* Animations */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Status Box Colors */
    .stSuccess { background-color: #ECFDF5; border-left: 5px solid #10B981; color: #065F46; }
    .stError { background-color: #FEF2F2; border-left: 5px solid #EF4444; color: #991B1B; }
    .stInfo { background-color: #EFF6FF; border-left: 5px solid #3B82F6; color: #1E40AF; }

</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {}
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'
if 'login_time' not in st.session_state:
    st.session_state['login_time'] = None

# --- HELPER FUNCTIONS ---
def switch_page(page_name):
    st.session_state['page'] = page_name
    st.rerun()

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = {}
    st.session_state['login_time'] = None
    switch_page('login')

def get_greeting():
    hour = datetime.now().hour
    if hour < 12: return "Good Morning"
    elif hour < 18: return "Good Afternoon"
    else: return "Good Evening"

# --- PAGE: LOGIN ---
def login_page():
    # Centered Layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>🛡️ Face Recognition Attendance System</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6B7280;'>Secure AI-Powered Biometric Access</p>", unsafe_allow_html=True)
        st.divider()

        # Tabs for cleaner UI
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            st.info("Look directly at the camera to verify your identity.")
            img_file = st.camera_input("Biometric Scan", key="login_cam", label_visibility="hidden")
            
            if img_file:
                with st.spinner("🔄 Verifying Biometrics..."):
                    try:
                        files = {"file": img_file.getvalue()}
                        res = requests.post(f"{API_URL}/recognize", files=files)
                        data = res.json()
                        
                        if data.get('status') == 'success':
                            # Success Logic
                            st.session_state['logged_in'] = True
                            st.session_state['user_info'] = data
                            st.session_state['login_time'] = datetime.now().strftime("%I:%M %p")
                            
                            st.success(f"✅ Identity Verified: {data['name']}")
                            time.sleep(1)
                            switch_page('dashboard')
                        else:
                            st.error("❌ Access Denied: User not recognized.")
                    except Exception as e:
                        st.error(f"⚠️ Server Error: {e}")

        with tab2:
            st.write("New employee? Create your secure profile.")
            if st.button("Start Registration Process"):
                switch_page('register')

# --- PAGE: REGISTRATION (Multi-Shot) ---
def register_page():
    st.markdown("## 📝 New Profile Registration")
    st.markdown("---")
    
    if 'reg_photos' not in st.session_state:
        st.session_state['reg_photos'] = []
    
    col_cam, col_form = st.columns([1.5, 1])
    
    with col_form:
        st.markdown("### 👤 User Details")
        with st.form("reg_details"):
            name = st.text_input("Full Name", placeholder="e.g. John Doe")
            dept = st.text_input("Department", placeholder="e.g. Engineering")
            submitted = st.form_submit_button("Confirm Details (Step 1)")
            
            if submitted:
                if name and dept:
                    st.session_state['reg_name'] = name
                    st.session_state['reg_dept'] = dept
                    st.success("Details saved. Now capture photos.")
                else:
                    st.warning("Please fill all fields.")

        # Progress Bar
        progress = len(st.session_state['reg_photos']) / 5
        st.progress(progress, text=f"Photos Captured: {len(st.session_state['reg_photos'])} / 5")
        
        if len(st.session_state['reg_photos']) >= 5:
            if st.button("🚀 Finalize Registration", type="primary"):
                if 'reg_name' in st.session_state:
                    with st.spinner("Processing & Encrypting..."):
                        try:
                            files_to_send = []
                            for i, pic in enumerate(st.session_state['reg_photos']):
                                files_to_send.append(('files', (f'photo_{i}.jpg', pic.getvalue(), 'image/jpeg')))
                            
                            payload = {'name': st.session_state['reg_name'], 'department': st.session_state['reg_dept']}
                            res = requests.post(f"{API_URL}/register", data=payload, files=files_to_send)
                            
                            if res.status_code == 200 and res.json().get('status') == 'success':
                                st.balloons()
                                st.success("✅ Registration Complete!")
                                time.sleep(2)
                                st.session_state['reg_photos'] = []
                                switch_page('login')
                            else:
                                st.error(f"Failed: {res.json().get('msg')}")
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.error("Please fill Name & Dept first.")
        
        if st.button("⬅️ Cancel"):
            st.session_state['reg_photos'] = []
            switch_page('login')

    with col_cam:
        if len(st.session_state['reg_photos']) < 5:
            st.info(f"📸 Capture Angle {len(st.session_state['reg_photos']) + 1}/5")
            picture = st.camera_input("Register Cam", key=f"cam_{len(st.session_state['reg_photos'])}")
            if picture:
                st.session_state['reg_photos'].append(picture)
                st.rerun()
        else:
            st.success("✅ Capture Complete!")
            # Show Grid of photos
            cols = st.columns(3)
            for i, p in enumerate(st.session_state['reg_photos']):
                cols[i%3].image(p, width=100)

# --- PAGE: DASHBOARD ---
def dashboard_page():
    user = st.session_state['user_info']
    login_time = st.session_state.get('login_time', "N/A")
    today_date = datetime.now().strftime("%A, %d %B %Y")
    
    # --- Sidebar Info ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        st.markdown(f"### {user.get('name', 'User')}")
        st.markdown(f"**{user.get('dept', 'Unknown')} Department**")
        st.divider()
        st.markdown(f"📅 **{today_date}**")
        st.markdown(f"⏰ **{datetime.now().strftime('%H:%M')}**")
        st.divider()
        if st.button("🚪 Secure Logout"):
            logout()

    # --- Main Dashboard ---
    st.markdown(f"## {get_greeting()}, **{user.get('name', '').split()[0]}**! 👋")
    st.markdown("Here is your daily attendance summary.")
    st.markdown("---")

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Current Status", "✅ Checked In", delta="Active")
    c2.metric("Check-In Time", login_time, delta="On Time")
    c3.metric("Attendance Rate", "98%", "+2%")
    c4.metric("Pending Tasks", "3", "Normal", delta_color="off")

    st.markdown("### 📊 Activity Log")
    
    # Styled Table
    # We add the "Current Login" as the top row dynamically
    data = [
        {"Event": "Login Success", "Time": login_time, "Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Verified"},
        {"Event": "System Check", "Time": "08:55 AM", "Date": datetime.now().strftime("%Y-%m-%d"), "Status": "Auto"},
        {"Event": "Logout", "Time": "05:00 PM", "Date": "Yesterday", "Status": "User"},
    ]
    st.dataframe(data, use_container_width=True)

    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    b1, b2, b3 = st.columns(3)
    if b1.button("📄 Download Report"):
        st.toast("Downloading Monthly Report...")
    if b2.button("🔧 Report Issue"):
        st.toast("Support ticket created.")
    if b3.button("📅 View Calendar"):
        st.toast("Opening Calendar...")

# --- ROUTER ---
def main():
    if st.session_state['logged_in']:
        dashboard_page()
    elif st.session_state['page'] == 'register':
        register_page()
    else:
        login_page()

if __name__ == "__main__":
    main()

