# Human-in-the-Loop Research Agent

A research agent built with LangGraph that incorporates human feedback into the research process. The agent can pause execution to ask for clarification and adapt its research strategy based on human input.

## 🚀 Features

- **Interactive Research**: Pause and ask for human feedback during research
- **Web Search**: Uses Tavily API for comprehensive searches
- **Structured Output**: Organized results with analysis, strategy, findings, and next steps
- **State Management**: Maintains conversation context across interactions

## 🛠️ Setup

### Prerequisites
- Python 3.12+
- Poetry

### Installation

1. **Clone and install**
   ```bash
   git clone <repository-url>
   cd human_feedback
   poetry install
   ```

2. **Environment setup**
   
   Create `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

3. **Activate environment**
   ```bash
   poetry env activate
   ```



