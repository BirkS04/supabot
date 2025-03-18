import os
import streamlit as st
import json
from dotenv import load_dotenv


from components.messages import insert_message, get_messages
from components.chats import insert_chat, get_chats, delete_chat_and_messages, update_chat_last_used
from components.users import create_user, sign_in_user
from components.pdf import extract_pdf_content_as_json, main, umformen, image_to_base64, file_content, invoke_and_add

from langchain_google_genai import ChatGoogleGenerativeAI
from supabase import create_client, Client

load_dotenv()


os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

sess = st.session_state
# Initialize session state variables if they don't already exist.  These are used to store various aspects of the application's state.

#current chat id
if "current_chat" not in sess:
    sess.current_chat = [0]

#login status
if "logged_in" not in sess:
    sess.logged_in = False

#user email
if "email" not in sess:
    sess.email = ["filler"]

#user password
if "p" not in sess:
    sess.p = ["filler"]

#password confirmation
if "p2" not in sess:
    sess.p2 = ["filler"]

#counter to avoid infinite loop
if "rerun_counter" not in sess:
    sess.rerun_counter = 0

if "user_id" not in sess:
    sess.user_id = ""



def list_chats_and_current(chats: list):
    for chat in chats:
        chat_id = chat["id"]
        chat_name = chat["name"]
        button = st.button(label=chat_name, key=f"chatid_{chat_id}")
        if button:
            sess.current_chat.pop(0)
            sess.current_chat.append(chat)
            update_chat_last_used(chat_id)
            st.rerun(scope="app")

st.title("🤖Bot🤖")

# Main application logic, handling user authentication and chat functionality.
if not sess.logged_in:
    with st.sidebar:
        st.markdown("## Under Development")
        st.error("Please do not user your real credentials, use a made up email and password")
        st.success("Note: the agents etc. are working fine, but the creds. are not that secure")

        with st.expander("Sign Up"):
            email_sign_up = st.text_input(label="Email:", key="sing_up email")
            p_sign_up = st.text_input(label="Password:", key="sing_up password", type="password")
            p2_sign_up = st.text_input(label="Confirm Password:", key="sing_up password2", type="password")
            if email_sign_up and p_sign_up and p2_sign_up:
                user = create_user(email=email_sign_up, password=p_sign_up, password_confirmation=p2_sign_up)
                if user:
                    st.success("User Created")
                    sess.user_id = user.user.id
                    sess.logged_in = True
                    st.rerun(scope="app")
                    sess.rerun_counter += 1

        with st.expander(label="Log In", expanded=False):
            email = st.text_input("Email")
            p = st.text_input(type="password", label="Password")
            if email and p:
                signed_user = sign_in_user(email, p)
                if signed_user:
                    st.success("Logged In")
                    sess.user_id = signed_user.user.id
                    sess.logged_in = True
                    st.rerun(scope="app")
                    sess.rerun_counter += 1

# st.write(sess.rerun_counter)
if sess.logged_in:
    st.write("Logged In")

    user_id = sess.user_id
    chat_data = get_chats(user_id)
    chats = chat_data.data
    
    # st.write(chats)

    
    if sess.rerun_counter == 0:
        sess.rerun_counter = 1
        st.write("rerun counter is 0")
        if len(chats) != 0:
            sess.current_chat.pop(0)
            sess.current_chat.append(chats[-1]["id"])
        st.rerun(scope="app")
    
    with st.sidebar:
        logout = st.button("Log Out")
        if logout:
            sess.logged_in = False
            sess.rerun_counter = 0
            st.rerun(scope="app")

        if len(chats) != 0:
            sess.current_chat.pop(0)
            sess.current_chat.append(chats[0])
            st.markdown("### Create a New Chat")
            new_chat = st.chat_input("New Chat Name")
    

            if new_chat:
                insert_chat(user_id, new_chat)
                chat_data = get_chats(user_id)
                chats = chat_data.data
                new_chat = chats[0]
                sess.current_chat.pop(0)
                sess.current_chat.append(new_chat)
                st.rerun(scope="app")
        else:
            st.markdown("### Create your first Chat!")
            first_chat = st.chat_input("First Chat Name")

            if first_chat:
                insert_chat(user_id, first_chat)
                chat_data = get_chats(user_id)
                chats = chat_data.data
                first_chat = chats[0]
                sess.current_chat.pop(0)
                sess.current_chat.append(first_chat)
                st.rerun(scope="app")

    with st.sidebar:
        if len(chats) != 0:
            delete_button = st.button(f":x: Delete current Chat: {sess.current_chat[0]["name"]} :x:")
            if delete_button:
                chat_id = sess.current_chat[0]["id"]
                delete_chat_and_messages(chat_id)
                st.rerun(scope="app")


        with st.expander(label="Your Chats"):

            list_chats_and_current(chats)

    if len(chats) == 0:
        st.chat_input("You need to create a Chat first", disabled=True)
    else:
        system_prompt = st.chat_input("System Prompt")

        query = st.chat_input("Frag etwas")

        if system_prompt:
            insert_message(chat_id=sess.current_chat[0]["id"], role="system", message_content=system_prompt)

        if query:
            insert_message(chat_id=sess.current_chat[0]["id"], role="human", message_content=query)

        with st.sidebar:
            with st.expander(label="Upload Files"):

                files = st.file_uploader(label="Upload a PDF", type=["pdf"], accept_multiple_files= True)

                if files:
                    upload = st.button("Upload files")
                    if upload:
                        for i, file in enumerate(files):
                            with st.spinner("PDFs being processed"):

                                #upload_button = st.button(f"ADD: {file.name}")

                                content = extract_pdf_content_as_json(file)
                                insert_message(chat_id=sess.current_chat[0]["id"], role="pdf", message_content=content)
                                st.success(f"PDF {i + 1} processed")
        st.write("Current Chat ID:")
        st.write(sess.current_chat[0]["id"])
        message_list = get_messages(chat_id=sess.current_chat[0]["id"])
        messages = message_list.data
        # msg_list = []
        # for message in messages:
        #     msg_list.append(message)
        # st.write(msg_list)
        # st.write(messages)
        for msg in messages:
            id = msg["id"]
            role = msg["role"]
            content = msg["content"]
            st.write(content)
            if role == "system":
                with st.chat_message(role):
                    st.markdown(content)
            elif role == "pdf":
                with st.expander(label=f":page_facing_up: Your PDF"):
                    json_string = json.loads(content)
                    for i, item in enumerate(json_string):
                        st.text_area(label=f"{i}",value=item, height=200, key=f"{id},{i}")
            else:
                with st.chat_message(role):
                    st.markdown(content)
                    
            

        if query:
            invoke_and_add(query=query, chat_id=sess.current_chat[0]["id"])

else:
    st.chat_input("Not logged in", disabled=True)
