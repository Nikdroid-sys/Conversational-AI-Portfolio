# Projects

## Professional Projects (Enterprise | Confidential)

> The following projects were developed during my role at Tata Consultancy Services.
> Client names, internal systems, and proprietary details are intentionally omitted.
---

## 🏢 Professional Experience: Tata Consultancy Services (TCS)

### Senior GenAI Systems Engineer | Sept 2022 – Present

#### Core Platform: "AI Axis" – Enterprise Multi-Agent Orchestration Layer

Nature: Internal Strategic Initiative | Lead Backend Engineer

* The Problem: Inconsistent AI deployments and "Shadow AI" across 3+ business units.
* The Solution: Architected a standardized FastAPI Microservices Platform to manage the full lifecycle of agentic systems (Creation, Registry, Execution, and Monitoring).
* Strategic Impact: * 80% Reduction in Onboarding: Standardized agent templates (Escalation, Branching, HITL) allowed non-technical teams to deploy workflows without low-level coding.
* Governance at Scale: Integrated FastMCP 3.0 and NeMo Guardrails into the core middleware, ensuring every agentic call adhered to enterprise PII and safety policies.
* Inference Efficiency: Orchestrated a Semantic Caching Layer (GPTCache), reducing redundant API costs by 30% and improving response latency for common enterprise queries.



---

#### Flagship System: "Self-Healing" Agentic RAG (Reasoning Engine)

Nature: High-Precision Implementation for BFSI/Regulated Domains

* The Problem: Standard RAG pipelines suffered from a 30% hallucination rate due to poor retrieval quality.
* The Solution: Engineered a Stateful Cyclic Graph (LangGraph) featuring a "Reflexion Pattern."
* Autonomous Grader Node: Implemented a logic gate that scores retrieved context; if relevance falls below a threshold, a 'Query Rewrite' agent is triggered to autonomously refine the search and retry.
* Fact-Consistency Loop: Built a 'Hallucination Grader' that performs a cross-check between the generated answer and the source citations before the user sees the output.


* Performance Metrics: * Recall Optimization: Successfully resolved 20% of complex queries that initially failed on first-pass retrieval.
* Production Stability: Decoupled design (Langflow) from execution (FastAPI), achieving 99.9% uptime for mission-critical judicial and financial data retrieval.



---

#### Framework: LLM Strategy & Benchmarking Suite

Role: Lead Evaluator / GenAI Strategist

* Objective: Developed a data-driven framework to determine the optimal balance between Prompt Engineering, RAG, and Fine-Tuning (PEFT).
* Key Contributions:
* Automated Evaluation: Built a fleet of Evaluator Agents to benchmark model performance across 12 distinct BFSI support tasks.
* Technique Selection: Proved that ReAct (Reasoning + Acting) and Chain-of-Thought (CoT) prompting reduced hallucinations by ~15% for high-stakes decision-making workflows.
* Security Architecture: Designed an audit-ready RAG pipeline integrating Azure Blob Storage with LlamaIndex, ensuring document-level traceability and encrypted logging for compliance.



---


## Personal Projects Portfolio (Public)

## 1. Project: Agentic-Data-Factory (Lead Architect)

Nature: Production-Grade Synthetic Data Engineering Pipeline

Role: Senior AI Systems Architect

Core Stack: LangGraph, FastMCP 3.0, FastAPI, uv, NeMo Guardrails, Arize Phoenix, DeepEval

### 🏗️ Architectural Vision

Developed a decoupled, three-tier autonomous pipeline to solve the "Cold Start" problem in LLM fine-tuning. This system transitions enterprise data from "Unstructured Noise" to "Fine-Tuning Ready" `JSONL` assets without manual human labeling.

### 💡 Key Engineering Milestones:

* Stateful Multi-Agent Orchestration: Designed a Reflexion Architecture using LangGraph where a *Synthesizer Agent* generates QA pairs and an *Auditor Agent* performs a factual consistency check. If the "Faithfulness" score (calculated via DeepEval) is $<0.85$, the state triggers a recursive self-correction loop.
* Resource Abstraction (MCP): Implemented FastMCP 3.0 to create a "Cloud-Agnostic Resource Layer," allowing the agents to seamlessly toggle between local file systems, S3, and Azure Blob storage using standardized tool-calling.
* Enterprise Governance: Integrated NeMo Guardrails as a deterministic security layer. Every synthetic record is scrubbed for PII (Names, IPs, SSNs) and filtered for topical relevance before reaching the final training set.
* Observability & Traceability: Leveraged Arize Phoenix (OpenTelemetry) to monitor "Agent Thought-Chains." This allowed for a 20% reduction in tool-call latency by identifying and pruning redundant reasoning steps.

---

## 2. Project: Guardian-MCP (Security-First AI Governance)

Nature: Zero-Trust Tool-Calling & Security Gateway

Role: Lead Security Researcher / GenAI Engineer

Core Stack: FastMCP 3.0, Google OSV API, uv, Python

### 🛡️ System Overview

Engineered a security-critical "Interceptor Pattern" for autonomous agents to eliminate "Agent Liability" (the risk of an LLM installing vulnerable or malicious code during a task).

### 💡 Key Engineering Milestones:

* Real-time Vulnerability Interception: Created a middleware that hooks into `uv pip install` commands. It performs an asynchronous lookup against the Google OSV Database to block packages with active CVEs before they touch the disk.
* Isolated "Clean Room" Provisioning: Utilized `uv` to create ephemeral, "hidden" virtual environments for agent tasks, ensuring zero pollution of the host system's global Python environment.
* Self-Healing Patching: If a package is blocked (e.g., *Flask 0.12.1* due to CVE-2018-1000656), the system returns a structured "Security Feedback" to the LLM, prompting it to autonomously research and suggest a patched version (e.g., *Flask 3.1.3*).

---

## 3. Project: Bharat-Legal AI (Privacy-First Legal RAG)

Nature: Local-First, Multilingual Judicial Intelligence System

Role: Principal Developer

Core Stack: Ollama (Llama 3.3/Phi-4), Qdrant, LangGraph, sentence-transformers

### ⚖️ Technical Strategy

Designed a specialized RAG system for the Indian legal ecosystem, prioritizing zero data-leakage and CPU-only efficiency for local law firms.

### 💡 Key Engineering Milestones:

* Hybrid Retrieval Engine: Combined BM25 keyword matching with semantic vector search in Qdrant, utilizing Reciprocal Rank Fusion (RRF) to handle the complex, jargon-heavy terminology of Indian Gazettes.
* Statute-Level Chunking: Developed a custom document parser for legal PDFs that maintains hierarchical context (Section > Sub-section > Clause), ensuring the LLM cites specific law sections with 90%+ retrieval accuracy.
* Edge AI Optimization: Quantized the model to 4-bit GGUF using Ollama, enabling full-scale legal reasoning on consumer-grade i5/i7 CPUs with sub-2-second token latency.

---

## 4. Project: Local AI Ops Copilot

Nature: Multi-Agent Diagnostics for Air-Gapped Environments

Role: AI Ops Specialist

Core Stack: CrewAI, FAISS, HuggingFace, FastAPI

### 🛠️ Strategic Implementation

Developed a "Local-First" diagnostic system for engineering teams to perform root-cause analysis (RCA) on logs and internal docs without cloud dependencies.

### 💡 Key Engineering Milestones:

* Cognitive Task Separation: Designed a three-agent crew (*Log Analyzer*, *Knowledge Retriever*, *Solution Synthesizer*) to prevent context-window saturation and improve reasoning focus.
* Safety-First HITL: Implemented a Human-in-the-Loop confidence scoring system. If the AI’s solution has a risk classification of "High," the system freezes execution until a human operator approves the remediation step.
* Impact: Reduced average incident diagnosis time (MTTR) by ~40% in simulated local environments.

---

