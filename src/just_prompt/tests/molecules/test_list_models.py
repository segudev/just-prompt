"""
Tests for list_models functionality.
"""

import pytest
from unittest.mock import patch
from just_prompt.molecules.list_models import list_models


@patch('just_prompt.atoms.shared.model_router.ModelRouter.route_list_models')
def test_list_models(mock_route_list_models):
    """Test listing models."""
    # Set up mock
    mock_route_list_models.return_value = ["model1", "model2", "model3"]
    
    # Test with full provider name
    models = list_models("openai")
    assert isinstance(models, list)
    assert len(models) == 3
    assert models == ["model1", "model2", "model3"]
    mock_route_list_models.assert_called_with("openai")
    
    # Test with short provider name
    models = list_models("o")
    assert isinstance(models, list)
    assert len(models) == 3
    assert models == ["model1", "model2", "model3"]
    mock_route_list_models.assert_called_with("o")
    
    # Test invalid provider
    with pytest.raises(ValueError):
        list_models("unknown")