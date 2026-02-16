import streamlit as st
import requests
from Ressources.Config import URL
from Ressources.Translations import translations
from Services.Service_File import Service_File

def view_chatbot():
    chatbot = translations[st.session_state['languages']]['chatbotPage']

    view_history()

    st.title(chatbot['selectedModel'] + " : " + st.session_state['model_selected'])
    if st.session_state['chat_id'] is None :
        view_select_model()
    view_file_upload()

    if st.session_state['chat_id'] is not None :
        for message in st.session_state['selected_chat']:
            if message['chat_message_is_ia'] == 1:
                with st.chat_message("assistant"):
                    st.write(message['chat_message'])
            else:
                with st.chat_message("user"):
                    st.write(message['chat_message'])
    view_chat()


def view_select_model():
    st.selectbox(
        translations[st.session_state['languages']]['chatbotPage']['chooseModel'],
        ("Bert", "BigBird", "Splinter", "Squeeze"),
        index=0,
        key="model",
        on_change=function_select_model
    )


def view_history(): 
    Global = translations[st.session_state['languages']]

    function_initialize_history()

    col1, col2, col3 = st.sidebar.columns([3, 1, 1])
    col1.write(Global['language'])
    col2.button('EN ', on_click=function_set_language, args=('en',))
    col3.button('FR ', on_click=function_set_language, args=('fr',))

    col1, col2, col3 = st.sidebar.columns([3, 1, 3])
    col1.write(st.session_state['user_name'].capitalize())
    col3.button(translations[st.session_state['languages']]['logout'], on_click=function_logout_user)

    st.sidebar.title('')

    col1, col2, col3 = st.sidebar.columns([3, 1, 1])
    col1.write(Global['home'])
    col3.button('➕', on_click=function_new_chat)

    for option in st.session_state.chat_history.values():
        col1, col2, col3 = st.sidebar.columns([3, 1, 1])
        col1.write(option['chat_title'], key=f"chat_title_{option['chat_id']}")
        col2.button('👀', key=f"show_{option['chat_id']}", on_click=function_show_chat, args=(option['chat_id'],))
        col3.button('🗑️', key=f"del_{option['chat_id']}", on_click=function_delete_chat, args=(option['chat_id'],))


def view_chat():
    chatbot = translations[st.session_state['languages']]['chatbotPage']
    st.chat_input(chatbot['enterQuestion'], key='prompt', on_submit=function_send_message)
   

def view_file_upload():
    file = st.file_uploader('Upload a file', type=['.docx', '.pdf', '.xlsx', '.csv'])  
    st.write('') 

    if st.session_state['is_chat_show'] == False:
        st.session_state['have_file'] = False
        st.session_state['file_content'] = ''

    serviceFile = Service_File()
    string = ''

    if file is not None:
 
        string += serviceFile.file_for_string(file)
        st.session_state['have_file'] = True

        st.session_state['file_content'] = string


def function_initialize_history():
    try:
        response = requests.get(URL + "/chatHistory", json={
            'user_id': st.session_state['user_id'],
            'user_is_connected': st.session_state['user_is_connected'],
        })

        st.session_state.chat_history = dict(sorted(response.json().items(), key=lambda item: item[1]['chat_date'], reverse=True))

    except Exception as e:
        st.error(translations[st.session_state['languages']]['generalError'])


def function_send_message():
    st.session_state['user_question'] = st.session_state['prompt']

    try:
        response = requests.post(URL + "/predict", json={
            'user_id': st.session_state['user_id'],
            'chat_id': st.session_state['chat_id'],
            'user_is_connected': st.session_state['user_is_connected'],
            'user_question': st.session_state['user_question'],
            'file_content': st.session_state['file_content'],
            'have_file': st.session_state['have_file'],
            'model_selected': st.session_state['model_selected']
        })

        content = response.json()
    
        if st.session_state['chat_id'] == None:      
            st.session_state['chat_id'] = int(content['chat_id'])
            function_initialize_history()

        st.session_state['user_question'] = ''

        function_show_chat(int(content['chat_id']))

    except Exception as e:
        st.error(translations[st.session_state['languages']]['generalError'])


def function_new_chat():
    st.session_state['chat_id'] = None
    st.session_state['selected_chat'] = None
    st.session_state['user_question'] = ''
    st.session_state['file_content'] = None
    st.session_state['have_file'] = False
    st.session_state['is_chat_show'] = False 
    st.session_state['model_selected'] = "Bert"  


def function_show_chat(chat_id):
    st.session_state['file_content'] = None
    st.session_state['have_file'] = False

    try:
        st.session_state['chat_id'] = int(chat_id)

        chat_message_response = requests.get(URL + "/chatMessage", json={
            'user_id': st.session_state['user_id'],
            'user_is_connected': st.session_state['user_is_connected'],
            'chat_id': chat_id
        })

        chat_message_content = chat_message_response.json()

        chat_reponse = requests.get(URL + "/getChat", json={
            'user_id': st.session_state['user_id'],
            'user_is_connected': st.session_state['user_is_connected'],
            'chat_id': chat_id
        })

        chat_content = chat_reponse.json()

        if chat_content[3] is not None:
            st.session_state['have_file'] = True
            st.session_state['file_content'] = chat_content[3]

        st.session_state['is_chat_show'] = True
        st.session_state['selected_chat'] = chat_message_content
        st.session_state['model_selected'] = st.session_state['chat_history'][str(chat_id)]['chat_model']
    
    except Exception as e:
        st.error(translations[st.session_state['languages']]['generalError'])


def function_delete_chat(chat_id):
    try:
        requests.post(URL + "/deleteChat", json={
            'user_id': st.session_state['user_id'],
            'chat_id': chat_id,
            'user_is_connected': st.session_state['user_is_connected'],
        })

        del st.session_state.chat_history[str(chat_id)]

        if st.session_state['chat_id'] == chat_id:
            st.session_state['model_selected'] = "Bert"
            st.session_state['chat_id'] = None
            st.session_state['selected_chat'] = None
            st.session_state['have_file'] = False
            st.session_state['file_content'] = None
            st.session_state['is_chat_show'] = False

    except Exception as e:
        st.error(translations[st.session_state['languages']]['generalError'])


def function_set_language(locale):
    st.session_state['languages'] = locale


def function_select_model():
    st.session_state['model_selected'] = st.session_state['model']


def function_logout_user():
    st.session_state['user_id'] = None
    st.session_state['user_name'] = None
    st.session_state['user_is_connected'] = False
    st.session_state['chat_history'] = {}
    st.session_state['selected_chat'] = {}
    st.session_state['user_question'] = ''
    st.session_state['chat_id'] = None
    st.session_state['current_page'] = 'Login'
    st.session_state['login_pressed'] = False
    st.session_state['signup_pressed'] = False
    st.session_state['model_selected'] = "Bert"
    st.session_state['file_content'] = None
    st.session_state['is_chat_show'] = False

