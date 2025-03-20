"""
Tests for prompt functionality.
"""

import pytest
from just_prompt.molecules.prompt import prompt


# Simple mock test that doesn't rely on real API calls
def test_prompt_basic():
    """Test basic prompt functionality."""
    # Define a simple test case
    test_prompt = "Test prompt"
    test_models = ["openai:gpt-4o-mini"]
    
    # Skip the actual API calls for this simple test
    pytest.skip("Skipping API call-dependent test")