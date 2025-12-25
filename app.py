import streamlit as st
from googleapiclient.discovery import build
import requests

# Set page config
st.set_page_config(page_title="AI Script to Google Doc", page_icon="📝")

st.title("📝 AI Script to Google Doc")

# 1. NEW 2025 AUTH: Use st.user instead of st.experimental_user
if not st.user.is_logged_in:
    st.info("Please log in with your Google account to save scripts directly to your Drive.")
    if st.button("Log in with Google"):
        st.login()
    st.stop()  # Stop the app here if not logged in
else:
    # Sidebar Logout option
    st.sidebar.write(f"Logged in as: **{st.user.name}**")
    if st.sidebar.button("Log out"):
        st.logout()

    # --- MAIN APP CONTENT ---
    st.write("Successfully authenticated with Google! You can now export your scripts.")
    
    # Input Area
    script_content = st.text_area("Paste your AI-generated script here:", height=300)
    doc_title = st.text_input("Document Title:", value="My New YouTube Script")

    if st.button("Create Google Doc 🚀"):
        if not script_content:
            st.warning("Please enter some script content first!")
        else:
            try:
                with st.spinner("Creating your document..."):
                    # Use the credentials from the logged-in user
                    # In 2025, st.user.credentials provides the OAuth token directly
                    creds = st.user.credentials
                    service = build('docs', 'v1', credentials=creds)

                    # 1. Create a blank document
                    doc = service.documents().create(body={'title': doc_title}).execute()
                    doc_id = doc.get('documentId')

                    # 2. Insert text into the document