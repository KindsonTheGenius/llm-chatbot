import streamlit as st
import numpy as np

st.title("Basic Bot")

# Initialize the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
# assign the user's input to the prompt variable and checked if it's not None in the same line
if prompt := st.chat_input("What's up"): # The argument is a placeholder

    # Display the user message in the chat container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
