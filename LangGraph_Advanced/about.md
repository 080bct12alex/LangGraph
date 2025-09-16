# Chatbot Development Along with Advanced LangGraph Concepts

## Chatbot Development

A new chatbot is being developed using **LangGraph**, featuring capabilities such as:

- **Standard chatting** like other LLM-based chatbots.
- **Document analysis** to provide accurate answers (RAG).
- Various **tools for executing actions** and a **user interface**.
- **LangSmith integration** to enhance its functionality.

This project aims to create a versatile and interactive chatbot.

---

## Advanced LangGraph Concepts

This section explores advanced LangGraph concepts by implementing the following:

- **Memory**, **Persistence**, and **Check pointers** in the chatbot.
- Adding **Human in the Loop (HITL)** and **fault tolerance**.

while Gradually increasing the chatbot's complexity.

---

# Project Vision

The goal of this project is to build a versatile, intelligent, and interactive chatbot that can grow and adapt based on user needs and evolving technologies. Through continuous development and integration of advanced AI techniques, this chatbot will become more intuitive and capable of handling a wide range of tasks and conversations.

---

# Chatbot Design Workflow

The chatbot design focuses on creating a simple, sequential workflow consisting of a **single node**. Here's how it works:

1. **User messages** are sent to the chat node.
2. A **Large Language Model (LLM)** processes the query and generates a response.
3. The interaction continues in a loop as the user engages.

Understanding the state related to this workflow is essential for successfully building the chatbot.

---

## Chatbot Design Workflow (Detailed)

The workflow is structured around **state management**, which ensures a continuous, coherent conversation. The key components of this process are:

- **Message Types**: The state stores various message types such as:
  - **Human messages**: What the user types.
  - **AI-generated responses**: The chatbot’s replies.
  - **System messages**: Defining roles and states.
  - **Tool messages**: For executing specific actions.

By organizing these messages effectively, developers can ensure a coherent conversational history.

---

## State Management in Chatbot

Maintaining the **conversation state** is crucial for chatbot development. The conversation’s state should capture all exchanged messages between the user and the LLM. This is done by storing them in a **list** within a defined **chat state**. This state will ensure a smooth and continuous conversation flow.

### Reducer Function Implementation

To manage message history efficiently, a **reducer function** is used. The `add messages` function (recommended in LangGraph) is employed instead of typical operators to ensure proper message appending. This is crucial for preserving prior messages, which helps in maintaining a seamless and coherent dialogue with users.

---

## Looping Chatbot Interaction

The chatbot currently operates within a **while loop**, allowing continuous interaction until the user types 'exit', 'quit', or 'bye'. However, the chatbot faces the challenge of **lacking memory**, as it does not recall previous interactions. This is because the `invoke` function resets the conversation state with each loop iteration, leading to the loss of context after every message exchange.

---

## Memory and Persistence

The core issue here is the chatbot being repeatedly invoked in a loop, causing the state to reset each time. To address this:

- **Persistence** will be used to save the state rather than resetting it after each execution.
- The state can be stored in **in-memory RAM** for simplicity, or in a **database** for long-term persistence.
  
For this basic chatbot development, in-memory storage is preferred.

---

## Using Checkpoints

To enhance memory and retain conversation context, **checkpoints** are utilized. Here's the approach:

1. **Import memory saver** from LangGraph.
2. **Create a check pointer object** in the workflow while defining the graph.
3. Each user interaction is treated as a **separate thread**, identified by a **thread ID**.
4. A **config variable** is sent during invocation, allowing the chatbot to remember previous interactions.

This ensures the chatbot can reference past conversations, enhancing user experience.

---

## Final Chatbot Functionality

In its final form, the chatbot will:

- **Capture and retain** conversation history in its state.
- **Reference previous messages** stored in memory for coherent interactions.
- **Access stored state** during user queries for a seamless dialogue.

However, using **RAM** for memory storage means that once the program is restarted, the memory is lost. This underscores the importance of using a **database** for persistent state retention in production environments.

---

## Persistence in Chatbots

To retain conversation context even after an app restart or deletion, **database storage** becomes critical. The chatbot will be designed to store its conversation history persistently, ensuring that user interactions are not lost.



