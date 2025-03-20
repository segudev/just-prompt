"""
Data types and models for just-prompt MCP server.
"""

from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel


class ModelProviders(Enum):
    """
    Enum of supported model providers with their full and short names.
    """
    OPENAI = ("openai", "o")
    ANTHROPIC = ("anthropic", "a")
    GEMINI = ("gemini", "g") 
    GROQ = ("groq", "q")
    DEEPSEEK = ("deepseek", "d")
    OLLAMA = ("ollama", "l")
    
    def __init__(self, full_name, short_name):
        self.full_name = full_name
        self.short_name = short_name
        
    @classmethod
    def from_name(cls, name):
        """
        Get provider enum from full or short name.
        
        Args:
            name: The provider name (full or short)
            
        Returns:
            ModelProviders: The corresponding provider enum, or None if not found
        """
        for provider in cls:
            if provider.full_name == name or provider.short_name == name:
                return provider
        return None


class ModelAlias(BaseModel):
    """
    Model class representing a provider and model combination.
    """
    provider: str
    model: str


class PromptRequest(BaseModel):
    """
    Request model for prompt endpoint.
    """
    text: str
    models_prefixed_by_provider: List[str]


class PromptResponse(BaseModel):
    """
    Response model for prompt endpoint.
    """
    responses: List[str]


class PromptFromFileRequest(BaseModel):
    """
    Request model for prompt_from_file endpoint.
    """
    file: str
    models_prefixed_by_provider: List[str]


class PromptFromFileResponse(BaseModel):
    """
    Response model for prompt_from_file endpoint.
    """
    responses: List[str]


class PromptFromFileToFileRequest(BaseModel):
    """
    Request model for prompt_from_file_to_file endpoint.
    """
    file: str
    models_prefixed_by_provider: List[str]
    output_dir: str = "."


class PromptFromFileToFileResponse(BaseModel):
    """
    Response model for prompt_from_file_to_file endpoint.
    """
    file_paths: List[str]


class ListProvidersRequest(BaseModel):
    """
    Request model for list_providers endpoint.
    """
    pass


class ListProvidersResponse(BaseModel):
    """
    Response model for list_providers endpoint.
    Returns all providers with long and short names.
    """
    providers: List[Dict[str, str]]


class ListModelsRequest(BaseModel):
    """
    Request model for list_models endpoint.
    """
    provider: str


class ListModelsResponse(BaseModel):
    """
    Response model for list_models endpoint.
    Returns all models for a given provider.
    """
    models: List[str]