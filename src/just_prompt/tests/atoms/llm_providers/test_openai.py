"""
Tests for OpenAI provider.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from just_prompt.atoms.llm_providers import openai

# Load environment variables
load_dotenv()


@patch('just_prompt.atoms.llm_providers.openai.client.models.list')
def test_list_models(mock_list):
    """Test listing OpenAI models."""
    # Set up mock
    mock_model = MagicMock()
    mock_model.id = "gpt-4o"
    mock_model2 = MagicMock()
    mock_model2.id = "gpt-4o-mini"
    mock_list.return_value.data = [mock_model, mock_model2]
    
    # Call function
    models = openai.list_models()
    
    # Assertions
    assert isinstance(models, list)
    assert len(models) == 2
    assert "gpt-4o" in models
    assert "gpt-4o-mini" in models
    
    # Verify mock called
    mock_list.assert_called_once()


@patch('just_prompt.atoms.llm_providers.openai.client.chat.completions.create')
def test_prompt(mock_create):
    """Test sending prompt to OpenAI."""
    # Set up mock
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Paris is the capital of France."
    mock_create.return_value = mock_response
    
    # Call function
    response = openai.prompt("What is the capital of France?", "gpt-4o-mini")
    
    # Assertions
    assert isinstance(response, str)
    assert response == "Paris is the capital of France."
    
    # Verify mock called correctly
    mock_create.assert_called_once()
    args = mock_create.call_args[1]
    assert args["model"] == "gpt-4o-mini"
    assert args["messages"][0]["content"] == "What is the capital of France?"


@patch('just_prompt.atoms.llm_providers.openai.client.chat.completions.create')
def test_prompt_error(mock_create):
    """Test error handling in prompt function."""
    # Set up mock to raise exception
    mock_create.side_effect = Exception("Test error")
    
    # Call function and check error handling
    with pytest.raises(ValueError) as exc_info:
        openai.prompt("What is the capital of France?", "gpt-4o-mini")
    
    # Verify error message
    assert "Failed to get response from OpenAI" in str(exc_info.value)