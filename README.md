# agent_memory

This project is a multi-agent system with a supervisor agent that manages smaller agents.

Instead of giving every agent the full memory, each agent only gets the memory related to its task. The supervisor handles memory retrieval, tool usage, and tracking what agents are doing.

## Features

- Spawns sub-agents for tasks
- Retrieves related memory from a vector database
- Stores long-term memory
- Tracks agent activity and status
- Shared workspace between agents
- Web search support
- Saves completed task results back into memory

## Classes

### AgentRegistry

Keeps track of active agents.

Methods:
- `register(agent)` → adds an agent
- `remove(agent_id)` → removes an agent
- `get_status(agent_id)` → gets agent info

---

### AgentState

Tracks what an agent is currently doing.

States:
- idle
- thinking
- searching
- blocked
- complete
- failed

Methods update the current state values.

---

### SharedWorkspace

A shared space where agents store:
- notes
- findings
- completed tasks

---

### retrieve_relevant_memory(query)

Searches the vector database for memory related to the current task.

Returns relevant stored context.

---

### WebSearchTool

Handles web searches using DuckDuckGo.

Method:
- `search(query)` → returns search results

---

### agent

Base agent class.

Stores:
- name
- role
- memory
- memory limit
- unique id

Methods:
- `add_memory()`
- `get_role()`

---

### llm_agent

LLM-based agent class.

Method:
- `generate_response()` → generates responses or tool calls

---

### supervisor_agent

Main controller of the system.

The supervisor:
- manages sub-agents
- retrieves memory
- routes tool calls
- stores findings
- updates the shared workspace
- saves synthesized knowledge

Methods:
- `call_llm()`->  sends tasks to the LLM
- `tool_router()`-> handles tools
- `synthesize()` ->  summarizes results
- `save_to_memory()`->  stores information
- `run()` -> runs the full task pipeline

## Stack

- Python
- ChromaDB
- SentenceTransformers
- Supermemory
- Llama API
- DuckDuckGo Search
