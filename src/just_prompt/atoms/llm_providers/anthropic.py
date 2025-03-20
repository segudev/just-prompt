"""
Anthropic provider implementation.
"""

import os
import anthropic
from typing import List
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def prompt(text: str, model: str) -> str:
    """
    Send a prompt to Anthropic Claude and get a response.

    Args:
        text: The prompt text
        model: The model name

    Returns:
        Response string from the model
    """
    try:
        logger.info(f"Sending prompt to Anthropic model: {model}")
        message = client.messages.create(
            model=model, max_tokens=4096, messages=[{"role": "user", "content": text}]
        )

        return message.content[0].text
    except Exception as e:
        logger.error(f"Error sending prompt to Anthropic: {e}")
        raise ValueError(f"Failed to get response from Anthropic: {str(e)}")


def list_models() -> List[str]:
    """
    List available Anthropic models.

    Returns:
        List of model names
    """
    try:
        logger.info("Listing Anthropic models")
        response = client.models.list()

        models = [model.id for model in response.data]
        return models
    except Exception as e:
        logger.error(f"Error listing Anthropic models: {e}")
        # Return some known models if API fails
        logger.info("Returning hardcoded list of known Anthropic models")
        return [
            "claude-3-7-sonnet",
            "claude-3-5-sonnet",
            "claude-3-5-sonnet-20240620",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-haiku",
        ]
