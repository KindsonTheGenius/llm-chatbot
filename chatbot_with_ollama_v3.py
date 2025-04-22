import streamlit as st
import requests
from datetime import datetime

# --- Sidebar ---
st.sidebar.title("⚙️ Settings")
model_options = ["mistral", "llama2", "gemma"]
MODEL_NAME = st.sidebar.selectbox("Choose a model", model_options)

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []

st.sidebar.markdown("---")
st.sidebar.markdown("**Local Chatbot Powered by Ollama**")
st.sidebar.markdown("Built with ❤️ using Streamlit")

# --- Styles ---
st.markdown("""
    <style>
        .chat-title {
            font-size: 2.3rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1.5rem;
            color: #4A90E2;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            max-height: 70vh;
            overflow-y: auto;
            padding: 10px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        }
        .chat-bubble-user {
            align-self: flex-end;
            background-color: #DCF8C6;
            color: #000;
            padding: 12px;
            border-radius: 12px;
            margin: 5px 0;
            max-width: 80%;
        }
        .chat-bubble-assistant {
            align-self: flex-start;
            background-color: #F1F0F0;
            color: #000;
            padding: 12px;
            border-radius: 12px;
            margin: 5px 0;
            max-width: 80%;
        }
        .timestamp {
            font-size: 0.7rem;
            color: #888;
            margin: 0 5px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="chat-title">💬 Ollama Chatbot UI</div>', unsafe_allow_html=True)

# --- Initialize state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat container ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    timestamp = message.get("timestamp", datetime.now().strftime("%H:%M"))
    bubble_class = "chat-bubble-user" if role == "user" else "chat-bubble-assistant"
    avatar = "🧑‍💻" if role == "user" else "🤖"

    st.markdown(
        f'<div class="{bubble_class}">'
        f'<strong>{avatar} {role.capitalize()}:</strong><br>{content}'
        f'<div class="timestamp">{timestamp}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# --- User input ---
if prompt := st.chat_input("Type your message..."):

    now = datetime.now().strftime("%H:%M")

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": now
    })

    # Send to Ollama
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ],
                "stream": False
            }
        )

        if response.status_code == 200:
            reply = response.json()["message"]["content"]
        else:
            reply = "⚠️ Error: Could not connect to local model."

    # Add assistant reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    # Rerun to show the new messages
    st.experimental_rerun()
