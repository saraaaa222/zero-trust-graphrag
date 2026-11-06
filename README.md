# Enterprise Zero-Trust GraphRAG

A zero-trust retrieval-augmented generation pipeline that cryptographically signs data chunks, enforces clearance-level access control via a Neo4j knowledge graph, and gates LLM responses through a LangGraph security agent — with a Streamlit dashboard for interactive querying.

## 🎬 System Walkthrough & Demo

> **[Watch the Screen Recording Walkthrough](./Screen%20Recording%202026-11-07%20at%202.30.47%20AM.mov)**

* **0:00 – 0:20 | Backend Provenance:** Inspecting the Neo4j Knowledge Graph where unstructured chunks are cryptographically signed with immutable SHA-256 passports and linked directly to clearance nodes (`EXECUTIVE_ONLY`).
* **0:20 – 0:40 | Executive Authorization:** Querying the Streamlit dashboard as an Executive (`EXECUTIVE_ONLY`) to successfully retrieve sensitive Q3 financial records (Green Success).
* **0:40 – 1:00 | Zero-Trust Enforcement:** Switching clearance to `STANDARD_EMPLOYEE` and observing the LangGraph state machine instantly intercept and block unauthorized data synthesis (Red `ACCESS DENIED`).
