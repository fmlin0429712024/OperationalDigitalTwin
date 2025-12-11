import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import datetime
import random
from firebase_config import db

# --- Page Config ---
st.set_page_config(
    page_title="Operational Digital Twin | Prescient Devices",
    page_icon="🏭",
    layout="wide"
)

# --- Custom CSS for "Premium" Feel ---
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# --- Mock Data Generator (Fallback if no Firebase) ---
def get_mock_data():
    """Generate fake dataframe if Firestore is not connected."""
    now = datetime.datetime.now()
    devices = [f"INST-{i:03d}" for i in range(1, 6)]
    data = []
    for _ in range(50): # 50 historical points
        ts = now - datetime.timedelta(minutes=random.randint(0, 15))
        dev = random.choice(devices)
        status = random.choice(["RUNNING", "IDLE", "RUNNING", "RUNNING", "ERROR"])
        data.append({
            "device_id": dev,
            "timestamp": ts,
            "status": status,
            "temperature": random.uniform(20, 80),
            "vibration": random.uniform(0.01, 1.5) if status == "ERROR" else random.uniform(0.01, 0.4),
            "throughput": random.randint(10, 20) if status == "RUNNING" else 0
        })
    return pd.DataFrame(data).sort_values("timestamp")

# --- Data Fetching ---
@st.cache_data(ttl=2) # Short cache for "real-time" feel
def fetch_data():
    if db is None:
        return get_mock_data()
    
    # Fetch last 100 records
    from google.cloud.firestore import Query
    docs = db.collection("telemetry_stream")\
             .order_by("timestamp", direction=Query.DESCENDING)\
             .limit(200)\
             .stream()
    
    data = []
    for doc in docs:
        d = doc.to_dict()
        flat = d.copy()
        # Flatten metrics
        if 'metrics' in d:
            flat['temperature'] = d['metrics'].get('temperature')
            flat['vibration'] = d['metrics'].get('vibration')
            flat['throughput'] = d['metrics'].get('throughput')
            del flat['metrics']
        if 'meta' in d:
            del flat['meta']
        data.append(flat)
    
    if not data:
        return pd.DataFrame(columns=["device_id", "timestamp", "status", "temperature", "vibration"])
    
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# --- Main Layout ---

# Header
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🏭 Operational Digital Twin")
    st.caption("Real-time Operational & Business Intelligence • Powered by Edge AI")
with c2:
    if db:
        st.success("☁️ Connected to Firebase")
    else:
        st.warning("⚠️ Demo Mode (Local Mock Data)")

# --- Solution Overview ---
with st.expander("ℹ️ Solution Overview", expanded=False):
    st.markdown("""
    **Operational Digital Twin for Analytical Instrumentation**
    
    This Proof of Concept (PoC) demonstrates how Prescient Devices helps manufacturers transform raw edge data into actionable insights.
    
    *   **Real-time Visibility**: Monitor fleet status and health instantly.
    *   **Operational Intelligence (OI)**: Detect anomalies like high vibration before failure.
    *   **Business Intelligence (BI)**: Track utilization and revenue impact.
    
    [Read the Full Prescient Customer Story](https://www.prescientdevices.com/customer-story/industrial-digital-twin-for-oi-and-bi)
    """)

# Auto-Refresh Loop Helper
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

# Refresh button
if st.button('🔄 Refresh Data'):
    st.rerun()

# 1. Fetch Data
df = fetch_data()

# 2. KPI Section (OI & BI)
st.markdown("### 📊 Enterprise View")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

active_devices = df[df['status'] == 'RUNNING']['device_id'].nunique()
total_devices = df['device_id'].nunique()
avg_utilization = (len(df[df['status'] == 'RUNNING']) / len(df)) * 100 if len(df) > 0 else 0
critical_errors = len(df[df['status'] == 'ERROR'])

kpi1.metric("Active Fleet", f"{active_devices}/{total_devices}", delta=f"{active_devices} Online")
kpi2.metric("OEE (Utilization)", f"{avg_utilization:.1f}%", delta="1.2%")
kpi3.metric("Critical Alerts (24h)", critical_errors, delta=f"-{random.randint(1,3)}", delta_color="inverse")
# BI Calculation: Approx $100 per unit throughput
est_revenue = df['throughput'].sum() * 10 
kpi4.metric("Est. Throughput Revenue", f"${est_revenue:,.0f}", delta="+8%")

# 3. Fleet Monitoring (OI)
st.markdown("---")
col_monitor, col_details = st.columns([2, 1])

with col_monitor:
    st.subheader("Real-time Device Telemetry")
    
    # Filter
    selected_device = st.selectbox("Select Device for Deep Dive", df['device_id'].unique())
    
    device_df = df[df['device_id'] == selected_device].sort_values("timestamp")
    
    # Temperature Chart
    fig_temp = px.line(device_df, x="timestamp", y="temperature", title=f"{selected_device} - Temperature Trend", markers=True)
    fig_temp.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_temp)

    # Vibration Chart
    fig_vib = px.line(device_df, x="timestamp", y="vibration", title=f"{selected_device} - Vibration Analysis", markers=True)
    fig_vib.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
    fig_vib.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_vib)

with col_details:
    st.subheader("🛑 Alert Feed")
    errors = df[df['status'] == 'ERROR'].sort_values("timestamp", ascending=False).head(5)
    if not errors.empty:
        for index, row in errors.iterrows():
            st.error(f"**{row['device_id']}** at {row['timestamp'].strftime('%H:%M:%S')}\n\nHigh Vibration detected.")
    else:
        st.success("No active alerts in the last window.")

    st.subheader("💡 Lab Insights (BI)")
    st.info("""
    **Optimization Opportunity**:  
    Device **INST-003** shows 15% lower throughput than fleet average. 
    
    *Recommended Action*: Schedule preventive maintenance for calibration.
    """)
    
    st.markdown("#### Projected OI Value")
    st.progress(78, text="Quarterly Target Reached (78%)")

# 4. Raw Data
with st.expander("Show Raw Telemetry Stream"):
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)
