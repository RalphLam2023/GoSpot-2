import streamlit as st
import requests
import datetime

# Configure page settings
st.set_page_config(page_title="GoSpot - Driver App", page_icon="🚗", layout="centered")

st.title("🚗 GoSpot")
st.subheader("Get a Spot before you go.")

st.markdown("---")
st.write("**Plan Your Parking**")

# UI Inputs mimicking the driver search flow
col1, col2 = st.columns(2)
with col1:
    target_time = st.time_input("Target Arrival Time", datetime.time(7, 30))
    day_of_week = st.selectbox("Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
with col2:
    destination = st.selectbox("Destination", ["Mapúa University (Intramuros)", "Lyceum", "Letran"])
    is_exam_week = st.checkbox("Is it Exam/Event Week?", value=True)

# Map day string to integer (0=Monday, 6=Sunday)
day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}

if st.button("Find Parking", type="primary", use_container_width=True):
    # Convert time to minutes from midnight
    time_minutes = target_time.hour * 60 + target_time.minute
    
    # Prepare payload for FastAPI
    payload = {
        "day_of_week": day_map[day_of_week],
        "time_of_day_minute": time_minutes,
        "total_capacity": 50,
        "is_academic_peak": 1 if is_exam_week else 0,
        "minutes_since_last_update": 10 # Simulating an update from 10 mins ago
    }
    
    # Call the FastAPI backend
    try:
        response = requests.post("https://gospot-api.onrender.com/v1/parking/predict](https://gospot-api.onrender.com/v1/parking/predict", json=payload)
        data = response.json()
        
        st.markdown("### 📍 Best Match: Intramuros Surface Lot")
        
        # Display metrics clearly
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Predicted Availability", value=f"{data['predicted_availability_percent']}%")
        m2.metric(label="Est. Free Slots", value=f"{data['estimated_free_slots']} / 50")
        m3.metric(label="Flat Rate", value=f"₱{data['flat_rate']}")
        
        # Confidence Badge
        if data['confidence_level'] == "HIGH":
            st.success(f"✅ **High Confidence** (Data updated recently. Score: {data['confidence_score']})")
        elif data['confidence_level'] == "MEDIUM":
            st.warning(f"⚠️ **Medium Confidence** (Data is aging. Score: {data['confidence_score']})")
        else:
            st.error(f"❌ **Low Confidence** (Relying purely on historical data. Score: {data['confidence_score']})")
            
        st.markdown("""
        **Safety & Amenities:**
        * 💡 Well-lit at night
        * 📹 Active CCTV
        * ♿ PWD Accessible Slots Available
        """)
        
    except requests.exceptions.ConnectionError:
        st.error("Error connecting to the backend. Is the FastAPI server running?")