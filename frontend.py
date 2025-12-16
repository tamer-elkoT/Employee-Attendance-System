import streamlit as st
import requests
import time

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api"
st.set_page_config(page_title="Face Attendance System", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #f5f7f9;
    }
    /* Cards */
    .css-1r6slb0 {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 50px;
        width: 100%;
        font-size: 18px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    /* Success Messages */
    .stSuccess {
        background-color: #dff0d8;
        color: #3c763d;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
# This acts as the "Memory" of the app
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {}
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# --- HELPER FUNCTIONS ---

def switch_page(page_name):
    st.session_state['page'] = page_name
    st.rerun()

def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = {}
    switch_page('login')

# --- PAGES ---

def login_page():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title("🛡️ Face Attendance System")
        st.markdown("### AI-Powered Access Control")
        st.markdown("Please verify your identity to access the secure dashboard.")
        
        st.info("ℹ️ **Tip:** Ensure good lighting and look directly at the camera.")
        
        if st.button("📝 Create New Account"):
            switch_page('register')

    with col2:
        st.subheader("Login Verification")
        img_file = st.camera_input("Scan Face to Login", key="login_cam")
        
        if img_file:
            with st.spinner("Authenticating biometric data..."):
                try:
                    files = {"file": img_file.getvalue()}
                    res = requests.post(f"{API_URL}/recognize", files=files)
                    data = res.json()
                    
                    st.write("Debug - Raw Server Response:", data)
                    if data.get('status') == 'success':
                        st.session_state['logged_in'] = True
                        st.session_state['user_info'] = data
                        st.balloons()
                        time.sleep(1) # Visual pause
                        switch_page('dashboard')
                    else:
                        st.error("❌ Access Denied: Face not recognized.")
                except Exception as e:
                    st.error(f"Server Error: {e}")

def register_page():
    st.title("📝 Multi-Shot Registration")
    
    # --- 1. Initialize Session State for Photos ---
    if 'reg_photos' not in st.session_state:
        st.session_state['reg_photos'] = []
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("⬅️ Back to Login"):
            # Clear photos when leaving
            st.session_state['reg_photos'] = []
            switch_page('login')
            
        st.markdown("### 📸 Photo Collection")
        st.info(f"Photos Captured: **{len(st.session_state['reg_photos'])} / 5**")
        
        # Show mini thumbnails of captured photos
        if st.session_state['reg_photos']:
            st.write("Previews:")
            cols = st.columns(3)
            for i, photo_data in enumerate(st.session_state['reg_photos']):
                cols[i % 3].image(photo_data, width=50)
                
        if st.button("🔄 Clear All Photos"):
            st.session_state['reg_photos'] = []
            st.rerun()

    with col2:
        # --- 2. The Form ---
        # We put the inputs OUTSIDE the form so they don't reset on every photo snap
        name = st.text_input("Full Name", key="reg_name_input")
        dept = st.text_input("Department", key="reg_dept_input")

        st.divider()

        # --- 3. The Smart Camera Logic ---
        # Only show camera if we have less than 5 photos
        if len(st.session_state['reg_photos']) < 5:
            st.warning(f"👉 Please take **Photo #{len(st.session_state['reg_photos']) + 1}**. Move your head slightly.")
            
            # TRICK: We use a dynamic key based on the list length. 
            # This forces Streamlit to create a BRAND NEW camera widget every time we save a photo.
            picture = st.camera_input("Take Photo", key=f"camera_{len(st.session_state['reg_photos'])}")
            
            if picture:
                # Save the photo to our list
                st.session_state['reg_photos'].append(picture)
                # Force a reload to reset the camera for the next shot
                st.rerun()
        
        else:
            # --- 4. Registration Block (Shows after 5 photos) ---
            st.success("✅ 5 Photos Captured! Ready to Register.")
            
            if st.button("🚀 Complete Registration", type="primary"):
                if not name or not dept:
                    st.error("⚠️ Please enter Name and Department.")
                else:
                    with st.spinner("Analyzing all 5 frames for best angle..."):
                        try:
                            # Prepare the list of files
                            files_to_send = []
                            for i, pic in enumerate(st.session_state['reg_photos']):
                                # Format: ('files', (filename, bytes, content_type))
                                files_to_send.append(
                                    ('files', (f'photo_{i}.jpg', pic.getvalue(), 'image/jpeg'))
                                )

                            payload = {'name': name, 'department': dept}
                            
                            # Send to Backend
                            res = requests.post(f"{API_URL}/register", data=payload, files=files_to_send)
                            
                            if res.status_code == 200 and res.json().get('status') == 'success':
                                st.balloons()
                                st.success("🎉 Registration Successful!")
                                time.sleep(2)
                                # Cleanup
                                st.session_state['reg_photos'] = []
                                switch_page('login')
                            else:
                                st.error(f"Failed: {res.json().get('msg')}")
                                
                        except Exception as e:
                            st.error(f"Connection Error: {e}")

def dashboard_page():
    user = st.session_state['user_info']
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
        st.title(f"Hello, {user.get('name', 'User').split()[0]}")
        st.write(f"**Dept:** {user.get('dept', 'N/A')}")
        st.divider()
        if st.button("🚪 Logout"):
            logout()

    # Main Content
    st.title("📊 Employee Dashboard")
    
    # KPIs / Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Status", "Active", "Online")
    m2.metric("Check-in Time", "09:00 AM", "On Time")
    m3.metric("Attendance Score", "98%", "+2%")

    st.divider()

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🗓️ Recent Activity")
        # Dummy Data for Visualization
        activity_data = [
            {"Date": "2025-12-16", "Time": "09:00 AM", "Status": "Check-In"},
            {"Date": "2025-12-15", "Time": "05:00 PM", "Status": "Check-Out"},
            {"Date": "2025-12-15", "Time": "08:55 AM", "Status": "Check-In"},
        ]
        st.table(activity_data)

    with col2:
        st.subheader("📢 Announcements")
        st.info("Holiday Party next Friday at 5 PM!")
        st.warning("System maintenance scheduled for Sunday.")

# --- MAIN APP ROUTER ---

def main():
    if st.session_state['logged_in']:
        dashboard_page()
    elif st.session_state['page'] == 'register':
        register_page()
    else:
        login_page()

if __name__ == "__main__":
    main()