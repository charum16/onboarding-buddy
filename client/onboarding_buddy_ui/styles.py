from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
        :root { --ink:#202a29; --muted:#77817d; --line:#e7e9e5; --paper:#fbfbf8; --sidebar:#f2f3ef; --accent:#287d70; --accent-soft:#e5f0ec; }
        html, body, [class*="css"] { font-family:'DM Sans',sans-serif; color:var(--ink); }
        .stApp { background:var(--paper); }
        [data-testid="stSidebar"] { background:var(--sidebar); border-right:1px solid #e5e7e1; }
        [data-testid="stSidebar"] > div:first-child { padding:1.45rem 1rem 1rem; }
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap:.55rem; }
        [data-testid="stSidebar"] .stButton button { border:1px solid transparent; background:transparent; color:#46514d; text-align:left; border-radius:8px; padding:.55rem .7rem; font-size:.86rem; min-height:2.35rem; }
        [data-testid="stSidebar"] .stButton button:hover { background:#e8ebe5; border-color:#e1e5de; color:#202a29; }
        [data-testid="stSidebar"] .stButton button[kind="primary"] { background:#263b37; color:#fff; border-color:#263b37; font-weight:600; }
        [data-testid="stSidebar"] .stButton button[kind="primary"]:hover { background:#34534c; border-color:#34534c; }
        [data-testid="stSidebar"] label { color:#68736e; font-size:.78rem; }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section { background:#fafbf8; border:1px dashed #cbd2ca; border-radius:8px; }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] small { color:#7c8580; }
        .brand-lockup { display:flex; align-items:center; gap:11px; padding:.1rem .25rem .65rem; }
        .brand-mark { width:37px; height:37px; border-radius:10px; background:#263b37; color:#f7faf7; display:flex; align-items:center; justify-content:center; font-family:Manrope,sans-serif; font-size:17px; font-weight:800; letter-spacing:-1px; }
        .brand-name { font-family:Manrope,sans-serif; font-weight:800; font-size:15px; letter-spacing:-.45px; color:#26312e; }
        .brand-caption { font-size:8px; letter-spacing:1.35px; color:#87918b; margin-top:2px; font-weight:700; }
        .sidebar-rule { height:1px; background:#e0e4dc; margin:.3rem 0 .9rem; }
        .sidebar-rule-spaced { margin:1.1rem 0 .95rem; }
        .sidebar-section-label { color:#8a938d; font-size:9px; font-weight:700; letter-spacing:1.45px; padding:.1rem .55rem .35rem; }
        .sidebar-empty,.sidebar-help { color:#8a938d; font-size:11px; line-height:1.6; padding:0 .55rem; }
        .sidebar-footer { position:fixed; bottom:15px; color:#7d8982; font-size:10px; padding:.6rem .45rem; background:var(--sidebar); }
        .status-dot { display:inline-block; width:6px; height:6px; border-radius:50%; background:#4e9b78; margin-right:6px; }
        .main .block-container { max-width:940px; padding:0 2.2rem 7rem; }
        .topbar { display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--line); padding:1.35rem 0 1.1rem; margin-bottom:3.4rem; }
        .topbar-label,.conversation-kicker { color:#909994; font-size:9px; font-weight:700; letter-spacing:1.5px; }
        .topbar-status { color:#77827c; font-size:11px; }
        .topbar-status:first-letter { color:#4e9b78; }
        .welcome-wrap { max-width:690px; margin:5.3rem auto 2rem; }
        .welcome-eyebrow { color:var(--accent); font-size:10px; letter-spacing:1.7px; font-weight:700; margin-bottom:1.2rem; }
        .welcome-wrap h1 { font-family:Manrope,sans-serif; font-size:clamp(2.25rem,5vw,3.25rem); line-height:1.12; letter-spacing:-2px; color:#26312e; font-weight:700; margin:0 0 1.15rem; }
        .welcome-wrap h1 span { color:#84908a; }
        .welcome-copy { max-width:510px; color:#77827c; font-size:14px; line-height:1.8; margin-bottom:3rem; }
        .suggestion-label { font-size:9px; font-weight:700; letter-spacing:1.5px; color:#9aa39d; margin-bottom:.65rem; }
        .main .stButton button { border:1px solid #e3e7e1; background:#fff; color:#48544f; border-radius:8px; min-height:3rem; font-size:12px; text-align:left; padding:.7rem .9rem; }
        .main .stButton button:hover { border-color:#a8c6bb; color:#276f62; background:#f7faf7; }
        .conversation-heading { display:flex; justify-content:space-between; align-items:center; margin:-1.6rem 0 2rem; padding-bottom:1rem; border-bottom:1px solid var(--line); }
        .conversation-title { font-family:Manrope,sans-serif; font-size:19px; font-weight:700; color:#2a3531; margin-top:.3rem; }
        [data-testid="stChatMessage"] { background:transparent; border:none; padding:.9rem 0; }
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] { font-size:14px; line-height:1.8; }
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { margin-bottom:.8rem; }
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 { font-family:Manrope,sans-serif; color:#26312e; letter-spacing:-.4px; }
        [data-testid="stChatMessage"] pre { background:#f0f2ee; border:1px solid #e2e6df; border-radius:8px; }
        [data-testid="stChatMessage"] code { color:#2b6459; }
        [data-testid="stChatInput"] { border:1px solid #dfe4dd; border-radius:12px; background:#fff; box-shadow:0 5px 22px rgba(34,52,44,.055); }
        [data-testid="stChatInput"] textarea { font-size:14px; }
        [data-testid="stChatInput"] button { color:var(--accent); }
        [data-testid="stExpander"] { border:1px solid #e7eae5; border-radius:8px; background:#fafbf8; }
        [data-testid="stExpander"] summary { color:#66736c; font-size:12px; }
        .stAlert { border-radius:8px; }
        @media (max-width: 760px) {
          .main .block-container { padding-left:1rem; padding-right:1rem; }
          .topbar { margin-bottom:2rem; }
          .welcome-wrap { margin-top:3rem; }
          .welcome-wrap h1 { letter-spacing:-1.3px; }
          .sidebar-footer { position:static; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
