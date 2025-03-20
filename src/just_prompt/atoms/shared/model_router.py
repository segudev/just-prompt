"""
Model router for dispatching requests to the appropriate provider.
"""

import logging
from typing import List, Dict, Any, Optional
import importlib
from .utils import split_provider_and_model
from .data_types import ModelProviders

logger = logging.getLogger(__name__)


class ModelRouter:
    """
    Routes requests to the appropriate provider based on the model string.
    """
    
    @staticmethod
    def route_prompt(model_string: str, text: str) -> str:
        """
        Route a prompt to the appropriate provider.
        
        Args:
            model_string: String in format "provider:model"
            text: The prompt text
            
        Returns:
            Response from the model
        """
        provider_prefix, model = split_provider_and_model(model_string)
        provider = ModelProviders.from_name(provider_prefix)
        
        if not provider:
            raise ValueError(f"Unknown provider prefix: {provider_prefix}")
        
        # Import the appropriate provider module
        try:
            module_name = f"just_prompt.atoms.llm_providers.{provider.full_name}"
            provider_module = importlib.import_module(module_name)
            
            # Call the prompt function
            return provider_module.prompt(text, model)
        except ImportError as e:
            logger.error(f"Failed to import provider module: {e}")
            raise ValueError(f"Provider not available: {provider.full_name}")
        except Exception as e:
            logger.error(f"Error routing prompt to {provider.full_name}: {e}")
            raise
    
    @staticmethod
    def route_list_models(provider_name: str) -> List[str]:
        """
        Route a list_models request to the appropriate provider.
        
        Args:
            provider_name: Provider name (full or short)
            
        Returns:
            List of model names
        """
        provider = ModelProviders.from_name(provider_name)
        
        if not provider:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        # Import the appropriate provider module
        try:
            module_name = f"just_prompt.atoms.llm_providers.{provider.full_name}"
            provider_module = importlib.import_module(module_name)
            
            # Call the list_models function
            return provider_module.list_models()
        except ImportError as e:
            logger.error(f"Failed to import provider module: {e}")
            raise ValueError(f"Provider not available: {provider.full_name}")
        except Exception as e:
            logger.error(f"Error listing models for {provider.full_name}: {e}")
            raise
    
    @staticmethod
    def magic_model_correction(provider: str, model: str, weak_provider_and_model: str) -> str:
        """
        Correct a model name using a weak AI model if needed.
        
        Args:
            provider: Provider name
            model: Original model name
            weak_provider_and_model: Model to use for correction, e.g. "o:gpt-4o-mini"
            
        Returns:
            Corrected model name
        """
        provider_module_name = f"just_prompt.atoms.llm_providers.{provider}"
        
        try:
            provider_module = importlib.import_module(provider_module_name)
            available_models = provider_module.list_models()
            
            # If model is already in available models, no correction needed
            if model in available_models:
                logger.info(f"Using {provider} and {model}")
                return model
            
            # Model needs correction - use weak model to correct it
            weak_provider, weak_model = split_provider_and_model(weak_provider_and_model)
            weak_provider_enum = ModelProviders.from_name(weak_provider)
            
            if not weak_provider_enum:
                logger.warning(f"Invalid weak model provider: {weak_provider}, skipping correction")
                return model
                
            weak_module_name = f"just_prompt.atoms.llm_providers.{weak_provider_enum.full_name}"
            weak_module = importlib.import_module(weak_module_name)
            
            # Build prompt for the weak model
            prompt = f"""
Given a user-provided model name "{model}" for the provider "{provider}", and the list of actual available models below,
return the closest matching model name from the available models list.
Only return the exact model name, nothing else.

Available models: {', '.join(available_models)}
"""
            # Get correction from weak model
            corrected_model = weak_module.prompt(prompt, weak_model).strip()
            
            # Verify the corrected model exists in the available models
            if corrected_model in available_models:
                logger.info(f"weak_provider_and_model: {weak_provider_and_model}")
                logger.info(f"models_prefixed_by_provider: {provider}:{model}")
                logger.info(f"corrected_model: {corrected_model}")
                return corrected_model
            else:
                logger.warning(f"Corrected model {corrected_model} not found in available models")
                return model
                
        except Exception as e:
            logger.error(f"Error in model correction: {e}")
            return model