# GitHub Code Intelligence Platform

A Retrieval-Augmented Generation (RAG) pipeline designed to ingest, index, and query GitHub repositories. This project allows users to converse with a codebase, ask technical questions, track down bugs, and understand repository structure using natural language.

> **Status:** *Under Active Development*

---

## Features (In Progress)

* **Repo Ingestion:** Clones and parses public/private GitHub repositories.
* **Smart Chunking:** Code-aware splitting (AST or syntax-based) to maintain context for functions, classes, and markdown documentation.
* **Vector Storage:** High-performance vector embeddings storage for semantic code search.
* **Contextual Q&A:** LLM-powered responses grounded strictly in the codebase's context to minimize hallucinations.

---

## Current Architecture

The pipeline follows a standard RAG pattern optimized for source code:

1.  **Ingestion & Parsing:** Pulls files via GitHub API / Git clone and filters out noise (e.g., lockfiles, binaries).
2.  **Embedding Generation:** Converts code snippets and documentation into dense vectors using specialized code-embedding models.
3.  **Vector Store:** Indexed using a vector database for semantic similarity search.
4.  **Retrieval & Generation:** Matches user queries against the vector store, injects relevant code snippets into the prompt context, and generates answers via an LLM.

---

## ⚙️ Tech Stack (Current)

* **Language:** Python 3.11
* **Frameworks:** LangChain
* **Vector Database:** Qdrant
* **Embeddings:** BGE-M3
* **LLM Engine:** Gemini(tentative)

---

## Getting Started

### Prerequisites

* Python 3.10 or higher
* A GitHub Personal Access Token (PAT) for private repo access
* LLM API Key
