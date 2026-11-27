from __future__ import annotations

import os
from html import escape

import streamlit as st

from onboarding_buddy_ui.api import APIError, BuddyAPI
from onboarding_buddy_ui.components import render_message, render_sources
from onboarding_buddy_ui.styles import apply_styles


st.set_page_config(
    page_title="Onboarding Buddy",
    page_icon="OB",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_styles()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
try:
    API_BASE_URL = st.secrets.get("API_BASE_URL", API_BASE_URL)
except Exception:
    pass
api = BuddyAPI(API_BASE_URL)


def init_state() -> None:
    defaults = {
        "active_conversation_id": None,
        "active_conversation_name": None,
        "messages": [],
        "loaded_conversation_id": None,
        "api_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def refresh_conversations() -> list[dict]:
    try:
        return api.list_conversations()
    except APIError as exc:
        st.sidebar.error(str(exc))
        return []


def start_new_conversation() -> None:
    st.session_state.active_conversation_id = None
    st.session_state.active_conversation_name = None
    st.session_state.messages = []
    st.session_state.loaded_conversation_id = None
    st.rerun()


def open_conversation(conversation: dict) -> None:
    conversation_id = conversation["id"]
    try:
        persisted = api.get_messages(conversation_id)
    except APIError as exc:
        st.sidebar.error(str(exc))
        return

    # The current API stores content without a sender field. These persisted
    # records are therefore presented as prior assistant responses only.
    st.session_state.active_conversation_id = conversation_id
    st.session_state.active_conversation_name = conversation.get("convo_name", "Conversation")
    st.session_state.messages = [
        {"role": "assistant", "content": item.get("content", ""), "chunks": []}
        for item in persisted
    ]
    st.session_state.loaded_conversation_id = conversation_id
    st.rerun()


init_state()

# Sidebar: product identity, session history, and document ingestion.
with st.sidebar:
    st.markdown(
        '<div class="brand-lockup"><div class="brand-mark">ob</div>'
        '<div><div class="brand-name">onboarding buddy</div>'
        '<div class="brand-caption">YOUR WORKPLACE COMPANION</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sidebar-rule"></div>', unsafe_allow_html=True)

    if st.button("＋  New conversation", use_container_width=True, type="primary"):
        start_new_conversation()

    st.markdown('<div class="sidebar-section-label">WORKSPACE</div>', unsafe_allow_html=True)
    conversations = refresh_conversations()
    if conversations:
        active_id = st.session_state.active_conversation_id
        for convo in conversations:
            label = convo.get("convo_name") or f"Conversation {convo['id']}"
            selected = convo["id"] == active_id
            item_col, delete_col = st.columns([5, 1], gap="small")
            with item_col:
                button_label = ("●  " if selected else "　 ") + label
                if st.button(
                    button_label,
                    key=f"conversation_{convo['id']}",
                    use_container_width=True,
                    help=f"Open {label}",
                ):
                    open_conversation(convo)
            with delete_col:
                if st.button("×", key=f"delete_{convo['id']}", help="Delete conversation"):
                    try:
                        api.delete_conversation(convo["id"])
                        if st.session_state.active_conversation_id == convo["id"]:
                            st.session_state.active_conversation_id = None
                            st.session_state.active_conversation_name = None
                            st.session_state.messages = []
                            st.session_state.loaded_conversation_id = None
                        st.rerun()
                    except APIError as exc:
                        st.error(str(exc))
    else:
        st.markdown('<p class="sidebar-empty">Your conversations will appear here.</p>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-rule sidebar-rule-spaced"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-label">KNOWLEDGE BASE</div>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-help">Add a guide or document to give Buddy context for its answers.</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "txt", "md"],
        label_visibility="collapsed",
        help="Supported formats: PDF, TXT and Markdown.",
    )
    chunk_strategy = st.selectbox(
        "Chunking strategy",
        options=["fixed_size", "paragraph"],
        format_func=lambda value: "Fixed size" if value == "fixed_size" else "By paragraph",
    )
    if st.button("Add to knowledge base", use_container_width=True, disabled=uploaded_file is None):
        with st.spinner("Processing document…"):
            try:
                result = api.upload_document(uploaded_file, chunk_strategy)
                st.success(f"Added {result.get('filename', uploaded_file.name)}")
            except APIError as exc:
                st.error(str(exc))

    st.markdown('<div class="sidebar-footer"><span class="status-dot"></span> Connected to Onboarding Buddy API</div>', unsafe_allow_html=True)

# Main conversation workspace.
st.markdown('<div class="topbar"><span class="topbar-label">ONBOARDING / ASSISTANT</span><span class="topbar-status">●  Knowledge assistant</span></div>', unsafe_allow_html=True)

messages = st.session_state.messages
if not messages:
    st.markdown(
        '<section class="welcome-wrap">'
        '<div class="welcome-eyebrow">A BETTER WAY TO GET STARTED</div>'
        '<h1>Find your footing.<br><span>We’ll help with the rest.</span></h1>'
        '<p class="welcome-copy">Ask questions about your onboarding documents, workplace processes, and the information your team has shared.</p>'
        '<div class="suggestion-label">TRY ASKING</div>'
        '</section>',
        unsafe_allow_html=True,
    )
    suggestions = [
        ("First day", "What should I focus on during my first day?"),
        ("Getting set up", "What tools and accounts do I need to get started?"),
        ("Team processes", "Where can I find the key team processes?"),
    ]
    cols = st.columns(3)
    for col, (title, prompt) in zip(cols, suggestions):
        with col:
            if st.button(f"{title}  ↗", key=f"suggest_{title}", use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()
else:
    title = st.session_state.active_conversation_name or "Your conversation"
    st.markdown(f'<div class="conversation-heading"><div><div class="conversation-kicker">CURRENT SESSION</div><div class="conversation-title">{escape(title)}</div></div></div>', unsafe_allow_html=True)
    for index, message in enumerate(messages):
        render_message(message, index)

# Input stays at the bottom of the page using Streamlit's native chat input.
prompt = st.chat_input("Ask anything about your onboarding…")
if not prompt and st.session_state.get("pending_prompt"):
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    clean_prompt = prompt.strip()
    if clean_prompt:
        if st.session_state.active_conversation_id is None:
            try:
                created = api.create_conversation(clean_prompt[:60] or "New conversation")
                st.session_state.active_conversation_id = created["id"]
                st.session_state.active_conversation_name = created.get("convo_name", "New conversation")
                st.session_state.loaded_conversation_id = created["id"]
            except APIError as exc:
                st.error(f"Could not start a conversation: {exc}")
                st.stop()

        st.session_state.messages.append({"role": "user", "content": clean_prompt, "chunks": []})
        with st.spinner("Buddy is thinking…"):
            try:
                result = api.send_message(st.session_state.active_conversation_id, clean_prompt)
                assistant_message = {
                    "role": "assistant",
                    "content": result.get("response", ""),
                    "chunks": result.get("chunks", []),
                }
                st.session_state.messages.append(assistant_message)
            except APIError as exc:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"I couldn't complete that request. {exc}",
                    "chunks": [],
                    "error": True,
                })
        st.rerun()
