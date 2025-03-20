# Just Prompt - A lightweight MCP server for LLM providers

just-prompt is a Model Control Protocol (MCP) server that provides a unified interface to various Large Language Model (LLM) providers including OpenAI, Anthropic, Google Gemini, Groq, DeepSeek, and Ollama.

## Features

- Unified API for multiple LLM providers
- Support for text prompts from strings or files
- Ability to save responses to files
- Asynchronous processing of requests to multiple models
- Automatic model name correction using a "weak" model
- Easy listing of available providers and models

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/just-prompt.git
cd just-prompt

# Install with pip
pip install -e .
```

### Environment Variables

Create a `.env` file with your API keys (you can copy the `.env.sample` file):

```bash
cp .env.sample .env
```

Then edit the `.env` file to add your API keys:

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OLLAMA_HOST=http://localhost:11434
```

## Usage

### Starting the Server

```bash
python -m just_prompt.server
```

Or use the command-line interface:

```bash
just-prompt --host 0.0.0.0 --port 8000 --weak-model o:gpt-4o-mini
```

### API Endpoints

#### Send a Prompt

```bash
curl -X POST http://localhost:8000/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is the capital of France?",
    "models_prefixed_by_provider": ["o:gpt-4o-mini", "a:claude-3-5-haiku"]
  }'
```

#### Send a Prompt from a File

```bash
curl -X POST http://localhost:8000/prompt_from_file \
  -H "Content-Type: application/json" \
  -d '{
    "file": "/path/to/prompt.txt",
    "models_prefixed_by_provider": ["o:gpt-4o-mini", "a:claude-3-5-haiku"]
  }'
```

#### Send a Prompt from a File and Save Responses to Files

```bash
curl -X POST http://localhost:8000/prompt_from_file_to_file \
  -H "Content-Type: application/json" \
  -d '{
    "file": "/path/to/prompt.txt",
    "models_prefixed_by_provider": ["o:gpt-4o-mini", "a:claude-3-5-haiku"],
    "output_dir": "/path/to/output"
  }'
```

#### List Providers

```bash
curl -X POST http://localhost:8000/list_providers \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### List Models for a Provider

```bash
curl -X POST http://localhost:8000/list_models \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai"
  }'
```

## Provider Prefixes

- `o` or `openai`: OpenAI (e.g., `o:gpt-4o-mini`)
- `a` or `anthropic`: Anthropic (e.g., `a:claude-3-5-haiku`)
- `g` or `gemini`: Google Gemini (e.g., `g:gemini-1.5-flash`)
- `q` or `groq`: Groq (e.g., `q:llama-3.1-70b-versatile`)
- `d` or `deepseek`: DeepSeek (e.g., `d:deepseek-coder`)
- `l` or `ollama`: Ollama (e.g., `l:llama3.1`)

## Running Tests

```bash
uv run pytest
```

## Context Priming
READ README.md, ai_docs/* and run git ls-files to understand the context of the project.