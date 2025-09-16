from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# Create table for thread names if it doesn't already exist
conn.execute('''
CREATE TABLE IF NOT EXISTS thread_names (
    thread_id TEXT PRIMARY KEY,
    name TEXT NOT NULL
)
''')
conn.commit()

# Retrieve all threads along with their names
def retrieve_all_threads():
    all_threads = set()
    thread_names = {}

    for checkpoint in checkpointer.list(None):
        thread_id = checkpoint.config['configurable']['thread_id']
        all_threads.add(thread_id)

        # Get the name of the thread from the database
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM thread_names WHERE thread_id = ?", (str(thread_id),))
        row = cursor.fetchone()

        if row:
            thread_names[str(thread_id)] = row[0]
        else:
            thread_names[str(thread_id)] = 'Unnamed Conversation'

    return list(all_threads), thread_names

# Store a conversation name
def store_conversation_name(thread_id, name):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO thread_names (thread_id, name) VALUES (?, ?)
    ''', (str(thread_id), name))
    conn.commit()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)
