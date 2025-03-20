"""
Tests for Gemini provider.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from just_prompt.atoms.llm_providers import gemini

# Load environment variables
load_dotenv()


@patch('google.generativeai.list_models')
def test_list_models(mock_list_models):
    """Test listing Gemini models."""
    # Set up mock
    model1 = MagicMock()
    model1.name = "models/gemini-1.5-pro"
    model1.supported_generation_methods = ["generateContent"]
    model2 = MagicMock()
    model2.name = "models/gemini-1.5-flash"
    model2.supported_generation_methods = ["generateContent"]
    
    mock_list_models.return_value = [model1, model2]
    
    # Call function
    models = gemini.list_models()
    
    # Assertions
    assert isinstance(models, list)
    assert len(models) == 2
    assert "gemini-1.5-pro" in models
    assert "gemini-1.5-flash" in models
    
    # Verify mock called
    mock_list_models.assert_called_once()


@patch('google.generativeai.GenerativeModel')
def test_prompt(mock_generative_model):
    """Test sending prompt to Gemini."""
    # Set up mock
    mock_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Paris is the capital of France."
    mock_instance.generate_content.return_value = mock_response
    mock_generative_model.return_value = mock_instance
    
    # Call function
    response = gemini.prompt("What is the capital of France?", "gemini-2.0-flash")
    
    # Assertions
    assert isinstance(response, str)
    assert response == "Paris is the capital of France."
    
    # Verify mock called correctly
    mock_generative_model.assert_called_once_with(model_name="gemini-2.0-flash")
    mock_instance.generate_content.assert_called_once_with("What is the capital of France?")


@patch('google.generativeai.GenerativeModel')
def test_prompt_error(mock_generative_model):
    """Test error handling in prompt function."""
    # Set up mock to raise exception
    mock_instance = MagicMock()
    mock_instance.generate_content.side_effect = Exception("Test error")
    mock_generative_model.return_value = mock_instance
    
    # Call function and check error handling
    with pytest.raises(ValueError) as exc_info:
        gemini.prompt("What is the capital of France?", "gemini-2.0-flash")
    
    # Verify error message
    assert "Failed to get response from Gemini" in str(exc_info.value)