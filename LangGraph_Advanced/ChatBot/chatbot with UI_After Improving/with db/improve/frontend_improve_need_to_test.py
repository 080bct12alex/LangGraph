import streamlit as st
from langgraph_database_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

# **************************************** utility functions *************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

    # Automatically generate a sequential name
    conversation_count = len(st.session_state['chat_threads']) + 1
    st.session_state['thread_names'][str(thread_id)] = f'Conversation {conversation_count}'

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

def update_thread_name(thread_id, new_name):
    # Check for name conflicts in session
    if new_name in st.session_state['thread_names'].values():
        st.session_state['error_message'] = f"The name '{new_name}' already exists. Please choose a different name."
        return
    st.session_state['error_message'] = None  # Reset error message
    st.session_state['thread_names'][str(thread_id)] = new_name
    store_conversation_name(thread_id, new_name)

# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state or 'thread_names' not in st.session_state:
    st.session_state['chat_threads'], st.session_state['thread_names'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# **************************************** Sidebar UI *********************************
st.sidebar.title('LangGraph Chatbot')

# New chat button
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

# Add search filter for conversations
search_query = st.sidebar.text_input("Search Conversations", "")

# Update the filtered conversations when the search query is updated
filtered_threads = [thread_id for thread_id in st.session_state['chat_threads']
                    if search_query.lower() in st.session_state['thread_names'].get(str(thread_id), '').lower()]

for thread_id in filtered_threads[::-1]:
    thread_name = st.session_state['thread_names'].get(str(thread_id), 'Unnamed Conversation')

    with st.expander(f"{thread_name}"):
        # Allow renaming the conversation directly inside the expander
        new_name = st.text_input(f"Rename {thread_name}", value=thread_name, key=f"rename_{thread_id}")
        
        if new_name and new_name != thread_name:
            update_thread_name(thread_id, new_name)
            
            if st.session_state.get('error_message'):
                st.warning(st.session_state['error_message'])
            else:
                store_conversation_name(thread_id, new_name)
                st.success(f"Conversation renamed to '{new_name}'")

        # Button to select and load this conversation
        if st.button(f"Go to {thread_name}", key=f"goto_{thread_id}"):
            st.session_state['thread_id'] = thread_id
            messages = load_conversation(thread_id)

            temp_messages = []
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    role = 'user'
                else:
                    role = 'assistant'
                temp_messages.append({'role': role, 'content': msg.content})

            st.session_state['message_history'] = temp_messages

# **************************************** Main UI ************************************

# Loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
