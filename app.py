import streamlit as st
from streamlit_oauth import OAuth2Component
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# --- 1. CONFIGURATION ---
CLIENT_ID = st.secrets["auth"]["client_id"]
CLIENT_SECRET = st.secrets["auth"]["client_secret"]
REDIRECT_URI = st.secrets["auth"]["redirect_uri"]
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
# We specifically ask for Google Docs and Drive access
SCOPES = "https://www.googleapis.com/auth/documents https://www.googleapis.com/auth/drive.file"

oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, TOKEN_URL, REDIRECT_URI)

st.title("📝 AI Script to Google Doc")

# --- 2. THE LOGIN LOGIC ---
if 'auth_token' not in st.session_state:
    # If not logged in, show the manual OAuth button
    result = oauth2.authorize_button("Log in with Google", SCOPES)
    if result and 'token' in result:
        st.session_state.auth_token = result['token']
        st.rerun()
else:
    # --- 3. THE APP CONTENT ---
    token = st.session_state.auth_token.get('access_token')
    
    st.success("✅ Connected to Google Docs!")
    if st.button("Log out"):
        del st.session_state.auth_token
        st.rerun()

    script_content = st.text_area("Your YouTube Script:", height=300)
    doc_title = st.text_input("Document Title:", value="My New YouTube Script")

    if st.button("Create Google Doc 🚀"):
        try:
            with st.spinner("Creating your document..."):
                creds = Credentials(token=token)
                service = build('docs', 'v1', credentials=creds)

                # Create and update the doc
                doc = service.documents().create(body={'title': doc_title}).execute()
                doc_id = doc.get('documentId')

                requests_body = [{'insertText': {'location': {'index': 1}, 'text': script_content}}]
                service.documents().batchUpdate(documentId=doc_id, body={'requests': requests_body}).execute()

                st.success("Saved to Drive!")
                st.link_button("📂 Open Document", f"https://docs.google.com/document/d/{doc_id}/edit")
        except Exception as e:
            st.error(f"Error: {e}")