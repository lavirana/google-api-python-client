import streamlit as st
from googleapiclient.discovery import build
import requests

# 1. Add these to your secrets.toml or Streamlit Cloud Secrets
# [auth]
# client_id = "YOUR_CLIENT_ID"
# client_secret = "YOUR_CLIENT_SECRET"
# redirect_uri = "https://your-app.streamlit.app/oauth2callback"

st.title("📝 AI Script to Google Doc")

# Built-in Streamlit OAuth Login (v1.42+)
if not st.experimental_user.is_logged_in:
    if st.button("Log in with Google"):
        st.login()
else:
    st.write(f"Logged in as: {st.experimental_user.name}")
    
    # Text area for the script (Input from your YouTube Tool)
    script_content = st.text_area("Your YouTube Script:", height=300)
    doc_title = st.text_input("Document Title:", "My New YouTube Script")

    if st.button("Create Google Doc 🚀"):
        if script_content:
            try:
                # Use the token provided by st.login
                creds = st.experimental_user.credentials
                service = build('docs', 'v1', credentials=creds)

                # Create a blank document
                doc = service.documents().create(body={'title': doc_title}).execute()
                doc_id = doc.get('documentId')

                # Insert the script text into the document
                requests_body = [
                    {
                        'insertText': {
                            'location': {'index': 1},
                            'text': script_content
                        }
                    }
                ]
                service.documents().batchUpdate(documentId=doc_id, body={'requests': requests_body}).execute()

                st.success(f"Document Created! ID: {doc_id}")
                st.markdown(f"[Click here to open your Doc](https://docs.google.com/document/d/{doc_id}/edit)")

            except Exception as e:
                st.error(f"Error creating document: {e}")