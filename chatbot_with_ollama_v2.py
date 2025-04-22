import streamlit as st
import requests

# --- Custom Styles ---
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
        }
        .main {
            padding: 2rem;
            background-color: #ffffff;
            border-radius: 10px;
        }
        .chat-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4A90E2;
            text-align: center;
            margin-bottom: 1rem;
        }
        .chat-bubble-user {
            background-color: #DCF8C6;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 8px 0;
            max-width: 80%;
            align-self: flex-end;
        }
        .chat-bubble-assistant {
            background-color: #F1F0F0;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 8px 0;
            max-width: 80%;
            align-self: flex-start;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-title">💬 Local Mistral Chatbot</div>', unsafe_allow_html=True)

# --- Model Setup ---
MODEL_NAME = "mistral"

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render chat history ---
for message in st.session_state.messages:
    bubble_class = "chat-bubble-user" if message["role"] == "user" else "chat-bubble-assistant"
    with st.container():
        st.markdown(f'<div class="chat-container"><div class="{bubble_class}">{message["content"]}</div></div>', unsafe_allow_html=True)

# --- Accept user input ---
if prompt := st.chat_input("Type your message..."):

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-container"><div class="chat-bubble-user">{prompt}</div></div>', unsafe_allow_html=True)

    # Send to Ollama
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                "stream": False
            }
        )

        if response.status_code == 200:
            reply = response.json()["message"]["content"]
        else:
            reply = "⚠️ Error: Could not connect to local model."

    # Show assistant response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(f'<div class="chat-container"><div class="chat-bubble-assistant">{reply}</div></div>', unsafe_allow_html=True)
