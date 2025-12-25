import streamlit as st
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import requests

# Set page config
st.set_page_config(page_title="AI Script to Google Doc", page_icon="📝")

st.title("📝 AI Script to Google Doc")

# 1. AUTHENTICATION (Stable 2025 Version)
# st.user is the new standard for identity and auth
if not st.user.is_logged_in:
    st.info("Please log in with your Google account to save scripts directly to your Drive.")
    if st.button("Log in with Google"):
        st.login()
    st.stop() 
else:
    # Sidebar Info & Logout
    st.sidebar.write(f"Logged in as: **{st.user.name}**")
    if st.sidebar.button("Log out"):
        st.logout()

    # --- MAIN APP CONTENT ---
    st.write("✅ Authentication Successful! Ready to create your Google Doc.")
    
    # Input Area
    script_content = st.text_area("Paste your AI-generated script here:", height=300)
    doc_title = st.text_input("Document Title:", value="My New YouTube Script")

    if st.button("Create Google Doc 🚀"):
        if not script_content:
            st.warning("Please enter some script content first!")
        else:
            try:
                with st.spinner("Talking to Google..."):
                    # 2025 FIX: Get the access token directly from st.user
                    token = st.user.get("access_token")
                    
                    if not token:
                        st.error("No access token found. Please logout and login again.")
                        st.stop()

                    # Reconstruct the Credentials object for the Google Discovery Build
                    creds = Credentials(token=token)
                    service = build('docs', 'v1', credentials=creds)

                    # 1. Create the blank document
                    doc = service.documents().create(body={'title': doc_title}).execute()
                    doc_id = doc.get('documentId')

                    # 2. Insert the script text
                    # Index 1 is the starting point of a new Google Doc
                    requests_body = [
                        {
                            'insertText': {
                                'location': {'index': 1},
                                'text': script_content
                            }
                        }
                    ]
                    
                    # 3. Apply the text insertion
                    service.documents().batchUpdate(
                        documentId=doc_id, 
                        body={'requests': requests_body}
                    ).execute()

                    # Success Message
                    st.success(f"Document Created Successfully!")
                    st.link_button("📂 Open Your Google Doc", f"https://docs.google.com/document/d/{doc_id}/edit")

            except Exception as e:
                st.error(f"Failed to create document: {e}")
                st.info("💡 Pro Tip: Make sure the Google Docs API is enabled in your Cloud Console.")