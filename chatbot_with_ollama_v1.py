import streamlit as st
import requests

st.title("Your Local Mistral Chatbot (via Ollama)")

# Set default model name (can be any model available locally, e.g., mistral, llama2, etc.)
MODEL_NAME = "mistral"

# Initialize the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's up?"):

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send request to local Ollama server
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": MODEL_NAME,
                    "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    "stream": False  # Set to True for streaming support (more complex handling)
                }
            )

            if response.status_code == 200:
                response_content = response.json()["message"]["content"]
            else:
                response_content = "Error: Unable to get response from local model."

            st.markdown(response_content)

    # Add assistant reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})
