# Armenian Voice AI Support Agent (RAG-based)

An end-to-end Voice AI customer support agent for Armenian banks built using the open-source **LiveKit** framework.
This agent provides real-time, accurate information regarding **Credits, Deposits, and Branch Locations** by strictly adhering to a curated knowledge base.

## Key Features

- **Voice-First Experience:** Low-latency, natural Armenian speech synthesis and real-time speech-to-text transcription.
- **RAG Architecture:** Grounded AI responses using a local vector database to ensure domain-specific accuracy and reliability.
- **Automated Data Ingestion:** Scalable web-scraping pipeline designed to extract and clean structured data directly from Armenian banking websites.
- **On-Premise Capable Infrastructure:** Operates via a local LiveKit server, ensuring strict data control and user privacy.

### Architecture & Model Engineering

This project implements a precise Retrieval-Augmented Generation (RAG) architecture tailored for low-latency voice interactions. Below is a detailed breakdown of the engineering decisions:

- **Model:** `paraphrase-multilingual-MiniLM-L12-v2` (HuggingFace)
- **Justification:** Armenian operates as a low-resource language in many NLP tasks. This multilingual model was selected for its exceptional optimization in semantic search and its ability to capture complex contextual nuances in Armenian text. Furthermore, running this lightweight model entirely locally eliminates external API dependencies, reduces operational costs, and minimizes critical latency during the real-time retrieval phase.

### Vector Database

- **Technology:** ChromaDB (Local / Persistent SQLite-backed)
- **Justification:** For a voice-driven agent, avoiding cloud latency is paramount. ChromaDB was selected because it operates directly on the local filesystem. Utilizing efficient nearest-neighbor search algorithms, it provides sub-millisecond retrieval times for chunked banking data, making it the perfect backend for real-time Voice AI.

### Data Processing & Chunking Strategy

- **Logic:** To ensure the LLM receives complete thoughts, the scraped text is processed using LangChain's `RecursiveCharacterTextSplitter`. A carefully calculated chunk size and overlap ensure that semantic boundaries remain intact and critical financial context is preserved during vectorization.
- **Dynamic Retrieval:** The agent features a custom `search_bank_info` tool. When a query is detected, the agent autonomously vectorizes the user's intent, queries ChromaDB for the most relevant context, and synthesizes the answer strictly based on that retrieved chunk.

### Core Agent Logic & Guardrails

- **Prompt Engineering & Security:** Powered by OpenAI GPT-4o as the core reasoning engine. To prevent hallucinations and topic drift, strict system instructions are applied. The agent is explicitly constrained to communicate solely in Armenian and strictly limit its domain to Credits, Deposits, and Branch Locations.
- **Voice Pipeline:** The system integrates Silero VAD (Voice Activity Detection) to accurately detect speech boundaries, combined with robust STT and TTS models for an interruption-friendly, natural conversational flow.

## Prerequisites

* Python 3.10+
* LiveKit Server binary installed locally
* Active OpenAI API Key

## Installation & Setup

**Install dependencies:**
```bash
pip install -r requirements.txt

Start the local LiveKit server:

livekit-server --dev

Build the Knowledge Base (in a new terminal):

python scraper.py
python build_db.py

Start the Voice Agent:

python agent.py start

Local Testing
To interact with the agent locally without building a custom frontend interface, generate a secure access token by running:

python get_token.py

Copy the generated JWT token and paste it into any LiveKit-compatible frontend client (such as LiveKit Meet or LiveKit Agents Playground) to join the bank-room and initiate the voice conversation.