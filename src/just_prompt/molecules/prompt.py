"""
Prompt functionality for just-prompt.
"""

from typing import List
import logging
import concurrent.futures
from ..atoms.shared.validator import validate_models_prefixed_by_provider
from ..atoms.shared.utils import split_provider_and_model
from ..atoms.shared.model_router import ModelRouter

logger = logging.getLogger(__name__)


def _process_model_prompt(model_string: str, text: str) -> str:
    """
    Process a single model prompt.
    
    Args:
        model_string: String in format "provider:model"
        text: The prompt text
        
    Returns:
        Response from the model
    """
    try:
        return ModelRouter.route_prompt(model_string, text)
    except Exception as e:
        logger.error(f"Error processing prompt for {model_string}: {e}")
        return f"Error ({model_string}): {str(e)}"


def _correct_model_name(provider: str, model: str, weak_provider_and_model: str) -> str:
    """
    Correct a model name using the weak model.
    
    Args:
        provider: Provider name
        model: Model name
        weak_provider_and_model: Weak model for correction
        
    Returns:
        Corrected model name
    """
    try:
        return ModelRouter.magic_model_correction(provider, model, weak_provider_and_model)
    except Exception as e:
        logger.error(f"Error correcting model name {provider}:{model}: {e}")
        return model


def prompt(text: str, models_prefixed_by_provider: List[str], weak_provider_and_model: str = "o:gpt-4o-mini") -> List[str]:
    """
    Send a prompt to multiple models using parallel processing.
    
    Args:
        text: The prompt text
        models_prefixed_by_provider: List of model strings in format "provider:model"
        weak_provider_and_model: Model to use for model name correction
        
    Returns:
        List of responses from the models
    """
    # Validate model strings
    validate_models_prefixed_by_provider(models_prefixed_by_provider)
    
    # Prepare corrected model strings
    corrected_models = []
    for model_string in models_prefixed_by_provider:
        provider, model = split_provider_and_model(model_string)
        
        # Check if model needs correction
        corrected_model = _correct_model_name(provider, model, weak_provider_and_model)
        
        # Use corrected model
        if corrected_model != model:
            model_string = f"{provider}:{corrected_model}"
        
        corrected_models.append(model_string)
    
    # Process each model in parallel using ThreadPoolExecutor
    responses = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all tasks
        future_to_model = {
            executor.submit(_process_model_prompt, model_string, text): model_string
            for model_string in corrected_models
        }
        
        # Collect results in order
        for model_string in corrected_models:
            for future, future_model in future_to_model.items():
                if future_model == model_string:
                    responses.append(future.result())
                    break
    
    return responses