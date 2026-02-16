import streamlit as st
import requests
from Ressources.Config import URL
from Ressources.Translations import translations


def view_login():
    Global = translations[st.session_state['languages']]
    signup = translations[st.session_state['languages']]['loginPage']

    st.title(signup['login'])
    st.write(signup['description'])

    username = st.text_input(Global["username"], key='username')
    password = st.text_input(Global["password"], type="password", key='password')

    login_disabled = not username or not password
    st.button(signup['login'], on_click=function_login_button_pressed, disabled=login_disabled)

    col1, col2, col3 = st.sidebar.columns([3, 1, 1])
    col1.write(Global['language'])
    col2.button('EN ', on_click=function_set_language, args=('en',))
    col3.button('FR ', on_click=function_set_language, args=('fr',))
    
    col1, col3 = st.sidebar.columns([4, 1])
    col1.write(signup['createAccount'])
    col3.button("👋", on_click=function_signup_button_pressed)


def function_login_button_pressed():
    try:
        response = requests.post(URL + "/login", json={
            'username': st.session_state['username'],
            'password': st.session_state['password']
        })

        content = response.json()
            
        if content['state']:
            st.session_state['current_page'] = 'Chatbot'
            st.session_state['login_pressed'] = True

            st.session_state['user_id'] = content['user_id']
            st.session_state['user_name'] = content['user_name']
            st.session_state['user_is_connected'] = content['user_is_connected']

            st.session_state['username'] = None
            st.session_state['password'] = None
        else:
            st.error(content['message'])
            
    except Exception as e:
        st.error(translations[st.session_state['languages']]['generalError'])


def function_signup_button_pressed():
    st.session_state['current_page'] = 'Signup'
    st.session_state['signup_pressed'] = True
    st.session_state['username'] = None
    st.session_state['password'] = None


def function_set_language(locale):
    st.session_state['languages'] = locale