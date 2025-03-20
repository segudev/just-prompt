"""
Tests for list_models functionality.
"""

import pytest
import os
from dotenv import load_dotenv
from just_prompt.molecules.list_models import list_models

# Load environment variables
load_dotenv()

def test_list_models_openai():
    """Test listing OpenAI models with real API call."""
    # Skip if API key isn't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Test with full provider name
    models = list_models("openai")
    
    # Assertions
    assert isinstance(models, list)
    assert len(models) > 0
    
    # Check for specific model patterns that should exist
    assert any("gpt" in model.lower() for model in models)

def test_list_models_with_short_name():
    """Test listing models using short provider name."""
    # Skip if API key isn't available
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OpenAI API key not available")
        
    # Test with short provider name
    models = list_models("o")
    
    # Assertions
    assert isinstance(models, list)
    assert len(models) > 0
    
    # Check for specific model patterns that should exist
    assert any("gpt" in model.lower() for model in models)

def test_list_models_invalid_provider():
    """Test with invalid provider name."""
    # Test invalid provider
    with pytest.raises(ValueError):
        list_models("unknown_provider")