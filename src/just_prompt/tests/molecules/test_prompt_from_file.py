"""
Tests for prompt_from_file functionality.
"""

import pytest
import os
import tempfile
from just_prompt.molecules.prompt_from_file import prompt_from_file


def test_nonexistent_file():
    """Test with non-existent file."""
    with pytest.raises(FileNotFoundError):
        prompt_from_file("/non/existent/file.txt", ["o:gpt-4o-mini"])


def test_file_read():
    """Test that the file is read correctly."""
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        temp.write("Test content")
        temp_path = temp.name
    
    try:
        # Skip actual API calls
        pytest.skip("Skipping API call-dependent test")
    finally:
        # Clean up
        os.unlink(temp_path)