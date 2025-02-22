import streamlit as st
import time
import pandas as pd
# import requests  # uncomment when we add real api calls
from backend.llm import get_ollama_response

st.set_page_config(page_title="GoGen", layout="wide", page_icon="🌐")

# css
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
        background-color: #e0f7fa;
        color: #00796b;
        align-self: flex-end;
    }
    .assistant-bubble {
        background-color: #ffffff;
        color: #333;
        align-self: flex-start;
    }
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

# left sidebar
st.sidebar.header("How can GoGen help?")
st.sidebar.write("""
- Create personalized travel itineraries  
- Discover destinations tailored to your interests  
- Suggest attractions, accommodations, and dining options  
- Provide travel tips and advice
""")

# placeholders for testing
def detect_location(text):
    """
    A simple function to check if the user input contains a known destination.
    You can replace or extend this with a more robust NLP solution.
    """
    known_locations = ["Paris", "London", "New York", "Tokyo", "Rome", "Barcelona", "Sydney", "Berlin"]
    for loc in known_locations:
        if loc.lower() in text.lower():
            return loc
    return None

def fetch_map_coordinates(location):
    """
    Simulated API call for map coordinates.
    Replace this dictionary with a real geocoding API call if needed.
    """
    city_coords = {
        "Paris": {"lat": 48.8566, "lon": 2.3522},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "New York": {"lat": 40.7128, "lon": -74.0060},
        "Tokyo": {"lat": 35.6895, "lon": 139.6917},
        "Rome": {"lat": 41.9028, "lon": 12.4964},
        "Barcelona": {"lat": 41.3851, "lon": 2.1734},
        "Sydney": {"lat": -33.8688, "lon": 151.2093},
        "Berlin": {"lat": 52.5200, "lon": 13.4050}
    }
    return city_coords.get(location)

def fetch_hotels(location):
    """Simulated API call for hotels data."""
    sample_hotels = {
        "Paris": ["Hotel Le Meurice", "Hôtel Plaza Athénée", "Le Bristol Paris"],
        "London": ["The Savoy", "The Ritz London", "Claridge's"],   
    }
    return sample_hotels.get(location, ["Hotel A", "Hotel B", "Hotel C"])

def fetch_tourist_spots(location):
    """Simulated API call for top tourist spots."""
    sample_spots = {
        "Paris": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"],
        "London": ["Big Ben", "London Eye", "Tower Bridge"],
    }
    return sample_spots.get(location, ["Attraction 1", "Attraction 2", "Attraction 3"])

def fetch_flights(location):
    """Simulated API call for flight information."""
    sample_flights = {
        "Paris": ["Flight 1: $500", "Flight 2: $450", "Flight 3: $550"],
        "London": ["Flight 1: $600", "Flight 2: $580", "Flight 3: $620"],
    }
    return sample_flights.get(location, ["Flight Option A", "Flight Option B", "Flight Option C"])

# display info (map, hotels, tourist spots)
def display_destination_info(location, container):
    """Displays map, hotels, tourist spots, and flight info in the given container."""
    with container:
        st.subheader(f"Destination Info: {location}")
        
        # map
        coords = fetch_map_coordinates(location)
        if coords:
            st.markdown("### Map")
            df = pd.DataFrame([coords])
            st.map(df)
            st.write(f"Coordinates: {coords['lat']}, {coords['lon']}")
        else:
            st.write("Map information not available.")
        
        # hotels
        st.markdown("### Hotels")
        hotels = fetch_hotels(location)
        for hotel in hotels:
            st.write(f"- {hotel}")
        
        # tourists
        st.markdown("### Tourist Spots")
        spots = fetch_tourist_spots(location)
        for spot in spots:
            st.write(f"- {spot}")
        
        # flights
        st.markdown("### Flight Options")
        flights = fetch_flights(location)
        for flight in flights:
            st.write(f"- {flight}")



# frontend/backend logic
left_col, right_col = st.columns([3, 1])
chat_placeholder = left_col.empty()

if "messages" not in st.session_state:
    st.session_state.messages = []

def render_chat():
    """Render the chat history in the left column."""
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

st.markdown("""
    <style>
    .stChatInput textarea::placeholder {
         color: black;
    }
    </style>
    """, unsafe_allow_html=True)

user_input = st.chat_input("Ask GoGen anything about travel...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_chat()  
    time.sleep(0.1)  

    location = detect_location(user_input)
    if location:
        display_destination_info(location, right_col)
    
    with st.spinner("GoGen is thinking..."):
        response = get_ollama_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    render_chat()
