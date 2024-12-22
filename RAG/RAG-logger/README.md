# RAG Logger

RAG Logger is an open-source logging tool designed specifically for Retrieval-Augmented Generation (RAG) applications. It serves as a lightweight, open-source alternative to LangSmith, focusing on RAG-specific logging needs.

## Features

- 📊 **Comprehensive RAG Pipeline Logging**
  - Query tracking
  - Retrieval results logging (text & images)
  - LLM interaction recording
  - Step-by-step performance monitoring

- 💾 **Structured Storage**
  - JSON-based log format
  - Daily log organization
  - Automatic file management
  - Metadata enrichment

## Quick Start
```python
from logger import RAGLogger

# Initialize logger
logger = RAGLogger(log_dir="logs")

# Log a query
logger.log_query("What is machine learning?")

# Track retrieval step
logger.start_step("retrieval")
logger.log_retrieval(
    source="text",
    total_docs=100,
    retrieved_docs=[{"id": 1, "content": "..."}]
)
logger.end_step("retrieval")

# Record LLM interaction
logger.log_llm(
    llm_input="User query and context",
    llm_output="Generated response"
)

# Save logs
logger.save()
```
 
## Log Structure
```json
{
    "timestamp": "2024-03-20 10:00:00",
    "query": "What is machine learning?",
    "total_time": 8.5,
    "steps": {
        "query_understanding": {
            "name": "query_understanding",
            "start_time": 1234567890.0,
            "end_time": 1234567891.0,
            "duration": 1.0,
            "metadata": {
                "detected_intent": "definition_query",
                "topic": "machine_learning",
                "confidence": 0.95
            }
        },
        "text_embedding": {
            "name": "text_embedding", 
            "start_time": 1234567891.0,
            "end_time": 1234567892.5,
            "duration": 1.5,
            "metadata": {
                "model": "text-embedding-3-small",
                "embedding_dim": 1536,
                "batch_size": 32
            }
        },
        "text_retrieval": {
            "name": "text_retrieval",
            "start_time": 1234567892.5,
            "end_time": 1234567894.0,
            "duration": 1.5,
            "metadata": {
                "index_type": "faiss",
                "top_k": 5,
                "similarity_threshold": 0.7
            }
        },
        "llm_generation": {
            "name": "llm_generation",
            "start_time": 1234567894.0,
            "end_time": 1234567898.5,
            "duration": 4.5,
            "metadata": {
                "model": "gpt-4o",
                "max_tokens": 1024,
                "temperature": 0.7
            }
        }
    },
    "retrieval_results": {
        "text": {
            "total_docs": 1000,
            "retrieved_docs": [
                {
                    "id": "doc_123",
                    "book": "Introduction to Machine Learning",
                    "chapter": "Chapter 1: Overview",
                    "content": "Machine learning is a core field of artificial intelligence...",
                    "similarity_score": 0.92,
                    "metadata": {
                        "page": 12,
                        "last_updated": "2024-01-01"
                    }
                }
            ],
            "metadata": {
                "index_size": "2.5GB",
                "last_updated": "2024-03-19"
            }
        }
    },
    "llm_input": {
        "query": "What is machine learning?",
        "context": "...(retrieved text contents)",
        "system_prompt": "You are a professional educational assistant...",
        "metadata": {
            "max_context_length": 4096,
            "format": "markdown"
        }
    },
    "llm_output": {
        "content": "Machine learning is a key branch of artificial intelligence...",
        "metadata": {
            "token_count": 512,
            "generation_time": 4.5
        }
    },
    "messages": [
        {
            "timestamp": "2024-03-20 10:00:00",
            "level": "INFO",
            "step": "query_understanding",
            "message": "Successfully identified query intent: definition_query"
        },
        {
            "timestamp": "2024-03-20 10:00:01",
            "level": "INFO", 
            "step": "text_retrieval",
            "message": "Retrieved 5 relevant documents from 1000 total documents"
        },
        {
            "timestamp": "2024-03-20 10:00:03",
            "level": "INFO",
            "step": "llm_generation",
            "message": "Response generation completed, tokens: 512"
        }
    ],
    "error_tracking": {
        "has_errors": false,
        "error_count": 0,
        "warnings": []
    }
}
```
