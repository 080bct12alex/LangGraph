##  Improvement Made:

-  Implement a memory feature i.e short-term memory to store key information (like user name) and recall it as needed throughout the conversation.  
    
       Implementing Persistence in Langgraph
 
 we can use **Langgraph's Persistence** feature to retain context across multiple invocations. Persistence allows the chatbot to remember information from previous states and conversations
here 
- Instead of invoking the chatbot afresh in every loop, you can set up persistence to **carry forward the context** (i.e., store information such as user name) throughout the chat.
- Langgraph's persistence mechanism will ensure that the state is **not cleared** after each loop, but rather **retained** for the entire conversation.
- Ensuring that important details, like the user's name, are available throughout the session.

- The principle behind persistence is that when your execution reaches its end, you do not erase the things stored in your state. Instead you store it somewhere. Now you have multiple options for storing. 
The first option is that you store it in a database. So that you can bring it back anytime in the future.
And the second is that you store it in your memory as in RAM. 

     But since we are currently building a basic level chatbot, we will store our state in memory. 


# Step-by-Step : Implementing Persistence in Chatbot

## 1. **Problem**
- the chatbot doesn't remember the previous interactions (e.g., the user's name). This happens because each time the chatbot is invoked, the state is reset. To solve this, we will use **persistence** to retain the conversation history, allowing the chatbot to remember previous interactions.

- Example: If the user says "Hi, my name is Alex", and then asks, "Can you tell me my name?", the chatbot does not recall that the user's name is Alex.

## 2. **Solution: Using Langgraph's Persistence**

### 2.1. **Creating the Workflow with Persistence**

- **Step 1: Import the Necessary Modules**
  First,  import the required modules for persistence.
   For example, Langgraph’s `memory_saver` class.
  
  ```python
  from langgraph.checkpoint.memory import MemorySaver


 **Step 2: Define a Check Pointer**

When creating the workflow, you need to define a check pointer. The check pointer is an object of the `MemorySaver` class, which will manage the state.

```python
checkpointer = MemorySaver()
```



**Step 3: Compile the Graph with the Check Pointer**

While compiling your graph, you must define that your graph will use this check pointer. This ensures the graph will have a persistent memory across interactions.

```python
chatbot = graph.compile(checkpointer=checkpointer)

```


### 3.2. Understanding the Thread Concept

A thread represents an individual user’s interaction with the chatbot. The chatbot can handle multiple users simultaneously, and each interaction is considered a separate thread.

### Step 4: Define a Thread for Each User

Define a thread ID for each user so that the chatbot can track their individual conversation.

```python
thread_id = generate_thread_id(user="Alex")

```
or simply
```python
thread_id = '1'

```


### Step 5: Define the Config Variable

When invoking the chatbot, you need to pass a config variable to keep track of the thread. The config variable will be a dictionary that includes the thread ID.

```python
config = {
    "configurable": {
        "thread_id": thread_id
    }
}
```

### Step 6: Pass the Config While Invoking the Chatbot

Now, when you invoke the chatbot, pass the `config` variable alongside the user message. This ensures that the chatbot remembers the context and previous interactions for that specific thread.

```python
chatbot_response(user_input="Hi, my name is Alex", config=config)
```

### Step 7: Storing the State in RAM

When the chatbot receives a message, it stores the state in RAM. This allows the chatbot to retain all the previous messages and interactions within the same session/user.

```python
state = chatbot.get_state(config=config)
```


### Step 8: Access the State for Future Interactions

When the user asks for information related to previous interactions (e.g., "What is my name?"), the chatbot will fetch the previous state from RAM and continue the conversation without losing context.

```python
chatbot_response(user_input="What is my name?", config=config)
```



### Step 9: Use RAM or Database for State Storage

By default, Langgraph stores the state in RAM. However, if you restart the program or clear the memory, the state will be lost.

#### In Production:
You should use a database (e.g., SQLite, MongoDB) to store the state persistently across sessions. This ensures that users can resume their conversations even after restarting the application.

```python
persistent_memory = DatabaseMemory(storage_path="path_to_db")

```
Using a database ensures that user data and interactions are preserved across sessions and restarts.



## 3.7. How Persistence Works Behind the Scenes

### Initial Interaction:
The first time the user interacts (e.g., "Hi, my name is Alex"), the system stores the interaction in the state. The state will contain information like:

```json
{
    "user_input": "Hi, my name is Alex",
    "response": "Hello Alex, how can I assist you?"

}

Final State:

At the end of each session, the chatbot saves the state in memory (RAM or database). When the workflow ends, the state is saved and can be reloaded during the next session.

Using a database ensures that user data and interactions are preserved across sessions and restarts.




```




### 4. Key Concepts Recap

- **Check Pointer**: An object of the `MemorySaver` class that manages the chatbot’s memory. It keeps track of the conversation state across interactions.
- **Thread**: Each user’s unique interaction with the chatbot. It helps the chatbot handle multiple users independently.
- **Config Variable**: A dictionary that includes the thread ID. It ensures the chatbot associates each message with a specific user.
- **State Storage**: Conversation history can be stored in RAM (default) or a database (recommended for production). This ensures the chatbot remembers past interactions.
- **Persistence**: Ensures that the chatbot can maintain context across sessions. This is essential for continuous and context-aware conversations.



### 5. Conclusion

By using Langgraph’s persistence and check pointer, you can ensure that your chatbot remembers previous interactions, allowing for a continuous, context-aware conversation. 






## Future Improvements:






