from __future__ import annotations

import streamlit as st


def render_message(message: dict, index: int) -> None:
    role = message.get("role", "assistant")
    content = message.get("content", "")
    if role == "user":
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(content)
        return

    with st.chat_message("assistant", avatar=":material/smart_toy:"):
        st.markdown(content)
        if message.get("error"):
            st.caption("There was a problem generating this response.")
        chunks = message.get("chunks") or []
        if chunks:
            render_sources(chunks, index)


def render_sources(chunks: list[dict], index: int) -> None:
    with st.expander(f"Sources · {len(chunks)} passages", expanded=False):
        for source_index, chunk in enumerate(chunks, start=1):
            doc_name = chunk.get("doc_name", "Document")
            page = chunk.get("page_number")
            page_label = f" · page {page}" if page is not None else ""
            st.markdown(f"**{source_index}. {doc_name}{page_label}**")
            st.caption(chunk.get("content", ""))
            if source_index != len(chunks):
                st.divider()
