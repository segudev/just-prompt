"""
Validation utilities for just-prompt.
"""

from typing import List
import logging
from .data_types import ModelProviders
from .utils import split_provider_and_model

logger = logging.getLogger(__name__)


def validate_models_prefixed_by_provider(models_prefixed_by_provider: List[str]) -> bool:
    """
    Validate that provider prefixes in model strings are valid.
    
    Args:
        models_prefixed_by_provider: List of model strings in format "provider:model"
        
    Returns:
        True if all valid, raises ValueError otherwise
    """
    if not models_prefixed_by_provider:
        raise ValueError("No models provided")
    
    for model_string in models_prefixed_by_provider:
        try:
            provider_prefix, model_name = split_provider_and_model(model_string)
            provider = ModelProviders.from_name(provider_prefix)
            if provider is None:
                raise ValueError(f"Unknown provider prefix: {provider_prefix}")
        except Exception as e:
            logger.error(f"Validation error for model string '{model_string}': {str(e)}")
            raise
    
    return True


def validate_provider(provider: str) -> bool:
    """
    Validate that a provider name is valid.
    
    Args:
        provider: Provider name (full or short)
        
    Returns:
        True if valid, raises ValueError otherwise
    """
    provider_enum = ModelProviders.from_name(provider)
    if provider_enum is None:
        raise ValueError(f"Unknown provider: {provider}")
    
    return True