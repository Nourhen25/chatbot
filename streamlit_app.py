import streamlit as st
import os
import requests

# Show title and description.
st.title("💬 Chatbot - Mental Health Support")
st.write(
    "This is a simple chatbot powered by DeepSeek API, designed to provide mental health support. "
    "To use this app, you need to provide your DeepSeek API key. "
    "Ensure that you store your API key securely."
)

# Ask user for their DeepSeek API key via `st.text_input`.
# You can also store the API key in `./.streamlit/secrets.toml` and access it via `st.secrets`.
deepseek_api_key = st.text_input("DeepSeek API Key", type="password")
if not deepseek_api_key:
    st.info("Please add your DeepSeek API key to continue.", icon="🗝️")
else:
    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("How are you feeling today?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using DeepSeek API.
        url = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek endpoint
        headers = {
            "Authorization": f"Bearer {deepseek_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",  # Specify the model, adjust this if needed
            "messages": [{"role": "user", "content": prompt}]
        }

        # Make the request to DeepSeek's API
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            bot_response = response.json().get("choices")[0].get("message").get("content")
        else:
            bot_response = "I'm sorry, I couldn't process your request."

        # Display the response from DeepSeek API
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)
