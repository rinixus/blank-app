import os
import streamlit as st
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import json

# NOTE: Since this is a sandbox environment, we cannot easily set up
# external Google Cloud Credentials.
# We will check for a 'client_secret.json' file.
# If it exists, we use Real Auth.
# If not, we use the "Dev Mock Auth" as agreed.

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
REDIRECT_URI = "http://localhost:8501/"

def login():
    """
    Handles authentication.
    Returns a dictionary {'email': ..., 'name': ...} if logged in, else None.
    """

    # 1. Check if user is already in session
    if 'user' in st.session_state:
        return st.session_state['user']

    # 2. Check for Real Google Auth Credentials
    if os.path.exists(CLIENT_SECRETS_FILE):
        return _real_google_login()
    else:
        return _dev_mock_login()

def _real_google_login():
    """
    Real Google OAuth Flow.
    """
    st.warning("Running in Real Google Auth Mode (client_secret.json found).")

    # Initialize the Flow
    try:
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
    except Exception as e:
        st.error(f"Error loading client secrets: {e}")
        return None

    # Get the authorization URL
    auth_url, _ = flow.authorization_url(prompt='consent')

    st.markdown(f"Please [Login with Google]({auth_url})")

    # In a typical Streamlit app without a specialized component,
    # capturing the callback code requires checking query params.
    # Note: st.query_params is the modern API (Streamlit >= 1.30)

    code = st.query_params.get("code")

    if code:
        try:
            flow.fetch_token(code=code)
            credentials = flow.credentials

            # Use the credentials to get user info
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()

            user = {
                'email': user_info.get('email'),
                'name': user_info.get('name')
            }
            st.session_state['user'] = user

            # Clear query params to prevent re-triggering
            st.query_params.clear()
            st.rerun()

        except Exception as e:
            st.error(f"Authentication failed: {e}")
            st.text("Ensure your Redirect URI in Google Console matches: " + REDIRECT_URI)

    return None

def _dev_mock_login():
    """
    Simulates a login screen for development/demo purposes.
    """
    st.markdown("## Login to MIXMOVIE.AI")
    st.info("Dev Mode: Google API keys not found. Using Mock Login.")

    with st.form("login_form"):
        email = st.text_input("Email", "demo@mixmovie.ai")
        name = st.text_input("Name", "Showrunner User")
        submit = st.form_submit_button("Login with Google (Simulated)")

        if submit:
            user = {'email': email, 'name': name}
            st.session_state['user'] = user
            st.rerun()

    return None

def logout():
    if 'user' in st.session_state:
        del st.session_state['user']
        st.rerun()
