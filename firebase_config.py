import firebase_admin
from firebase_admin import credentials, firestore
import os
import streamlit as st

# Function to initialize Firebase
def init_firebase():
    # Check if already initialized to avoid multiple app initialization errors
    if not firebase_admin._apps:
        try:
            # Try to load from local serviceAccountKey.json (Development)
            if os.path.exists("serviceAccountKey.json"):
                cred = credentials.Certificate("serviceAccountKey.json")
                firebase_admin.initialize_app(cred)
            else:
                # Fallback or Streamlit Secrets (Production)
                # If you use Streamlit Cloud, you would store this in st.secrets
                # For now, we will print a warning if missing
                print("Warning: serviceAccountKey.json not found. Database calls will fail.")
                return None
        except Exception as e:
            print(f"Failed to initialize Firebase: {e}")
            return None
    
    return firestore.client()

# Singleton-like access
db = init_firebase()
