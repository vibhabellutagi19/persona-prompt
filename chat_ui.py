import streamlit as st
import requests
import time

st.set_page_config(page_title="🧠 Chat with Hitesh.ai", layout="centered")

st.markdown("""
<style>
.chat-bubble-user {
    background-color: #96c2dd;
    padding: 0.6em 1em;
    border-radius: 1em;
    margin-bottom: 0.5em;
    max-width: 80%;
    align-self: flex-end;
    color: black;
}
.chat-bubble-assistant {
    background-color: #c9dcee;
    padding: 0.6em 1em;
    border-radius: 1em;
    margin-bottom: 0.5em;
    max-width: 80%;
    align-self: flex-start;
    color: black;
}
.chat-area {
    display: flex;
    flex-direction: column;
}
.typing {
    font-style: italic;
    opacity: 0.7;
    animation: blink 1s steps(1) infinite;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Chat with Hitesh.ai")

query = st.text_input("💬 Ask something...", placeholder="e.g., How does a rocket work?")

chat_container = st.container()

# Handle query
if query:
    with chat_container:
        st.markdown(f'<div class="chat-bubble-user">🧑‍💻 <strong>You:</strong> {query}</div>', unsafe_allow_html=True)

        response_placeholder = st.empty()
        loader_placeholder = st.empty()

        loader_placeholder.markdown(
            '<span class="typing">🤖 Thinking...</span>',
            unsafe_allow_html=True
        )

        streamed_response = ""
        try:
            with requests.get("http://localhost:8000/chat/with_hc", params={"query": query}, stream=True) as r:
                r.raise_for_status()

                first_line_displayed = False
                for chunk in r.iter_lines():
                    if chunk:
                        line = chunk.decode("utf-8").strip()
                        streamed_response += line + "\n"

                        if not first_line_displayed:
                            loader_placeholder.empty()
                            response_placeholder.markdown(
                                f'<div class="chat-bubble-assistant"> <span id="typed"></span></div>',
                                unsafe_allow_html=True
                            )
                            first_line_displayed = True

                        response_placeholder.markdown(
                            f'<div class="chat-bubble-assistant"> {streamed_response.replace("\n", "<br>")}</div>',
                            unsafe_allow_html=True
                        )
                        time.sleep(0.04)

        except Exception as e:
            loader_placeholder.empty()
            response_placeholder.error(f"⚠️ Error: {e}")