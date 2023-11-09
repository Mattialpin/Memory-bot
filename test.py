import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
#THIS IS THE WORKING VERSION: DO NOT TOUCH
#  

# Define a function to initialize the session state
@st.cache_data
def initialize_session_state():
    return {"generated": [], "past": [], "input": "", "stored_session": []}

# Initialize the session state
st.session_state = initialize_session_state()

# Function to get user input text from a text input field
def get_text():
    input_text = st.text_input("You:", st.session_state["input"])
    st.session_state["input"] = input_text  # Update the input value in the session state
    return input_text

st.title(" TechnoAlpin Bot 🤖")
# Create a text input field in the sidebar for the OpenAI API key
api = st.sidebar.text_input("API-KEY", 
                placeholder="Paste your OpenAI API key here (sk-...)",
                type="password")

MODEL = st.sidebar.selectbox(label='Model', options=['gpt-3.5-turbo', 'text-davinci-003', 'text-davinci-002', 'code-davinci-002'])
# Check if an API key is provided
if api:
     # Initialize the OpenAI language model with the provided API key and selected model
    llm = OpenAI(temperature=0, openai_api_key=api, model_name=MODEL, verbose=False)

    entity_memory_key = 'entity_memory'  # Use a separate key for entity_memory
    # If entity_memory is not in the session state, initialize it
    if entity_memory_key not in st.session_state:
        st.session_state[entity_memory_key] = ConversationEntityMemory(llm=llm, k=10)

    Conversation = ConversationChain(llm=llm, prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE, memory=st.session_state[entity_memory_key])
else:
    st.error("No API found")
# Get user input text from the text input field
user_input = get_text()

if user_input:
    output = Conversation.run(input=user_input)
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(output)
# Display a conversation expander to show the user's input and the generated response
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        st.info(st.session_state["past"][i], icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")