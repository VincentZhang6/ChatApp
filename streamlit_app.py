import streamlit as st
import random
import time
from openai import OpenAI

def response_generator():
    default_response = "Sorry, Vincent didn't pay for OpenAI API to make me a real cool chatbot, so I'll just spew random stuff"
    response = random.choice(
        [
            "Hi there, how can i help?",
            "Rock n roll!",
            "You wanna a piece of me boy?",
            "Whatever",
            "Ask Vincent to pay for OpenAI API so I can talk like a real person!"
        ]
    ) if st.session_state.counter > 0 else default_response

    for word in response.split():
        yield word + " "
        time.sleep(0.05)
    st.session_state.counter += 1
    print(st.session_state.counter)

st.title("Chat Bot Example")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])
# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set counter
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Display chat messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["chat_history"])

if user_prompt := st.chat_input("Say something here"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_prompt)
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "chat_history": user_prompt
    })

    # bot_response = "Echoing: {}".format(user_prompt)
    # Display bot response in chat message container
    with st.chat_message("assistant"):
        # st.markdown(bot_response)
        bot_response = st.write_stream(response_generator())
        # stream = client.chat.completions.create(
        #     model = st.session_state["openai_model"],
        #     messages=[
        #         {"role": m["role"], "chat_history": m["chat_history"]} for m in st.session_state.messages
        #     ],
        #     stream = True
        # )
        # bot_response = st.write_stream(stream)
    # Add assitant response to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "chat_history": bot_response
    })