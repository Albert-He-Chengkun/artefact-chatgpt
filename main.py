import streamlit as st
import streamlit_authenticator as stauth
from chatgpt import chat_page

auth = {'credentials': {'usernames': {st.secrets['username']: {
    'name': st.secrets['username'],
    'password': st.secrets['password']}}}}

authenticator = stauth.Authenticate(
    auth['credentials'],
    st.secrets['cookie']['name'],
    st.secrets['cookie']['key'],
    st.secrets['cookie']['expiry_days'],
    st.secrets['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    col1, col2 = st.columns([6, 1])
    with col1:
        # chat_page()
        st.subheader('Under maintenance......will be back soon')
    with col2:
        authenticator.logout('Logout', 'main')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


