import json
import time
from datetime import datetime
import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class RAGStep:
    """Data class for recording RAG processing steps"""
    name: str
    start_time: float = 0.0
    end_time: float = 0.0
    duration: float = 0.0
    metadata: Dict[str, Any] = None

@dataclass
class RetrievalResult:
    """Data class for retrieval results"""
    total_docs: int = 0
    retrieved_docs: List[Dict] = None
    metadata: Dict[str, Any] = None

@dataclass
class RAGLogData:
    """Data class for RAG log data"""
    timestamp: str
    query: str
    total_time: float = 0.0
    steps: Dict[str, RAGStep] = None
    retrieval_results: Dict[str, RetrievalResult] = None
    llm_input: str = ""
    llm_output: str = ""
    messages: List[Dict] = None

class RAGLogger:
    """Logger for RAG (Retrieval-Augmented Generation) scenarios"""
    
    def __init__(self, log_dir: str = "logs", auto_save: bool = True):
        """
        Initialize RAG logger
        
        Args:
            log_dir: Directory for storing logs
            auto_save: Whether to automatically save logs (when logging ends)
        """
        self.log_dir = log_dir
        self.auto_save = auto_save
        self.start_time = time.time()
        
        # Create log directory structure
        self.today = datetime.now().strftime("%Y%m%d")
        self.daily_log_dir = os.path.join(self.log_dir, self.today)
        os.makedirs(self.daily_log_dir, exist_ok=True)
        
        # Initialize log data
        self.step_times = {}
        self.log_data = RAGLogData(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            query="",
            steps={},
            retrieval_results={},
            messages=[]
        )
        
        self.info("RAG Logger initialized successfully")

    def start_step(self, step_name: str, metadata: Dict[str, Any] = None) -> None:
        """
        Start recording a processing step
        
        Args:
            step_name: Name of the step
            metadata: Metadata related to the step
        """
        self.step_times[step_name] = time.time()
        self.log_data.steps[step_name] = RAGStep(
            name=step_name,
            start_time=self.step_times[step_name],
            metadata=metadata
        )
        print(f"[{step_name}] Started...")

    def end_step(self, step_name: str, metadata: Dict[str, Any] = None) -> None:
        """
        End recording a processing step
        
        Args:
            step_name: Name of the step
            metadata: Metadata related to the step
        """
        if step_name in self.step_times:
            end_time = time.time()
            duration = end_time - self.step_times[step_name]
            
            step = self.log_data.steps.get(step_name)
            if step:
                step.end_time = end_time
                step.duration = duration
                if metadata:
                    step.metadata = metadata if not step.metadata else {**step.metadata, **metadata}
                    
            print(f"[{step_name}] Completed (Duration: {duration:.2f}s)")

    def log_retrieval(self, 
                     source: str,
                     total_docs: int,
                     retrieved_docs: List[Dict],
                     metadata: Dict[str, Any] = None) -> None:
        """
        Log retrieval results
        
        Args:
            source: Retrieval source (e.g., 'text', 'image')
            total_docs: Total number of documents
            retrieved_docs: List of retrieved documents
            metadata: Metadata related to retrieval
        """
        self.log_data.retrieval_results[source] = RetrievalResult(
            total_docs=total_docs,
            retrieved_docs=retrieved_docs,
            metadata=metadata
        )
        print(f"[{source} Retrieval] Retrieved {len(retrieved_docs)} results from {total_docs} documents")

    def log_llm(self, llm_input: str, llm_output: str) -> None:
        """
        Log LLM interaction
        
        Args:
            llm_input: Input content to LLM
            llm_output: Output content from LLM
        """
        self.log_data.llm_input = llm_input
        self.log_data.llm_output = llm_output
        print(f"[LLM] Generated response (Length: {len(llm_output)})")

    def log_query(self, query: str) -> None:
        """
        Log query content
        
        Args:
            query: User query content
        """
        self.log_data.query = query
        print(f"[Query] {query}")

    def info(self, message: str) -> None:
        """Log information level message"""
        self._log_message("INFO", message)

    def warning(self, message: str) -> None:
        """Log warning level message"""
        self._log_message("WARNING", message)

    def error(self, message: str) -> None:
        """Log error level message"""
        self._log_message("ERROR", message)

    def _log_message(self, level: str, message: str) -> None:
        """Internal method for logging messages"""
        print(f"[{level}] {message}")
        if not self.log_data.messages:
            self.log_data.messages = []
        self.log_data.messages.append({
            "level": level,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def save(self, filename_prefix: str = "rag_log") -> str:
        """
        Save log to file
        
        Args:
            filename_prefix: Prefix for log filename
            
        Returns:
            str: Path to saved log file
        """
        self.log_data.total_time = time.time() - self.start_time
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(self.daily_log_dir, filename)
        
        # Convert log data to dictionary
        log_dict = asdict(self.log_data)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_dict, f, ensure_ascii=False, indent=2)
        
        print(f"Log saved to: {filepath}")
        return filepath

    def __del__(self):
        """Destructor - save log if auto_save is enabled"""
        if self.auto_save:
            self.save()
