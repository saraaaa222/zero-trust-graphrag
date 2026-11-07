# 🛡️ Enterprise Zero-Trust GraphRAG

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://www.langgraph.dev)
[![Neo4j](https://img.shields.io/badge/GraphDB-Neo4j%20Aura-008CC1.svg)](https://neo4j.com/)
[![Security](https://img.shields.io/badge/Security-Zero--Trust%20RBAC-critical)](https://github.com/saraaaa222/zero-trust-graphrag)

An advanced, production-grade Retrieval-Augmented Generation (RAG) security architecture that mathematically enforces **Role-Based Access Control (RBAC)** before any LLM synthesis occurs. It combines **Neo4j** knowledge graphs, **SHA-256 cryptographic data passports**, and a deterministic **LangGraph** security state machine powered by **Gemini**.

---

## 🎬 System Walkthrough & Demo

> > **[Watch the Screen Recording Walkthrough](./demo.mov)**

* **0:00 – 0:20 | Backend Provenance:** Inspecting the Neo4j Knowledge Graph where unstructured enterprise data chunks are cryptographically signed with immutable SHA-256 passports and linked directly to security clearance nodes (`EXECUTIVE_ONLY`).
* **0:20 – 0:40 | Executive Authorization:** Querying the Streamlit dashboard as an Executive (`EXECUTIVE_ONLY`) to successfully retrieve sensitive Q3 financial records (Green Success).
* **0:40 – 1:00 | Zero-Trust Enforcement:** Switching clearance to `STANDARD_EMPLOYEE` and observing the LangGraph state machine instantly intercept and block unauthorized data synthesis (Red `ACCESS DENIED`).

---

## 🏗️ System Architecture & Data Flow

```mermaid
graph TD
    User([User Query & Active Role]) --> Streamlit[Streamlit Security Gateway]
    Streamlit --> LangGraph[LangGraph State Machine Interceptor]
    LangGraph --> Neo4j[(Neo4j Knowledge Graph)]
    
    subgraph Cryptographic Provenance Layer
        Neo4j -->|Fetch Chunk & SHA-256 Hash| Verify{Passport Validation Match?}
    end

    Verify -->|Authorized| Gemini[Gemini LLM Context Synthesis]
    Verify -->|Unauthorized / Tampered| Block[Hard Intercept & Access Denied]

    Gemini --> Success[Render Green Success & Financial Data]
    Block --> Failure[Render Red Security Error Box]
