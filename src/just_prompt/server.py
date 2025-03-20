"""
FastAPI server for just-prompt MCP.
"""

import logging
import os
from typing import List, Dict
import uvicorn
from fastapi import FastAPI, HTTPException
from .atoms.shared.data_types import (
    PromptRequest,
    PromptResponse,
    PromptFromFileRequest,
    PromptFromFileResponse,
    PromptFromFileToFileRequest,
    PromptFromFileToFileResponse,
    ListProvidersRequest,
    ListProvidersResponse,
    ListModelsRequest,
    ListModelsResponse
)
from .molecules.prompt import prompt
from .molecules.prompt_from_file import prompt_from_file
from .molecules.prompt_from_file_to_file import prompt_from_file_to_file
from .molecules.list_providers import list_providers as list_providers_func
from .molecules.list_models import list_models as list_models_func
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="just-prompt MCP Server",
    description="A lightweight MCP server for various LLM providers",
    version="0.1.0"
)


@app.post("/prompt", response_model=PromptResponse)
async def prompt_endpoint(request: PromptRequest):
    """
    Send a prompt to multiple models.
    """
    try:
        responses = prompt(request.text, request.models_prefixed_by_provider)
        return PromptResponse(responses=responses)
    except Exception as e:
        logger.error(f"Error in prompt endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/prompt_from_file", response_model=PromptFromFileResponse)
async def prompt_from_file_endpoint(request: PromptFromFileRequest):
    """
    Send a prompt from a file to multiple models.
    """
    try:
        responses = prompt_from_file(request.file, request.models_prefixed_by_provider)
        return PromptFromFileResponse(responses=responses)
    except Exception as e:
        logger.error(f"Error in prompt_from_file endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/prompt_from_file_to_file", response_model=PromptFromFileToFileResponse)
async def prompt_from_file_to_file_endpoint(request: PromptFromFileToFileRequest):
    """
    Send a prompt from a file to multiple models and save responses to files.
    """
    try:
        file_paths = prompt_from_file_to_file(
            request.file, 
            request.models_prefixed_by_provider,
            request.output_dir
        )
        return PromptFromFileToFileResponse(file_paths=file_paths)
    except Exception as e:
        logger.error(f"Error in prompt_from_file_to_file endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/list_providers", response_model=ListProvidersResponse)
async def list_providers_endpoint(request: ListProvidersRequest = ListProvidersRequest()):
    """
    List all available providers.
    """
    try:
        providers = list_providers_func()
        return ListProvidersResponse(providers=providers)
    except Exception as e:
        logger.error(f"Error in list_providers endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/list_models", response_model=ListModelsResponse)
async def list_models_endpoint(request: ListModelsRequest):
    """
    List all available models for a provider.
    """
    try:
        models = list_models_func(request.provider)
        return ListModelsResponse(models=models)
    except Exception as e:
        logger.error(f"Error in list_models endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def serve(weak_provider_and_model: str = "o:gpt-4o-mini") -> None:
    """
    Start the FastAPI server.
    
    Args:
        weak_provider_and_model: Model to use for model name correction
    """
    # Set global weak model for corrections
    os.environ["WEAK_PROVIDER_AND_MODEL"] = weak_provider_and_model
    
    logger.info(f"Starting server with weak model: {weak_provider_and_model}")
    
    # Get host and port from environment or use defaults
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    
    # Start server
    uvicorn.run(app, host=host, port=port)