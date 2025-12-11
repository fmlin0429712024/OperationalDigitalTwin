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
                # Production / Cloud Run (Uses Application Default Credentials)
                print("ℹ️ Using Application Default Credentials (ADC)")
                firebase_admin.initialize_app()
        except Exception as e:
            print(f"Failed to initialize Firebase: {e}")
            return None
    
    return firestore.client()

# Singleton-like access
db = init_firebase()
