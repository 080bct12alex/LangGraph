# LangGraph Core Concepts | Agentic AI using LangGraph 

This discusses the foundational concepts of LangGraph, focusing on its ability to orchestrate LLM workflows through detailed graph representation. It explains how to manage LLM workflows using techniques like prompt chaining, routing, parallel execution, and more. 

This repo covers:
- ✅ key building blocks of LangGraph.
- how to **design and manage LLM workflows** using concepts like:
    - Prompt chaining  
    - Routing  
    - Parallel execution  
    - Graph-based orchestration  
- ✅ How LangGraph structures workflows with nodes and edges  
- ✅ How state, reducers, and orchestrators work together  
- ✅ The full execution model that powers agentic AI systems  

---



## 📌 Overview

-   🔀 [Introduction to LangGraph](#introduction-to-langgraph)  
    Understand what LangGraph is , focusing on orchestration of complex, adaptive LLM workflows.
    
-   📊 [Core Concepts of LangGraph](#core-concepts-of-langgraph)  
    Learn how LangGraph models workflows as graphs with nodes and edges to define dynamic control flow and task execution.
    
-   🧱[Understanding LLM Workflows](#understanding-llm-workflows)

  
    Explore the typical structure of LLM-based workflows involving prompting, reasoning, tool use, and decision-making.
    
-   🔁 [Common LLM Workflow Patterns](#common-llm-workflow-patterns)  
    A breakdown of 5 powerful patterns in LangGraph:
    
    -   Prompt Chaining – chaining sequential tasks
        
    -   Routing – branching based on LLM decisions
        
    -   Parallelization – running tasks in parallel
        
    -   Orchestrator-Worker – central controller and agents
        
    -   Evaluator-Optimizer – feedback loops for refinement
        
-   🧠 [State Management in LangGraph](#state-management-in-langgraph)  
    Understand LangGraph’s evolving shared memory model that holds workflow data and ensures context continuity.
    
-   🛠️ [Reducers for State Updates](#reducers-for-state-updates)  
    Learn how reducers update state during execution—by replacing, adding, or merging values efficiently.
    
-   ⚙️ [Execution Model of LangGraph](#execution-model-of-langgraph)  
    A peek under the hood: how LangGraph executes workflows via message-passing, looping, and edge-triggered logic.
---

## Introduction to LangGraph

> LangGraph: An Orchestration Framework for LLM Workflows

Lang Graph is an orchestration framework that transforms an LLM workflow into a graph, 
designed for building intelligent, stateful, and multi-step LLM workflows. 

It represents an LLM workflow as a graph, where each node represents a specific task within the workflow and edges define the execution order between these tasks.
It allows for the execution of tasks sequentially or in parallel.

LangGraph offers features such as parallel execution, loops, branching based on conditions, memory, and resumability, making it suitable for developing agentic and production-grade AI applications. 

---
---

## Core Concepts of LangGraph

LangGraph models workflows as graphs where:

- **Nodes** = tasks (prompting, logic, tools)
- **Edges** = flow between tasks
- Workflows are adaptive, stateful, and resumable

This model enables structured reasoning, flexible execution paths, and supports real-world agentic behaviors.

---


## Understanding LLM Workflows

A workflow is defined as a series of tasks executed in a specific order to achieve a goal. 
An LLM workflow is a workflow where multiple tasks within the series depend on or utilize Large Language Models (LLMs) to achieve specific goals, such as automated hiring, where multiple steps like writing job descriptions and conducting interviews are involved.

These workflows are step-by-step processes for building complex LLM applications, with each step performing tasks like prompting, reasoning, tool calling, memory access, or decision-making. 
LLM workflows can exhibit various structures, including linear, parallel, branched, and looped patterns, and can support advanced behaviors like multi-agent communication. 

Overall, the structure of these workflows varies by application, emphasizing the need for tailored execution in different contexts.

Here is a mind map illustrating common LLM workflows:

![LLM Workflows](https://i.ibb.co/p6x28T7s/Chat-GPT-Image-Jul-18-2025-01-16-39-PM.png)

---

## Common LLM Workflow Patterns

Different workflows vary, but some common ones appear frequently across various contexts. Here are 5 common LLM orchestration patterns:

| Pattern                 | Description                                                                |
| ----------------------- | -------------------------------------------------------------------------- |
| **Prompt Chaining**     | Sequential LLM calls where each step refines or builds on previous output. |
| **Routing**             | LLM decides which tool or path to take based on input type.                |
| **Parallelization**     | Independent sub-tasks run concurrently for faster output.                  |
| **Orchestrator-Worker** | One LLM dynamically delegates tasks to others based on context.            |
| **Evaluator-Optimizer** | Generator-Evaluator loop to refine outputs over multiple iterations.       |


![LLM Workflows](https://i.ibb.co/p6x28T7s/Chat-GPT-Image-Jul-18-2025-01-16-39-PM.png)

**Prompt Chaining:** Involves sequential calls to an LLM, breaking down complex tasks into smaller sub-tasks and allowing for checks on intermediate outputs.  
Tasks are broken down into sub-tasks using process called chaining. For instance, when generating a detailed report from a given topic, the first LLM creates an outline, which is then used by a second LLM to produce the report. This method allows for checkpoints to ensure the output meets specific criteria, such as word count limits.

**Routing:** An LLM acts as a decision-maker, directing a task to the most appropriate LLM or tool based on the input query. This decision-making process is essential for efficient workflow design.

**Parallelization:** A task is divided into multiple subtasks (sub task predefined for LLMs) that can be executed concurrently / simultaneously in parallel, enhancing efficiency with their results merged to produce a final outcome. This approach allows for quicker results by enabling simultaneous evaluations without needing prior knowledge from one check to inform the others.

**Orchestrator Worker:** Similar to parallelization, it involves dividing one task into multiple parallel subtasks but the specific nature of these parallel subtasks is dynamically determined by an orchestrator LLM based on the input query. For example, an orchestrator LLM analyzes the query and assigns tasks to various LLM workers depending on the context. (sub task dynamically assigned for LLMs)

**Evaluator Optimizer:** An iterative workflow for tasks requiring refinement like drafting emails or writing blogs (recognizing that perfection often requires multiple attempts), involving two language models (LLMs) — a Generator LLM that produces a solution and an Evaluator LLM that provides feedback for subsequent iterations until the solution meets criteria.

---

## Graph Structure

### Nodes and Edges

The concept of graphs, vertices, and edges is central to Lang Graph, which serves as an orchestrator framework for LLM workflows.
This structure simplifies the representation of complex workflows, allowing for easy execution and iteration based on user feedback.

LangGraph converts any LLM workflow into a graph structure consisting of nodes (vertices) and edges.  
Each node within a LangGraph represents a single task in the workflow and is typically implemented as a Python function.  
Edges define the flow of execution, indicating which node will be executed next after a particular node completes its task.  
Edges can represent different types of flow: sequential, parallel, conditional (branching), or looped execution.  

Here is a flowchart visualizing an essay evaluation workflow:

**Essay Evaluation Workflow**

![Essay Evaluation Workflow](https://i.ibb.co/fYQXrkvN/UPSC-Essay-Evaluation-Workflow.png)

Using the example of an essay evaluation website, the workflow is expressed as a graph where each node represents a task and edges dictate execution flow, including types like sequential, parallel, and conditional edges.

---

## State Management in LangGraph

In the context of LLM workflows, the state is crucial.  
The state in LangGraph is a shared, mutable memory that flows through the workflow, holding all data passed between nodes during execution.

This shared memory, accessible and mutable by all nodes within the LangGraph, drives the workflow's progress and allows for real-time updates as information changes.

It contains evolving data points necessary for execution, the logical progression of the workflow, such as essay text or calculated scores.  
Every node in the graph has access to the entire state, receives it as input, performs partial updates, and then passes the modified state to the next node.

In code, the state is typically implemented as a special Python dictionary called a typed dictionary or a Pydantic object. 

---

## Reducers for State Updates

Reducers in LangGraph define how updates from nodes are applied to the shared state, determining whether new data replaces, adds to, or merges with existing values.  
Each key within the state can have its own specific reducer.  
Reducers are crucial in scenarios where the default "replace" update policy is undesirable, such as in a chatbot where all messages should be appended to maintain conversation history rather than overwriting previous ones.  
For example, in a workflow, summing two numbers and keeping the results mutable can lead to updated values being lost, as seen in a chatbot scenario where previous messages are overwritten. To avoid this, reducers ensure that updates can be handled in various ways, preserving necessary data for accurate historical reference.

They are particularly useful when creating parallel workflows. 

---

## Execution Model of LangGraph

LangGraph's execution model is inspired by Google Pregel, a system for large-scale graph processing that processes workflows.

The workflow execution involves several phases:

**Graph Definition:** Involves defining the nodes, edges, and the initial state of the workflow. 

**Compilation:** Checks the graph structure for logical correctness and consistency, ensuring no orphan nodes or structural issues exist. 

**Execution Phase:**

- **Invocation:** The initial state is passed to the first node, activating it and triggering its associated Python function. 
- **Message Passing:** After a node performs its work and makes partial updates to the state, the updated state is automatically passed to the next node via edges, activating it. This process occurs in rounds. 
- **Superstep:** A "round" of execution in LangGraph, which can involve one or more steps, including multiple nodes executing in parallel. 

The workflow execution automatically stops when there are no active nodes and no messages being passed across edges. 

The system handles the calling and state passing between nodes internally, abstracting this complexity from the developer. 

**In short:**

**Execution Model**  
LangGraph's execution model, inspired by Google's Pregel, processes workflows by defining graphs with nodes and edges, followed by a compilation step to ensure logical consistency. Once compiled, the process is executed in rounds known as 'supersteps', where each node processes the state and updates it through message passing. The execution concludes when no active nodes remain and no messages are being transmitted.
