"""
Tests for validator functions.
"""

import pytest
from just_prompt.atoms.shared.validator import validate_models_prefixed_by_provider, validate_provider


def test_validate_models_prefixed_by_provider():
    """Test validating model strings."""
    # Valid model strings
    assert validate_models_prefixed_by_provider(["openai:gpt-4o-mini"]) == True
    assert validate_models_prefixed_by_provider(["anthropic:claude-3-5-haiku"]) == True
    assert validate_models_prefixed_by_provider(["o:gpt-4o-mini", "a:claude-3-5-haiku"]) == True
    
    # Invalid model strings
    with pytest.raises(ValueError):
        validate_models_prefixed_by_provider([])
    
    with pytest.raises(ValueError):
        validate_models_prefixed_by_provider(["unknown:model"])
    
    with pytest.raises(ValueError):
        validate_models_prefixed_by_provider(["invalid-format"])


def test_validate_provider():
    """Test validating provider names."""
    # Valid providers
    assert validate_provider("openai") == True
    assert validate_provider("anthropic") == True
    assert validate_provider("o") == True
    assert validate_provider("a") == True
    
    # Invalid providers
    with pytest.raises(ValueError):
        validate_provider("unknown")
        
    with pytest.raises(ValueError):
        validate_provider("")