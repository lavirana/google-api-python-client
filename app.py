import streamlit as st
from googleapiclient.discovery import build
import requests

# Set page config
st.set_page_config(page_title="AI Script to Google Doc", page_icon="📝")

st.title("📝 AI Script to Google Doc")

# 1. AUTHENTICATION: Use the stable 2025 st.user object
if not st.user.is_logged_in:
    st.info("Please log in with your Google account to save scripts directly to your Drive.")
    if st.button("Log in with Google"):
        st.login()
    st.stop() 
else:
    # Sidebar Logout
    st.sidebar.write(f"Logged in as: **{st.user.name}**")
    if st.sidebar.button("Log out"):
        st.logout()

    # --- MAIN APP CONTENT ---
    st.write("✅ Ready to export! Enter your script details below.")
    
    script_content = st.text_area("Paste your AI-generated script here:", height=300)
    doc_title = st.text_input("Document Title:", value="My New YouTube Script")

    if st.button("Create Google Doc 🚀"):
        if not script_content:
            st.warning("Please enter some script content first!")
        else:
            try:
                with st.spinner("Creating your document..."):
                    # Use credentials from st.user (Available in Streamlit 1.42+)
                    creds = st.user.credentials
                    service = build('docs', 'v1', credentials=creds)

                    # 1. Create a blank document
                    doc = service.documents().create(body={'title': doc_title}).execute()
                    doc_id = doc.get('documentId')

                    # 2. Prepare the text insertion
                    # Note: index 1 is the start of a new Google Doc
                    requests_body = [
                        {
                            'insertText': {
                                'location': {'index': 1},
                                'text': script_content
                            }
                        }
                    ]
                    
                    # 3. Execute the update to add the script text
                    service.documents().batchUpdate(
                        documentId=doc_id, 
                        body={'requests': requests_body}
                    ).execute()

                    st.success(f"Successfully saved to your Google Drive!")
                    st.link_button("📂 Open Document", f"https://docs.google.com/document/d/{doc_id}/edit")

            except Exception as e:
                # This 'except' block fixes your SyntaxError
                st.error(f"Technical Error: {e}")
                st.info("💡 Ensure 'Google Docs API' is enabled in your Google Cloud Console.")