# ARAI (Assistant Researcher AI)

This repository demonstrates an agentic workflow called ARAI, designed to facilitate research paper analysis and interaction. The workflow is divided into two main flows:

- Offline Flow
- Online Flow

## Offline Flow

The goal of the offline flow is to parse, index, and store research papers.

### Agents

- **DocumentParser**: Parses documents and extracts content.
- **FirstPageSummarizer**: Summarizes the first page of documents.
- **JargonExtractor**: Identifies and extracts jargon, abbreviations, and acronyms.
- **ChunkEnricher**: Enriches document chunks with additional information.

## Online Flow

The goal of the online flow is to enable interactive conversations with research papers.

### Agents

- **InputAgent**: Handles user input.
- **Organizer**: Organizes and routes tasks based on input.
- **JargonDetector**: Detects jargon in the input.
- **QueryRewriter**: Rewrites queries for better understanding.
- **QueryDecomposer**: Decomposes complex queries into simpler ones.
- **RetrieverAgent**: Retrieves relevant documents.
- **RerankerAgent**: Reranks retrieved documents based on relevance.
- **DocumentCompressor**: Compresses documents to essential information.
- **Reviewer**: Reviews and approves or rejects documents.
- **ContextAnalyzer**: Analyzes the context of approved documents.
- **AnswerGenerator**: Generates answers based on analyzed documents.
- **BadNewsGenerator**: Handles scenarios requiring human intervention.

## Memories

- **PersonaMemory**: Stores background information of research papers.
- **JargonMemory**: Stores jargon, abbreviations, and acronyms found in research papers.
- **LongTermMemory**: Stores information parsed from research papers.
- **ShortTermMemory**: Stores information retrieved during conversations.
- **ContextMemory**: Stores global information related to retrieved local information.
- **SessionMemory**: Stores information related to the entire conversation session.
- **EventMemory**: Manages information for Pub-Sub events.
- **ChatMemory**: Stores chat history.

*Note: ARAI is a work in progress and may undergo rapid changes without prior notice.*