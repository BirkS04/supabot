import streamlit as st


from supabase import create_client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)


def insert_chat(user_id, chat_name):
    response = (
        supabase.table("chats")
        .insert({"user_id": user_id, "name": chat_name})
        .execute()
    )
    return response

def get_chats(user_id):
    response = (
        supabase.table("chats")
        .select("*")
        .eq("user_id", user_id)
        .order("last_used", desc=True)
        .execute()
    )
    return response


def delete_chat_and_messages(chat_id):
    response = (
    supabase.table("messages")
    .delete()
    .eq("chat_id", chat_id)
    .execute()
    )

    response2 = (
        supabase.table("chats")
        .delete()
        .eq("id", chat_id)
        .execute()
    )

    return [response, response2]


def update_chat_last_used(chat_id):
    response = (
        supabase.table("chats")
        .update({"last_used": "now()"})
        .eq("id", chat_id)
        .execute()
    )
    return response

