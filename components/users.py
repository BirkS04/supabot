import streamlit as st

from supabase import create_client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

jwt_secret = st.secrets["SUPABASE_JWT"]


def create_user(email, password, password_confirmation):
    if password != password_confirmation:
        st.write("Passwords do not match")
    try:
        response = supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )
        return response
    except Exception as e:
        st.error("Invalid email or password")
        return None

def sign_in_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": email, 
                "password": password,
            }
        )
        return response
    
    except Exception as e:
        st.error("Invalid email or password")
        return None

def google_login():
    response = supabase.auth.sign_in_with_oauth(
        {
            "provider": "google",
        }
    )
    return response