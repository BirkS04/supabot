import os
import dotenv

from supabase import create_client
dotenv.load_dotenv()


url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)


def insert_message(chat_id, message_content, role):
    response = (
        supabase.table("messages")
        .insert({"chat_id": chat_id, "content": message_content, "role": role})
        .execute()
    )
    return response

def get_messages(chat_id):
    response = (
        supabase.table("messages")
        .select("*")
        .eq("chat_id", chat_id)
        .execute()
    )
    return response


