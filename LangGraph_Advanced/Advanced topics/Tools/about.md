# Introduction to Chatbot
 building an agentic AI, specifically a chatbot.

## Adding New Features

### Action / Tool Capabilities
The chatbot provides accurate responses but currently lacks the ability to perform actions **autonomously**. We need to know how to enable our chatbot to execute specific actions, essentially showcasing its capabilities.

### Tool Integration
 Adding tools to our chatbot, which will enable it to not only engage in normal conversations but also perform specific tasks when requested. There are no limits on the types of tools you can integrate, but since learning, starting with some basic tools.

#### Calculator Tool
New functionalities are being added to our chatbots, including the ability to perform numerical calculations, effectively transforming them into calculator tools.

#### Internet Search Tool
The chatbot currently lacks the capability to perform internet searches. For instance, if one were to inquire about the top news in Nepal, the chatbot would not be able to provide that information.

#### Stock Price Tool
The chatbot will enhance its capabilities by adding an internet search tool for retrieving results and a stock tool to provide stock-related information.

### Added Features
A tool is introduced that retrieves real-time stock prices for companies using a chatbot interface, which can switch between normal chat functionality and task execution using integrated tools. The chatbot can perform searches using DuckDuckGo, calculate results, and retrieve a company's stock price when prompted.

 covering the fundamentals of adding tools in LangGraph 

## Concept in Integrating Tools in LangGraph

### Tool Node Concept
In LangGraph, a **Tool Node** is a critical component that manages the collection of tools integrated into a chatbot system, such as a calculator or search tool. When an action is needed, the chatbot uses the Tool Node to identify the appropriate tool for execution and route the input data accordingly. 

Essentially, the Tool Node acts as an automated bridge, facilitating communication between the chatbot and external tools to execute tasks efficiently.

### Tool Condition Concept
The "tools condition" is a built-in function that determines the direction in which a conversation will proceed—whether it will continue as a normal LLM (Large Language Model) chat or trigger a tool call. It is a pre-built conditional edge function that can inform the flow graph whether to go towards a tool node, an LLM node, or an end node. 

Once the tool node and the tools condition are understood, it becomes easier to understand the integration of tools in LangGraph.

## Code Implementation
Made necessary imports, including pre-built tools from LangChain and the custom tool named 'Calculator'. Three tools are created: DuckDuckGo Search, Calculator, and Get Stock Price, utilizing a free API from Alpha Vantage. A state graph is established with two nodes (Chat node and Tool node) to manage message flow, allowing for both standard interactions and tool-triggered responses as per workflow needs.

## Refining
The current output from the tools node is not user-friendly, as it often presents technical data in JSON format that non-technical users cannot easily understand. 

Additionally, the existing structure does not support multi-step queries, causing issues when combining queries like retrieving Apple's stock price and calculating the cost of purchasing shares. 

To resolve these problems, the structure needs to be modified to allow the tools' output to be sent back to the chat node for better presentation, enabling a more efficient and refined user experience.

## Conclusion 
learned about various tools and their applications in LangGraph. 


