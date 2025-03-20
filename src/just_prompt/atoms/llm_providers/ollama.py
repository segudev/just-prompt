"""
Ollama provider implementation.
"""

import os
from typing import List
import logging
import ollama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Set Ollama host if provided
if os.environ.get("OLLAMA_HOST"):
    ollama.set_host(os.environ.get("OLLAMA_HOST"))


def prompt(text: str, model: str) -> str:
    """
    Send a prompt to Ollama and get a response.

    Args:
        text: The prompt text
        model: The model name

    Returns:
        Response string from the model
    """
    try:
        logger.info(f"Sending prompt to Ollama model: {model}")

        # Create chat completion
        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": text,
                },
            ],
        )

        # Extract response content
        return response.message.content
    except Exception as e:
        logger.error(f"Error sending prompt to Ollama: {e}")
        raise ValueError(f"Failed to get response from Ollama: {str(e)}")


def list_models() -> List[str]:
    """
    List available Ollama models.

    Returns:
        List of model names
    """
    try:
        logger.info("Listing Ollama models")
        response = ollama.list()

        # Extract model names
        models = [model.get("name") for model in response.get("models", [])]

        return models
    except Exception as e:
        logger.error(f"Error listing Ollama models: {e}")
        # Return some known models if API fails
        logger.info("Returning hardcoded list of known Ollama models")
        return [
            "llama3:latest",
            "llama3.1:latest",
            "gemma:latest",
            "gemma:7b",
            "qwen:latest",
            "qwen2.5-1.5b:latest",
        ]
