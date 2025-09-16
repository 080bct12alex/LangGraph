# Chatbot Overview
After the addition of a **streaming feature** to the chatbot, making the chatbot interactions more engaging.


## Resume Chat Feature
Now, enhancing the chatbot by incorporating a **Resume Chat** feature, similar to the one found in ChatGPT. This addition aims to improve user experience by allowing seamless interaction with past conversations.

---

## Development Steps

### 1. **Chatbot UI Design**
A new feature is being developed that allows users to either **start a fresh conversation** or **resume an existing one**. 
The code for the feature is divided into manageable tasks, focusing first on modifying the user interface by adding a **sidebar** for managing conversations. This implementation builds on existing code without requiring backend changes, streamlining the development process.


### 2. **Dynamic Thread ID Generation**
To enhance functionality, **unique thread IDs** are programmatically generated for new conversations using Python's `UUID` library. A utility function will be created to generate a random thread ID, which will be stored in the session state if it hasn't already been set. This update ensures that the chatbot can handle multiple threads without manual ID input.


### 3. **Message History Management**
Thread IDs for new conversations are generated automatically and displayed in the sidebar for user reference. When the "New Chat" button is clicked:
- Existing conversation history is cleared.
- A new thread ID is generated and stored.
- The UI resets for a fresh discussion.

However, during testing, it was found that while loading new conversations works, **previous conversations** and their **thread IDs** are lost / disappearing, indicating a need for further adjustments.


### 4. **Retaining Thread IDs**
To resolve the issue of losing previous thread IDs when starting a new chat, a **list** is created within the session to store all thread IDs. A utility function called `addThread` ensures that every time a new chat is created or the page is loaded, the current thread ID is added to this list.This change allows all previous thread IDs to be displayed in the sidebar, enabling users to resume conversations effortlessly / easily .


### 5. **Loading Previous Conversations**
The task is to enable the loading of previous conversations when a user clicks on a specific thread button. This is achieved by:
- Extracting the thread ID.
- Invoking the backend to retrieve associated messages.
- Formatting them to match the current message history structure.

Ultimately, incorporating this functionality allows users to switch between different conversation threads seamlessly , 
with the added challenge of displaying the **most recent threads at the top** ;Solved using reversing the list.

---

## Problem
Up to now, we have used **memory savers**  for persistence. And this is a checkpoint which stores all the messages from all the threads in the **RAM**. So when we are refreshing the program, our program is being terminated ; running out  (clear) of RAM. So all the associated memory is also getting exhausted, i.e., as I refresh this chatbot, all our old conversations are gone and cannot be accessed again.
causing past conversations to be lost. 

---

##  Solution

### **Database Integration**
To prevent loss of past conversations upon program refresh,  connect the **Lang Graph backend** to a **database**, ensuring  previous messages are retained, This means even when you refresh, your past conversations will not be lost.

---

##  Improvements  Needed

### **Logical Conversation Names**
Give a **logical names** to the conversation on the UI rather than displaying these thread  IDs as it happens in ChatGPT.
This will enhance the user experience and make conversations easier to identify.

### **Goal**
The ultimate goal is to develop a **feature-rich chatbot** based on this improvement, including tools and specific features such as:
- **MCP**
- **RAG (Retrieval-Augmented Generation)** 


