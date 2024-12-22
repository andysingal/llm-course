from logger import RAGLogger

def simulate_rag_process():
    # Initialize logger
    logger = RAGLogger(log_dir="logs", auto_save=True)
    
    try:
        # Log query
        query = "What is machine learning?"
        logger.log_query(query)
        
        # Log text retrieval step
        logger.start_step("text_retrieval")
        # Simulate text retrieval process
        text_docs = [
            {"id": 1, "content": "Machine learning is a subfield of artificial intelligence"},
            {"id": 2, "content": "Machine learning trains models using data"}
        ]
        logger.log_retrieval("text", total_docs=100, retrieved_docs=text_docs)
        logger.end_step("text_retrieval")
        
        # Log image retrieval step
        logger.start_step("image_retrieval")
        # Simulate image retrieval process
        image_docs = [
            {"id": 1, "path": "ml_diagram.png"},
            {"id": 2, "path": "neural_network.png"}
        ]
        logger.log_retrieval("image", total_docs=50, retrieved_docs=image_docs)
        logger.end_step("image_retrieval")
        
        # Log LLM generation step
        logger.start_step("llm_generation")
        llm_input = f"Query: {query}\nContext: {text_docs}"
        llm_output = "Machine learning is a method that improves system performance through data training..."
        logger.log_llm(llm_input, llm_output)
        logger.end_step("llm_generation")
        
        # Manually save log (if auto-save is disabled)
        if not logger.auto_save:
            logger.save()
            
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    simulate_rag_process()
