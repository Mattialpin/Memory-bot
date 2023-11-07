import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
#THIS IS THE WORKING VERSION
# Define a function to initialize the session state
@st.cache_data
def initialize_session_state():
    return {"generated": [], "past": [], "input": "", "stored_session": []}

# Initialize the session state
st.session_state = initialize_session_state()

def get_text():
    input_text = st.text_input("You:", st.session_state["input"])
    st.session_state["input"] = input_text  # Update the input value in the session state
    return input_text

st.title("Bot 🤖")

api = st.sidebar.text_input("API-KEY", 
                placeholder="Paste your OpenAI API key here (sk-...)",
                type="password")

MODEL = st.sidebar.selectbox(label='Model', options=['gpt-3.5-turbo', 'text-davinci-003', 'text-davinci-002', 'code-davinci-002'])

if api:
    llm = OpenAI(temperature=0, openai_api_key=api, model_name=MODEL, verbose=False)

    entity_memory_key = 'entity_memory'  # Use a separate key for entity_memory
    if entity_memory_key not in st.session_state:
        st.session_state[entity_memory_key] = ConversationEntityMemory(llm=llm, k=10)

    Conversation = ConversationChain(llm=llm, prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE, memory=st.session_state[entity_memory_key])
else:
    st.error("No API found")

user_input = get_text()

if user_input:
    output = Conversation.run(input=user_input)
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(output)

with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        st.info(st.session_state["past"][i], icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")
