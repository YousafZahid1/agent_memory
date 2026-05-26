# import from vector_build for class SharedWorkspace:



#Backend have the data more secvure in a database
# 
# 
"""



The project is spawn agents with relative memory when working on a issue or something
and the second thing is have  supervisor agent with agent control panel where the supervisor is able to to see other agents!!

This is the project

"""
from functools import lru_cache
import json
import uuid
import os
from dotenv import load_dotenv
from llama_api_client import LlamaAPIClient
from supermemory import Supermemory

load_dotenv()

mem_client = Supermemory(
    api_key=os.environ["SUPERMEMORY_API_KEY"]
)
USER_ID = "yousaf"

conversation = [
    {"role": "assistant", "content": "Hello, how are you doing?"},
    {"role": "user", "content": "Hello! I am Yousaf. I am testing this device. I love to code! and I attend TJHSST"},
    {"role": "user", "content": "Can I go to the hackathon?"},
]

# Get user profile + relevant memories for context
profile = mem_client.profile(container_tag=USER_ID, q=conversation[-1]["content"])

static = "\n".join(profile.profile.static)
dynamic = "\n".join(profile.profile.dynamic)
memories = "\n".join(r.get("memory", "") for r in profile.search_results.results)

context = f"""Static profile:
{static}

Dynamic profile:
{dynamic}

Relevant memories:
{memories}"""







"""
Supermemoery here setting up 

"""






# Before goign to second part would have to create a Agent control pannel for the supervisor which we just created upward!!

# #2nd part create subagents but only give them limited amount of memeory


# 1: Supervisor


# 2: Agent 1
from vector_build import db
from llama_api_client import LlamaAPIClient
from ddgs import DDGS
conversation = [
    {"role": "assistant", "content": "Hello, how are you doing?"},
    {"role": "user", "content": "Hello! I am Yousaf. I am testing this device. I love to code! and I attend TJHSST"},
    {"role": "user", "content": "Can I go to the hackathon?"},
]# be able to add or update memeory!!
#needs to be stored in DB!!!!

# Get user profile + relevant memories for context
profile = mem_client.profile(container_tag=USER_ID, q=conversation[-1]["content"])

static = "\n".join(profile.profile.static)
dynamic = "\n".join(profile.profile.dynamic)
memories = "\n".join(r.get("memory", "") for r in profile.search_results.results)

context = f"""Static profile:
{static}

Dynamic profile:
{dynamic}

Relevant memories:
{memories}"""





##

class AgentRegistry: # for supervisor
    def __init__(self):
        self.agents = {}

    def register(self, agent):
        self.agents[agent.id] = agent

    def remove(self, agent_id):
        del self.agents[agent_id]

    def get_status(self, agent_id):
        return self.agents.get(agent_id)

###

class AgentState: # needs to be exclusive to Supervisor!###
    def __init__(self, state="idle",thinking="",searching="",blocked="",complete="",failed=""):
        self.state = state
        self.thinking = thinking
        self.searching = searching
        self.blocked = blocked
        self.complete = complete
        self.failed = failed
        
    def update_state(self, new_state):
        self.state = new_state
    def update_thinking(self, new_thinking):
        self.thinking = new_thinking
    def update_searching(self, new_searching):
        self.searching = new_searching
    def update_blocked(self, new_blocked):
        self.blocked = new_blocked
    def update_complete(self, new_complete):
        self.complete = new_complete
    def update_failed(self, new_failed):
        self.failed = new_failed
    
##The supervisor uses this to monitor.



class SharedWorkspace:
    def __init__(self):
        self.notes = []
        self.findings = []
        self.completed_tasks = []
        
#memeoery for shared Univerisal memeory part!



def retrieve_relevant_memory(query):
    obj = db(query)
    results = obj.func()
    return results["retrieved_docs"]
        # when an agent calls this takes the query and converts to a vector and matches in the DB with relevant vectors and returns that memeroy

class WebSearchTool:
    def __init__(self, max_results=5):
        self.max_results = max_results

    def search(self, query):
        results_data = []

        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=self.max_results)

                for r in results:
                    results_data.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", "")
                    })

        except Exception as e:
            return f"Web search error: {e}"

        return results_data






class agent:
    def __init__(self,name,role,memory_limit): # role means supervisor vs agent(mini)
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.memory_limit = memory_limit
        self.memory = []
        
    def add_memory(self,content):
        self.memory.append(content[:])
    def get_role(self):
        return "Sub Agent" if self.role=="agent" else "Supervisor Agent"

####

class llm_agent(agent):
    def __init__(self,name,role,memory_limit , context):
        super().__init__(name,role,memory_limit)
        self.llm_client = LlamaAPIClient( api_key=os.environ["LLAMA_API_KEY"], base_url="https://api.llama.com/v1/")
        self.context = context

    def generate_response(self, conversation):

        system_prompt = f"""
You are a {self.get_role()} named {self.name} alongside your memeory {self.context}.

If you need web information, respond ONLY in JSON:

{{
    "tool": "web_search",
    "query": "search query here"
}}

Otherwise respond normally.

Do not fake search results.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            *conversation
        ]

        response = self.llm_client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=messages,
        )

        output = response.completion_message.content.text

        return output





class supervisor_agent(agent):
    def __init__(self, name, role, memory_limit, context):
        super().__init__(name, role, memory_limit)
        self.registry = AgentRegistry()
        self.shared_workspace = SharedWorkspace()
        self.web_tool = WebSearchTool()
        self.state = AgentState()
        self.context = context
        self.role = "Supervisor Agent"

        self.client = LlamaAPIClient(
            api_key=os.environ["LLAMA_API_KEY"],
            base_url="https://api.llama.com/v1/"
        )

        self.system_prompt = f"""
You are a Supervisor Agent.

Respond ONLY in JSON tool calls or final text.

Tool calls:
{{"action":"web_search","query":"..."}}
{{"action":"write_workspace","content":"..."}}
{{"action":"spawn_agent","name":"...","role":"agent"}}

Context:
{self.context}
"""# both tool_r0uter and cll_llm should be ina  while looop until model decides to stop!
    parent_prompt=str()
    while True:

        def call_llm(self, user_input, retrieved_context=None):
            global parent_prompt
            user_message = user_input
            if retrieved_context:
                user_message = f"Relevant context from memory:\n{retrieved_context}\n\nTask:\n{user_input}"

            response = self.client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
            )
            parent_prompt+= f"{user_message}  \t {response.completion_message.content.text}\n"
            return response.completion_message.content.text
        @lru_cache(maxsize=128)
        def tool_router(self, output): #instead of sending llm response to tool router ; DO reason+React ; from one shot execution to iterative loop! then observeration comes in; and gives agents raw data back; once agent has enough info and sotps calling tool and gives final resposne
            try:
                data = json.loads(output)
                action = data.get("action")

                if action == "web_search":
                    search_results = self.web_tool.search(data["query"])
                    self.shared_workspace.findings.append({
                        "type": "web_search",
                        "query": data["query"],
                        "results": search_results
                    })
                    return {"status": "success", "action": "web_search", "results": search_results}

                if action == "write_workspace":
                    self.shared_workspace.notes.append(data["content"])
                    self.shared_workspace.findings.append({
                        "type": "workspace_write",
                        "content": data["content"]
                    })
                    return {"status": "success", "action": "write_workspace", "message": "Note stored"}

                if action == "spawn_agent":
                    a = agent(data["name"], data.get("role", "agent"), 10)
                    self.registry.register(a)
                    self.shared_workspace.findings.append({
                        "type": "agent_spawned",
                        "agent_name": data["name"],
                        "agent_id": a.id
                    })
                    return {"status": "success", "action": "spawn_agent", "agent_id": a.id}

            except json.JSONDecodeError:
                return {"status": "error", "message": "Invalid JSON from LLM", "raw_output": output}
            except Exception as e:
                return {"status": "error", "message": str(e), "raw_output": output}

        parent_prompt+= f"{user_message}  \t {response.completion_message.content.text} \t {tool_router(self, output) }\n"
        response1 = self.client.chat.completions.create(
                        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": f" You have all this information such s the questions longside the response being generted when you think the information is enough say STOP or when tokens are being wasted by the same question again and again say \"stop\" in your response {parent_prompt}"}
                        ],
                    )
        if "stop" in str(response1.completion_message.content.text): break #while loop not "function"


####
    
    def synthesize(self, task, tool_result):
        # Send tool results back to LLM to produce a real answer
        tool_output_text = json.dumps(tool_result, indent=2)
        synthesis_prompt = (
            f"You were given this task: {task}\n\n"
            f"You used a tool and got these results:\n{tool_output_text}\n\n"
            f"Now write a clear, detailed summary of what you learned. "
            f"This will be saved as memory for future tasks."
        )
        response = self.client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[
                {"role": "system", "content": "You are a Supervisor Agent. Summarize findings clearly and in full detail."},
                {"role": "user", "content": synthesis_prompt}
            ],
        )
        return response.completion_message.content.text
    @lru_cache(maxsize=128)
    def save_to_memory(self, task, synthesis):
        from sentence_transformers import SentenceTransformer
        import chromadb

        model = SentenceTransformer("all-MiniLM-L6-v2")
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="vectordb_for_rag")

        # Save the full synthesized knowledge, not the raw tool call
        text = f"Task: {task}\nLearned: {synthesis}"
        embedding = model.encode(text).tolist()
        doc_id = f"task_{str(uuid.uuid4())[:8]}"

        collection.upsert(
            documents=[text],
            metadatas=[{"source": "supervisor_task", "task": task}],
            ids=[doc_id],
            embeddings=[embedding]
        )

        try:
            mem_client.add(content=text, container_tag=USER_ID)
        except Exception:
            pass
    @lru_cache(maxsize=128)
    def run(self, task):
        self.state.update_state("thinking")

        try:
            retrieved_context = retrieve_relevant_memory(task)
        except Exception:
            retrieved_context = None

        llm_response = self.call_llm(task, retrieved_context)

        self.state.update_searching("routing tools")

        tool_result = self.tool_router(llm_response)

        # If a tool was used, synthesize the results into real knowledge
        if isinstance(tool_result, dict) and tool_result.get("status") == "success":
            synthesis = self.synthesize(task, tool_result)
        else:
            # LLM responded directly without a tool — that IS the answer
            synthesis = llm_response

        self.save_to_memory(task, synthesis)

        self.shared_workspace.completed_tasks.append({
            "task": task,
            "synthesis": synthesis,
            "tool_result": tool_result,
        })

        self.state.update_state("complete")

        return {
            "task": task,
            "status": "completed",
            "answer": synthesis,
            "tool_result": tool_result,
            "context_used": retrieved_context is not None
        }


if __name__ == "__main__":
    supervisor = supervisor_agent(
        name="Supervisor",
        role="supervisor",
        memory_limit=100,
        context="You are a Supervisor Agent managing a team of research agents."
    )

    print("=== Supervisor Agent Control Panel ===\n")

    test_task = "Tell me about Yousaf" ##Question
    print(f"Task: {test_task}\n")

    result = supervisor.run(test_task)

    print("=== Execution Complete ===")
    print(f"Status: {result['status']}")
    print(f"Context Used: {result['context_used']}")
    print(f"\nAnswer (saved to memory):\n{result['answer']}")
    print(f"\nTool Result: {result['tool_result']}")
    print(f"\nShared Workspace Notes: {supervisor.shared_workspace.notes}")
    print(f"Findings: {supervisor.shared_workspace.findings}")
    print(f"Completed Tasks: {len(supervisor.shared_workspace.completed_tasks)}")
    print(f"Active Agents: {len(supervisor.registry.agents)}")