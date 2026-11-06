import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph
from neo4j import GraphDatabase

from data_passport import generate_signature

load_dotenv()


class AgentState(TypedDict):
    query: str
    user_clearance: str
    retrieved_nodes: list
    secure_context: str
    final_response: str


def retrieve_data(state: AgentState) -> dict:
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
    )
    query = """
    MATCH (c:Chunk)-[:REQUIRES_CLEARANCE]->(cl:ClearanceLevel)
    RETURN c.chunk_id AS chunk_id,
           c.content AS content,
           c.source_document AS source_document,
           c.cryptographic_hash AS stored_hash,
           cl.level AS required_clearance
    """
    with driver.session() as session:
        result = session.run(query)
        nodes = [record.data() for record in result]
    driver.close()
    return {"retrieved_nodes": nodes}


def zero_trust_gate(state: AgentState) -> dict:
    secure_chunks = []
    for node in state["retrieved_nodes"]:
        recalculated = generate_signature(
            node["content"], node["source_document"], node["required_clearance"]
        )
        if recalculated == node["stored_hash"] and state["user_clearance"] == node["required_clearance"]:
            secure_chunks.append(node["content"])
    return {"secure_context": "\n".join(secure_chunks)}


def generate_response(state: AgentState) -> dict:
    if not state["secure_context"]:
        return {"final_response": "ACCESS DENIED: Insufficient Clearance or Data Tampering Detected."}

    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")
    prompt = (
        f"Context:\n{state['secure_context']}\n\n"
        f"Question: {state['query']}\n\n"
        "Answer the question professionally using only the provided context."
    )
    result = llm.invoke(prompt)
    content = result.content
    if isinstance(content, list):
        text = "".join(block.get("text", "") for block in content if isinstance(block, dict))
    else:
        text = content
    return {"final_response": text}


graph = StateGraph(AgentState)
graph.add_node("retrieve_data", retrieve_data)
graph.add_node("zero_trust_gate", zero_trust_gate)
graph.add_node("generate_response", generate_response)

graph.set_entry_point("retrieve_data")
graph.add_edge("retrieve_data", "zero_trust_gate")
graph.add_edge("zero_trust_gate", "generate_response")
graph.add_edge("generate_response", END)

app = graph.compile()


def run_secure_query(query: str, clearance_level: str) -> str:
    result = app.invoke({
        "query": query,
        "user_clearance": clearance_level,
        "retrieved_nodes": [],
        "secure_context": "",
        "final_response": "",
    })
    return result["final_response"]


if __name__ == "__main__":
    query = "What was the Q3 revenue?"

    print("=" * 70)
    print("RUN A: user_clearance = EXECUTIVE_ONLY")
    print("=" * 70)
    print(f"\nFINAL RESPONSE:\n{run_secure_query(query, 'EXECUTIVE_ONLY')}\n")

    print("=" * 70)
    print("RUN B: user_clearance = STANDARD_EMPLOYEE")
    print("=" * 70)
    print(f"\nFINAL RESPONSE:\n{run_secure_query(query, 'STANDARD_EMPLOYEE')}\n")
