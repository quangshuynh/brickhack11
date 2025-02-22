import streamlit as st
from backend.llm import get_ollama_response

st.set_page_config(
    page_title="Travel Buddy AI",
    layout="wide",
    page_icon="✈️"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(to right bottom, #87CEEB, #E0FFFF);
    }
    .st-emotion-cache-1v0mbdj {
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.9);
    }
    </style>
    """, unsafe_allow_html=True)

# Header with emoji and styling
st.markdown("# ✈️ Travel Buddy AI 🌎")
st.markdown("### Your personal AI travel assistant is here to help plan your next adventure! 🗺️")

# Info box
with st.expander("ℹ️ How can I help you?"):
    st.write("""
    I can assist you with:
    - Planning travel itineraries 🗓️
    - Finding destinations based on your interests 🎯
    - Suggesting local attractions and activities 🎨
    - Providing travel tips and advice 💡
    - Recommending accommodations and restaurants 🏨
    """)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to ask?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.chat_message("assistant"):
        response = get_ollama_response(st.session_state.messages)
        st.markdown(response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
