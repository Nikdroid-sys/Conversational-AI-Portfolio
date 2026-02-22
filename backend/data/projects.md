# Projects

## Professional Projects (Enterprise | Confidential)

> The following projects were developed during my role at Tata Consultancy Services.
> Client names, internal systems, and proprietary details are intentionally omitted.

### Project 1: No-Code Multi-Agent AI Orchestration Platform
Project: Self-Correcting Agentic RAG (Reasoning Engine)
Role: GenAI Engineer

Timeline: 2024–2025

Nature: Advanced RAG Implementation for High-Precision Domains

Description:

Developed an "Agentic RAG" system designed to eliminate hallucinations by implementing a self-healing reasoning loop. Unlike traditional linear RAG, this system autonomously evaluates the quality of its own retrieved data and re-searches if the initial results are irrelevant or hallucinated.

Key Contributions:

Architected Multi-Agent Loops: Leveraged LangGraph to create a stateful cyclic graph where a 'Grader' node assesses document relevance. If the score falls below a threshold, the system triggers a 'Query Rewrite' agent to refine the search terms and retry the retrieval.

Visual-to-Production Workflow: Used Langflow as a visual IDE to map complex logic gates and edge cases (e.g., "What if the vector DB returns nothing?"). Exported the logic as a JSON schema to be served via a "headless" FastAPI backend for enterprise stability.

Hallucination Guardrails: Integrated a 'Hallucination Grader' that performs a factual consistency check between the retrieved context and the final generation, ensuring the AI never "imagines" facts not present in the source documents.

Hybrid Retrieval Optimization: Combined semantic vector search with keyword-based retrieval, using Cross-Encoders for re-ranking to ensure the most contextually dense information reached the LLM.

Performance Monitoring: Integrated LangSmith for deep-trace observability, allowing for visual debugging of every "turn" the agent took during the self-correction process.

Technologies:

Orchestration: LangGraph, Langflow, Python

API Framework: FastAPI

Vector DB:  Azure AI Search

Models: Azure OpenAI (GPT-4o), LangChain

Observability: LangSmith

Impact:

Reduced Hallucinations by ~30% compared to standard RAG pipelines by implementing autonomous self-grading.

Increased Retrieval Recall: The 'Query Rewrite' loop successfully answered 20% of complex queries that initially failed on the first search attempt.

Production Readiness: Decoupled the design (Langflow) from execution (FastAPI), allowing for 99.9% uptime and version-controlled logic deployments.




Role: GenAI Engineer  
Timeline: 2025–2026  
Nature: Internal enterprise platform

Description:
- Built a backend platform to dynamically create and orchestrate multi-agent AI systems.
- Enabled non-technical users to configure agent workflows without writing code.

Key Contributions:
- Designed FastAPI microservices to manage agent lifecycle and execution.
- Implemented prompt-driven agent templates supporting escalation, HITL, and branching logic.
- Integrated LangGraph, AutoGen, and similar frameworks for agent orchestration.
- Built a dynamic script ingestion system for Python-based agents.
- Reduced agent onboarding and setup time by ~80%.

Technologies:
FastAPI, LangGraph, AutoGen, Python, Azure OpenAI

---

### Project 2: LLM Strategy Evaluation & Benchmarking Framework
Role: GenAI Engineer  
Timeline: 2024–2025  
Nature: Enterprise benchmarking suite

Description:
- Developed a framework to evaluate when to use prompting, RAG, or fine-tuning for enterprise GenAI use cases.

Key Contributions:
- Benchmarked prompting, RAG, and fine-tuning across 12 BFSI and support tasks.
- Built evaluator agents to assess output quality and hallucination risk.
- Designed reusable prompt templates using CoT, ReAct, and graph-based reasoning.
- Reduced hallucinations by ~15% through strategy selection and evaluation.

Technologies:
Azure OpenAI, Python, FastAPI, Prompt Engineering

---

### Project 3: Secure RAG Architecture for Regulated Domains
Role: GenAI Engineer  
Timeline: 2024–2025  
Nature: Compliance-focused GenAI system

Description:
- Designed a secure, audit-ready RAG architecture for regulated industries.

Key Contributions:
- Built RAG pipelines with grounding, traceability, and observability.
- Integrated FastAPI with LlamaIndex and Azure Blob Storage.
- Implemented encryption, audit logging, and HITL workflows.
- Ensured document-level traceability for responsible AI usage.

Technologies:
FastAPI, LlamaIndex, Azure Blob, Azure OpenAI

---

### Project 4: Enterprise RAG Chatbot on Microsoft Teams
Role: AI Developer  
Timeline: 2023

Description:
- Developed a real-time chatbot to answer internal enterprise queries via Microsoft Teams.

Key Contributions:
- Implemented document chunking and retrieval using LlamaIndex and Qdrant.
- Used Azure OpenAI for response generation.
- Reduced manual ticket volume by ~40%.
- Improved UAT query resolution by ~60%.
- Tuned retrieval for multilingual enterprise data.

Technologies:
LlamaIndex, Qdrant, Azure OpenAI, Microsoft Teams

---

## Personal Projects (Public)

### Conversational AI Portfolio Platform
Nature: Personal project

Description:
- Built a ChatGPT-style conversational interface to answer questions about my profile and work.

Key Contributions:
- Implemented a RAG-backed FastAPI service with conversational memory.
- Designed grounded responses using structured project and resume context.
- Built a lightweight React UI with streaming responses.

Technologies:
LangChain, FastAPI, React


### Project: Local Multilingual Legal AI System (India)

Nature: Personal Project

Description:
Developed a privacy-first, CPU-optimized, and locally hosted legal AI system designed specifically for the Indian judicial ecosystem. The system helps advocates and legal researchers by providing grounded, citable legal answers based on ingested legal documents (Acts, Judgments, Constitution, etc.).

Key Contributions:

* Built a Legal RAG (Retrieve, Augment, Generate) pipeline to ensure accurate answers using local legal documents.
* Implemented Hybrid Search combining traditional keyword search (BM25) with semantic vector search, re-ranked using Reciprocal Rank Fusion (RRF).
* Designed automatic ingestion of legal documents and efficient indexing for fast startup times.
* Ensured privacy-by-design, with all data processing running locally on the user’s machine.
* Optimized system for CPU-only operation, allowing it to run on consumer-grade hardware without needing a dedicated GPU.

Technologies:

* Backend: FastAPI, LangGraph, Ollama
* Vector DB: Qdrant
* Frontend: React, TypeScript, Vite
* Embeddings: `sentence-transformers/all-MiniLM-L6-v2`

Impact:

* Improved efficiency in legal research by automating document ingestion and retrieval.
* Provided a scalable, privacy-respecting solution for the legal community in India, ensuring secure handling of sensitive data.


### Project: Local AI Ops Copilot

Nature: Personal Project

Description:
Developed a fully local, offline, and CPU-optimized multi-agent AI system for operational debugging. This system analyzes logs, configurations, and internal documentation to generate actionable root-cause analysis and remediation guidance — all without sending any data to the cloud.

Key Contributions:

* Built an offline, CPU-only GenAI system focused on operational diagnostics for engineering teams.
* Designed a multi-agent architecture to separate cognitive responsibilities: Context Analyzer, Knowledge Retriever, and Solution Synthesizer.
* Integrated a lightweight RAG pipeline using HuggingFace embeddings, FAISS for local vector search, and simple chunking techniques to keep inference efficient.
* Implemented Human-in-the-loop safety mechanisms, including confidence scoring and risk classification, to ensure that AI suggestions are safe and verifiable.
* Optimized the entire system to run on consumer-grade hardware (i5-class CPU), with minimal LLM inference per request (around 2 calls).

Technologies:

* LLM Orchestration: CrewAI
* Local Inference: Ollama
* Embeddings: HuggingFace sentence-transformers
* Vector DB: FAISS
* Backend: FastAPI
* Language: Python

Impact:

* Improved incident diagnosis speed and reduced on-call fatigue by automating root-cause analysis and providing actionable remediation steps.
* Delivered a cloud-free, privacy-first solution that can be deployed in sensitive environments, such as regulated industries or air-gapped systems.
* Enabled better reuse of internal knowledge without relying on expensive, cloud-dependent observability tools.

