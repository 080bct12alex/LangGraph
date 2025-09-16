# Chatbot Development - Database Integration

## **Current Problem: Memory Savers**
The Current memory savers for short-term memory only store conversations in **RAM**, ause past conversations to disappear when the application is closed or the page is reloaded.
This limitation leads to the loss of chat data and hinders users from revisiting past discussions.

Solution using changing these memory savers in favor of a database integration, allowing for persistent storage of conversations. This change will enable users to revisit their chats even days later, resuming discussions from where they left off.
## ** Solution: Database Integration**
Solution using changing these memory savers in favor of a database integration, allowing for **persistent database storage** of conversations.
This change will allow conversations to be stored in a database, ensuring  users to revisit  their chats even days later and continue their chats even after days or weeks , resuming discussions from where they left off.

The integration of a **database** ensures that chat threads remain intact even after the program is closed or the website is reopened. This feature significantly enhances user experience by enabling users to easily access their past conversations at any time.

---

## **Step-by-Step Process**
 requires modifications to both the backend and frontend of the project.

### **Backend Changes**

A new file called **`Langgraph Database Backend.py`** will be created to incorporate the necessary backend changes for this integration.

#### 1. **SQLite Check Pointer**
  
-First  **Install Langraph Check Point SQLite Library**: Replace the in-memory saver with **SQLite**, as a more suitable option for learning ; can change to SQL later for production
  
- **Create SQLite Database**: 
  - Name the database **`chatbot.db`** in  project directory while ensuring the **`check_same_thread`** parameter is set to **`false`** to enable multi-threaded access, as SQLite by default supports single-threaded access.

- **Establish Connection**: Finally, Set up a connection object to interface  the SQLite server with  checkpoint, ensuring that all incoming chat data can be stored in the database efficiently.

#### 2. **Visualizing the Database**

Once the backend is set up, the **Chatbot DB** will store all the conversations. To visualize the stored messages across multiple threads:

- Install the **Sequelite Viewer extension** in **VS Code**.
- The extension provides a clear and organized view of all stored chat threads, checkpoints, and interactions.

Each execution generates multiple checkpoints, reflecting interactions within the same threads, providing a clear view of conversational history. By installing the extension, users can enhance their understanding of how checkpoints accumulate and visualize their database effectively. This allows users to see how conversations evolve over time 


---

### **Frontend Adjustments**

For the frontend, the main modification involves initializing the chat threads with data retrieved from the backend.

#### 1. **Initialization of Chat Threads**

Instead of starting with an empty list of threads, the chatbot will now query the database for **existing threads**. 

- **Backend Query**: Fetch the existing threads from the database.
- **Frontend Display**: Display all threads — both previously existing ones and newly created threads within the same session — ensuring users can continue from where they left off.

This adjustment guarantees continuity in conversations, making it seamless for users to resume chats at any point.

In short : To update the chatbot's front end, in code upto resume; where only a single line of code needs modification to initialize chat threads. Instead of starting with an empty list, the chatbot will now query the backend for existing threads in the database. This adjustment allows for continuity in conversations, displaying previously existing threads along with any new ones created during the session.

---

## **Conclusion**

The **database integration** introduces persistent storage to the chatbot, enabling the retention of past conversations. By combining both backend and frontend changes, this approach ensures that chat history is always available to users, even after refreshing the page or closing the program. The implementation of this feature is a significant improvement to the overall user experience.



##  Improvements  Needed

### **Logical Conversation Names**
Give a **logical names** to the conversation on the UI rather than displaying these thread  IDs as it happens in ChatGPT.
This will enhance the user experience and make conversations easier to identify.

### **Goal**
The ultimate goal is to develop a **feature-rich chatbot** based on this improvement, including tools and specific features such as:
- **MCP**
- **RAG (Retrieval-Augmented Generation)** 

