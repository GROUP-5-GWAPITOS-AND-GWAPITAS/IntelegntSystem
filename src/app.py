# src/app.py
"""Streamlit chatbot UI for the PC Hardware QA bot."""
import streamlit as st
from model import classify
from answer_key import ANSWER_KEY

st.set_page_config(
    page_title="Hardware QA Chatbot",
    page_icon="🖥️",
    layout="centered",
)

st.title("🖥️ PC Hardware QA Chatbot")
st.caption(
    "Ask about any of the 11 hardware parts. "
    "Powered by GloVe word embeddings + cosine similarity."
)

# ---- Session state ----
if "history" not in st.session_state:
    st.session_state.history = []

# ---- Sidebar ----
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    st.divider()
    st.subheader("📋 Answer Key")
    for it in ANSWER_KEY:
        st.markdown(f"**{it['id']}.** {it['canonical']}")

    st.divider()
    st.caption("Thresholds: correct ≥ 0.68 · partial ≥ 0.70")
    st.caption("Fuzzy match ≥ 0.80")

# ---- Welcome message ----
if not st.session_state.history:
    with st.chat_message("assistant"):
        st.write(
            "Hi! 👋 I'm your PC hardware assistant. "
            "Try asking things like:\n"
            "- *What is the brain of the computer?*\n"
            "- *CPU*\n"
            "- *keybord* (typos are okay!)\n"
            "- *the thing that stores my files*"
        )

# ---- Input ----
user_input = st.chat_input("Ask about a PC hardware part...")

if user_input is not None:
    result = classify(user_input)
    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("bot", result))

# ---- Render history ----
for role, content in st.session_state.history:
    if role == "user":
        with st.chat_message("user"):
            st.write(content)
    else:
        with st.chat_message("assistant"):
            st.write(content["reply"])
            if content["status"] != "empty":
                with st.expander("🔍 Similarity Matrix (11 scores)"):
                    for item, score in zip(ANSWER_KEY, content["matrix"]):
                        st.write(f"#{item['id']} {item['canonical']}: `{score:.4f}`")