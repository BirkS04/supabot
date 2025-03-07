import PyPDF2
import fitz
import os
import base64
import tempfile
import json
import streamlit as st

from components.messages import insert_message, get_messages


from langchain_google_genai import ChatGoogleGenerativeAI


os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY")
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

def image_to_base64(image_bytes):
    """Konvertiert Bildbytes in einen Base64-String."""
    try:
        return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        st.error(f"Fehler bei der Base64-Konvertierung: {e}")
        return ""

def extract_pdf_content_as_json(file_obj):
    """Extrahiert Text und Bilder aus einer PDF-Datei und formatiert als JSON."""
    content = []
    try:
        # Temporäre Datei erstellen, um PyMuPDF-Kompatibilität sicherzustellen
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_obj.read())
            temp_path = temp_file.name

        # PDF mit dem temporären Pfad öffnen
        doc = fitz.open(temp_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Text extrahieren
            text = page.get_text()
            if text.strip():
                content.append({
                    "type": "text",
                    "text": text.strip()
                })

            # Bilder extrahieren
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                base64_string = image_to_base64(image_bytes)
                image_ext = base_image["ext"]
                # Bild als Base64-String hinzufügen
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{image_ext};base64,{base64_string}"
                    }
                })
        doc.close()
    except Exception as e:
        st.error(f"Fehler bei der PDF-Verarbeitung: {e}")

    json_string = json.dumps(content)

    return json_string


def main(file):

        with st.spinner("PDF wird verarbeitet..."):
            content = extract_pdf_content_as_json(file)

        st.success("PDF erfolgreich verarbeitet!")
        return content



def umformen(query: str,chat_id: int):
    db_results = get_messages(chat_id=chat_id)

    chat_messages = db_results.data
    message_list = []
    for msg in chat_messages:
        if msg["role"] == "system":
            role = "system"
            content = msg["content"]
        elif msg["role"] == "pdf":
            role = "user"
            json_string = msg["content"]
            content = json.loads(json_string)
        elif msg["role"] == "human":
            role = "user"
            content = msg["content"]
        else:
            role = "assistant"
            content = msg["content"]
        message_list.append({"role": role, "content": content})
    message_list.append({"role": "user", "content": query})
    return message_list


def file_content(uploaded_file):
    # Dateiinhalt verarbeiten
    try:
        # Datei als Binärdaten öffnen
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        st.write(f"Pages: {len(pdf_reader.pages)}")

        # Inhalt jeder Seite anzeigen
        file_text = ""
        for page_number, page in enumerate(pdf_reader.pages, start=1):
            text = page.extract_text()
            text += f"Page {page_number}:"
            file_text += text
        return file_text
    except Exception as e:
        st.error(f"Fehler beim Verarbeiten der PDF: {e}")


def invoke_and_add(query, chat_id):
    message_list = umformen(query=query, chat_id=chat_id)
    # st.write(message_list)
    # with open("verhalten.txt", "w", encoding="utf-8") as verhaltentxt:
    #     json.dump(message_list, verhaltentxt)
    # print(message_list)
    with st.chat_message("AI"):
        ai_response = st.write_stream(llm.stream(message_list))
        role = "ai"
    new_content = ai_response
    insert_message(chat_id=chat_id, role=role, message_content=new_content)