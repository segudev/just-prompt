"""
Prompt from file to file functionality for just-prompt.
"""

from typing import List
import logging
import os
from pathlib import Path
from .prompt_from_file import prompt_from_file

logger = logging.getLogger(__name__)


def prompt_from_file_to_file(file: str, models_prefixed_by_provider: List[str], output_dir: str = ".", weak_provider_and_model: str = "o:gpt-4o-mini") -> List[str]:
    """
    Read text from a file, send it as prompt to multiple models, and save responses to files.
    
    Args:
        file: Path to the text file
        models_prefixed_by_provider: List of model strings in format "provider:model"
        output_dir: Directory to save response files
        weak_provider_and_model: Model to use for model name correction
        
    Returns:
        List of paths to the output files
    """
    # Validate output directory
    output_path = Path(output_dir)
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    
    if not output_path.is_dir():
        raise ValueError(f"Not a directory: {output_dir}")
    
    # Get the base name of the input file
    input_file_name = Path(file).stem
    
    # Get responses
    responses = prompt_from_file(file, models_prefixed_by_provider, weak_provider_and_model)
    
    # Save responses to files
    output_files = []
    for i, (model_string, response) in enumerate(zip(models_prefixed_by_provider, responses)):
        # Sanitize model string for filename (replace colons with underscores)
        safe_model_name = model_string.replace(":", "_")
        
        # Create output filename
        output_file = output_path / f"{input_file_name}_{safe_model_name}.txt"
        
        # Write response to file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response)
            output_files.append(str(output_file))
        except Exception as e:
            logger.error(f"Error writing response to {output_file}: {e}")
            output_files.append(f"Error: {str(e)}")
    
    return output_files