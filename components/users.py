import os
import dotenv
dotenv.load_dotenv()
import jwt
import streamlit as st

from supabase import create_client, Client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

jwt_secret = os.environ.get("SUPABASE_JWT")


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
