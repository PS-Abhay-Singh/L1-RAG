import streamlit as st
import requests

API_BASE = "http://localhost:8001"

st.set_page_config(page_title="ResearchPaperAI", layout="wide")

st.title("ResearchPaperAI Chat UI")

if "history" not in st.session_state:
    st.session_state.history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "session_" + st.session_state.get("user_id", "anon")

with st.sidebar:
    st.header("Actions")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if st.button("Upload") and uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post(f"{API_BASE}/upload", files=files)
        if response.ok:
            data = response.json()
            st.session_state.uploaded_files.append(data["file_name"])
            st.success(f"Uploaded {data['file_name']} with {data['chunks']} chunks")
        else:
            st.error(response.text)

    st.markdown("---")
    st.subheader("Manage uploaded PDFs")
    delete_file = st.selectbox("Select a file to delete", [""] + st.session_state.uploaded_files)
    if st.button("Delete selected PDF") and delete_file:
        response = requests.post(f"{API_BASE}/delete-pdf", json={"file_name": delete_file})
        if response.ok:
            st.session_state.uploaded_files = [f for f in st.session_state.uploaded_files if f != delete_file]
            st.success(f"Deleted {delete_file} from Pinecone and uploads")
        else:
            st.error(response.text)

    st.markdown("---")
    st.subheader("Conversation")
    st.write("Use the chat box below to ask about your uploaded papers.")

user_query = st.text_input("Ask a question", key="query_input")
col_send, col_clear = st.columns([1, 5])
with col_send:
    if st.button("Send") and user_query:
        payload = {"query": user_query, "history": st.session_state.history}
        response = requests.post(f"{API_BASE}/chat", json=payload)
        if response.ok:
            data = response.json()
            st.session_state.history = data["history"]
            st.session_state.citations = data["citations"]
        else:
            st.error(response.text)
with col_clear:
    if st.button("Clear History"):
        st.session_state.history = []
        st.session_state.citations = []

# Citations — horizontal row above conversation
st.markdown("---")
st.subheader("📎 Citations")
if "citations" in st.session_state and st.session_state.citations:
    citations = st.session_state.citations
    cols = st.columns(len(citations))
    for col, (i, citation) in zip(cols, enumerate(citations, 1)):
        with col:
            st.markdown(
                f"""
                <div style="background:#1e1e2e;border-left:3px solid #7c6af7;padding:8px 12px;
                            border-radius:6px;font-size:0.82rem;line-height:1.5;height:100%">
                    <span style="color:#a78bfa;font-weight:600">[{i}]</span>&nbsp;
                    <span style="color:#e2e8f0">{citation.get('paper','Unknown')}</span><br/>
                    <span style="color:#94a3b8;font-style:italic">{citation.get('section','Unknown section')}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.caption("No citations yet.")

st.markdown("---")

st.subheader("Conversation")
for entry in st.session_state.history:
    if entry["speaker"] == "user":
        st.markdown(f"**You:** {entry['text']}")
    else:
        st.markdown(f"**Assistant:** {entry['text']}")
