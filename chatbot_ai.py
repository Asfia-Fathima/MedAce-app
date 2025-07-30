import streamlit as st
from groq import Groq

def run_chatbot_ui():
    st.subheader("💬 Health Assistant")

    with st.expander("ℹ Disclaimer"):
        st.caption(
            """We appreciate your engagement! This AI assistant is designed to provide
            information on healthcare-related topics like any disease or virus, its symptoms, and preventive measures. 
            It should not replace professional medical advice, diagnosis, or treatment."""
        )

    system_prompt = """You are a doctor with 10 years of experience in solving patients' diseases and curing them.
    Your role is to provide accurate, up-to-date, and helpful information on healthcare topics, and only healthcare topics.
    If a query is unrelated to health, reply with: "Sorry, I'm an AI health assistant and can help you with any query related to healthcare." 
    Do not provide programming help or hallucinate answers.
    """

    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

    if "groq_model" not in st.session_state:
        st.session_state["groq_model"] = "gemma2-9b-it"

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    # Inject report context into conversation (FIXED INDENTATION)
    if "report_text" in st.session_state:
        report_summary = f"The user has uploaded a medical report with the following extracted content:\n\n{st.session_state['report_text'][:1500]}..."
        st.session_state.messages.append({"role": "user", "content": report_summary})
        del st.session_state["report_text"]

    # Display chat history (skip 'system' role)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What health-related question do you have?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                stream = client.chat.completions.create(
                    model=st.session_state["groq_model"],
                    messages=st.session_state.messages,
                    temperature=0.1,
                    stream=True,
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

            except Exception as e:
                st.error("An error occurred while processing your request.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Sorry, something went wrong. Please try again later."
                })
