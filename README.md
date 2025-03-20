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

```bash
# Clone the repository
git clone https://github.com/yourusername/just-prompt.git
cd just-prompt

# Install with pip
uv sync
```

### Environment Variables

Create a `.env` file with your API keys (you can copy the `.env.sample` file):

```bash
cp .env.sample .env
```

Then edit the `.env` file to add your API keys (or export them in your shell):

```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
OLLAMA_HOST=http://localhost:11434
```

## Claude Code Installation

### Using `mcp add-json`

With the default model set to `anthropic:claude-3-7-sonnet`.

Copy this and paste it into claude code with BUT don't run until you copy the json

```
claude mcp add just-prompt "$(pbpaste)"
```

JSON to copy

```
{
    "command": "uv",
    "args": ["--directory", ".", "run", "just-prompt"]
}
```

With a custom default model set to `openai:gpt-4o`.

```
{
    "command": "uv",
    "args": ["--directory", ".", "run", "just-prompt", "--default-models", "openai:gpt-4o"]
}
```

With multiple default models:

```
{
    "command": "uv",
    "args": ["--directory", ".", "run", "just-prompt", "--default-models", "anthropic:claude-3-7-sonnet,openai:gpt-4o,gemini:gemini-1.5-pro"]
}
```

### Using `mcp add` with project scope

```bash
# With default model (anthropic:claude-3-7-sonnet)
claude mcp add just-prompt -s project \
  -- \
    uv --directory . \
    run just-prompt

# With custom default model
claude mcp add just-prompt -s project \
  -- \
  uv --directory . \
  run just-prompt --default-models "openai:gpt-4o"

# With multiple default models
claude mcp add just-prompt -s project \
  -- \
  uv --directory . \
  run just-prompt --default-models "anthropic:claude-3-7-sonnet-20250219,openai:o3-mini,gemini:gemini-2.0-flash"
```


## `mcp remove`

claude mcp remove just-prompt


### Starting the Server

```bash
uv run just-prompt
```

Or use the command-line interface:

```bash
# Using a single default model (default is anthropic:claude-3-7-sonnet)
uv run just-prompt --host 0.0.0.0 --port 8000 --default-models anthropic:claude-3-7-sonnet

# Using multiple default models (comma-separated)
uv run just-prompt --host 0.0.0.0 --port 8000 --default-models "anthropic:claude-3-7-sonnet,openai:gpt-4o,gemini:gemini-1.5-pro"

# Check available providers without starting the server
uv run just-prompt --show-providers
```

The `--default-models` parameter sets the models to use when none are explicitly provided to the API endpoints. The first model in the list is also used for model name correction when needed.

When starting the server, it will automatically check which API keys are available in your environment and inform you which providers you can use. If a key is missing, the provider will be listed as unavailable, but the server will still start and can be used with the providers that are available.

### API Endpoints

#### Send a Prompt

```bash
# Using specific models
curl -X POST http://localhost:8000/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is the capital of France?",
    "models_prefixed_by_provider": ["anthropic:claude-3-7-sonnet", "openai:gpt-4o"]
  }'

# Using default models (set when starting the server)
curl -X POST http://localhost:8000/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "text": "What is the capital of France?"
  }'
```

#### Send a Prompt from a File

```bash
# Using specific models
curl -X POST http://localhost:8000/prompt_from_file \
  -H "Content-Type: application/json" \
  -d '{
    "file": "/path/to/prompt.txt",
    "models_prefixed_by_provider": ["anthropic:claude-3-7-sonnet", "openai:gpt-4o"]
  }'

# Using default models
curl -X POST http://localhost:8000/prompt_from_file \
  -H "Content-Type: application/json" \
  -d '{
    "file": "/path/to/prompt.txt"
  }'
```

#### Send a Prompt from a File and Save Responses to Files

```bash
# Using specific models
curl -X POST http://localhost:8000/prompt_from_file_to_file \
  -H "Content-Type: application/json" \
  -d '{
    "file": "/path/to/prompt.txt",
    "models_prefixed_by_provider": ["anthropic:claude-3-7-sonnet", "openai:gpt-4o"],
    "output_dir": "/path/to/output"
  }'

# Using default models
curl -X POST http://localhost:8000/prompt_from_file_to_file \
  -H "Content-Type: application/json" \
  -d '{
    "file": "/path/to/prompt.txt",
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
    "provider": "ollama"
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

## Codebase Structure

```
.
├── ai_docs/                   # Documentation for AI model details
│   ├── llm_providers_details.xml
│   └── pocket-pick-mcp-server-example.xml
├── list_models.py             # Script to list available LLM models
├── pyproject.toml             # Python project configuration
├── specs/                     # Project specifications
│   └── init-just-prompt.md
├── src/                       # Source code directory
│   └── just_prompt/
│       ├── __init__.py
│       ├── __main__.py
│       ├── atoms/             # Core components
│       │   ├── llm_providers/ # Individual provider implementations
│       │   │   ├── anthropic.py
│       │   │   ├── deepseek.py
│       │   │   ├── gemini.py
│       │   │   ├── groq.py
│       │   │   ├── ollama.py
│       │   │   └── openai.py
│       │   └── shared/        # Shared utilities and data types
│       │       ├── data_types.py
│       │       ├── model_router.py
│       │       ├── utils.py
│       │       └── validator.py
│       ├── molecules/         # Higher-level functionality
│       │   ├── list_models.py
│       │   ├── list_providers.py
│       │   ├── prompt.py
│       │   ├── prompt_from_file.py
│       │   └── prompt_from_file_to_file.py
│       ├── server.py          # MCP server implementation
│       └── tests/             # Test directory
│           ├── atoms/         # Tests for atoms
│           │   ├── llm_providers/
│           │   └── shared/
│           └── molecules/     # Tests for molecules
```

## Context Priming
READ README.md, specs/*,run git ls-files, and 'eza --git-ignore --tree' to understand the context of the project.