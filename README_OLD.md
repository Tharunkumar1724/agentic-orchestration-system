# 🤖 Agentic Orchestration System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

> **A production-ready AI orchestration platform for building intelligent, multi-agent workflows with comprehensive metrics tracking and real-time monitoring.**

Build complex AI systems by composing agents, tools, and workflows. Track performance, quality, and execution metrics in real-time. Designed for both developers and researchers.

---

## 🌟 Key Features

### 🎯 Core Capabilities
- **Multi-Agent Workflows**: Sequential, parallel, and router-based agent orchestration
- **Dynamic Tool Creation**: 11+ tool templates - create tools programmatically without YAML
- **Comprehensive Metrics**: Track 12+ metrics including accuracy, quality, latency, and token usage
- **Real-Time Monitoring**: WebSocket-based execution tracking with live metrics
- **Agent Communication**: Built-in context preservation and memory management (KAG)
- **Structured Output**: 4 output formats (structured, compact, text, raw) - 80% smaller responses

### 🛠️ Advanced Features
- **DuckDuckGo Integration**: Built-in web search with region support
- **LLM Flexibility**: Support for Groq, Gemini, Anthropic Claude, and more
- **Solution Chains**: Execute multi-workflow solutions with handoff context
- **Interactive Chat**: Conversational workflows with memory and metrics
- **REST + WebSocket APIs**: Full CRUD operations with real-time updates

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- API keys: Groq/Gemini/Anthropic (optional for testing)

### 1. Install Backend
```powershell
# Clone repository
git clone https://github.com/Tharunkumar1724/agentic-orchestration-system.git
cd agentic-orchestration-system

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your API keys
```

### 2. Start Backend Server
```powershell
# Option 1: Using start script
.\start_backend.ps1

# Option 2: Manual start
uvicorn app.main:app --reload --port 8000
```

### 3. Start Frontend Dashboard (Optional)
```powershell
cd frontend
npm install
npm start
# Access at http://localhost:3000
```

### 4. Try It Out
```powershell
# Run example workflow
python example_complete_workflow.py

# Test metrics system
python test_metrics_complete.py

# Interactive tool creator
python interactive_tool_creator.py
```

---

## 📊 Metrics System

Track **12+ comprehensive metrics** across all executions:

### Performance Metrics
- **Latency**: Execution time in milliseconds
- **Token Usage**: Input/output/total token counts
- **Tool Invocations**: Count and success rate

### Quality Metrics
- **Accuracy**: Task completion accuracy (0-100%)
- **Response Quality**: Output quality score
- **Hallucination Rate**: Factual accuracy tracking
- **Context Quality**: Relevance and coherence

### Execution Metrics
- **Task Completion Rate**: Success percentage
- **Decision Depth**: Reasoning complexity
- **Branching Factor**: Workflow complexity
- **Retrieval Errors**: Data access failures

**View Metrics**: Automatically displayed in workflow results, solution execution, and chat responses.

---

## 🎨 Output Formats

Choose the format that fits your needs:

```bash
# Structured (default) - Clean JSON with summary
curl -X POST "http://localhost:8000/v1/workflows/my-workflow/run"

# Compact - 80% smaller, essential data only
curl -X POST "http://localhost:8000/v1/workflows/my-workflow/run?format=compact"

# Text - Human-readable report
curl -X POST "http://localhost:8000/v1/workflows/my-workflow/run?format=text"

# Raw - Full technical details
curl -X POST "http://localhost:8000/v1/workflows/my-workflow/run?format=raw"
```

---

## 🛠️ Dynamic Tool Creation

Create tools on-the-fly without YAML files:

```python
from agentic_tool_client import AgenticToolClient

client = AgenticToolClient()

# Create a web search tool
search_tool = client.create_duckduckgo_search(
    name="Web Search",
    max_results=5,
    region="us-en"
)

# Create an API tool
api_tool = client.create_rest_api_tool(
    name="GitHub API",
    endpoint="https://api.github.com/users/{username}",
    method="GET"
)

# Use in workflow
workflow = client.create_workflow(
    name="Research Workflow",
    agents=[...],
    tools=[search_tool["tool"]["id"], api_tool["tool"]["id"]]
)
```

**11 Tool Templates Available:**
- DuckDuckGo Search, REST API, GraphQL, Web Scraper
- Database (SQL), File Reader, File Writer
- Python Executor, Shell Command, HTTP Request, Custom

---

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[Complete Guide](GETTING_STARTED.md)** - Comprehensive setup and usage
- **[API Reference](COMPLETE_URL_API_REFERENCE.md)** - Full REST API documentation

### Core Features
- **[Metrics System](METRICS_SYSTEM_COMPLETE.md)** - Comprehensive metrics tracking
- **[Output Formatting](OUTPUT_FORMATTING_GUIDE.md)** - Structured output formats
- **[Dynamic Tools](DYNAMIC_TOOL_CREATION_GUIDE.md)** - Create tools programmatically
- **[Workflow Communication](WORKFLOW_COMMUNICATION_COMPLETE.md)** - Agent-to-agent messaging

### Advanced Topics
- **[Solution Chains](SOLUTION_SYSTEM_COMPLETE.md)** - Multi-workflow orchestration
- **[Chat Mode](CHAT_MODE.md)** - Conversational workflows
- **[KAG Service](ARCHITECTURE_COMPLETE_SUMMARY.md)** - Knowledge-aided generation
- **[Frontend Guide](COMPLETE_FRONTEND_GUIDE.md)** - Dashboard setup

### Quick References
- **[Metrics Quick Ref](OUTPUT_FORMAT_QUICKREF.md)** - Metrics at a glance
- **[DuckDuckGo Quick Ref](DUCKDUCKGO_QUICK_REF.md)** - Web search usage
- **[Execution Quick Ref](EXECUTION_QUICK_REFERENCE.md)** - Workflow execution

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend Dashboard                │
│         (React + ReactFlow + WebSocket)             │
└──────────────────┬──────────────────────────────────┘
                   │ REST API + WebSocket
┌──────────────────▼──────────────────────────────────┐
│              FastAPI Backend (Python)               │
│  ┌───────────────────────────────────────────────┐  │
│  │  Orchestrator (LangGraph)                     │  │
│  │  - Workflow Execution Engine                  │  │
│  │  - Metrics Tracking (MetricsService)          │  │
│  │  - Agent Communication (KAG)                  │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │  Services Layer                               │  │
│  │  - LLM Clients (Groq/Gemini/Claude)           │  │
│  │  - Tool Manager (11+ templates)               │  │
│  │  - Storage (YAML + JSON)                      │  │
│  │  - Output Formatter (4 formats)               │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**Tech Stack:**
- **Backend**: FastAPI, LangGraph, Pydantic
- **Frontend**: React, ReactFlow, Framer Motion, Tailwind CSS
- **LLMs**: Groq (Llama), Google Gemini, Anthropic Claude
- **Storage**: YAML (configs), JSON (runs), In-memory (sessions)

---

## 🔧 Configuration

### LLM Providers

**Groq (Default)**
```bash
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-key
```

**Google Gemini**
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-key
```

**Anthropic Claude**
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your-claude-key
ANTHROPIC_MODEL=claude-sonnet-4.5
```

### Environment Variables
```bash
# Required
GROQ_API_KEY=gsk_...           # For Groq LLMs
GEMINI_API_KEY=AI...           # For Gemini LLMs (optional)

# Optional
LLM_PROVIDER=groq              # groq, gemini, anthropic
PORT=8000                      # Backend server port
FRONTEND_PORT=3000             # Frontend dashboard port
```

---

## 🧪 Testing

```powershell
# Test metrics system
python test_metrics_complete.py

# Test dynamic tools
python test_dynamic_tools.py

# Test output formatting
python test_formatted_output.py

# Test solution execution
python test_solution_websocket_quick.py

# Test complete orchestration
python test_complete_orchestration.py
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to Contribute:**
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository

---

## 📦 Project Structure

```
agentic_app/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── routers/                # API endpoints
│   │   ├── workflows.py        # Workflow CRUD + execution
│   │   ├── solutions.py        # Solution orchestration
│   │   ├── chat.py             # Chat sessions
│   │   ├── agents.py           # Agent management
│   │   └── tools.py            # Tool management
│   ├── services/               # Core services
│   │   ├── orchestrator.py     # Workflow execution engine
│   │   ├── metrics_service.py  # Metrics tracking
│   │   ├── kag_service.py      # Knowledge-aided generation
│   │   ├── gemini_client.py    # Gemini LLM client
│   │   └── output_formatter.py # Output formatting
│   └── models/                 # Pydantic models
├── frontend/
│   └── src/
│       ├── components/         # React components
│       │   ├── Workflows.js    # Workflow manager
│       │   ├── Solutions.js    # Solution executor
│       │   ├── MetricsDisplay.js # Metrics visualization
│       │   └── ...
│       └── services/           # API clients
├── config/                     # YAML configurations
│   ├── tools/                  # Tool definitions
│   ├── agents/                 # Agent definitions
│   ├── workflows/              # Workflow definitions
│   ├── solutions/              # Solution definitions
│   └── runs/                   # Execution history
└── tests/                      # Test files
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangGraph** for workflow orchestration
- **FastAPI** for the backend framework
- **React Flow** for workflow visualization
- **Groq**, **Google Gemini**, **Anthropic** for LLM APIs

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Tharunkumar1724/agentic-orchestration-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Tharunkumar1724/agentic-orchestration-system/discussions)
- **Documentation**: Check the `/docs` folder and markdown files in the repository

---

## 🗺️ Roadmap

- [ ] **v1.0**: First stable release with full metrics system
- [ ] **v1.1**: Enhanced tool templates (15+)
- [ ] **v1.2**: Multi-LLM parallel execution
- [ ] **v1.3**: Advanced KAG with RAG integration
- [ ] **v2.0**: Production deployment templates (Docker, K8s)

---

**Built with ❤️ by [Tharunkumar1724](https://github.com/Tharunkumar1724)**

⭐ **Star this repo if you find it useful!**
