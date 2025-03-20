"""
Tests for Anthropic provider.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from just_prompt.atoms.llm_providers import anthropic

# Load environment variables
load_dotenv()


@patch('just_prompt.atoms.llm_providers.anthropic.client.models.list')
def test_list_models(mock_list):
    """Test listing Anthropic models."""
    # Set up mock
    mock_model = MagicMock()
    mock_model.id = "claude-3-opus-20240229"
    mock_model2 = MagicMock()
    mock_model2.id = "claude-3-5-sonnet-20240620"
    mock_list.return_value.data = [mock_model, mock_model2]
    
    # Call function
    models = anthropic.list_models()
    
    # Assertions
    assert isinstance(models, list)
    assert len(models) == 2
    assert "claude-3-opus-20240229" in models
    assert "claude-3-5-sonnet-20240620" in models
    
    # Verify mock called
    mock_list.assert_called_once()


@patch('just_prompt.atoms.llm_providers.anthropic.client.messages.create')
def test_prompt(mock_create):
    """Test sending prompt to Anthropic."""
    # Set up mock
    mock_response = MagicMock()
    mock_response.content = [MagicMock()]
    mock_response.content[0].text = "Paris is the capital of France."
    mock_create.return_value = mock_response
    
    # Call function
    response = anthropic.prompt("What is the capital of France?", "claude-3-5-haiku")
    
    # Assertions
    assert isinstance(response, str)
    assert response == "Paris is the capital of France."
    
    # Verify mock called correctly
    mock_create.assert_called_once()
    args = mock_create.call_args[1]
    assert args["model"] == "claude-3-5-haiku"
    assert args["messages"][0]["content"] == "What is the capital of France?"


@patch('just_prompt.atoms.llm_providers.anthropic.client.messages.create')
def test_prompt_error(mock_create):
    """Test error handling in prompt function."""
    # Set up mock to raise exception
    mock_create.side_effect = Exception("Test error")
    
    # Call function and check error handling
    with pytest.raises(ValueError) as exc_info:
        anthropic.prompt("What is the capital of France?", "claude-3-5-haiku")
    
    # Verify error message
    assert "Failed to get response from Anthropic" in str(exc_info.value)