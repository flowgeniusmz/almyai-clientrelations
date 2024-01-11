import streamlit as st
from st_login_form import login_form
from supabase import create_client, client
from msal_streamlit_authentication import msal_authentication
from datetime import datetime
import random


def get_loginform():
    client = login_form("FEOC Authentication", allow_guest=False)

    if st.session_state.authenticated:
        if st.session_state.username:
            st.success(f"Welcome {st.session_state.username}")
        else:
            st.success("Welcome Guest")
    else:
        st.error("Not Authenticated")


def check_authentication():
    """
    Check if the user is authenticated.
    
    Returns:
        bool: True if authenticated, False otherwise.
    """
    if "authenticated" not in st.session_state:
        get_loginform()
        return False
    return True
#https://app.supabase.com/project/rbaawqpeyigwmzukrmvc/editor/28594
#https://docs.streamlit.io/knowledge-base/tutorials/databases/supabase#create-a-supabase-database


def generate_varKey():
    # Get the current date in the format YYYY-MM-DD
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Generate a random integer between 1 and 100000
    random_int = random.randint(1, 100000)
    
    # Concatenate the date and the random integer to form varKey
    varKey = f"{current_date}-{random_int}"
    
    return varKey

def check_login():
    if "auth" not in st.session_state:
        st.session_state.auth = False
        return False
    elif not st.session_state.auth:
        return False
    else:
        return True

def get_msal_login_token():
    varAuth = {
        "clientId": "25e5c5fd-9ba1-4d2e-8936-0b328a42fab2",
        "authority": "https://login.microsoftonline.com/63ad517e-620a-4ee0-a614-b6bdde377b13", 
        "redirectUri": "https://clientrelations.streamlit.app/auth_redirect",
        #"postLogoutRedirectUri": "https://feoc-dev.streamlit.app/"  # Or another URI where you handle post-logout navigation
    }
    varCache = {
        "cacheLocation": "sessionStorage",
        "storeAuthStateInCookie": False
    }
    varLoginRequests = {
        "scopes": ["api://25e5c5fd-9ba1-4d2e-8936-0b328a42fab2/.default"]
    }
    varLogoutRequests = {} #optional
    varLoginButtonText = "Login"
    varLogoutButtonText = "Logout"
    varKey = "authlogin1"
    

    login_token = msal_authentication(
        auth=varAuth,
        cache=varCache,
        login_request=varLoginRequests,
        logout_request=varLogoutRequests,
        login_button_text=varLoginButtonText,
        logout_button_text=varLogoutButtonText, 
        key=varKey
    )
    st.write("token received", login_token)
    #   return login_token
