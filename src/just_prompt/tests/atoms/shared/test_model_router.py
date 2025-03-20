"""
Tests for model router.
"""

import pytest
from unittest.mock import patch, MagicMock
import importlib
from just_prompt.atoms.shared.model_router import ModelRouter


@patch('importlib.import_module')
def test_route_prompt(mock_import_module):
    """Test routing prompts to the appropriate provider."""
    # Set up mock
    mock_module = MagicMock()
    mock_module.prompt.return_value = "Paris is the capital of France."
    mock_import_module.return_value = mock_module
    
    # Test with full provider name
    response = ModelRouter.route_prompt("openai:gpt-4o-mini", "What is the capital of France?")
    assert response == "Paris is the capital of France."
    mock_import_module.assert_called_with("just_prompt.atoms.llm_providers.openai")
    mock_module.prompt.assert_called_with("What is the capital of France?", "gpt-4o-mini")
    
    # Test with short provider name
    response = ModelRouter.route_prompt("o:gpt-4o-mini", "What is the capital of France?")
    assert response == "Paris is the capital of France."
    
    # Test invalid provider
    with pytest.raises(ValueError):
        ModelRouter.route_prompt("unknown:model", "What is the capital of France?")


@patch('importlib.import_module')
def test_route_list_models(mock_import_module):
    """Test routing list_models requests to the appropriate provider."""
    # Set up mock
    mock_module = MagicMock()
    mock_module.list_models.return_value = ["model1", "model2"]
    mock_import_module.return_value = mock_module
    
    # Test with full provider name
    models = ModelRouter.route_list_models("openai")
    assert models == ["model1", "model2"]
    mock_import_module.assert_called_with("just_prompt.atoms.llm_providers.openai")
    mock_module.list_models.assert_called_once()
    
    # Test with short provider name
    models = ModelRouter.route_list_models("o")
    assert models == ["model1", "model2"]
    
    # Test invalid provider
    with pytest.raises(ValueError):
        ModelRouter.route_list_models("unknown")