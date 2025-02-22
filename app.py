import streamlit as st
import time
from backend.llm import get_ollama_response

st.set_page_config(page_title="GoGen", layout="wide", page_icon="🌐")

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        color: #333;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        padding: 20px;
    }
    .chat-bubble {
        border-radius: 25px;
        padding: 12px 20px;
        margin: 8px 0;
        max-width: 80%;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .chat-bubble:hover {
        transform: scale(1.02);
    }
    .user-bubble {
        background-color: #e0f7fa;  /* light cyan */
        color: #00796b;            /* teal */
        align-self: flex-end;
    }
    .assistant-bubble {
        background-color: #ffffff;
        color: #333;
        align-self: flex-start;
    }
    /* Custom styling for Streamlit chat input (if applicable) */
    .stChatInput textarea {
        border: none;
        border-radius: 20px;
        padding: 10px;
        background: #f0f0f0;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)


st.markdown("<h1 style='text-align:center;'>GoGen</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Your AI-powered travel companion</h3>", unsafe_allow_html=True)


st.sidebar.header("How can GoGen help?")
st.sidebar.write("""
- Create personalized travel itineraries  
- Discover destinations tailored to your interests  
- Suggest attractions, accommodations, and dining options  
- Provide travel tips and advice
""")


if "messages" not in st.session_state:
    st.session_state.messages = []

chat_placeholder = st.empty()

def render_chat():
    with chat_placeholder.container():
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f"<div class='chat-bubble user-bubble'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='chat-bubble assistant-bubble'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )
        st.markdown("</div>", unsafe_allow_html=True)


render_chat()
user_input = st.chat_input("Ask GoGen anything about travel...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_chat()  
    time.sleep(0.1)  

    with st.spinner("GoGen is thinking..."):
        response = get_ollama_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    render_chat()  
