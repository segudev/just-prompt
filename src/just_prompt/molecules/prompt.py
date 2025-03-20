"""
Prompt functionality for just-prompt.
"""

from typing import List
import logging
import asyncio
from ..atoms.shared.validator import validate_models_prefixed_by_provider
from ..atoms.shared.utils import split_provider_and_model
from ..atoms.shared.model_router import ModelRouter

logger = logging.getLogger(__name__)


async def _process_model_prompt(model_string: str, text: str) -> str:
    """
    Process a single model prompt asynchronously.
    
    Args:
        model_string: String in format "provider:model"
        text: The prompt text
        
    Returns:
        Response from the model
    """
    try:
        # Wrap the synchronous call in asyncio to make it non-blocking
        return await asyncio.to_thread(ModelRouter.route_prompt, model_string, text)
    except Exception as e:
        logger.error(f"Error processing prompt for {model_string}: {e}")
        return f"Error ({model_string}): {str(e)}"


async def prompt_async(text: str, models_prefixed_by_provider: List[str], weak_provider_and_model: str = "o:gpt-4o-mini") -> List[str]:
    """
    Send a prompt to multiple models asynchronously.
    
    Args:
        text: The prompt text
        models_prefixed_by_provider: List of model strings in format "provider:model"
        weak_provider_and_model: Model to use for model name correction
        
    Returns:
        List of responses from the models
    """
    # Validate model strings
    validate_models_prefixed_by_provider(models_prefixed_by_provider)
    
    # Process each model
    tasks = []
    for model_string in models_prefixed_by_provider:
        provider, model = split_provider_and_model(model_string)
        
        # Check if model needs correction
        corrected_model = await asyncio.to_thread(
            ModelRouter.magic_model_correction,
            provider, model, weak_provider_and_model
        )
        
        # Use corrected model
        if corrected_model != model:
            model_string = f"{provider}:{corrected_model}"
        
        tasks.append(_process_model_prompt(model_string, text))
    
    # Wait for all responses
    responses = await asyncio.gather(*tasks)
    return responses


def prompt(text: str, models_prefixed_by_provider: List[str], weak_provider_and_model: str = "o:gpt-4o-mini") -> List[str]:
    """
    Send a prompt to multiple models.
    
    Args:
        text: The prompt text
        models_prefixed_by_provider: List of model strings in format "provider:model"
        weak_provider_and_model: Model to use for model name correction
        
    Returns:
        List of responses from the models
    """
    return asyncio.run(prompt_async(text, models_prefixed_by_provider, weak_provider_and_model))