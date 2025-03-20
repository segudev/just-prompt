"""
Tests for Anthropic provider.
"""

import pytest
import os
from dotenv import load_dotenv
from just_prompt.atoms.llm_providers import anthropic

# Load environment variables
load_dotenv()

# Skip tests if API key not available
if not os.environ.get("ANTHROPIC_API_KEY"):
    pytest.skip("Anthropic API key not available", allow_module_level=True)


def test_list_models():
    """Test listing Anthropic models."""
    models = anthropic.list_models()
    
    # Assertions
    assert isinstance(models, list)
    assert len(models) > 0
    assert all(isinstance(model, str) for model in models)
    
    # Check for at least one expected model
    claude_models = [model for model in models if "claude" in model.lower()]
    assert len(claude_models) > 0, "No Claude models found"


def test_prompt():
    """Test sending prompt to Anthropic."""
    # Use the correct model name from the available models
    response = anthropic.prompt("What is the capital of France?", "claude-3-5-haiku-20241022")
    
    # Assertions
    assert isinstance(response, str)
    assert len(response) > 0
    assert "paris" in response.lower() or "Paris" in response