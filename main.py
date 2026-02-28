import streamlit as st
from google import genai
st.title("Simple Chatbot UI")

with st.sidebar:
    st.text_input("Enter Gemini API Key", type="password", key="api_key")
    # 2. Model Selection Selectbox
    model_options = {
        "Gemini 2.5 Flash":"gemini-2.5-flash",
        "Gemini 2.0 Flash (Fastest)": "gemini-2.0-flash",
        "Gemini 1.5 Flash": "gemini-1.5-flash",
        "Gemini 1.5 Pro (Most Capable)": "gemini-1.5-pro"
    }    
    st.selectbox("Choose Model", options=list(model_options.keys()), index=0, key="selected_model")

print("api_key: "+st.session_state.api_key)
if st.session_state.api_key:

    client = genai.Client(api_key=st.session_state.api_key)
    
    # 1. Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


    # 2. Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. React to user input
    if prompt := st.chat_input("Ask Gemini Anything"):
        print("chat message:" +prompt)
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 4. Generate assistant response
        with st.spinner("Gemini is thinking..."):
            response = client.models.generate_content(model=model_options.get(st.session_state.selected_model),contents=prompt, config={"system_instruction":"You are a helpful language assistant, to undestand and translate between languages"}) # Replace this with your AI model logic
        
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response.text)
            
            # Add assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": response.text})